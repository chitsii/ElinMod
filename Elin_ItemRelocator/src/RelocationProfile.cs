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
        public List<RelocationFilter> Filters = new List<RelocationFilter>();

        // Scope definition
        public enum FilterScope
        {
            Inventory,
            Zone
        }
    }

    [Serializable]
    public class RelocationFilter
    {
        public bool Enabled = true;

        // Basic filters
        public string CategoryId;
        public int? Rarity;
        public string RarityOp = ">="; // Default operator
        public string Quality; // Changed from int? to string for inequalities e.g. ">=2"
        public string IdThing;

        // Advanced Text Filter
        public string Text; // e.g. "bread", ":fire>=10"

        public bool IsMatch(Thing t)
        {
            if (!Enabled) return true; // Fix: If disabled, it should not fail the AND check

            // Check Category
            if (!string.IsNullOrEmpty(CategoryId))
            {
                if (!t.category.IsChildOf(CategoryId)) return false;
            }

            // Check Rarity
            if (Rarity.HasValue)
            {
                string op = string.IsNullOrEmpty(RarityOp) ? ">=" : RarityOp;
                if (!EvaluateCondition((int)t.rarity, op + Rarity.Value)) return false;
            }

            // Check Quality (String Logic)
            if (!string.IsNullOrEmpty(Quality))
            {
                 if (!EvaluateCondition((int)t.encLV, Quality)) return false;
            }

            // Check ID
            if (!string.IsNullOrEmpty(IdThing))
            {
                if (t.id != IdThing) return false;
            }

            // Check Text
            if (!string.IsNullOrEmpty(Text))
            {
                if (!IsTextMatch(t, Text)) return false;
            }

            return true;
        }

        // Helper for UI display
        public string GetDescription()
        {
             List<string> parts = new List<string>();
             if (!string.IsNullOrEmpty(CategoryId)) parts.Add("Category: " + GetCategoryName(CategoryId));
             if (Rarity.HasValue) parts.Add("Rarity " + (string.IsNullOrEmpty(RarityOp) ? ">=" : RarityOp) + " " + Rarity.Value);
             if (!string.IsNullOrEmpty(Quality)) parts.Add("Quality " + Quality);
             if (!string.IsNullOrEmpty(IdThing)) parts.Add("ID: " + IdThing);
             if (!string.IsNullOrEmpty(Text)) parts.Add("Text: " + Text);

             if (parts.Count == 0) return "Empty Filter";
             return string.Join(", ", parts);
        }

        private string GetCategoryName(string id)
        {
             var source = EClass.sources.categories.map.TryGetValue(id);
             return source != null ? source.GetName() : id;
        }

        private bool IsTextMatch(Thing t, string query)
        {
            // Split by space for AND condition
            string[] parts = query.Split(new char[]{' ', '　'}, StringSplitOptions.RemoveEmptyEntries);

            foreach(var part in parts)
            {
                string term = part.Trim();
                if (term.StartsWith("@"))
                {
                    // Native-style Attribute search
                    if (!EvaluateAttribute(t, term.Substring(1))) return false;
                }
                else
                {
                    // Name search
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

            if (name.Contains(q)) return true;
            if (rawName.Contains(q)) return true;
            return false;
        }

        // Generic evaluator for ">=10", "=5", etc.
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

            // Defaults
            if (op == null)
            {
                // If just number, assume >=
                op = ">=";
            }

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
            // Parse operator: >=, <=, !=, >, <, =
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

            // If no operator found, check if it just exists (value > 0)
            if (op == null)
            {
                op = ">";
                val = 0;
            }

            int eleId = 0;
            var sourceEle = EClass.sources.elements.map.Values.FirstOrDefault(e =>
                (e.alias != null && e.alias.Equals(key, StringComparison.OrdinalIgnoreCase)) ||
                (e.GetName().Equals(key, StringComparison.OrdinalIgnoreCase))
            );

            if (sourceEle != null)
            {
                eleId = sourceEle.id;
            }
            else
            {
               if (!int.TryParse(key, out eleId)) return false;
            }

            int currentVal = t.elements.Value(eleId);

            // Reuse generic evaluator logic? Or just switch here.
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
}
