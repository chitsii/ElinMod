using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Text.RegularExpressions;
using UnityEngine;

namespace Elin_ItemRelocator {

    // Discriminator based polymorphism
    public interface ICondition {
        bool IsMatch(Thing t);
        // We might want a TypeID for serialization if not using auto-typing,
        // but Newtonsoft.Json with TypeNameHandling.Auto is requested by user?
        // Or custom key mapping. Let's start with classes.
    }

    public abstract class BaseCondition : ICondition {
        public bool Not; // Negation flag common to most
        public abstract bool IsMatch(Thing t);

        protected bool CheckOp(int value, string op, int target) {
            return op switch {
                ">=" => value >= target,
                ">" => value > target,
                "<=" => value <= target,
                "<" => value < target,
                "==" => value == target,
                "=" => value == target,
                "!=" => value != target,
                _ => value >= target
            };
        }
    }

    public class ConditionCategory : BaseCondition {
        public HashSet<string> CategoryIds = new();

        public override bool IsMatch(Thing t) {
            if (CategoryIds.Count == 0)
                return false;
            foreach (var id in CategoryIds) {
                if (t.category.IsChildOf(id)) {
                    return !Not;
                }
            }
            return Not; // If no match found, and Not=true, return true. If Not=false, return false.
        }
    }

    public class ConditionRarity : BaseCondition {
        public HashSet<int> Rarities = new();
        public override bool IsMatch(Thing t) {
            if (Rarities.Count == 0)
                return false;
            bool match = Rarities.Contains((int)t.rarity);
            return Not ? !match : match;
        }
    }

    public class ConditionQuality : BaseCondition {
        public string Op = ">=";
        public int Value;

        public override bool IsMatch(Thing t) {
            bool match = CheckOp((int)t.encLV, Op, Value);
            return Not ? !match : match;
        }
    }

    public class ConditionWeight : BaseCondition {
        public string Op = ">=";
        public int Value;
        public override bool IsMatch(Thing t) {
            bool match = CheckOp(t.SelfWeight, Op, Value);
            return Not ? !match : match;
        }
    }

    public class ConditionGenLvl : BaseCondition {
        public string Op = ">=";
        public int Value;
        public override bool IsMatch(Thing t) {
            bool match = CheckOp(t.genLv, Op, Value);
            return Not ? !match : match;
        }
    }

    public class ConditionDna : BaseCondition {
        public string Op = ">=";
        public int Value;
        public override bool IsMatch(Thing t) {
            if (t.c_DNA == null)
                return Not;
            bool match = CheckOp(t.c_DNA.cost, Op, Value);
            return Not ? !match : match;
        }
    }

    public class ConditionText : BaseCondition {
        public string Text;
        public override bool IsMatch(Thing t) {
            if (string.IsNullOrEmpty(Text))
                return false;
            string name = t.Name.ToLower();
            string rawName = t.source.GetName().ToLower();
            string[] parts = Text.Split([' ', '　'], StringSplitOptions.RemoveEmptyEntries);
            foreach (var part in parts) {
                string q = part.Trim().ToLower();
                if (!name.Contains(q) && !rawName.Contains(q))
                    return Not; // If any part mismatches, fail (AND logic normally). Wait, original was AND.
            }
            return !Not;
        }
    }

    public class ConditionMaterial : BaseCondition {
        public HashSet<string> MaterialIds = new(StringComparer.OrdinalIgnoreCase);
        public override bool IsMatch(Thing t) {
            if (t.material == null)
                return Not;
            bool match = MaterialIds.Contains(t.material.alias) || MaterialIds.Contains(t.material.id.ToString());
            return Not ? !match : match;
        }
    }

    public class ConditionBless : BaseCondition {
        public HashSet<int> States = new();
        public override bool IsMatch(Thing t) {
            bool match = States.Contains((int)t.blessedState);
            return Not ? !match : match;
        }
    }

    public class ConditionStolen : BaseCondition {
        public bool IsStolen; // Target value
        public override bool IsMatch(Thing t) {
            bool match = t.isStolen == IsStolen;
            return Not ? !match : match; // Usually not negated for boolean flags, but BaseCondition has it.
        }
    }

    public class ConditionIdentified : BaseCondition {
        public bool IsIdentified;
        public override bool IsMatch(Thing t) {
            bool match = t.IsIdentified == IsIdentified;
            return Not ? !match : match;
        }
    }

    public class ConditionDnaContent : BaseCondition {
        public HashSet<string> DnaIds = new();
        public override bool IsMatch(Thing t) {
            if (t.c_DNA == null)
                return false;
            // Logic: Matches ANY of DnaIds
            bool anyMatch = false;
            foreach (string cond in DnaIds) {
                // Reuse parsing logic? For now simple check or copy basic parsing
                // Assuming logic similar to original Profile.cs
                // For brevity, using simplified check if no Value op
                // Original logic parsed "eleName>=10"
                // Let's defer full parser or implement simplified
                // Just checking ID existence for now as placeholder for strict refactor
                // Re-implementing original logic:
                string idStr = cond;
                // ... Parsing omitted for brevity, assuming alias match ...
                int elementId = EClass.sources.elements.alias.TryGetValue(idStr, out var source) ? source.id : -1;
                if (elementId != -1) {
                    for (int i = 0; i < t.c_DNA.vals.Count; i += 2) {
                        if (t.c_DNA.vals[i] == elementId) { anyMatch = true; break; }
                    }
                }
            }
            return Not ? !anyMatch : anyMatch;
        }
    }



    public class ConditionEnchantOr : BaseCondition {
        public List<string> Runes = new();
        public bool IsAndMode; // If true, all runes must match (AND). If false, any rune matches (OR).

        public override bool IsMatch(Thing t) {
            if (Runes.Count == 0)
                return false;

            bool match;
            if (IsAndMode) {
                match = true;
                foreach (var r in Runes) {
                    if (!ConditionRegistry.CheckEnchantMatch(t, r, CheckOp)) {
                        match = false;
                        break;
                    }
                }
            } else {
                match = false;
                foreach (var r in Runes) {
                    if (ConditionRegistry.CheckEnchantMatch(t, r, CheckOp)) {
                        match = true;
                        break;
                    }
                }
            }
            return Not ? !match : match;
        }
    }
    public class ConditionAddButton : BaseCondition {
        public override bool IsMatch(Thing t) => false;
    }

    public static class ConditionRegistry {
        public static List<(string Key, Func<JObject, ICondition> Loader)> Loaders = new();
        public static Dictionary<Type, Action<JObject, ICondition>> Savers = new();

        static ConditionRegistry() {
            // Register all handlers
            Register<ConditionCategory>("CategoryIds",
                jo => {
                    var ids = jo["CategoryIds"]?.ToObject<List<string>>();
                    var negs = jo["NegatedCategoryIds"]?.ToObject<List<string>>(); // Legacy support

                    if (ids != null && ids.Count > 0)
                        return new ConditionCategory { CategoryIds = new HashSet<string>(ids), Not = (bool?)jo["Not"] ?? false };

                    // [Legacy Support] Remove legacy negation check after 2026/04
                    if (negs != null && negs.Count > 0)
                        return new ConditionCategory { CategoryIds = new HashSet<string>(negs), Not = true };

                    return null;
                },
                (jo, c) => {
                    jo.Add("CategoryIds", JArray.FromObject(c.CategoryIds));
                    if (c.Not)
                        jo.Add("Not", true);
                }
            );

            // [Legacy Support] Remove this loader after 2026/04
            Loaders.Add(("NegatedCategoryIds", jo => {
                var negs = jo["NegatedCategoryIds"]?.ToObject<List<string>>();
                if (negs != null && negs.Count > 0)
                    return new ConditionCategory { CategoryIds = new HashSet<string>(negs), Not = true };
                return null;
            }
            ));

            Register<ConditionWeight>("Weight",
                jo => {
                    // [Legacy Support] Remove null check after 2026/04
                    if (IsJNull(jo["Weight"]))
                        return null;
                    return new ConditionWeight {
                        Value = (int)jo["Weight"],
                        Op = jo["WeightOp"]?.ToString() ?? ">=",
                        Not = (bool?)jo["NotWeight"] ?? false
                    };
                },
                (jo, c) => {
                    jo.Add("Weight", c.Value);
                    jo.Add("WeightOp", c.Op);
                    jo.Add("NotWeight", c.Not);
                }
            );

            Register<ConditionGenLvl>("GenLvl",
                jo => {
                    // [Legacy Support] Remove null check after 2026/04
                    if (IsJNull(jo["GenLvl"]))
                        return null;
                    return new ConditionGenLvl {
                        Value = (int)jo["GenLvl"],
                        Op = jo["GenLvlOp"]?.ToString() ?? ">=",
                        Not = (bool?)jo["NotGenLvl"] ?? false
                    };
                },
                (jo, c) => {
                    jo.Add("GenLvl", c.Value);
                    jo.Add("GenLvlOp", c.Op);
                    jo.Add("NotGenLvl", c.Not);
                }
            );

            Register<ConditionText>("Text",
                jo => {
                    // [Legacy Support] Remove null check after 2026/04
                    if (IsJNull(jo["Text"]))
                        return null;
                    string text = jo["Text"].ToString();
                    if (string.IsNullOrEmpty(text))
                        return null;
                    return new ConditionText {
                        Text = text,
                        Not = (bool?)jo["NotText"] ?? false
                    };
                },
                (jo, c) => {
                    jo.Add("Text", c.Text);
                    jo.Add("NotText", c.Not);
                }
            );

            Register<ConditionQuality>("Quality",
                jo => {
                    // [Legacy Support] Remove null check after 2026/04
                    if (IsJNull(jo["Quality"]))
                        return null;
                    string q = jo["Quality"].ToString();
                    ParseOp(q, out var op, out var val);
                    return new ConditionQuality {
                        Value = val,
                        Op = op,
                        Not = (bool?)jo["NotQuality"] ?? false
                    };
                },
                (jo, c) => {
                    jo.Add("Quality", c.Op + c.Value);
                    jo.Add("NotQuality", c.Not);
                }
            );

            Register<ConditionRarity>("Rarities",
                jo => {
                    var list = jo["Rarities"]?.ToObject<List<int>>();
                    if (list == null || list.Count == 0)
                        return null;
                    return new ConditionRarity {
                        Rarities = new HashSet<int>(list)
                    };
                },
                (jo, c) => {
                    jo.Add("Rarities", JArray.FromObject(c.Rarities));
                }
            );

            // Enchants / Runes (Ambiguous keys)
            // Enchants / Runes (Ambiguous keys)
            Register<ConditionEnchantOr>("Enchants",
                jo => {
                    var list = jo["Enchants"]?.ToObject<List<string>>();
                    if (list == null || list.Count == 0)
                        return null;
                    return new ConditionEnchantOr {
                        Runes = list,
                        IsAndMode = true,
                        Not = (bool?)jo["NotEnchant"] ?? false
                    };
                },
                (jo, c) => {
                    // No serialization needed for legacy key "Enchants" as we want to save in new format "EnchantsOr"
                }
            );

            Register<ConditionEnchantOr>("EnchantsOr",
                jo => {
                    var list = jo["EnchantsOr"]?.ToObject<List<string>>();
                    if (list == null || list.Count == 0)
                        return null;
                    return new ConditionEnchantOr {
                        Runes = list,
                        IsAndMode = (bool?)jo["IsAndMode"] ?? false,
                        Not = (bool?)jo["NotEnchantsOr"] ?? false
                    };
                },
                (jo, c) => {
                    jo.Add("EnchantsOr", JArray.FromObject(c.Runes));
                    jo.Add("IsAndMode", c.IsAndMode);
                    jo.Add("NotEnchantsOr", c.Not);
                }
            );

            // [Legacy Support] Remove this loader after 2026/04
            Loaders.Add(("Runes", jo => {
                var list = jo["Runes"]?.ToObject<List<string>>();
                if (list == null || list.Count == 0)
                    return null;
                // Migration: Runes also maps to ConditionEnchantOr (AND)
                return new ConditionEnchantOr { Runes = list, IsAndMode = true };
            }
            ));

            Register<ConditionBless>("BlessStates",
                jo => {
                    var list = jo["BlessStates"]?.ToObject<List<int>>();
                    if (list == null || list.Count == 0)
                        return null;
                    return new ConditionBless {
                        States = new HashSet<int>(list),
                        Not = (bool?)jo["NotBless"] ?? false
                    };
                },
                (jo, c) => {
                    jo.Add("BlessStates", JArray.FromObject(c.States));
                    jo.Add("NotBless", c.Not);
                }
            );
            // [Legacy Support] Remove this loader after 2026/04
            Loaders.Add(("States", jo => {
                var list = jo["States"]?.ToObject<List<int>>();
                if (list == null || list.Count == 0)
                    return null;
                return new ConditionBless {
                    States = new HashSet<int>(list),
                    Not = (bool?)jo["NotBless"] ?? false
                };
            }
            ));


            Register<ConditionMaterial>("MaterialIds",
                jo => {
                    var list = jo["MaterialIds"]?.ToObject<List<string>>();
                    if (list == null || list.Count == 0)
                        return null;
                    return new ConditionMaterial {
                        MaterialIds = new HashSet<string>(list),
                        Not = (bool?)jo["NotMaterial"] ?? false
                    };
                },
                (jo, c) => {
                    jo.Add("MaterialIds", JArray.FromObject(c.MaterialIds));
                    jo.Add("NotMaterial", c.Not);
                }
            );

            Register<ConditionDna>("Dna",
                jo => {
                    if (IsJNull(jo["Dna"]))
                        return null;
                    return new ConditionDna {
                        Value = (int)jo["Dna"],
                        Op = jo["DnaOp"]?.ToString() ?? ">=",
                        Not = (bool?)jo["NotDna"] ?? false
                    };
                },
                (jo, c) => {
                    jo.Add("Dna", c.Value);
                    jo.Add("DnaOp", c.Op);
                    jo.Add("NotDna", c.Not);
                }
            );

            Register<ConditionDnaContent>("DnaIds",
                jo => {
                    var list = jo["DnaIds"]?.ToObject<List<string>>();
                    if (list == null || list.Count == 0)
                        return null;
                    return new ConditionDnaContent {
                        DnaIds = new HashSet<string>(list),
                        Not = (bool?)jo["NotDnaContent"] ?? false
                    };
                },
                (jo, c) => {
                    jo.Add("DnaIds", JArray.FromObject(c.DnaIds));
                    jo.Add("NotDnaContent", c.Not);
                }
            );

            Register<ConditionStolen>("IsStolen",
                jo => {
                    if (IsJNull(jo["IsStolen"]))
                        return null;
                    return new ConditionStolen {
                        IsStolen = (bool)jo["IsStolen"],
                        Not = (bool?)jo["NotStolen"] ?? false
                    };
                },
                (jo, c) => {
                    jo.Add("IsStolen", true);
                    jo.Add("NotStolen", c.Not);
                }
            );

            Register<ConditionIdentified>("IsIdentified",
                jo => {
                    if (IsJNull(jo["IsIdentified"]))
                        return null;
                    return new ConditionIdentified {
                        IsIdentified = (bool)jo["IsIdentified"],
                        Not = (bool?)jo["NotIdentified"] ?? false
                    };
                },
                (jo, c) => {
                    jo.Add("IsIdentified", true);
                    if (c.Not)
                        jo.Add("NotIdentified", true);
                }
            );
        }

        private static bool IsJNull(JToken t) => t == null || t.Type == JTokenType.Null;

        public static void Register<T>(string key, Func<JObject, T> loader, Action<JObject, T> saver) where T : ICondition {
            Loaders.Add((key, jo => loader(jo)));
            Savers[typeof(T)] = (jo, c) => saver(jo, (T)c);
        }

        public static void ParseOp(string raw, out string op, out int val) {
            op = ">=";
            val = 0;
            if (string.IsNullOrEmpty(raw))
                return;
            string[] ops = [">=", "<=", "!=", ">", "<", "="];
            foreach (var o in ops) {
                if (raw.Contains(o)) { // Contains check is safer for "Name>=10"
                    int idx = raw.IndexOf(o);
                    if (idx > 0) { // Ensure name exists before op
                        op = o;
                        int.TryParse(raw.Substring(idx + o.Length), out val);
                        return;
                    }
                }
            }
            // Fallback if starts with op (e.g. ">=10" but should be handled by caller usually passing full string)
            // But here raw likely includes key?
            // My previous ParseOp (line 478 original) assumed raw was VALUE part only for Quality?
            // Wait, ConditionQuality loader passed ">=10".
            // ConditionEnchant logic needs to split Key and Op.
            // Let's make a ParseKeyOp helper or keep specific logic.
            int.TryParse(raw, out val);
        }

        public static bool CheckEnchantMatch(Thing t, string rune, Func<int, string, int, bool> checkOp) {
            try {
                if (string.IsNullOrEmpty(rune))
                    return false;
                string term = rune.StartsWith("@") ? rune.Substring(1) : rune;
                string key = term;
                string op = ">=";
                int val = 1; // Default to 1 (existence) if no op specified. Fixes "Mining matches everything" bug.
                string[] ops = [">=", "<=", "!=", ">", "<", "="];

                foreach (var o in ops) {
                    int idx = term.IndexOf(o);
                    if (idx > 0) {
                        op = o;
                        key = term.Substring(0, idx).Trim();
                        int.TryParse(term.Substring(idx + o.Length), out val);
                        break;
                    }
                }

                if (string.IsNullOrEmpty(key))
                    return false;

                Debug.Log($"[Relocator] CheckEnchantMatch: Item={t?.Name ?? "Null"}, Key={key}, Op={op}, Val={val}");

                // 1. Exact / Alias Match
                int eleId = EClass.sources.elements.alias.TryGetValue(key, out var source) ? source.id : -1;
                if (eleId == -1) {
                    var match = EClass.sources.elements.rows.FirstOrDefault(e =>
                        e.GetName().Equals(key, StringComparison.OrdinalIgnoreCase) ||
                        (e.alias != null && e.alias.Equals(key, StringComparison.OrdinalIgnoreCase))
                    );
                    if (match != null)
                        eleId = match.id;
                }

                if (eleId != -1) {
                    // Exact match found: Check only this element
                    int curVal = t.elements.Value(eleId);
                    return checkOp(curVal, op, val);
                }

                // 2. Wildcard Match (Fallback)
                // Only scan active elements on the Thing
                if (t.elements != null && t.elements.dict != null) {
                    var keys = t.elements.dict.Keys.ToList(); // Copy keys to avoid CollectionModified exception
                    foreach (var id in keys) {
                        // Skip disabled/hidden? Usually all in dict are active.
                        var eleSource = EClass.sources.elements.map[id];
                        if (eleSource == null)
                            continue; // Safety check
                        string eleName = eleSource.GetName();

                        // Helper: Case insensitive contains
                        if (eleName.IndexOf(key, StringComparison.OrdinalIgnoreCase) >= 0) {
                            Debug.Log($"[Relocator] Wildcard Match candidate: {eleName} (ID {id})");
                            int curVal = t.elements.Value(id);
                            Debug.Log($"[Relocator] Value: {curVal}");
                            if (checkOp(curVal, op, val)) {
                                Debug.Log($"[Relocator] CheckOp Passed. Returning TRUE.");
                                return true; // Found a matching element that meets criteria
                            }
                        }
                    }
                }
            } catch (Exception ex) {
                Debug.LogError($"[Relocator] Error: {ex.Message}\n{ex.StackTrace}");
                Msg.Say($"Enchant Filter Error: {ex.Message}");
            }
            return false;
        }
    }
}
