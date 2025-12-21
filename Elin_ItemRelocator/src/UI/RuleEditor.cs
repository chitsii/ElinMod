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
                                      if (rule.Enchants is null)
                                          rule.Enchants = [];
                                      rule.Enchants.Add(text);
                                      refresh();
                                  });
                              });
                          })
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatWeapon), () => {
                              RelocatorPickers.ShowEnchantPicker(1, (ele) => {
                                  AddEnchantFilterDialog(ele, (text) => {
                                      if (rule.Enchants is null)
                                          rule.Enchants = [];
                                      rule.Enchants.Add(text);
                                      refresh();
                                  });
                              });
                          })
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatArmor), () => {
                              RelocatorPickers.ShowEnchantPicker(2, (ele) => {
                                  AddEnchantFilterDialog(ele, (text) => {
                                      if (rule.Enchants is null)
                                          rule.Enchants = [];
                                      rule.Enchants.Add(text);
                                      refresh();
                                  });
                              });
                          })
                          .Show();
                 })
                .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Category), () => {
                    RelocatorPickers.ShowCategoryPicker([], (selectedIds) => {
                        if (selectedIds.Count > 0) {
                            foreach (var id in selectedIds)
                                if (!rule.CategoryIds.Contains(id))
                                    rule.CategoryIds.Add(id);
                            refresh();
                        }
                    });
                })
                .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Rarity), () => {
                    RelocatorPickers.ShowRarityPicker(rule.Rarities?.ToList(), (selected) => {
                        if (rule.Rarities is null)
                            rule.Rarities = [];
                        foreach (var r in selected)
                            rule.Rarities.Add(r);
                        refresh();
                    });
                })
                .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Enhancement), () => {
                    Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.EditEnhancement), "", (c, text) => {
                        if (!c && !string.IsNullOrEmpty(text)) {
                            rule.Quality = text;
                            rule.InvalidateCache();
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
                                 rule.InvalidateCache();
                                 refresh();
                             }
                         }
                     }, (Dialog.InputType)0);
                 })
                  .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Material), () => {
                      RelocatorPickers.ShowMaterialPicker(rule.MaterialIds?.ToList(), (aliases) => {
                          rule.MaterialIds = new HashSet<string>(aliases);
                          refresh();
                      });
                  })
                  .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Bless), () => {
                      RelocatorPickers.ShowBlessPicker(rule.BlessStates?.ToList(), (states) => {
                          rule.BlessStates = new HashSet<int>(states);
                          refresh();
                      });
                  })
                  .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.Stolen), (child) => {
                      child
                           .AddButton("Yes (Is Stolen)", () => { rule.IsStolen = true; refresh(); })
                           .AddButton("No (Not Stolen)", () => { rule.IsStolen = false; refresh(); });
                  })
                  .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.Identified), (child) => {
                      child
                           .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.StateIdentified), () => { rule.IsIdentified = true; refresh(); })
                           .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.StateUnidentified), () => { rule.IsIdentified = false; refresh(); });
                  })
                  .Show();
        }

        public static void EditRuleCondition(FilterNode node, Action refresh) {
            var rule = node.Rule;
            switch (node.CondType) {
            case ConditionType.Text:
                Dialog.InputName("Edit Text", rule.Text, (c, val) => { if (!c) { rule.Text = val; refresh(); } }, (Dialog.InputType)0);
                break;
            case ConditionType.Enchant:
                RelocatorMenu.Create()
                    .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.EditValue), () => {
                        // Parse current string
                        string current = node.CondValue;
                        string name = current;
                        string valPart = "";
                        string[] ops = [">=", "<=", "!=", ">", "<", "="];
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
                break;

            case ConditionType.Rarity:
                RelocatorPickers.ShowRarityPicker(rule.Rarities?.ToList(), (selected) => {
                    rule.Rarities = new HashSet<int>(selected);
                    refresh();
                });
                break;
            case ConditionType.Quality:
                Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.EditEnhancement), rule.Quality, (c, val) => { if (!c) { rule.Quality = val; rule.InvalidateCache(); refresh(); } }, (Dialog.InputType)0);
                break;
            case ConditionType.Category:
                RelocatorPickers.ShowCategoryPicker([node.CondValue], (ids) => {
                    rule.CategoryIds.Remove(node.CondValue);
                    foreach (var id in ids)
                        if (!rule.CategoryIds.Contains(id))
                            rule.CategoryIds.Add(id);
                    refresh();
                });
                break;
            case ConditionType.Weight:
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
                            rule.InvalidateCache();
                            refresh();
                        }
                    }
                }, (Dialog.InputType)0);
                break;
            case ConditionType.Material:
                RelocatorPickers.ShowMaterialPicker(rule.MaterialIds?.ToList(), (aliases) => {
                    rule.MaterialIds = new HashSet<string>(aliases);
                    refresh();
                });
                break;
            case ConditionType.Bless:
                RelocatorPickers.ShowBlessPicker(rule.BlessStates?.ToList(), (states) => {
                    rule.BlessStates = new HashSet<int>(states);
                    refresh();
                });
                break;
            case ConditionType.Stolen:
                RelocatorMenu.Create()
                     .AddButton("Yes (Is Stolen)", () => { rule.IsStolen = true; refresh(); })
                     .AddButton("No (Not Stolen)", () => { rule.IsStolen = false; refresh(); })
                     .Show();
                break;
            case ConditionType.Identified:
                RelocatorMenu.Create()
                     .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.StateIdentified), () => { node.Rule.IsIdentified = true; refresh(); })
                     .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.StateUnidentified), () => { node.Rule.IsIdentified = false; refresh(); })
                     .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Remove), () => { node.Rule.IsIdentified = null; refresh(); })
                     .Show();
                break;
            }
        }
    }
}
