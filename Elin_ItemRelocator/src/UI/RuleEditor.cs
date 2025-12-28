using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Linq;

namespace Elin_ItemRelocator {
    public static class RuleEditor {

        private static void AddEnchantFilterDialog(SourceElement.Row ele, Action<string> onConfirm) {
            Dialog.InputName("Amount (e.g. >=10)", "", (c2, val) => {
                if (!c2) {
                    string filterText = "@" + ele.GetName();
                    if (!string.IsNullOrEmpty(val)) {
                        if (char.IsDigit(val[0]))
                            val = ">=" + val;
                        filterText += val;
                    }
                    onConfirm(filterText);
                }
            }, (Dialog.InputType)0);
        }

        public static void ShowAddConditionMenu(RelocationRule rule, Action refresh) {
            RelocatorMenu.Create()
                .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Text), () => {
                    Dialog.InputName("Enter Text/Tag", "", (c, text) => {
                        if (!c && !string.IsNullOrEmpty(text)) {
                            // Find existing? Or just add new? Existing logic was "append" to single string.
                            // New logic: Just add a ConditionText.
                            rule.Conditions.Add(new ConditionText { Text = text });
                            refresh();
                        }
                    }, (Dialog.InputType)0);
                })
                 .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Enchant), () => {
                     RelocatorMenu.Create()
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatAll), () => {
                              RelocatorPickers.ShowEnchantPicker(0, (ele) => {
                                  AddEnchantFilterDialog(ele, (text) => {
                                      // Add new ConditionEnchant
                                      rule.Conditions.Add(new ConditionEnchant { Runes = [text] });
                                      refresh();
                                  });
                              });
                          })
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatWeapon), () => {
                              RelocatorPickers.ShowEnchantPicker(1, (ele) => {
                                  AddEnchantFilterDialog(ele, (text) => {
                                      rule.Conditions.Add(new ConditionEnchant { Runes = [text] });
                                      refresh();
                                  });
                              });
                          })
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatArmor), () => {
                              RelocatorPickers.ShowEnchantPicker(2, (ele) => {
                                  AddEnchantFilterDialog(ele, (text) => {
                                      rule.Conditions.Add(new ConditionEnchant { Runes = [text] });
                                      refresh();
                                  });
                              });
                          })
                          .Show();
                 })
                .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Category), () => {
                    RelocatorPickers.ShowCategoryPicker([], (selectedIds) => {
                        if (selectedIds.Count > 0) {
                            rule.Conditions.Add(new ConditionCategory { CategoryIds = new HashSet<string>(selectedIds) });
                            refresh();
                        }
                    });
                })
                .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Rarity), () => {
                    RelocatorPickers.ShowRarityPicker(null, (selected) => {
                        rule.Conditions.Add(new ConditionRarity { Rarities = new HashSet<int>(selected) });
                        refresh();
                    });
                })
                .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Enhancement), () => {
                    Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.EditEnhancement), "", (c, text) => {
                        if (!c && !string.IsNullOrEmpty(text)) {
                            string op = ">=";
                            int val = 0;
                            // Parse
                            if (text.StartsWith(">=") || text.StartsWith("<=") || text.StartsWith("==") || text.StartsWith("!=")) { op = text.Substring(0, 2); int.TryParse(text.Substring(2), out val); } else if (text.StartsWith(">") || text.StartsWith("<") || text.StartsWith("=")) { op = text.Substring(0, 1); int.TryParse(text.Substring(1), out val); } else { int.TryParse(text, out val); }

                            rule.Conditions.Add(new ConditionQuality { Op = op, Value = val });
                            refresh();
                        }
                    }, (Dialog.InputType)0);
                })
                 .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Weight), () => {
                     Dialog.InputName("Enter Weight (e.g. >=10)", "", (c, text) => {
                         if (!c && !string.IsNullOrEmpty(text)) {
                             if (char.IsDigit(text[0]))
                                 text = ">=" + text;
                             string op = ">=";
                             int val = 0;
                             if (text.StartsWith(">=") || text.StartsWith("<=") || text.StartsWith("==") || text.StartsWith("!=")) { op = text.Substring(0, 2); int.TryParse(text.Substring(2), out val); } else if (text.StartsWith(">") || text.StartsWith("<") || text.StartsWith("=")) { op = text.Substring(0, 1); int.TryParse(text.Substring(1), out val); } else { int.TryParse(text, out val); }

                             rule.Conditions.Add(new ConditionWeight { Op = op, Value = val });
                             refresh();
                         }
                     }, (Dialog.InputType)0);
                 })
                  .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Material), () => {
                      RelocatorPickers.ShowMaterialPicker(null, (aliases) => {
                          rule.Conditions.Add(new ConditionMaterial { MaterialIds = new HashSet<string>(aliases) });
                          refresh();
                      });
                  })
                  .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Bless), () => {
                      RelocatorPickers.ShowBlessPicker(null, (states) => {
                          rule.Conditions.Add(new ConditionBless { States = new HashSet<int>(states) });
                          refresh();
                      });
                  })
                  .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.Stolen), (child) => {
                      child
                           .AddButton("Yes (Is Stolen)", () => { rule.Conditions.Add(new ConditionStolen { IsStolen = true }); refresh(); })
                           .AddButton("No (Not Stolen)", () => { rule.Conditions.Add(new ConditionStolen { IsStolen = false }); refresh(); });
                  })
                  .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.Identified), (child) => {
                      child
                           .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.StateIdentified), () => { rule.Conditions.Add(new ConditionIdentified { IsIdentified = true }); refresh(); })
                           .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.StateUnidentified), () => { rule.Conditions.Add(new ConditionIdentified { IsIdentified = false }); refresh(); });
                  })
                  .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.GenLvl), () => {
                      Dialog.InputName("Enter GenLvl (e.g. >=10)", "", (c, text) => {
                          if (!c && !string.IsNullOrEmpty(text)) {
                              if (char.IsDigit(text[0]))
                                  text = ">=" + text;
                              string op = ">=";
                              int val = 0;
                              if (text.StartsWith(">=") || text.StartsWith("<=") || text.StartsWith("==") || text.StartsWith("!=")) { op = text.Substring(0, 2); int.TryParse(text.Substring(2), out val); } else if (text.StartsWith(">") || text.StartsWith("<") || text.StartsWith("=")) { op = text.Substring(0, 1); int.TryParse(text.Substring(1), out val); } else { int.TryParse(text, out val); }

                              rule.Conditions.Add(new ConditionGenLvl { Op = op, Value = val });
                              refresh();
                          }
                      }, (Dialog.InputType)0);
                  })
                  .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Dna), () => {
                      Dialog.InputName("Enter DNA Cost (e.g. >=100)", "", (c, text) => {
                          if (!c && !string.IsNullOrEmpty(text)) {
                              if (char.IsDigit(text[0]))
                                  text = ">=" + text;
                              string op = ">=";
                              int val = 0;
                              if (text.StartsWith(">=") || text.StartsWith("<=") || text.StartsWith("==") || text.StartsWith("!=")) { op = text.Substring(0, 2); int.TryParse(text.Substring(2), out val); } else if (text.StartsWith(">") || text.StartsWith("<") || text.StartsWith("=")) { op = text.Substring(0, 1); int.TryParse(text.Substring(1), out val); } else { int.TryParse(text, out val); }

                              rule.Conditions.Add(new ConditionDna { Op = op, Value = val });
                              refresh();
                          }
                      }, (Dialog.InputType)0);
                  })
                  .AddButton("DNA Content", () => {
                      RelocatorPickers.ShowDnaContentPicker(null, (selectedList) => {
                          rule.Conditions.Add(new ConditionDnaContent { DnaIds = new HashSet<string>(selectedList) });
                          refresh();
                      });
                  })
                  .Show();
        }

        public static void EditRuleCondition(FilterNode node, Action refresh) {
            var rule = node.Rule;
            var cond = node.ConditionRef;
            if (cond == null)
                return;

            // Common removal logic?
            // Actually each type might need specific menu + Remove option.

            Action showMenu = () => {
                var menu = RelocatorMenu.Create();
                menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Remove), () => {
                    rule.Conditions.Remove(cond);
                    refresh();
                });

                // Type specific edits starts below

                // Type specific edits
                if (cond is ConditionText t) {
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => Dialog.InputName("Edit Text", t.Text, (c, val) => { if (!c) { t.Text = val; refresh(); } }, (Dialog.InputType)0));
                } else if (cond is ConditionWeight w) {
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => Dialog.InputName("Weight", w.Op + w.Value, (c, val) => {
                        if (!c && !string.IsNullOrEmpty(val)) {
                            string op = ">=";
                            int v = 0;
                            if (char.IsDigit(val[0]))
                                val = ">=" + val;
                            if (val.StartsWith(">=") || val.StartsWith("<=") || val.StartsWith("==") || val.StartsWith("!=")) { op = val.Substring(0, 2); int.TryParse(val.Substring(2), out v); } else if (val.StartsWith(">") || val.StartsWith("<") || val.StartsWith("=")) { op = val.Substring(0, 1); int.TryParse(val.Substring(1), out v); } else { int.TryParse(val, out v); }
                            w.Op = op;
                            w.Value = v;
                            refresh();
                        }
                    }, (Dialog.InputType)0));
                } else if (cond is ConditionGenLvl g) {
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => Dialog.InputName("Gen Level", g.Op + g.Value, (c, val) => {
                        if (!c && !string.IsNullOrEmpty(val)) {
                            string op = ">=";
                            int v = 0;
                            if (char.IsDigit(val[0]))
                                val = ">=" + val;
                            if (val.StartsWith(">=") || val.StartsWith("<=") || val.StartsWith("==") || val.StartsWith("!=")) { op = val.Substring(0, 2); int.TryParse(val.Substring(2), out v); } else if (val.StartsWith(">") || val.StartsWith("<") || val.StartsWith("=")) { op = val.Substring(0, 1); int.TryParse(val.Substring(1), out v); } else { int.TryParse(val, out v); }
                            g.Op = op;
                            g.Value = v;
                            refresh();
                        }
                    }, (Dialog.InputType)0));
                } else if (cond is ConditionDna d) {
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => Dialog.InputName("DNA Cost", d.Op + d.Value, (c, val) => {
                        if (!c && !string.IsNullOrEmpty(val)) {
                            string op = ">=";
                            int v = 0;
                            if (char.IsDigit(val[0]))
                                val = ">=" + val;
                            if (val.StartsWith(">=") || val.StartsWith("<=") || val.StartsWith("==") || val.StartsWith("!=")) { op = val.Substring(0, 2); int.TryParse(val.Substring(2), out v); } else if (val.StartsWith(">") || val.StartsWith("<") || val.StartsWith("=")) { op = val.Substring(0, 1); int.TryParse(val.Substring(1), out v); } else { int.TryParse(val, out v); }
                            d.Op = op;
                            d.Value = v;
                            refresh();
                        }
                    }, (Dialog.InputType)0));
                } else if (cond is ConditionCategory c) {
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => RelocatorPickers.ShowCategoryPicker(c.CategoryIds.ToList(), (ids) => {
                        c.CategoryIds = new HashSet<string>(ids);
                        refresh();
                    }));
                } else if (cond is ConditionRarity r) {
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => RelocatorPickers.ShowRarityPicker(r.Rarities.ToList(), (ids) => {
                        r.Rarities = new HashSet<int>(ids);
                        refresh();
                    }));
                } else if (cond is ConditionQuality q) {
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => Dialog.InputName("Quality", q.Op + q.Value, (c, val) => {
                        if (!c && !string.IsNullOrEmpty(val)) {
                            string op = ">=";
                            int v = 0;
                            if (char.IsDigit(val[0]))
                                val = ">=" + val;
                            if (val.StartsWith(">=")) { op = ">="; int.TryParse(val.Substring(2), out v); } else { int.TryParse(val, out v); }
                            q.Op = op;
                            q.Value = v;
                            refresh();
                        }
                    }, (Dialog.InputType)0));
                } else if (cond is ConditionDnaContent dc) {
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => RelocatorPickers.ShowDnaContentPicker(dc.DnaIds.ToList(), (ids) => {
                        dc.DnaIds = new HashSet<string>(ids);
                        refresh();
                    }));
                } else if (cond is ConditionMaterial m) {
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => RelocatorPickers.ShowMaterialPicker(m.MaterialIds.ToList(), (ids) => {
                        m.MaterialIds = new HashSet<string>(ids);
                        refresh();
                    }));
                } else if (cond is ConditionBless b) {
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => RelocatorPickers.ShowBlessPicker(b.States.ToList(), (ids) => {
                        b.States = new HashSet<int>(ids);
                        refresh();
                    }));
                } else if (cond is ConditionStolen s) {
                    menu.AddButton("Set 'Is Stolen'", () => { s.IsStolen = true; refresh(); });
                    menu.AddButton("Set 'Not Stolen'", () => { s.IsStolen = false; refresh(); });
                } else if (cond is ConditionIdentified i) {
                    menu.AddButton("Set 'Identified'", () => { i.IsIdentified = true; refresh(); });
                    menu.AddButton("Set 'Unidentified'", () => { i.IsIdentified = false; refresh(); });
                } else if (cond is ConditionEnchant e) {
                    if (e.Runes.Count == 1) {
                        string current = e.Runes[0];
                        // attempt parse
                        string key = current;
                        string op = ">=";
                        int val = 0;
                        string[] ops = [">=", "<=", "!=", ">", "<", "="];
                        foreach (var o in ops) {
                            int idx = current.IndexOf(o);
                            if (idx > 0) {
                                op = o;
                                key = current.Substring(0, idx).Trim();
                                int.TryParse(current.Substring(idx + o.Length), out val);
                                break;
                            }
                        }

                        menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.EditValue), () => {
                            Dialog.InputName("Value", op + val, (cVal, textVal) => {
                                if (!cVal && !string.IsNullOrEmpty(textVal)) {
                                    // Reconstruct
                                    // Check if user typed new op
                                    string newOp = op;
                                    // int newVal = val; // Unused
                                    if (char.IsDigit(textVal[0]))
                                        textVal = op + textVal; // keep old op if just digits

                                    e.Runes[0] = key + textVal;
                                    refresh();
                                }
                            }, (Dialog.InputType)0);
                        });

                        menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.ChangeEnchant), () => {
                            // Show picker again
                            RelocatorPickers.ShowEnchantPicker(0, (ele) => {
                                e.Runes[0] = "@" + ele.GetName() + op + val;
                                refresh();
                            });
                        });
                    }

                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit) + " (Raw)", () => {
                        Dialog.InputName("Runes (comma sep)", string.Join(",", e.Runes), (c, val) => {
                            if (!c) { e.Runes = val.Split(',').Select(s => s.Trim()).ToList(); refresh(); }
                        }, (Dialog.InputType)0);
                    });
                }

                menu.Show();
            };

            showMenu();
        }
    }
}
