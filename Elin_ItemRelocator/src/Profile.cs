using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;
using System.Text.RegularExpressions;
using System.Reflection;

namespace Elin_ItemRelocator {
    [Serializable]
    public class RelocationProfile {
        public string ContainerName; // For display/debug
        public bool Enabled = true;
        public FilterScope Scope = FilterScope.Both;

        // Main Data
        public List<RelocationRule> Rules = [];


        public ResultSortMode SortMode = ResultSortMode.Default;

        // Scope definition
        public enum FilterScope {
            Inventory,
            Both, // Was Zone (1)
            ZoneOnly // New (2)
        }

        public enum ResultSortMode {
            Default,
            PriceAsc,
            PriceDesc,
            EnchantMagAsc,
            EnchantMagDesc,
            TotalEnchantMagDesc, // New: Sum of ALL enchants
            TotalWeightAsc,
            TotalWeightDesc,
            UnitWeightAsc,
            UnitWeightDesc,
            UidAsc,
            UidDesc
        }

        public enum RelocatorOp { Ge, Le, Eq, Ne, Gt, Lt }
    }

    [Serializable]
    public class RelocationRule {
        public string Name = "New Rule";
        public bool Enabled = true;

        public List<string> CategoryIds = [];
        // public int? Rarity; // Removed
        // public string RarityOp; // Removed
        public string Quality;
        public string Text;
        public List<string> Enchants = [];
        public int? Weight;
        public string WeightOp = ">=";

        // Negation Flags
        public HashSet<string> NegatedCategoryIds = [];
        public bool NotQuality;
        public bool NotText;
        public bool NotWeight;
        public bool NotMaterial;
        public bool NotBless;
        public bool NotStolen;

        // New Condition Fields
        public HashSet<string> MaterialIds = new(StringComparer.OrdinalIgnoreCase); // Multi-select

        public HashSet<int> BlessStates = []; // Multi-select

        public HashSet<int> Rarities = [];

        public bool? IsStolen;
        public bool? IsIdentified;
        public void InvalidateCache() => _cacheValid = false;

        // --- Cache Fields (Optimization) ---
        [JsonIgnore] private bool _cacheValid = false;
        [JsonIgnore] private int _cQualityVal; [JsonIgnore] private RelocationProfile.RelocatorOp _cQualityOp;
        [JsonIgnore] private int _cWeightVal; [JsonIgnore] private RelocationProfile.RelocatorOp _cWeightOp;

        // Matching Logic (AND within Rule)
        public bool IsMatch(Thing t) {
            if (!Enabled || t.c_lockedHard)
                return false;


            EnsureCache();

            // Safe Default: If no conditions are set, match nothing.
            if ((CategoryIds == null || CategoryIds.Count == 0) &&
                (Rarities == null || Rarities.Count == 0) &&
                string.IsNullOrEmpty(Quality) &&
                string.IsNullOrEmpty(Text) &&
                (Enchants == null || Enchants.Count == 0) &&
                !Weight.HasValue &&
                (MaterialIds == null || MaterialIds.Count == 0) &&
                (BlessStates == null || BlessStates.Count == 0) &&
                !IsStolen.HasValue &&
                !IsIdentified.HasValue) {
                return false;
            }

            // Check Category (Multi-match: OR logic within CategoryIds)
            if (CategoryIds is { Count: > 0 }) {
                bool hasPositive = false;
                bool positiveMatch = false;

                foreach (var id in CategoryIds) {
                    bool isNeg = NegatedCategoryIds is not null && NegatedCategoryIds.Contains(id);
                    if (isNeg) {
                        // Negative Condition: Must NOT be match
                        if (t.category.IsChildOf(id))
                            return false;
                    } else {
                        hasPositive = true;
                        if (t.category.IsChildOf(id))
                            positiveMatch = true;
                    }
                }

                if (hasPositive && !positiveMatch)
                    return false;
            }

            // Check Rarity (Multi-select)
            if (Rarities is { Count: > 0 }) {
                // Rarity is Rarity enum (int)
                // However, t.rarity is Rarity enum.
                if (!Rarities.Contains((int)t.rarity))
                    return false;
            }

            // Check Quality
            if (!string.IsNullOrEmpty(Quality)) {
                bool match = CheckOp((int)t.encLV, _cQualityOp, _cQualityVal);
                if (NotQuality)
                    match = !match;
                if (!match)
                    return false;
            }

            // Check Text
            if (!string.IsNullOrEmpty(Text)) {
                bool match = IsTextMatch(t, Text);
                if (NotText)
                    match = !match;
                if (!match)
                    return false;
            }

            // Check Enchants (New)
            if (Enchants is { Count: > 0 }) {
                bool matchEnchant = true;
                foreach (var e in Enchants) {
                    // Enchants are stored as "@Mining>=10" or just "@Mining"
                    string term = e.StartsWith("@") ? e.Substring(1) : e;
                    if (!EvaluateAttribute(t, term)) { matchEnchant = false; break; }
                }
                // Note: No negation flag for Enchants currently (assumed positive requirement)
                if (!matchEnchant)
                    return false;
            }

            // Check Weight (Unit Weight)
            if (Weight.HasValue) {
                bool match = CheckOp(t.SelfWeight, _cWeightOp, _cWeightVal);
                if (NotWeight)
                    match = !match;
                if (!match)
                    return false;
            }

            // Check Material (Optimized HashSet Lookup)
            if (MaterialIds is { Count: > 0 }) {
                bool match = false;
                if (t.material is not null) {
                    // O(1) Lookup
                    if (MaterialIds.Contains(t.material.alias) || MaterialIds.Contains(t.material.id.ToString()))
                        match = true;
                }
                if (NotMaterial)
                    match = !match;
                if (!match)
                    return false;
            }

            // Check Bless State
            if (BlessStates is { Count: > 0 }) {
                int bState = (int)t.blessedState;

                bool match = BlessStates.Contains(bState);

                if (NotBless)
                    match = !match;
                if (!match)
                    return false;
            }

            // Stolen Flag
            if (IsStolen.HasValue) {
                bool match = t.isStolen == IsStolen.Value;
                if (NotStolen)
                    match = !match;
                if (!match)
                    return false;
            }

            // Identified Flag
            if (IsIdentified.HasValue) {
                if (t.IsIdentified != IsIdentified.Value)
                    return false;
            }

            return true;
        }

        // Helper to get active conditions for UI
        public List<string> GetConditionList() {
            List<string> parts = [];
            // Categories
            if (CategoryIds is { Count: > 0 }) {
                foreach (var id in CategoryIds) {
                    var source = EClass.sources.categories.map.TryGetValue(id);
                    string name = source is not null ? source.GetName() : id;
                    bool isNeg = NegatedCategoryIds is not null && NegatedCategoryIds.Contains(id);
                    string prefix = isNeg ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                    parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Category) + ": " + name);
                }
            }
            if (Rarities is { Count: > 0 }) {
                parts.Add(RelocatorLang.GetText(RelocatorLang.LangKey.Rarity));
            }
            if (!string.IsNullOrEmpty(Quality)) {
                string prefix = NotQuality ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Enhancement) + " " + Quality);
            }
            if (!string.IsNullOrEmpty(Text)) {
                string prefix = NotText ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Text) + ": " + Text);
            }
            if (Weight.HasValue) {
                string prefix = NotWeight ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Weight) + " " + (string.IsNullOrEmpty(WeightOp) ? ">=" : WeightOp) + " " + Weight.Value);
            }
            return parts;
        }

        private bool IsTextMatch(Thing t, string query) {
            string[] parts = query.Split([' ', '　'], StringSplitOptions.RemoveEmptyEntries);
            foreach (var part in parts) {
                string term = part.Trim();
                if (!MatchesName(t, term))
                    return false;
            }
            return true;
        }

        private bool MatchesName(Thing t, string term) {
            string name = t.Name.ToLower();
            string rawName = t.source.GetName().ToLower();
            string q = term.ToLower();
            return name.Contains(q) || rawName.Contains(q);
        }

        private void EnsureCache() {
            if (_cacheValid)
                return;

            ParseOp(string.IsNullOrEmpty(WeightOp) ? ">=" : WeightOp, Weight.HasValue ? Weight.Value : 0, out _cWeightOp, out _cWeightVal);
            ParseOp(Quality, 0, out _cQualityOp, out _cQualityVal); // Quality string contains both op and value


            _cacheValid = true;
        }

        private void ParseOp(string condition, int defaultVal, out RelocationProfile.RelocatorOp op, out int val) {
            op = RelocationProfile.RelocatorOp.Ge;
            val = defaultVal;
            if (string.IsNullOrEmpty(condition))
                return;

            string[] ops = [">=", "<=", "!=", ">", "<", "="];
            string foundOp = null;
            string valStr = condition;

            foreach (var o in ops) {
                if (condition.StartsWith(o)) {
                    foundOp = o;
                    valStr = condition.Substring(o.Length).Trim();
                    break;
                }
            }
            // If condition was just a number (e.g. from Rarity property), op is default (>= usually)
            // But wait, Rarity property is int?. RarityOp is string.
            // If condition passed here is ">=10" (like from Quality), we parse it.
            // If condition passed is RarityOp (e.g. ">=") and value is separate...
            // Logic differs.
            // My EnsureCache calls: ParseOp(RarityOp, RarityValue).
            // RarityOp is just ">=". valStr becomes "".
            // So int.TryParse fails. val remains defaultVal. Correct.

            // IF Valid Op found
            if (foundOp is not null) {
                op = foundOp switch {
                    ">=" => RelocationProfile.RelocatorOp.Ge,
                    "<=" => RelocationProfile.RelocatorOp.Le,
                    "!=" => RelocationProfile.RelocatorOp.Ne,
                    ">" => RelocationProfile.RelocatorOp.Gt,
                    "<" => RelocationProfile.RelocatorOp.Lt,
                    "=" => RelocationProfile.RelocatorOp.Eq,
                    _ => RelocationProfile.RelocatorOp.Ge
                };
            }

            if (!string.IsNullOrEmpty(valStr)) {
                int.TryParse(valStr, out val);
            }
        }

        private bool CheckOp(int value, RelocationProfile.RelocatorOp op, int target) => op switch {
            RelocationProfile.RelocatorOp.Ge => value >= target,
            RelocationProfile.RelocatorOp.Gt => value > target,
            RelocationProfile.RelocatorOp.Le => value <= target,
            RelocationProfile.RelocatorOp.Lt => value < target,
            RelocationProfile.RelocatorOp.Eq => value == target,
            RelocationProfile.RelocatorOp.Ne => value != target,
            _ => false
        };

        private bool EvaluateAttribute(Thing t, string query) {
            string[] ops = [">=", "<=", "!=", ">", "<", "="];
            string op = null;
            string key = query;
            int val = 0;

            foreach (var o in ops) {
                int idx = query.IndexOf(o);
                if (idx > 0) {
                    op = o;
                    key = query.Substring(0, idx).Trim();
                    string valStr = query.Substring(idx + o.Length).Trim();
                    int.TryParse(valStr, out val);
                    break;
                }
            }
            if (op is null) { op = ">"; val = 0; }

            int eleId = 0;
            var sourceEle = EClass.sources.elements.map.Values.FirstOrDefault(e =>
                (e.alias != null && e.alias.Equals(key, StringComparison.OrdinalIgnoreCase)) ||
                (e.GetName().Equals(key, StringComparison.OrdinalIgnoreCase))
            );

            if (sourceEle is not null)
                eleId = sourceEle.id;
            else if (!int.TryParse(key, out eleId))
                return false;

            int currentVal = t.elements.Value(eleId);

            return op switch {
                ">=" => currentVal >= val,
                ">" => currentVal > val,
                "<=" => currentVal <= val,
                "<" => currentVal < val,
                "=" => currentVal == val,
                "!=" => currentVal != val,
                _ => false
            };
        }
    }

}
