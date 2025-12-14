using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Linq;
using System.Reflection;
using System.IO;
using System.Text;

namespace Elin_ItemRelocator
{
    public class LayerItemRelocator : ELayer
    {
        // ====================================================================
        private static RelocatorTable<Thing> previewTable;
        private static Thing currentContainer;
        // ====================================================================

        // ====================================================================
        // Main Entry Point
        // ====================================================================
        public static void Open(Thing container)
        {
             currentContainer = container;
             // Initialize Layers (Main and Preview)
             LayerList layerMain, layerPreview;
             InitLayers(out layerMain, out layerPreview);

             var profile = RelocatorManager.Instance.GetProfile(container);

             // Define Refresh Logic
             Action refresh = null;
             refresh = () => {
                 RefreshSettings(layerMain, profile, refresh);
                 RefreshPreview(layerPreview, container);
             };

             // Setup Bottom Buttons (Once)
             AddMainButtons(layerMain, profile, container, refresh);

             // Show Layers
             layerMain.Show(false);

             // Initial Data Load
             refresh();
        }

        // ====================================================================
        // Layer Initialization & Setup
        // ====================================================================
        private static void InitLayers(out LayerList main, out LayerList preview)
        {
             // 1. Create Main Layer
             var _main = EClass.ui.AddLayer<LayerList>();
             var winMain = _main.windows[0];
             winMain.SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Title));

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
                          txt.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
                          txt.color = new Color(0.1f, 0.1f, 0.1f);
                          txt.alignment = TextAnchor.MiddleLeft;
                          txt.resizeTextForBestFit = true;
                          txt.resizeTextMinSize = 10;
                          txt.resizeTextMaxSize = 13;
                          txt.horizontalOverflow = HorizontalWrapMode.Wrap;
                          txt.verticalOverflow = VerticalWrapMode.Truncate;
                          txt.raycastTarget = false; // Prevent blocking interactions
                           var rt = txt.rectTransform;
                           rt.anchorMin = Vector2.zero;
                           rt.anchorMax = Vector2.one;
                           rt.sizeDelta = Vector2.zero;
                       }

                      if(t != null) {
                          txt.text = t.Name;
                      } else { txt.text = ""; }

                       // Find the row button (parent's sibling child)
                       var rowBtn = cell.transform.parent.GetComponentInChildren<UIButton>();

                       if (rowBtn) {
                            // Clear internal cached tooltip to force update
                            var field = typeof(UIButton).GetField("tooltip", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic);
                            if (field != null) field.SetValue(rowBtn, null);

                            rowBtn.SetTooltip((tooltip) => {
                                if (t != null && tooltip.note != null) t.WriteNote(tooltip.note);
                            }, true);
                       } else {
                           // Failure to find button is rare but handled
                           // Debug.LogWarning("[Relocator] Tooltip setup failed: Row Button not found for " + t.Name);
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

             // Ensure Preview Window is on top and non-blocking background
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
             // _preview size handled by Table API

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
                if (_preview != null) _preview.Close();
             });
             OnKill(_preview, () => {
                 if (closing) return;
                 closing = true;
                 if (_main != null) _main.Close();
             });

             // Assign to out parameters
             main = _main;
             preview = _preview;
        }

        private static void OnKill(ELayer layer, Action action) {
             layer.onKill.AddListener(() => action());
        }

        // ====================================================================
        // List Refresh Logic
        // ====================================================================
        private static void RefreshSettings(LayerList layer, RelocationProfile profile, Action onRefresh)
        {
             layer.customItems.Clear();

             foreach(var filter in profile.Filters)
             {
                 var currentFilter = filter;
                 string desc = currentFilter.GetDescription();
                  if (!currentFilter.Enabled)
                      desc = "<color=#888888>" + desc + RelocatorLang.GetText(RelocatorLang.LangKey.DisabledSuffix) + "</color>";

                  layer.Add(desc, (idx) => {
                      RelocatorMenu.Create()
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => EditFilter(currentFilter, profile, onRefresh))
                          .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Remove), () => { profile.Filters.Remove(currentFilter); onRefresh(); })
                        //   .AddButton(currentFilter.Enabled ? RelocatorLang.GetText(RelocatorLang.LangKey.Disable) : RelocatorLang.GetText(RelocatorLang.LangKey.Enable), () => { currentFilter.Enabled = !currentFilter.Enabled; onRefresh(); })
                          .Show();
                  });
             }
             // Standard LayerList refresh
             layer.list.List();
        }

        private static void RefreshPreview(LayerList layer, Thing container)
        {
               List<Thing> matches = RelocatorManager.Instance.GetMatches(container).ToList();
               int count = matches.Count;
               string countStr = count >= 100 ? "100+" : count.ToString();

               if (previewTable != null)
               {
                   previewTable.SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Preview) + " (" + countStr + ")");
                   previewTable.SetDataSource(matches);
                   previewTable.Refresh();
               }
        }

        // ====================================================================
        // Interaction Logic (Buttons & Menus)
        // ====================================================================
        private static void AddMainButtons(LayerList layer, RelocationProfile profile, Thing container, Action refresh)
        {
             layer.windows[0].AddBottomButton(RelocatorLang.GetText(RelocatorLang.LangKey.AddFilter), () => ShowAddFilterMenu(profile, refresh));
             layer.windows[0].AddBottomButton(RelocatorLang.GetText(RelocatorLang.LangKey.Settings), () => ShowSettingsMenu(profile, refresh));
             layer.windows[0].AddBottomButton(RelocatorLang.GetText(RelocatorLang.LangKey.Execute), () => {
                 RelocatorManager.Instance.ExecuteRelocation(container);
                 Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Relocated), ""));
                 layer.Close();
             });
        }

        private static void ShowAddFilterMenu(RelocationProfile profile, Action refresh)
        {
             RelocatorMenu.Create()
                 .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Text), () => {
                     Dialog.InputName("Enter Text/Tag", "", (cancel, text) => {
                         if (!cancel && !string.IsNullOrEmpty(text)) {
                             profile.Filters.Add(new RelocationFilter { Text = text });
                             refresh();
                         }
                     });
                 })
                 .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Enchant), () => {
                     RelocatorPickers.ShowEnchantPicker((ele) => {
                         AddEnchantFilterDialog(ele, (text) => {
                             profile.Filters.Add(new RelocationFilter { Text = text });
                             refresh();
                         });
                     });
                 })
                 .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Category), () => {
                     // Singleton Check
                     var existing = profile.Filters.FirstOrDefault(f => f.CategoryIds != null && f.CategoryIds.Count > 0);
                     if (existing != null) {
                         EditFilter(existing, profile, refresh);
                     } else {
                         RelocatorPickers.ShowCategoryPicker(new List<string>(), (selectedIds) => {
                             if (selectedIds.Count > 0) {
                                 var f = new RelocationFilter { CategoryIds = selectedIds };
                                 profile.Filters.Add(f);
                                 refresh();
                             }
                         });
                    }
                 })
                 .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.Rarity), (child) => {
                      var updateList = Lang.GetList("quality");
                      for(int i=0; i<updateList.Length; i++) {
                          int r = i - 1;
                          string text = updateList[i] + " (" + r + ")";
                          child.AddButton(text, () => {
                              ShowOperatorMenu(op => {
                                  profile.Filters.Add(new RelocationFilter { Rarity = r, RarityOp = op });
                                  refresh();
                              });
                          });
                      }
                 })
                 .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Quality), () => {
                      Dialog.InputName("Enter Quality (e.g. >=2)\nSupported: ==, >=, <=, <, >, !=", "", (cancel, text) => {
                          if (!cancel && !string.IsNullOrEmpty(text)) {
                              profile.Filters.Add(new RelocationFilter { Quality = text });
                              refresh();
                          }
                      });
                  })
                 .Show();
        }

        private static void ShowSettingsMenu(RelocationProfile profile, Action refresh)
        {
             RelocatorMenu.Create()
                 .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Scope) + ": " + (profile.Scope == RelocationProfile.FilterScope.Inventory ? RelocatorLang.GetText(RelocatorLang.LangKey.Inventory) : RelocatorLang.GetText(RelocatorLang.LangKey.Zone)), () => {
                     if (profile.Scope == RelocationProfile.FilterScope.Inventory)
                         profile.Scope = RelocationProfile.FilterScope.Zone;
                     else
                         profile.Scope = RelocationProfile.FilterScope.Inventory;
                     refresh();
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
                             Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.PresetName), "", (cancel, text) => {
                                 if (!cancel && !string.IsNullOrEmpty(text)) {
                                     RelocatorManager.Instance.SavePreset(text, profile);
                                 }
                             });
                         })
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.LoadPreset), () => {
                             RelocatorPickers.ShowPresetPicker((name) => {
                                 var loaded = RelocatorManager.Instance.LoadPreset(name);
                                 if (loaded != null) {
                                     profile.Filters = loaded.Filters;
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

        private static void EditFilter(RelocationFilter filter, RelocationProfile profile, Action refresh)
        {
            if (!string.IsNullOrEmpty(filter.Text))
            {
                 // Check if it is an Enchant filter (starts with @)
                 if (filter.Text.StartsWith("@")) {
                      RelocatorPickers.ShowEnchantPicker((ele) => {
                          AddEnchantFilterDialog(ele, (text) => {
                              filter.Text = text;
                              refresh();
                          });
                      });
                 } else {
                     Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.EditSearchText), filter.Text, (cancel, text) => {
                          if (!cancel) {
                              filter.Text = text;
                              refresh();
                          }
                     });
                 }
            }
            else if (filter.CategoryIds != null && filter.CategoryIds.Count > 0)
            {
                 RelocatorPickers.ShowCategoryPicker(filter.CategoryIds, (selectedIds) => {
                    filter.CategoryIds = selectedIds;
                    // The original RefreshPreview() call here is missing context (LayerList, Thing).
                    // Assuming it should be `refresh()` as per other filter edits.
                    // If RefreshPreview() was intended, it needs to be called with appropriate arguments.
                    // For now, adhering to the provided snippet's `refresh()` placement.
                    refresh();
                });
            }
            else if (filter.Rarity.HasValue)
            {
                 var rareMenu = RelocatorMenu.Create();
                 var updateList = Lang.GetList("quality");
                 for(int i=0; i<updateList.Length; i++) {
                      int r = i - 1;
                      string text = updateList[i] + " (" + r + ")";
                      rareMenu.AddButton(text, () => {
                          ShowOperatorMenu(op => {
                              filter.Rarity = r;
                              filter.RarityOp = op;
                              refresh();
                          });
                      });
                  }
                  rareMenu.Show();
            }
            else if (!string.IsNullOrEmpty(filter.Quality))
            {
                 Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.EditQuality), filter.Quality, (cancel, text) => {
                      if (!cancel) {
                          filter.Quality = text;
                          refresh();
                      }
                 });
            }
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
              });
        }

        private static string GetSortText(RelocationProfile.ResultSortMode mode)
        {
            switch(mode)
            {
                case RelocationProfile.ResultSortMode.Default: return RelocatorLang.GetText(RelocatorLang.LangKey.SortDefault);
                case RelocationProfile.ResultSortMode.PriceAsc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortPriceAsc);
                case RelocationProfile.ResultSortMode.PriceDesc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortPriceDesc);
                case RelocationProfile.ResultSortMode.EnchantMagAsc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortMagAsc);
                case RelocationProfile.ResultSortMode.EnchantMagDesc: return RelocatorLang.GetText(RelocatorLang.LangKey.SortMagDesc);
                default: return mode.ToString();
            }
        }
    }
}
