using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Linq;

namespace Elin_ItemRelocator
{
    public class LayerItemRelocator : ELayer
    {
        // Tree Node Wrapper
        private class FilterNode
        {
            public RelocationRule Rule;     // Level 1: Rule

            // Level 2: Condition Details
            public ConditionType CondType;
            public string CondValue; // ID or Text
            public string DisplayText;

            public bool IsRule { get { return Rule != null && CondType == ConditionType.None; } }
            public bool IsCondition { get { return CondType != ConditionType.None && CondType != ConditionType.AddButton && CondType != ConditionType.Settings; } }
            public bool IsAddButton { get { return CondType == ConditionType.AddButton; } }
            public bool IsSettings { get { return CondType == ConditionType.Settings; } }

            // Override Equals/GetHashCode for Persistence (Expansion State)
            public override bool Equals(object obj)
            {
                var other = obj as FilterNode;
                if (other == null) return false;
                if (IsRule && other.IsRule) return Rule == other.Rule; // Identity based on Rule instance
                return base.Equals(obj);
            }
            public override int GetHashCode()
            {
                if (IsRule) return Rule.GetHashCode();
                return base.GetHashCode();
            }
        }

        private enum ConditionType { None, Category, Rarity, Quality, Text, Id, AddButton, Settings, Weight, Material, Bless, Stolen }

        // ====================================================================
        // Fields
        // ====================================================================
        private static RelocatorTable<Thing> previewTable;
        private static RelocatorAccordion<FilterNode> mainAccordion;
        private static Thing currentContainer;

        // ====================================================================
        // Main Entry Point
        // ====================================================================
        public static void Open(Thing container)
        {
             currentContainer = container;

             // Setup Accordion Logic FIRST
             mainAccordion = RelocatorAccordion<FilterNode>.Create();
             var profile = RelocatorManager.Instance.GetProfile(container);

             // UX: Default Empty Rule for new/empty profiles
             if (profile.Rules.Count == 0) {
                 profile.Rules.Add(new RelocationRule { Name = RelocatorLang.GetText(RelocatorLang.LangKey.NewRuleName) + " 1" });
             }

             Action refresh = null;
             // Define Refresh Logic
             refresh = () => {
                 // Rebuild Data
                 List<FilterNode> roots = new List<FilterNode>();


                 if (profile.Rules != null) {
                     foreach(var r in profile.Rules) {
                         var node = new FilterNode { Rule = r, CondType = ConditionType.None };
                         roots.Add(node);
                         // Default Open: Ensure rule is expanded regardless of state
                         // But we want persistence. Since we override Equals based on Rule,
                         // previously expanded rules remain expanded.
                         // But for FIRST load or New Rule, we should expand it.
                         // 'Expand' method relies on 'Equals'.
                         // If we call Expand(node) it will add it to the set.
                         // Persistence is handled by SetRoots not clearing 'expanded'.
                         // WE WANT TO FORCE EXPAND ALWAYS according to user request?
                         // "Default to open" implies new ones open.
                         // User said: "Adding condition closes rule is bad". Override Equals fixes that.
                         // "Rule default open" -> Let's force expand all on refresh? No, that prevents closing.
                         // But for UX, let's Expand if not already tracked (aka new).
                         // However, since we recreate nodes, we can't easily distinguish 'new' from 'closed'.
                         // Use 'mainAccordion.Expand(node)' which checks 'contains'.
                         mainAccordion.Expand(node);
                     }
                 }
                 mainAccordion.SetRoots(roots);
                 mainAccordion.Refresh();

                 RefreshPreview(null, container, profile);
             };

             // Configure Accordion
             mainAccordion.SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Title));

              mainAccordion.SetOnBuildRow((trans, node) => {
                  // Settings row logic removed
              });

             mainAccordion.SetChildren((node) => {
                 if (node.IsRule) {
                     var list = new List<FilterNode>();
                     var r = node.Rule;

                     // Deconstruct Rule into Nodes
                     if (r.CategoryIds.Count > 0) {
                        foreach(var id in r.CategoryIds) {
                            string name = id;
                            var source = EClass.sources.categories.map.TryGetValue(id);
                            if (source != null) name = source.GetName();
                            list.Add(new FilterNode { Rule = r, CondType = ConditionType.Category, CondValue = id, DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Category) + ": " + name });
                        }
                     }
                     if (r.Rarity.HasValue) {
                         string op = string.IsNullOrEmpty(r.RarityOp) ? ">=" : r.RarityOp;
                         list.Add(new FilterNode { Rule = r, CondType = ConditionType.Rarity, DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Rarity) + " " + op + " " + r.Rarity });
                     }
                     if (!string.IsNullOrEmpty(r.Quality)) {
                         list.Add(new FilterNode { Rule = r, CondType = ConditionType.Quality, DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Quality) + " " + r.Quality });
                     }
                     if (!string.IsNullOrEmpty(r.Text)) {
                         list.Add(new FilterNode { Rule = r, CondType = ConditionType.Text, DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Text) + ": " + r.Text });
                     }
                     if (r.Weight.HasValue) {
                         list.Add(new FilterNode { Rule = r, CondType = ConditionType.Weight, CondValue = r.Weight.Value.ToString(), DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Weight) + " " + (string.IsNullOrEmpty(r.WeightOp) ? ">=" : r.WeightOp) + " " + r.Weight });
                     }

                     // ADD BUTTON
                     // Material
                     if (r.MaterialIds != null && r.MaterialIds.Count > 0) {
                          string prefix = r.NotMaterial ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                          HashSet<string> allMats = r.MaterialIds;
                          string displayMat = "";
                          if (allMats.Count <= 3) {
                               List<string> names = new List<string>();
                               foreach(var mid in allMats) {
                                    var ms = EClass.sources.materials.rows.FirstOrDefault(m => m.alias.Equals(mid, StringComparison.OrdinalIgnoreCase) || m.id.ToString() == mid);
                                    names.Add(ms != null ? ms.GetName() : mid);
                               }
                               displayMat = string.Join(", ", names.ToArray());
                          } else {
                               displayMat = "(" + allMats.Count + ")";
                          }
                          list.Add(new FilterNode { Rule = r, CondType = ConditionType.Material, CondValue = "Multi", DisplayText = prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Material) + ": " + displayMat });
                     }

                     // Bless
                     if (r.BlessStates != null && r.BlessStates.Count > 0) {
                           string prefix = r.NotBless ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                           HashSet<int> allStates = r.BlessStates;

                           List<string> names = new List<string>();
                           foreach(var b in allStates) {
                               if (b==1) names.Add(RelocatorLang.GetText(RelocatorLang.LangKey.StateBlessed));
                               else if (b==-1) names.Add(RelocatorLang.GetText(RelocatorLang.LangKey.StateCursed));
                               else if (b==0) names.Add(RelocatorLang.GetText(RelocatorLang.LangKey.StateNormal));
                               else names.Add(RelocatorLang.GetText(RelocatorLang.LangKey.StateDoomed));
                           }
                           list.Add(new FilterNode { Rule = r, CondType = ConditionType.Bless, DisplayText = prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Bless) + ": " + string.Join(", ", names.ToArray()) });
                     }

                     // Stolen
                     if (r.IsStolen.HasValue) {
                          string prefix = r.NotStolen ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                          list.Add(new FilterNode { Rule = r, CondType = ConditionType.Stolen, DisplayText = prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Stolen) + ": " + (r.IsStolen.Value ? "Yes" : "No") });
                     }

                     // ADD BUTTON
                     list.Add(new FilterNode { Rule = r, CondType = ConditionType.AddButton, DisplayText = " + " });

                     return list;
                 }
                 return null;
             });

             mainAccordion.SetText((node) => {
                 if (node.IsRule) {
                     string status = node.Rule.Enabled ? "" : " (Disabled)";
                     return node.Rule.Name + " (" + node.Rule.GetConditionList().Count + ")" + status;
                 }
                 return node.DisplayText;
             });

             mainAccordion.SetGetBackgroundColor((node) => {
                 if (node.IsRule) {
                     return new Color(0.85f, 0.82f, 0.75f, 1f);
                 }
                 if (node.IsAddButton) {
                     return Color.clear;
                 }
                 return Color.clear;
             });

             mainAccordion.SetOnSelect((node) => {
                 if (node.IsAddButton) {
                     ShowAddConditionMenu(node.Rule, refresh);
                 }
                 else if (node.IsCondition) {
                     EditRuleCondition(node, refresh);
                 }
             });

             mainAccordion.SetOnRightClick((node) => {
                 if (node.IsRule) {
                     var menu = RelocatorMenu.Create();
                     menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Rename), () => {
                             Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.NewRuleName), node.Rule.Name, (c, text) => {
                                 if(!c && !string.IsNullOrEmpty(text)) { node.Rule.Name = text; refresh(); }
                             }, (Dialog.InputType)0);
                         })
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Remove), () => {
                             Dialog.YesNo(RelocatorLang.GetText(RelocatorLang.LangKey.Delete) + "?", () => { profile.Rules.Remove(node.Rule); refresh(); });
                         })
                         .AddButton(node.Rule.Enabled ? RelocatorLang.GetText(RelocatorLang.LangKey.Disable) : RelocatorLang.GetText(RelocatorLang.LangKey.Enable), () => { node.Rule.Enabled = !node.Rule.Enabled; refresh(); })
                         .Show();
                 }
             });



              mainAccordion.SetOnBuildRowExtra((node, rowGO) => {
                  if (node.IsCondition) {
                      // Negation Button
                      bool isNegated = false;
                      Action toggleNegation = null;

                      switch(node.CondType) {
                          case ConditionType.Category:
                              isNegated = node.Rule.NegatedCategoryIds != null && node.Rule.NegatedCategoryIds.Contains(node.CondValue);
                              toggleNegation = () => {
                                  if (node.Rule.NegatedCategoryIds == null) node.Rule.NegatedCategoryIds = new HashSet<string>();
                                  if (node.Rule.NegatedCategoryIds.Contains(node.CondValue)) node.Rule.NegatedCategoryIds.Remove(node.CondValue);
                                  else node.Rule.NegatedCategoryIds.Add(node.CondValue);
                                  refresh();
                              };
                              break;
                          case ConditionType.Rarity:
                              isNegated = node.Rule.NotRarity;
                              toggleNegation = () => { node.Rule.NotRarity = !node.Rule.NotRarity; refresh(); };
                              break;
                          case ConditionType.Quality:
                              isNegated = node.Rule.NotQuality;
                              toggleNegation = () => { node.Rule.NotQuality = !node.Rule.NotQuality; refresh(); };
                              break;
                          case ConditionType.Text:
                              isNegated = node.Rule.NotText;
                              toggleNegation = () => { node.Rule.NotText = !node.Rule.NotText; refresh(); };
                              break;
                          case ConditionType.Weight:
                              isNegated = node.Rule.NotWeight;
                              toggleNegation = () => { node.Rule.NotWeight = !node.Rule.NotWeight; refresh(); };
                              break;
                      }

                      if (toggleNegation != null) {
                          var btnNeg = CreateTinyButton(rowGO.transform, RelocatorLang.GetText(RelocatorLang.LangKey.Not), toggleNegation);
                          var txtNeg = btnNeg.GetComponentInChildren<Text>();
                          var imgNeg = btnNeg.GetComponent<Image>();
                          if (isNegated) {
                              if(txtNeg) txtNeg.color = Color.red; /*Red for Negated*/
                              if(imgNeg) imgNeg.color = new Color(1f, 0.8f, 0.8f);
                          } else {
                              if(txtNeg) txtNeg.color = SkinManager.CurrentColors.textDefault;
                              if(imgNeg) imgNeg.color = new Color(0.9f, 0.9f, 0.9f);
                          }
                      }

                      // Remove Button (Updated Signature)
                     var btnRemove = CreateTinyButton(rowGO.transform, "x", () => {
                          Dialog.YesNo(RelocatorLang.GetText(RelocatorLang.LangKey.Delete) + "?", () => {
                                 switch(node.CondType) {
                                     case ConditionType.Category:
                                         node.Rule.CategoryIds.Remove(node.CondValue);
                                         break;
                                     case ConditionType.Rarity:
                                         node.Rule.Rarity = null;
                                         break;
                                     case ConditionType.Quality:
                                         node.Rule.Quality = null;
                                         break;
                                     case ConditionType.Text:
                                         node.Rule.Text = null;
                                         break;
                                     case ConditionType.Weight:
                                         node.Rule.Weight = null;
                                         break;
                                     case ConditionType.Material:
                                         node.Rule.MaterialIds = null;
                                         break;
                                     case ConditionType.Bless:
                                         node.Rule.BlessStates = null;
                                         break;
                                     case ConditionType.Stolen:
                                         node.Rule.IsStolen = null;
                                         break;
                                 }
                                 refresh();
                          });
                     });
                 }
             });

             // Initialize Layers (Main and Preview)
             LayerList layerMain, layerPreview;
             InitLayers(out layerMain, out layerPreview);

             // Restore Footer Buttons ("Settings", "Execute", "Add Rule")
             // "Add Rule" stays in Accordion? No, user said "Except Add Filter".
             // "Add Filter" is gone. We have "Add Rule".
             // Let's put ALL main actions in Footer for consistency.
             var win = layerMain.windows[0];
             win.AddBottomButton(RelocatorLang.GetText(RelocatorLang.LangKey.AddRule), () => {
                 Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.NewRuleName), RelocatorLang.GetText(RelocatorLang.LangKey.NewRuleName), (c, text) => {
                     if (!c && !string.IsNullOrEmpty(text)) {
                         profile.Rules.Add(new RelocationRule { Name = text });
                         refresh();
                     }
                 }, (Dialog.InputType)0);
             });
             win.AddBottomButton(RelocatorLang.GetText(RelocatorLang.LangKey.Settings), () => ShowSettingsMenu(profile, refresh));
             win.AddBottomButton(RelocatorLang.GetText(RelocatorLang.LangKey.Execute), () => {
                 RelocatorManager.Instance.ExecuteRelocation(container);
                 Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Relocated), ""));
                 if (mainAccordion != null) mainAccordion.Close();
             });

             // Initial Data Load
             refresh();
        }

        // ====================================================================
        // Layer Initialization & Setup
        // ====================================================================
        private static void InitLayers(out LayerList main, out LayerList preview)
        {
             // 1. Create Main Layer via Accordion
             var _main = mainAccordion.Show();
             var winMain = _main.windows[0];

             // Add Help Button to Footer (Requested by User)
             winMain.AddBottomButton(" [ ? ] ", () => {
                  Dialog.Ok("<b>" + RelocatorLang.GetText(RelocatorLang.LangKey.HelpTitle) + "</b>\n\n" + RelocatorLang.GetText(RelocatorLang.LangKey.HelpText));
             });

             // 2. Create Preview Table
             previewTable = RelocatorTable<Thing>.Create()
                 .SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Preview))
                 .SetShowHeader(true)
                 .SetPreferredHeight(800)
                 .SetOnSelect((t) => {
                       var menu = RelocatorMenu.Create();
                       menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Move), () => {
                           if (currentContainer != null) {
                               RelocatorManager.Instance.RelocateSingleThing(t, currentContainer);
                               if (previewTable != null) previewTable.Refresh();
                           }
                       });
                       menu.Show();
                 })
                 .AddColumn(RelocatorLang.GetText(RelocatorLang.LangKey.Text), 350, (t, cell) => {
                      var txt = cell.GetComponentInChildren<Text>();
                      if (!txt) {
                          var g = new GameObject("Text");
                          g.transform.SetParent(cell.transform, false);
                          txt = g.AddComponent<Text>();
                          // Default Font & Dark Brown Color
                          txt.font = SkinManager.Instance.fontSet.ui.source.font;
                          txt.color = SkinManager.CurrentColors.textDefault;
                          txt.alignment = TextAnchor.MiddleLeft;
                          txt.resizeTextForBestFit = true;
                          txt.resizeTextMinSize = 10;
                          txt.resizeTextMaxSize = 13;
                          txt.horizontalOverflow = HorizontalWrapMode.Wrap;
                          txt.verticalOverflow = VerticalWrapMode.Truncate;
                          txt.raycastTarget = false;
                           var rt = txt.rectTransform;
                           rt.anchorMin = Vector2.zero;
                           rt.anchorMax = Vector2.one;
                           rt.sizeDelta = Vector2.zero;
                       }

                      if(t != null) {
                          txt.text = t.Name;
                      } else { txt.text = ""; }

                       // Find the row button
                       var rowBtn = cell.transform.parent.GetComponentInChildren<UIButton>();
                       if (rowBtn) {
                            var field = typeof(UIButton).GetField("tooltip", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic);
                            if (field != null) field.SetValue(rowBtn, null);
                            rowBtn.SetTooltip((tooltip) => {
                                if (t != null && tooltip.note != null) t.WriteNote(tooltip.note);
                            }, true);
                       }
                 })
                 .AddTextColumn(RelocatorLang.GetText(RelocatorLang.LangKey.Category), 100, t => t != null && t.category != null ? t.category.GetName() : "")
                 .AddTextColumn(RelocatorLang.GetText(RelocatorLang.LangKey.Parent), 100, t => {
                      if (t == null || t.parent == null) return "";
                      if (t.parent == EClass.pc.things) return RelocatorLang.GetText(RelocatorLang.LangKey.Inventory);
                      if (t.parent == EClass._map.things) return RelocatorLang.GetText(RelocatorLang.LangKey.Zone);
                      if (t.parent is Card) return (t.parent as Card).Name;
                      return t.parent.ToString();
                 });

             var _preview = previewTable.Show();
             var winPreview = _preview.windows[0];

             // Ensure Preview Window is on top
             _preview.transform.SetAsLastSibling();
             foreach (var g in _preview.GetComponentsInChildren<Graphic>(true))
             {
                 if (g.transform.IsChildOf(winPreview.transform) || g.gameObject == winPreview.gameObject)
                     continue;
                 g.raycastTarget = false;
             }

             // Resize Configuration
             winMain.setting.allowResize = true;

             winPreview.setting.allowResize = true;
             _main.SetSize(700, 800);

             // Position Configuration
             var rectMain = winMain.GetComponent<RectTransform>();
             var rectPreview = winPreview.GetComponent<RectTransform>();
             rectMain.anchoredPosition = new Vector2(-360, 0);
             rectPreview.anchoredPosition = new Vector2(360, 0);

             // Synced Closing Logic
             bool closing = false;
             OnKill(_main, () => {
                if (closing) return;
                closing = true;
                if (mainAccordion != null) mainAccordion.Close();
                if (_preview != null) _preview.Close();
             });
             OnKill(_preview, () => {
                 if (closing) return;
                 closing = true;
                 if (_main != null) _main.Close();
             });

             main = _main;
             preview = _preview;
        }

        private static void OnKill(ELayer layer, Action action) {
             layer.onKill.AddListener(() => action());
        }

        public override void OnRightClick() {
            // Disable default close
        }

        // ====================================================================
        // Refresh Logic
        // ====================================================================
        private static void RefreshPreview(LayerList layer, Thing container, RelocationProfile profile)
        {
                List<Thing> matches = RelocatorManager.Instance.GetMatches(container).ToList();
                 // Sort Matches
                 // profile is not passed here... wait, RelocatorManager has no reference to profile?
                 // RefreshPreview is used inside Show which has 'profile' variable in closure.
                 // But RefreshPreview below is static and takes (layer, container).
                 // Ah, 'profile' is NOT available here statically unless passed or accessed via closure if not static.
                 // This method is 'private static'!
                 // I need to change signature to accept profile or access it.
                 // Actually, it is called from 'InitLayers' or 'refresh' lambda?
                 // 'InitLayers' is called from Show(profile).
                 // 'refresh' lambda captures 'profile'.
                 // So I should pass 'profile' to RefreshPreview.
                 // 'RefreshPreview' is defined at line 435.
                 // I'll update the signature.

                 if (profile != null) // Add check
                 {
                     switch(profile.SortMode) {
                        case RelocationProfile.ResultSortMode.PriceAsc: matches.Sort((a,b) => a.GetPrice(CurrencyType.Money) - b.GetPrice(CurrencyType.Money)); break;
                        case RelocationProfile.ResultSortMode.PriceDesc: matches.Sort((a,b) => b.GetPrice(CurrencyType.Money) - a.GetPrice(CurrencyType.Money)); break;
                        case RelocationProfile.ResultSortMode.EnchantMagAsc: matches.Sort((a,b) => a.encLV - b.encLV); break;
                        case RelocationProfile.ResultSortMode.EnchantMagDesc: matches.Sort((a,b) => b.encLV - a.encLV); break;
                        case RelocationProfile.ResultSortMode.TotalWeightAsc: matches.Sort((a,b) => (a.SelfWeight * a.Num) - (b.SelfWeight * b.Num)); break;
                        case RelocationProfile.ResultSortMode.TotalWeightDesc: matches.Sort((a,b) => (b.SelfWeight * b.Num) - (a.SelfWeight * a.Num)); break;
                        case RelocationProfile.ResultSortMode.UnitWeightAsc: matches.Sort((a,b) => a.SelfWeight - b.SelfWeight); break;
                        case RelocationProfile.ResultSortMode.UnitWeightDesc: matches.Sort((a,b) => b.SelfWeight - a.SelfWeight); break;
                     }
                 }

                 int count = matches.Count;
                string countStr = count >= 100 ? "100+" : count.ToString();

                if (previewTable != null)
                {
                    previewTable.SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Preview) + " (" + countStr + ")");
                    previewTable.SetDataSource(matches);
                    previewTable.Refresh();
                }
        }

        private static void ShowAddConditionMenu(RelocationRule rule, Action refresh)
        {
             RelocatorMenu.Create()
                 .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Text), () => {
                     Dialog.InputName("Enter Text/Tag", "", (c, text) => {
                         if (!c && !string.IsNullOrEmpty(text)) {
                             if(string.IsNullOrEmpty(rule.Text)) rule.Text = text;
                             else rule.Text += " " + text;
                             refresh();
                         }
                     }, (Dialog.InputType)0);
                 })
                  .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Enchant), () => {
                      RelocatorMenu.Create()
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatAll), () => {
                              RelocatorPickers.ShowEnchantPicker(0, (ele) => {
                                  AddEnchantFilterDialog(ele, (text) => {
                                      if(string.IsNullOrEmpty(rule.Text)) rule.Text = text;
                                      else rule.Text += " " + text;
                                      refresh();
                                  });
                              });
                          })
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatWeapon), () => {
                              RelocatorPickers.ShowEnchantPicker(1, (ele) => {
                                  AddEnchantFilterDialog(ele, (text) => {
                                      if(string.IsNullOrEmpty(rule.Text)) rule.Text = text;
                                      else rule.Text += " " + text;
                                      refresh();
                                  });
                              });
                          })
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.CatArmor), () => {
                              RelocatorPickers.ShowEnchantPicker(2, (ele) => {
                                  AddEnchantFilterDialog(ele, (text) => {
                                      if(string.IsNullOrEmpty(rule.Text)) rule.Text = text;
                                      else rule.Text += " " + text;
                                      refresh();
                                  });
                              });
                          })
                          .Show();
                  })
                 .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Category), () => {
                      RelocatorPickers.ShowCategoryPicker(new List<string>(), (selectedIds) => {
                          if (selectedIds.Count > 0) {
                              foreach(var id in selectedIds) if(!rule.CategoryIds.Contains(id)) rule.CategoryIds.Add(id);
                              refresh();
                          }
                      });
                 })
                 .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.Rarity), (child) => {
                      var updateList = Lang.GetList("quality");
                      for(int i=0; i<updateList.Length; i++) {
                          int r = i - 1;
                          string text = updateList[i] + " (" + r + ")";
                          child.AddButton(text, () => {
                              ShowOperatorMenu(op => {
                                  rule.Rarity = r;
                                  rule.RarityOp = op;
                                  refresh();
                              });
                          });
                      }
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
                               if (char.IsDigit(text[0])) text = ">=" + text;

                               // Parse operator and value
                               string op = ">=";
                               string valStr = text;
                               if (text.StartsWith(">=") || text.StartsWith("<=") || text.StartsWith("==") || text.StartsWith("!=")) {
                                   op = text.Substring(0, 2); valStr = text.Substring(2);
                               } else if (text.StartsWith(">") || text.StartsWith("<") || text.StartsWith("=")) {
                                   op = text.Substring(0, 1); valStr = text.Substring(1);
                               }

                               int w;
                               if(int.TryParse(valStr, out w)) {
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

        private static void ShowSettingsMenu(RelocationProfile profile, Action refresh)
        {
             string currentScope = RelocatorLang.GetText(RelocatorLang.LangKey.Inventory); // Default
             if (profile.Scope == RelocationProfile.FilterScope.Both) currentScope = RelocatorLang.GetText(RelocatorLang.LangKey.ScopeBoth);
             else if (profile.Scope == RelocationProfile.FilterScope.ZoneOnly) currentScope = RelocatorLang.GetText(RelocatorLang.LangKey.Zone);

             RelocatorMenu.Create()
                 .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.Scope) + ": " + currentScope, (child) => {
                      child
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Inventory), () => {
                              profile.Scope = RelocationProfile.FilterScope.Inventory;
                              refresh();
                          })
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Zone), () => { // Zone Only
                              profile.Scope = RelocationProfile.FilterScope.ZoneOnly;
                              refresh();
                          })
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.ScopeBoth), () => { // Both
                              profile.Scope = RelocationProfile.FilterScope.Both;
                              refresh();
                          });
                 })
                 .AddCheck(RelocatorLang.GetText(RelocatorLang.LangKey.ExcludeHotbar), profile.ExcludeHotbar, (isOn) => {
                     profile.ExcludeHotbar = isOn;
                     refresh();
                 })
                 .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.SortLabel) + GetSortText(profile.SortMode), (child) => {
                     child
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortDefault), () => { profile.SortMode = RelocationProfile.ResultSortMode.Default; refresh(); })
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortPriceAsc), () => { profile.SortMode = RelocationProfile.ResultSortMode.PriceAsc; refresh(); })
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortPriceDesc), () => { profile.SortMode = RelocationProfile.ResultSortMode.PriceDesc; refresh(); })
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortMagAsc), () => { profile.SortMode = RelocationProfile.ResultSortMode.EnchantMagAsc; refresh(); })
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortMagDesc), () => { profile.SortMode = RelocationProfile.ResultSortMode.EnchantMagDesc; refresh(); });
                 })
                 .AddSeparator()
                 .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.Presets), (child) => {
                     child
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SavePreset), () => {
                             Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.PresetName), "", (c, text) => {
                                 if (!c && !string.IsNullOrEmpty(text)) {
                                     RelocatorManager.Instance.SavePreset(text, profile);
                                 }
                             }, (Dialog.InputType)0);
                         })
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.LoadPreset), () => {
                             RelocatorPickers.ShowPresetPicker((name) => {
                                 var loaded = RelocatorManager.Instance.LoadPreset(name);
                                 if (loaded != null) {
                                     profile.Rules = loaded.Rules;
                                     profile.Scope = loaded.Scope;
                                     profile.ExcludeHotbar = loaded.ExcludeHotbar;
                                     profile.SortMode = loaded.SortMode;
                                     refresh();
                                     Msg.Say(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Loaded));
                                 }
                             });
                         });
                 })
                 .Show();
        }

        private static void ShowOperatorMenu(Action<string> onSelect)
        {
              var opMenu = RelocatorMenu.Create();
              string[] ops = new string[] { ">=", "=", "<=", ">", "<", "!=" };
              foreach(var op in ops) {
                  opMenu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Operator) + ": " + op, () => onSelect(op));
              }
              opMenu.Show();
        }
        private static void AddEnchantFilterDialog(SourceElement.Row ele, Action<string> onConfirm)
        {
             Dialog.InputName("Amount (e.g. >=10)", "", (c2, val) => {
                  if (!c2) {
                      string filterText = "@" + ele.GetName();

                      if (!string.IsNullOrEmpty(val))
                      {
                          if (char.IsDigit(val[0])) val = ">=" + val;
                          filterText += val;
                      }

                      onConfirm(filterText);
                  }
              }, (Dialog.InputType)0);
        }

        private static Button CreateTinyButton(Transform parent, string label, Action onClick) {
             var btnGO = new GameObject("Btn_" + label);
             btnGO.transform.SetParent(parent, false);
             var le = btnGO.AddComponent<LayoutElement>();
             le.minWidth = 24; le.preferredWidth = 24; le.minHeight = 24; le.preferredHeight = 24;

             var img = btnGO.AddComponent<Image>();
             img.color = new Color(0.8f, 0.8f, 0.8f);

             var btn = btnGO.AddComponent<Button>();
             btn.targetGraphic = img;
             btn.onClick.AddListener(() => onClick());

             var txtGO = new GameObject("Text");
             txtGO.transform.SetParent(btnGO.transform, false);
             var txt = txtGO.AddComponent<Text>();
             Font f = null;
             if (SkinManager.Instance != null && SkinManager.Instance.fontSet != null && SkinManager.Instance.fontSet.ui != null && SkinManager.Instance.fontSet.ui.source != null) {
                 f = SkinManager.Instance.fontSet.ui.source.font;
             }
             if (f == null) f = UnityEngine.Resources.GetBuiltinResource<Font>("Arial.ttf"); // Fallback

             txt.font = f; txt.fontSize = 12; txt.text = label; txt.alignment = TextAnchor.MiddleCenter;

             Color c = Color.black;
             if (SkinManager.CurrentColors != null) c = SkinManager.CurrentColors.textDefault;
             txt.color = c;
             txt.rectTransform.anchorMin = Vector2.zero; txt.rectTransform.anchorMax = Vector2.one;
             txt.rectTransform.sizeDelta = Vector2.zero;
             txt.rectTransform.offsetMin = Vector2.zero; txt.rectTransform.offsetMax = Vector2.zero;

             return btn;
        }

        private static void EditRuleCondition(FilterNode node, Action refresh) {
             var rule = node.Rule;
             if (node.CondType == ConditionType.Text) {
                 Dialog.InputName("Edit Text", rule.Text, (c, val) => { if(!c) { rule.Text = val; refresh(); } }, (Dialog.InputType)0);
             }
             else if (node.CondType == ConditionType.Rarity) {
                 var updateList = Lang.GetList("quality");
                 var menu = RelocatorMenu.Create();
                 for(int i=0; i<updateList.Length; i++) {
                       int r = i - 1;
                       string text = updateList[i] + " (" + r + ")";
                       menu.AddButton(text, () => {
                           ShowOperatorMenu(op => {
                               rule.Rarity = r;
                               rule.RarityOp = op;
                               refresh();
                           });
                       });
                 }
                 menu.Show();
             }
             else if (node.CondType == ConditionType.Quality) {
                  Dialog.InputName("Edit Quality", rule.Quality, (c, val) => { if(!c) { rule.Quality = val; refresh(); } }, (Dialog.InputType)0);
             }
             else if (node.CondType == ConditionType.Category) {
                 RelocatorPickers.ShowCategoryPicker(new List<string>{node.CondValue}, (ids) => {
                     rule.CategoryIds.Remove(node.CondValue);
                     foreach(var id in ids) if(!rule.CategoryIds.Contains(id)) rule.CategoryIds.Add(id);
                     refresh();
                 });
             }
             else if (node.CondType == ConditionType.Weight) {
                  Dialog.InputName("Edit Weight", rule.Weight.ToString(), (c, val) => {
                      if(!c && !string.IsNullOrEmpty(val)) {
                           if (char.IsDigit(val[0])) val = ">=" + val;
                           string op = ">=";
                           string valStr = val;
                           if (val.StartsWith(">=") || val.StartsWith("<=") || val.StartsWith("==") || val.StartsWith("!=")) {
                               op = val.Substring(0, 2); valStr = val.Substring(2);
                           } else if (val.StartsWith(">") || val.StartsWith("<") || val.StartsWith("=")) {
                               op = val.Substring(0, 1); valStr = val.Substring(1);
                           }
                           int w;
                           if(int.TryParse(valStr, out w)) {
                               rule.Weight = w;
                               rule.WeightOp = op;
                               refresh();
                           }
                      }
                  }, (Dialog.InputType)0);
             }
             else if (node.CondType == ConditionType.Material) {
                  RelocatorPickers.ShowMaterialPicker(rule.MaterialIds != null ? rule.MaterialIds.ToList() : null, (aliases) => {
                       rule.MaterialIds = new HashSet<string>(aliases);
                       refresh();
                  });
             }
             else if (node.CondType == ConditionType.Bless) {
                  RelocatorPickers.ShowBlessPicker(rule.BlessStates != null ? rule.BlessStates.ToList() : null, (states) => {
                       rule.BlessStates = new HashSet<int>(states);
                       refresh();
                  });
             }
             else if (node.CondType == ConditionType.Stolen) {
                   RelocatorMenu.Create()
                        .AddButton("Yes (Is Stolen)", () => { rule.IsStolen = true; refresh(); })
                        .AddButton("No (Not Stolen)", () => { rule.IsStolen = false; refresh(); })
                        .Show();
             }
        }

        private static string GetSortText(RelocationProfile.ResultSortMode mode) {
            switch(mode) {
                case RelocationProfile.ResultSortMode.Default: return RelocatorLang.GetText(RelocatorLang.LangKey.SortDefault);
                case RelocationProfile.ResultSortMode.PriceAsc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortPriceAsc);
                case RelocationProfile.ResultSortMode.PriceDesc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortPriceDesc);
                case RelocationProfile.ResultSortMode.EnchantMagAsc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortMagAsc);
                case RelocationProfile.ResultSortMode.EnchantMagDesc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortMagDesc);
                case RelocationProfile.ResultSortMode.TotalWeightAsc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortWeightAsc);
                case RelocationProfile.ResultSortMode.TotalWeightDesc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortWeightDesc);
                case RelocationProfile.ResultSortMode.UnitWeightAsc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortUnitWeightAsc);
                case RelocationProfile.ResultSortMode.UnitWeightDesc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortUnitWeightDesc);
                default: return mode.ToString();
            }
        }
    }
}
