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
                            if (string.IsNullOrEmpty(rule.Text))
                                rule.Text = text;
                            else
                                rule.Text += " " + text;
                            refresh();
                        }
                    }, (Dialog.InputType)0);
                })
                 .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Enchant), () => {
                     RelocatorMenu.Create()
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatAll), () => {
                              RelocatorPickers.ShowEnchantPicker(0, (ele) => {
                                  AddEnchantFilterDialog(ele, (text) => {
                                      if (rule.Enchants == null)
                                          rule.Enchants = new List<string>();
                                      rule.Enchants.Add(text);
                                      refresh();
                                  });
                              });
                          })
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatWeapon), () => {
                              RelocatorPickers.ShowEnchantPicker(1, (ele) => {
                                  AddEnchantFilterDialog(ele, (text) => {
                                      if (rule.Enchants == null)
                                          rule.Enchants = new List<string>();
                                      rule.Enchants.Add(text);
                                      refresh();
                                  });
                              });
                          })
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatArmor), () => {
                              RelocatorPickers.ShowEnchantPicker(2, (ele) => {
                                  AddEnchantFilterDialog(ele, (text) => {
                                      if (rule.Enchants == null)
                                          rule.Enchants = new List<string>();
                                      rule.Enchants.Add(text);
                                      refresh();
                                  });
                              });
                          })
                          .Show();
                 })
                .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Category), () => {
                    RelocatorPickers.ShowCategoryPicker(new List<string>(), (selectedIds) => {
                        if (selectedIds.Count > 0) {
                            foreach (var id in selectedIds)
                                if (!rule.CategoryIds.Contains(id))
                                    rule.CategoryIds.Add(id);
                            refresh();
                        }
                    });
                })
                .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Rarity), () => {
                    RelocatorPickers.ShowRarityPicker(rule.Rarities != null ? rule.Rarities.ToList() : null, (selected) => {
                        if (rule.Rarities == null)
                            rule.Rarities = new HashSet<int>();
                        foreach (var r in selected)
                            rule.Rarities.Add(r);
                        refresh();
                    });
                })
                .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Quality), () => {
                    Dialog.InputName("Enter Quality (e.g. >=2)\nSupported: ==, >=, <=, <, >, !=", "", (c, text) => {
                        if (!c && !string.IsNullOrEmpty(text)) {
                            rule.Quality = text;
                            refresh();
                        }
                    }, (Dialog.InputType)0);
                })
                 .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Weight), () => {
                     Dialog.InputName("Enter Weight (e.g. >=10)", "", (c, text) => {
                         if (!c && !string.IsNullOrEmpty(text)) {
                             if (char.IsDigit(text[0]))
                                 text = ">=" + text;

                             // Parse operator and value
                             string op = ">=";
                             string valStr = text;
                             if (text.StartsWith(">=") || text.StartsWith("<=") || text.StartsWith("==") || text.StartsWith("!=")) {
                                 op = text.Substring(0, 2);
                                 valStr = text.Substring(2);
                             } else if (text.StartsWith(">") || text.StartsWith("<") || text.StartsWith("=")) {
                                 op = text.Substring(0, 1);
                                 valStr = text.Substring(1);
                             }

                             int w;
                             if (int.TryParse(valStr, out w)) {
                                 rule.Weight = w;
                                 rule.WeightOp = op;
                                 refresh();
                             }
                         }
                     }, (Dialog.InputType)0);
                 })
                  .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Material), () => {
                      RelocatorPickers.ShowMaterialPicker(rule.MaterialIds != null ? rule.MaterialIds.ToList() : null, (aliases) => {
                          rule.MaterialIds = new HashSet<string>(aliases);
                          refresh();
                      });
                  })
                  .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Bless), () => {
                      RelocatorPickers.ShowBlessPicker(rule.BlessStates != null ? rule.BlessStates.ToList() : null, (states) => {
                          rule.BlessStates = new HashSet<int>(states);
                          refresh();
                      });
                  })
                  .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.Stolen), (child) => {
                      child
                           .AddButton("Yes (Is Stolen)", () => { rule.IsStolen = true; refresh(); })
                           .AddButton("No (Not Stolen)", () => { rule.IsStolen = false; refresh(); });
                  })
                  .Show();
        }

        public static void EditRuleCondition(FilterNode node, Action refresh) {
            var rule = node.Rule;
            if (node.CondType == ConditionType.Text) {
                Dialog.InputName("Edit Text", rule.Text, (c, val) => { if (!c) { rule.Text = val; refresh(); } }, (Dialog.InputType)0);
            } else if (node.CondType == ConditionType.Enchant) {
                RelocatorMenu.Create()
                    .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.EditValue), () => {
                        // Parse current string
                        string current = node.CondValue;
                        string name = current;
                        string valPart = "";
                        string[] ops = new string[] { ">=", "<=", "!=", ">", "<", "=" };
                        foreach (var op in ops) {
                            int idx = current.IndexOf(op);
                            if (idx > 0) {
                                name = current.Substring(0, idx).Trim();
                                valPart = current.Substring(idx).Trim();
                                break;
                            }
                        }

                        Dialog.InputName("Amount (e.g. >=10)", valPart, (c, val) => {
                            if (!c && !string.IsNullOrEmpty(val)) {
                                if (char.IsDigit(val[0]))
                                    val = ">=" + val;

                                string newFilter = name + val;
                                rule.Enchants.Remove(node.CondValue);
                                rule.Enchants.Add(newFilter);
                                refresh();
                            }
                        }, (Dialog.InputType)0);
                    })
                    .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.ChangeEnchant), () => {
                        RelocatorMenu.Create()
                              .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatAll), () => {
                                  RelocatorPickers.ShowEnchantPicker(0, (ele) => {
                                      AddEnchantFilterDialog(ele, (text) => {
                                          rule.Enchants.Remove(node.CondValue);
                                          rule.Enchants.Add(text);
                                          refresh();
                                      });
                                  });
                              })
                              .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatWeapon), () => {
                                  RelocatorPickers.ShowEnchantPicker(1, (ele) => {
                                      AddEnchantFilterDialog(ele, (text) => {
                                          rule.Enchants.Remove(node.CondValue);
                                          rule.Enchants.Add(text);
                                          refresh();
                                      });
                                  });
                              })
                              .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatArmor), () => {
                                  RelocatorPickers.ShowEnchantPicker(2, (ele) => {
                                      AddEnchantFilterDialog(ele, (text) => {
                                          rule.Enchants.Remove(node.CondValue);
                                          rule.Enchants.Add(text);
                                          refresh();
                                      });
                                  });
                              })
                              .Show();
                    })
                    .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Remove), () => {
                        rule.Enchants.Remove(node.CondValue);
                        refresh();
                    })
                    .Show();
            } else if (node.CondType == ConditionType.Rarity) {
                RelocatorPickers.ShowRarityPicker(rule.Rarities != null ? rule.Rarities.ToList() : null, (selected) => {
                    rule.Rarities = new HashSet<int>(selected);
                    refresh();
                });
            } else if (node.CondType == ConditionType.Quality) {
                Dialog.InputName("Edit Quality", rule.Quality, (c, val) => { if (!c) { rule.Quality = val; refresh(); } }, (Dialog.InputType)0);
            } else if (node.CondType == ConditionType.Category) {
                RelocatorPickers.ShowCategoryPicker(new List<string> { node.CondValue }, (ids) => {
                    rule.CategoryIds.Remove(node.CondValue);
                    foreach (var id in ids)
                        if (!rule.CategoryIds.Contains(id))
                            rule.CategoryIds.Add(id);
                    refresh();
                });
            } else if (node.CondType == ConditionType.Weight) {
                Dialog.InputName("Edit Weight", rule.Weight.ToString(), (c, val) => {
                    if (!c && !string.IsNullOrEmpty(val)) {
                        if (char.IsDigit(val[0]))
                            val = ">=" + val;
                        string op = ">=";
                        string valStr = val;
                        if (val.StartsWith(">=") || val.StartsWith("<=") || val.StartsWith("==") || val.StartsWith("!=")) {
                            op = val.Substring(0, 2);
                            valStr = val.Substring(2);
                        } else if (val.StartsWith(">") || val.StartsWith("<") || val.StartsWith("=")) {
                            op = val.Substring(0, 1);
                            valStr = val.Substring(1);
                        }
                        int w;
                        if (int.TryParse(valStr, out w)) {
                            rule.Weight = w;
                            rule.WeightOp = op;
                            refresh();
                        }
                    }
                }, (Dialog.InputType)0);
            } else if (node.CondType == ConditionType.Material) {
                RelocatorPickers.ShowMaterialPicker(rule.MaterialIds != null ? rule.MaterialIds.ToList() : null, (aliases) => {
                    rule.MaterialIds = new HashSet<string>(aliases);
                    refresh();
                });
            } else if (node.CondType == ConditionType.Bless) {
                RelocatorPickers.ShowBlessPicker(rule.BlessStates != null ? rule.BlessStates.ToList() : null, (states) => {
                    rule.BlessStates = new HashSet<int>(states);
                    refresh();
                });
            } else if (node.CondType == ConditionType.Stolen) {
                RelocatorMenu.Create()
                     .AddButton("Yes (Is Stolen)", () => { rule.IsStolen = true; refresh(); })
                     .AddButton("No (Not Stolen)", () => { rule.IsStolen = false; refresh(); })
                     .Show();
            }
        }
    }
}
