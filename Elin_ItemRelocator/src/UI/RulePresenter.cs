using System;
using System.Collections.Generic;
using System.Linq;

namespace Elin_ItemRelocator {
    public static class RulePresenter {
        // Helper to get active conditions for UI
        public static List<string> GetConditionList(RelocationRule rule) {
            List<string> parts = [];

            // Iterate Order? Group by type?
            // Existing UI order: Category, Rarity, Quality, Text, Weight, GenLvl, Dna...
            // We can iterate the list and map to string.
            // Or prioritize types for consistent display order.

            foreach (var cond in rule.Conditions) {
                switch (cond) {
                case ConditionCategory c: {
                    foreach (var id in c.CategoryIds) {
                        var source = EClass.sources.categories.map.TryGetValue(id);
                        string name = source is not null ? source.GetName() : id;
                        string prefix = c.Not ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                        parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Category) + ": " + name);
                    }
                }
                break;
                case ConditionRarity r: {
                    string prefix = r.Not ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                    parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Rarity));
                }
                break;
                case ConditionQuality q: {
                    string prefix = q.Not ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                    parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Enhancement) + " " + q.Op + q.Value);
                }
                break;
                case ConditionText t: {
                    string prefix = t.Not ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                    parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Text) + ": " + t.Text);
                }
                break;
                case ConditionWeight w: {
                    string prefix = w.Not ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                    parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Weight) + " " + w.Op + " " + w.Value);
                }
                break;
                case ConditionGenLvl g: {
                    string prefix = g.Not ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                    parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.GenLvl) + " " + g.Op + " " + g.Value);
                }
                break;
                case ConditionDna d: {
                    string prefix = d.Not ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                    parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Dna) + " " + d.Op + " " + d.Value);
                }
                break;
                case ConditionDnaContent dc: {
                    string prefix = dc.Not ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                    parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.DnaContent) + ": " + string.Join(", ", dc.DnaIds));
                }
                break;
                case ConditionEnchantOr eOr: {
                    string prefix = eOr.Not ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                    string mode = eOr.IsAndMode ? " (AND)" : " (OR)";
                    parts.Add(prefix + RelocatorLang.GetText(RelocatorLang.LangKey.EnchantOr) + mode + ": " + string.Join(", ", eOr.Runes));
                }
                break;


                case ConditionMaterial m:
                    parts.Add(RelocatorLang.GetText(RelocatorLang.LangKey.Material));
                    break;
                case ConditionBless b:
                    parts.Add(RelocatorLang.GetText(RelocatorLang.LangKey.Bless));
                    break;
                }
            }
            return parts;
        }
    }
}
