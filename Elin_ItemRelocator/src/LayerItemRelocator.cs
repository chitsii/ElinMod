using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Linq;

namespace Elin_ItemRelocator
{
    public static class RelocatorUI
    {
        public enum LangKey
        {
            Settings,
            AddFilter,
            Preview,
            Execute,
            Scope,
            ExcludeHotbar,
            Rarity,
            Quality,
            Category,
            Text,
            Enchant,
            Remove,
            Edit,
            Enable,
            Disable,
            Title,
            Operator,
            Msg_Relocated,
            Inventory,
            Zone,
            ON,
            OFF,
            NoMatches,
            SelectEnchant,
            RelocatorCaption,
            DisabledSuffix,
            All,
            EditSearchText,
            EditCategoryID,
            EditQuality
        }

        private static Dictionary<LangKey, string[]> _dict = new Dictionary<LangKey, string[]>
        {
            { LangKey.Settings, new[] { "Settings", "設定" } },
            { LangKey.AddFilter, new[] { "Add Filter", "フィルタ追加" } },
            { LangKey.Preview, new[] { "Preview", "プレビュー" } },
            { LangKey.Execute, new[] { "Relocate", "実行" } },
            { LangKey.Scope, new[] { "Scope", "範囲" } },
            { LangKey.ExcludeHotbar, new[] { "Exclude Hotbar", "ツールベルト除外" } },
            { LangKey.Rarity, new[] { "Rarity", "レアリティ" } },
            { LangKey.Quality, new[] { "Quality", "品質" } },
            { LangKey.Category, new[] { "Category", "カテゴリ" } },
            { LangKey.Text, new[] { "Text (Name/Tag)", "テキスト (名前/タグ)" } },
            { LangKey.Enchant, new[] { "Enchant", "エンチャント" } },
            { LangKey.Remove, new[] { "Remove", "削除" } },
            { LangKey.Edit, new[] { "Edit", "編集" } },
            { LangKey.Enable, new[] { "Enable", "有効" } },
            { LangKey.Disable, new[] { "Disable", "無効" } },
            { LangKey.Title, new[] { "Item Relocator", "アイテムリロケータ" } },
            { LangKey.Operator, new[] { "Operator", "演算子" } },
            { LangKey.Msg_Relocated, new[] { "Relocated {0} items.", "{0}個のアイテムを移動しました。" } },
            { LangKey.Inventory, new[] { "Inventory", "インベントリ" } },
            { LangKey.Zone, new[] { "Zone", "ゾーン" } },
            { LangKey.ON, new[] { "ON", "ON" } },
            { LangKey.OFF, new[] { "OFF", "OFF" } },
            { LangKey.NoMatches, new[] { "No matches found.", "該当なし" } },
            { LangKey.SelectEnchant, new[] { "Select Enchant", "エンチャント選択" } },
            { LangKey.RelocatorCaption, new[] { "Relocator: {0} [{1}] (Matches: {2})", "リロケータ: {0} [{1}] (合致: {2})" } },
            { LangKey.DisabledSuffix, new[] { " (Disabled)", " (無効)" } },
            { LangKey.All, new[] { "All ", "すべて選択 " } },
            { LangKey.EditSearchText, new[] { "Edit Search Text", "検索テキスト編集" } },
            { LangKey.EditCategoryID, new[] { "Edit Category ID", "カテゴリID編集" } },
            { LangKey.EditQuality, new[] { "Edit Quality (e.g. >=2)", "品質設定 (例: >=2)" } }
        };

        public static string GetText(LangKey key)
        {
            int idx = (Lang.langCode == "JP") ? 1 : 0;
            if (_dict.ContainsKey(key)) return _dict[key][idx];
            return key.ToString();
        }

        public static void Open(Thing container)
        {
             // 1. Create Main Layer (Settings)
             var layer = EClass.ui.AddLayer<LayerList>();
             var winMain = layer.windows[0];
             winMain.SetCaption(GetText(LangKey.Title));

             // 2. Create Preview Layer (Results)
             var layerPreview = EClass.ui.AddLayer<LayerList>();
             var winPreview = layerPreview.windows[0];
             winPreview.SetCaption(GetText(LangKey.Preview));

             // INTERACTION FIX:
             // 1. Put Preview Layer ON TOP (Last Sibling)
             layerPreview.transform.SetAsLastSibling();

             // 2. Disable logic for background blocker
             // Iterate ALL graphics in the layer. If it's NOT the window or its children, disable raycast.
             // This ensures the "veil" is removed, but the window (and its scrollbar/buttons) keeps raycast.
             foreach (var g in layerPreview.GetComponentsInChildren<Graphic>(true))
             {
                 if (g.transform.IsChildOf(winPreview.transform) || g.gameObject == winPreview.gameObject)
                 {
                     // This is part of the window content (Text, Image, Scrollbar). Keep it.
                     continue;
                 }
                 // This is likely the background veil or debugger clutter. Disable input.
                 g.raycastTarget = false;
             }

             // Resize Logic: Apply AFTER layer creation
             // Sometimes AddLayer initializes size. We override it here.
             winMain.setting.allowResize = true;
             winPreview.setting.allowResize = true;

             // Initial Show (False) triggers some layout logic?
             // Let's set size explicitly.
             var rectMain = winMain.GetComponent<RectTransform>();
             var rectPreview = winPreview.GetComponent<RectTransform>();

             rectMain.sizeDelta = new Vector2(700, 800);
             rectPreview.sizeDelta = new Vector2(700, 800);
             rectMain.anchoredPosition = new Vector2(-360, 0);
             rectPreview.anchoredPosition = new Vector2(360, 0);

             // Sync Closing: Mutual Close
             bool closing = false;
             layer.onKill.AddListener(() => {
                if (closing) return;
                closing = true;
                if (layerPreview != null) layerPreview.Close();
             });
             layerPreview.onKill.AddListener(() => {
                 if (closing) return;
                 closing = true;
                 if (layer != null) layer.Close();
             });

             var profile = RelocatorManager.Instance.GetProfile(container);

             // Define Refresh
             Action refresh = null;
             refresh = () => {
                 // --- 1. Update Main Filter List ---
                 layer.customItems.Clear();

                 foreach(var filter in profile.Filters)
                 {
                     var currentFilter = filter;
                     string desc = currentFilter.GetDescription();
                      if (!currentFilter.Enabled)
                          desc = "<color=#888888>" + desc + GetText(LangKey.DisabledSuffix) + "</color>";

                      layer.Add(desc, (idx) => {
                          var menu = EClass.ui.CreateContextMenu("ContextMenu");
                          menu.AddButton(GetText(LangKey.Edit), () => EditFilter(currentFilter, profile, refresh));
                          menu.AddButton(GetText(LangKey.Remove), () => { profile.Filters.Remove(currentFilter); refresh(); });
                          menu.AddButton(currentFilter.Enabled ? GetText(LangKey.Disable) : GetText(LangKey.Enable), () => { currentFilter.Enabled = !currentFilter.Enabled; refresh(); });
                          menu.Show();
                      });
                  }
                  layer.list.List();

                  // --- 2. Update Preview List ---
                  layerPreview.customItems.Clear();

                  var matches = RelocatorManager.Instance.GetMatches(container);
                  int count = matches.Count();

                  string countStr = count >= 100 ? "100+" : count.ToString();
                  winPreview.SetCaption(GetText(LangKey.Preview) + " (" + countStr + ")");

                  if (count == 0)
                  {
                      layerPreview.Add(GetText(LangKey.NoMatches), (idx)=>{});
                  }
                  else
                  {
                      foreach(var t in matches)
                      {
                          string s = t.Name;
                          if (t.Num > 1) s += " x" + t.Num;
                          Card p = t.parent as Card;
                          if (p != null && p != EClass.pc) s += " <size=10>(" + p.Name + ")</size>";
                          layerPreview.Add(s, (idx)=> {
                              // Optional: Preview item details on click?
                          });
                      }
                      if(count >= 100) layerPreview.Add("... (Max 100)", (idx)=>{});
                  }
                  layerPreview.list.List();
             };

             AddButtons(layer, profile, container, refresh);

             // Final Show
             layerPreview.Show(false);
             layer.Show(false);

             // Ensure size again after Show, just in case Open/Show resets it
             rectMain.sizeDelta = new Vector2(700, 800);
             rectPreview.sizeDelta = new Vector2(700, 800);

             refresh();
        }

        private static int CountMatches(Thing container, RelocationProfile profile)
        {
            return RelocatorManager.Instance.GetMatches(container).Count();
        }

        private static void AddButtons(LayerList layer, RelocationProfile profile, Thing container, Action refresh)
        {
             // Add Filter Button
             layer.windows[0].AddBottomButton(GetText(LangKey.AddFilter), () => {
                 var menu = EClass.ui.CreateContextMenu("ContextMenu");

                 menu.AddButton(GetText(LangKey.Text), () => {
                     Dialog.InputName("Enter Text/Tag", "", (cancel, text) => {
                         if (!cancel && !string.IsNullOrEmpty(text)) {
                             profile.Filters.Add(new RelocationFilter { Text = text });
                             refresh();
                         }
                     });
                 });

                 menu.AddButton(GetText(LangKey.Enchant), () => {
                     ShowEnchantPicker((ele) => {
                         Dialog.InputName("Amount (e.g. >=10)", "", (c2, val) => {
                              if (!c2) {
                                  // Construct a text query that matches the enchant
                                  // This relies on `MatchEncSearch`.
                                  profile.Filters.Add(new RelocationFilter { Text = ele.alias });
                                  refresh();
                              }
                         });
                     });
                 });

                 menu.AddButton(GetText(LangKey.Category), () => {
                     ShowCategoryPicker((id) => {
                         profile.Filters.Add(new RelocationFilter { CategoryId = id });
                         refresh();
                     });
                 });

                 menu.AddButton(GetText(LangKey.Rarity), () => {
                      var rareMenu = EClass.ui.CreateContextMenu("ContextMenu");
                      var updateList = Lang.GetList("quality");
                      for(int i=0; i<updateList.Length; i++) {
                          int r = i - 1;
                          string text = updateList[i] + " (" + r + ")";
                          rareMenu.AddButton(text, () => {
                              var opMenu = EClass.ui.CreateContextMenu("ContextMenu");
                              string[] ops = new string[] { ">=", "=", "<=", ">", "<", "!=" };
                              foreach(var op in ops) {
                                  opMenu.AddButton(GetText(LangKey.Operator) + ": " + op, () => {
                                      profile.Filters.Add(new RelocationFilter { Rarity = r, RarityOp = op });
                                      refresh();
                                  });
                              }
                              opMenu.Show();
                          });
                      }
                      rareMenu.Show();
                 });

                 menu.AddButton(GetText(LangKey.Quality), () => {
                      Dialog.InputName("Enter Quality (e.g. >=2)\nSupported: ==, >=, <=, <, >, !=", "", (cancel, text) => {
                          if (!cancel && !string.IsNullOrEmpty(text)) {
                              profile.Filters.Add(new RelocationFilter { Quality = text });
                              refresh();
                          }
                      });
                  });

                 menu.Show();
             });

             // Settings Button (Replaces Scope/Hotbar buttons)
             layer.windows[0].AddBottomButton(GetText(LangKey.Settings), () => {
                 var menu = EClass.ui.CreateContextMenu("ContextMenu");

                 // Scope
                 string scopeText = GetText(LangKey.Scope) + ": " + (profile.Scope == RelocationProfile.FilterScope.Inventory ? GetText(LangKey.Inventory) : GetText(LangKey.Zone));
                 menu.AddButton(scopeText, () => {
                    if (profile.Scope == RelocationProfile.FilterScope.Inventory)
                        profile.Scope = RelocationProfile.FilterScope.Zone;
                    else
                        profile.Scope = RelocationProfile.FilterScope.Inventory;
                    refresh();
                 });

                 // Hotbar
                 string hotbarText = GetText(LangKey.ExcludeHotbar) + ": " + (profile.ExcludeHotbar ? GetText(LangKey.ON) : GetText(LangKey.OFF));
                 menu.AddButton(hotbarText, () => {
                     profile.ExcludeHotbar = !profile.ExcludeHotbar;
                     refresh();
                 });

                 // Removed Import/Export/Clear as per user request

                 menu.Show();
             });

             // Preview Button REMOVED (Real-time now)

             // Execute
             layer.windows[0].AddBottomButton(GetText(LangKey.Execute), () => {
                 RelocatorManager.Instance.ExecuteRelocation(container);
                 Msg.Say(string.Format(GetText(LangKey.Msg_Relocated), "")); // Just a dummy msg or real count if possible
                 layer.Close();
             });
        }

        // ShowPreview method removed or unused logic can be deleted, but keeping AddButtons clean first.

        private static void ShowPreview(Thing container)
        {
             // Deprecated by dual-window mode
        }



        private static void EditFilter(RelocationFilter filter, RelocationProfile profile, Action refresh)
        {
            if (!string.IsNullOrEmpty(filter.Text))
            {
                 Dialog.InputName(GetText(LangKey.EditSearchText), filter.Text, (cancel, text) => {
                      if (!cancel) {
                          filter.Text = text;
                          refresh();
                      }
                 });
            }
            else if (!string.IsNullOrEmpty(filter.CategoryId))
            {
                 Dialog.InputName(GetText(LangKey.EditCategoryID), filter.CategoryId, (cancel, text) => {
                      if (!cancel) {
                          filter.CategoryId = text;
                          refresh();
                      }
                 });
            }
            else if (filter.Rarity.HasValue)
            {
                 var rareMenu = EClass.ui.CreateContextMenu("ContextMenu");
                 var updateList = Lang.GetList("quality");
                 for(int i=0; i<updateList.Length; i++) {
                      int r = i - 1;
                      string text = updateList[i] + " (" + r + ")";
                      rareMenu.AddButton(text, () => {
                          // Step 2: Select Operator
                          var opMenu = EClass.ui.CreateContextMenu("ContextMenu");
                          string[] ops = new string[] { ">=", "=", "<=", ">", "<", "!=" };
                          foreach(var op in ops) {
                              opMenu.AddButton(GetText(LangKey.Operator) + ": " + op, () => {
                                  filter.Rarity = r;
                                  filter.RarityOp = op;
                                  refresh();
                              });
                          }
                          opMenu.Show();
                      });
                  }
                  rareMenu.Show();
            }
            else if (!string.IsNullOrEmpty(filter.Quality))
            {
                 Dialog.InputName(GetText(LangKey.EditQuality), filter.Quality, (cancel, text) => {
                      if (!cancel) {
                          filter.Quality = text;
                          refresh();
                      }
                 });
            }
        }

        // Re-implemented Dynamic Category Picker
        private static void ShowCategoryPicker(Action<string> onSelect)
        {
            var menu = EClass.ui.CreateContextMenu("ContextMenu");
            // Sort roots by name? Or sortVal?
            var roots = EClass.sources.categories.rows.Where(r => r.parent == null).OrderBy(r => r.id).ToList();

            foreach(var root in roots) {
                AddCategoryToMenu(menu, root, onSelect);
            }
            menu.Show();
        }

        private static void AddCategoryToMenu(UIContextMenu menu, SourceCategory.Row cat, Action<string> onSelect)
        {
            if (cat.children.Count > 0) {
               // Branch: Button opens sub-menu
               menu.AddButton(cat.GetName() + " >", () => {
                   var subMenu = EClass.ui.CreateContextMenu("ContextMenu");
                   // "Select All [This Category]" option
                   subMenu.AddButton(GetText(LangKey.All) + cat.GetName(), () => onSelect(cat.id));

                   // Separator logic is not directly exposed in simple AddButton API, but we can just list children.
                   foreach(var child in cat.children) {
                       AddCategoryToMenu(subMenu, child, onSelect);
                   }
                   subMenu.Show();
               });
            } else {
               // Leaf: Selects category
                 menu.AddButton(cat.GetName(), () => onSelect(cat.id));
            }
        }

        // Renamed and Filtered Attribute Picker
        private static void ShowEnchantPicker(Action<SourceElement.Row> onConfirm)
        {
            var layer = EClass.ui.AddLayer<LayerList>();
            layer.windows[0].SetCaption(GetText(LangKey.SelectEnchant));

            var sources = new List<SourceElement.Row>();
            foreach(var row in EClass.sources.elements.rows)
            {
                // Filter Logic: Weapon/Armor Enchants
                // 1. Must have an alias (to be searchable/usable in filter)
                if (string.IsNullOrEmpty(row.alias)) continue;

                // 2. Must be an Enchant
                // Check IsWeaponEnc, IsShieldEnc, or has encSlot defined (and valid)
                bool isEnc = row.IsWeaponEnc || row.IsShieldEnc;
                if (!string.IsNullOrEmpty(row.encSlot) && row.encSlot != "global")
                {
                    isEnc = true;
                }

                // 3. Include Primary Attributes? (STR, END...) usually fine to filter by.
                // But user specifically asked for "Weapon/Armor Enchants".
                // Let's stick to Enchants.
                // However, things like "Sustain STR" are enchants. "STR" itself is a stat.
                // Pure stats usually don't have encSlot?
                // Actually SourceElement.row (id=10 STR) has encSlot="global".
                // If we exclude 'global', we might exclude stats.
                // Let's check user intent: "Attributes... too many... only Weapon/Armor Enchants".
                // I'll exclude 'global' (stats) unless they claim to be weapon enc.

                if (isEnc)
                {
                    // 4. Exclude unnatural enchants
                    // Must have a chance to appear and not be excluded from random generation
                    if (row.chance == 0) continue;
                    if (row.tag.Contains("noRandomEnc")) continue;

                    sources.Add(row);
                }
            }

            sources.Sort((a,b) => a.GetName().CompareTo(b.GetName()));

            layer.SetList(sources, (row) => row.GetName() + " (" + row.alias + ")", (idx, val) => {
                onConfirm(sources[idx]);
                layer.Close();
            }, true);
        }
    }
}
