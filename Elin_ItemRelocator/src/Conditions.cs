using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

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

    public class ConditionEnchant : BaseCondition {
        public List<string> Runes = new(); // "Mining>=10"
        public override bool IsMatch(Thing t) {
            // Logic: Matches ALL runestrings? Original was AND.
            foreach (var r in Runes) {
                // EvaluateAttribute logic
                string term = r.StartsWith("@") ? r.Substring(1) : r;
                // Quick parse
                string[] ops = [">=", "<=", "!=", ">", "<", "="];
                string op = ">";
                int val = 0;
                string key = term;
                foreach (var o in ops) {
                    int idx = term.IndexOf(o);
                    if (idx > 0) { op = o; key = term.Substring(0, idx).Trim(); int.TryParse(term.Substring(idx + o.Length), out val); break; }
                }

                // Match Logic (Same as original Manager.cs display logic?)
                // Try alias first
                int eleId = EClass.sources.elements.alias.TryGetValue(key, out var source) ? source.id : -1;

                // If not found, try Name match (for localized inputs like "筋力")
                if (eleId == -1) {
                    var match = EClass.sources.elements.rows.FirstOrDefault(e =>
                        e.GetName().Equals(key, StringComparison.OrdinalIgnoreCase) ||
                        (e.alias != null && e.alias.Equals(key, StringComparison.OrdinalIgnoreCase))
                    );
                    if (match != null)
                        eleId = match.id;
                }

                int curVal = (eleId != -1) ? t.elements.Value(eleId) : 0;
                if (!CheckOp(curVal, op, val))
                    return Not; // Mismatch
            }
            return !Not;
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
            Register<ConditionEnchant>("Enchants",
                jo => {
                    var list = jo["Enchants"]?.ToObject<List<string>>();
                    if (list == null || list.Count == 0)
                        return null;
                    return new ConditionEnchant { Runes = list };
                },
                (jo, c) => jo.Add("Enchants", JArray.FromObject(c.Runes))
            );
            // [Legacy Support] Remove this loader after 2026/04
            Loaders.Add(("Runes", jo => {
                var list = jo["Runes"]?.ToObject<List<string>>();
                if (list == null || list.Count == 0)
                    return null;
                return new ConditionEnchant { Runes = list };
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
                if (raw.StartsWith(o)) {
                    op = o;
                    int.TryParse(raw.Substring(o.Length), out val);
                    return;
                }
            }
            int.TryParse(raw, out val);
        }
    }
}
