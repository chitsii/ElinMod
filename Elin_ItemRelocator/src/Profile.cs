using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;
using System.Text.RegularExpressions;

namespace Elin_ItemRelocator
{
    [Serializable]
    public class RelocationProfile
    {
        public string ContainerName; // For display/debug
        public bool Enabled = true;
        public FilterScope Scope = FilterScope.Inventory;
        public bool ExcludeHotbar = true; // Default to exclude

        // Main Data
        public List<RelocationRule> Rules = new List<RelocationRule>();

        // Legacy Support
        [JsonProperty]
        private List<RelocationFilter> Filters
        {
            set
            {
                if(value != null && value.Count > 0) {
                    // Migration: Convert legacy Filters to Rules
                    foreach(var f in value) {
                        var r = new RelocationRule();
                        r.Name = "Imported Rule";
                        if(f.CategoryIds != null) r.CategoryIds = f.CategoryIds;
                        r.Rarity = f.Rarity;
                        r.RarityOp = f.RarityOp;
                        r.Quality = f.Quality;
                        r.Text = f.Text;
                        Rules.Add(r);
                    }
                }
            }
        }

        public ResultSortMode SortMode = ResultSortMode.Default;

        // Scope definition
        public enum FilterScope
        {
            Inventory,
            Zone
        }

        public enum ResultSortMode
        {
            Default,
            PriceAsc,
            PriceDesc,
            EnchantMagAsc,
            EnchantMagDesc,
            TotalWeightAsc,
            TotalWeightDesc,
            UnitWeightAsc,
            UnitWeightDesc
        }
    }

    [Serializable]
    public class RelocationRule
    {
        public string Name = "New Rule";
        public bool Enabled = true;

        public List<string> CategoryIds = new List<string>();
        public int? Rarity;
        public string RarityOp = ">=";
        public string Quality;
        public string Text;
        public int? Weight;
        public string WeightOp = ">=";

        // Negation Flags
        public HashSet<string> NegatedCategoryIds = new HashSet<string>();
        public bool NotRarity;
        public bool NotQuality;
        public bool NotText;
        public bool NotWeight;

        // Matching Logic (AND within Rule)
        public bool IsMatch(Thing t)
        {
            if (!Enabled) return false;

            // Safe Default: If no conditions are set, match nothing.
            if ((CategoryIds == null || CategoryIds.Count == 0) &&
                !Rarity.HasValue &&
                string.IsNullOrEmpty(Quality) &&
                string.IsNullOrEmpty(Text) &&
                !Weight.HasValue)
            {
                return false;
            }

            // Check Category (Multi-match: OR logic within CategoryIds)
            if (CategoryIds != null && CategoryIds.Count > 0)
            {
                // Determine if this specific category condition is negated
                // NOTE: The current data structure stores negated IDs in a separate set.
                // But the logic "Is Match" iterates "CategoryIds".
                // If an ID is in "CategoryIds", it's a condition.
                // If it is ALSO in "NegatedCategoryIds", it means "NOT (IsChildOf(id))".
                // BUT, usually "CategoryIds" is treated as an OR group.
                // If we have Mixed (Positive and Negated)...
                // Interpret as: (Positive1 OR Positive2) AND (NOT Negative1) AND (NOT Negative2).
                // "CategoryIds" contains ALL IDs (both positive and negative ones).
                // So we separate them.

                bool hasPositive = false;
                bool positiveMatch = false;

                foreach(var id in CategoryIds) {
                    bool isNeg = NegatedCategoryIds != null && NegatedCategoryIds.Contains(id);
                    if (isNeg) {
                         // Negative Condition: Must NOT be match
                         if (t.category.IsChildOf(id)) return false;
                    } else {
                         hasPositive = true;
                         if (t.category.IsChildOf(id)) positiveMatch = true;
                    }
                }

                if (hasPositive && !positiveMatch) return false;
            }

            // Check Rarity
            if (Rarity.HasValue)
            {
                string op = string.IsNullOrEmpty(RarityOp) ? ">=" : RarityOp;
                bool match = EvaluateCondition((int)t.rarity, op + Rarity.Value);
                if (NotRarity) match = !match;
                if (!match) return false;
            }

            // Check Quality (String Logic)
            if (!string.IsNullOrEmpty(Quality))
            {
                  bool match = EvaluateCondition((int)t.encLV, Quality);
                  if (NotQuality) match = !match;
                  if (!match) return false;
            }

            // Check Text
            if (!string.IsNullOrEmpty(Text))
            {
                 bool match = IsTextMatch(t, Text);
                 if (NotText) match = !match;
                 if (!match) return false;
            }

            // Check Weight (Unit Weight)
            if (Weight.HasValue)
            {
                 string op = string.IsNullOrEmpty(WeightOp) ? ">=" : WeightOp;
                 // SelfWeight returns unit weight in Elin
                 bool match = EvaluateCondition(t.SelfWeight, op + Weight.Value);
                 if (NotWeight) match = !match;
                 if (!match) return false;
            }

            return true;
        }

        // Helper to get active conditions for UI
        public List<string> GetConditionList()
        {
             List<string> parts = new List<string>();
             // Categories
              if (CategoryIds != null && CategoryIds.Count > 0) {
                  foreach(var id in CategoryIds) {
                       var source = EClass.sources.categories.map.TryGetValue(id);
                       string name = source != null ? source.GetName() : id;
                       bool isNeg = NegatedCategoryIds != null && NegatedCategoryIds.Contains(id);
                       string prefix = isNeg ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                       parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Category) + ": " + name);
                  }
              }
              if (Rarity.HasValue) {
                  string prefix = NotRarity ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                  parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Rarity) + " " + (string.IsNullOrEmpty(RarityOp) ? ">=" : RarityOp) + " " + Rarity.Value);
              }
              if (!string.IsNullOrEmpty(Quality)) {
                  string prefix = NotQuality ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                  parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Quality) + " " + Quality);
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

        private bool IsTextMatch(Thing t, string query)
        {
            string[] parts = query.Split(new char[]{' ', '　'}, StringSplitOptions.RemoveEmptyEntries);
            foreach(var part in parts)
            {
                string term = part.Trim();
                if (term.StartsWith("@"))
                {
                    if (!EvaluateAttribute(t, term.Substring(1))) return false;
                }
                else
                {
                    if (!MatchesName(t, term)) return false;
                }
            }
            return true;
        }

        private bool MatchesName(Thing t, string term)
        {
            string name = t.Name.ToLower();
            string rawName = t.source.GetName().ToLower();
            string q = term.ToLower();
            return name.Contains(q) || rawName.Contains(q);
        }

        private bool EvaluateCondition(int value, string condition)
        {
            string[] ops = new string[]{ ">=", "<=", "!=", ">", "<", "=" };
            string op = null;
            string valStr = condition;
            int targetVal = 0;

            foreach(var o in ops)
            {
                if (condition.StartsWith(o))
                {
                    op = o;
                    valStr = condition.Substring(o.Length).Trim();
                    break;
                }
            }
            if (op == null) op = ">=";
            int.TryParse(valStr, out targetVal);

            switch(op)
            {
                case ">=": return value >= targetVal;
                case ">": return value > targetVal;
                case "<=": return value <= targetVal;
                case "<": return value < targetVal;
                case "=": return value == targetVal;
                case "!=": return value != targetVal;
                default: return false;
            }
        }

        private bool EvaluateAttribute(Thing t, string query)
        {
            string[] ops = new string[]{ ">=", "<=", "!=", ">", "<", "=" };
            string op = null;
            string key = query;
            int val = 0;

            foreach(var o in ops)
            {
                int idx = query.IndexOf(o);
                if (idx > 0)
                {
                    op = o;
                    key = query.Substring(0, idx).Trim();
                    string valStr = query.Substring(idx + o.Length).Trim();
                    int.TryParse(valStr, out val);
                    break;
                }
            }
            if (op == null) { op = ">"; val = 0; }

            int eleId = 0;
            var sourceEle = EClass.sources.elements.map.Values.FirstOrDefault(e =>
                (e.alias != null && e.alias.Equals(key, StringComparison.OrdinalIgnoreCase)) ||
                (e.GetName().Equals(key, StringComparison.OrdinalIgnoreCase))
            );

            if (sourceEle != null) eleId = sourceEle.id;
            else if (!int.TryParse(key, out eleId)) return false;

            int currentVal = t.elements.Value(eleId);

            switch(op)
            {
                case ">=": return currentVal >= val;
                case ">": return currentVal > val;
                case "<=": return currentVal <= val;
                case "<": return currentVal < val;
                case "=": return currentVal == val;
                case "!=": return currentVal != val;
                default: return false;
            }
        }
    }

    // Stub for Legacy JSON
    [Serializable]
    public class RelocationFilter
    {
        public List<string> CategoryIds;
        public int? Rarity;
        public string RarityOp;
        public string Quality;
        public string Text;
    }
}
