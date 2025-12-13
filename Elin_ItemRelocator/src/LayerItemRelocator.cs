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
    public static class RelocatorUI
    {
        public enum LangKey
        {
            Settings, AddFilter, Preview, Execute, Scope, ExcludeHotbar, Rarity, Quality, Category, Text, Enchant, Remove, Edit, Enable, Disable, Title, Operator, Msg_Relocated, Inventory, Zone, ON, OFF, NoMatches, SelectEnchant, RelocatorCaption, DisabledSuffix, All, EditSearchText, EditCategoryID, EditQuality
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
             // 1. Create Main Layer
             var layer = EClass.ui.AddLayer<LayerList>();
             var winMain = layer.windows[0];
             winMain.SetCaption(GetText(LangKey.Title));

             // 2. Create Preview Layer
             var layerPreview = EClass.ui.AddLayer<LayerList>();
             var winPreview = layerPreview.windows[0];
             winPreview.SetCaption(GetText(LangKey.Preview));

             // INTERACTION FIX
             layerPreview.transform.SetAsLastSibling();
             foreach (var g in layerPreview.GetComponentsInChildren<Graphic>(true))
             {
                 if (g.transform.IsChildOf(winPreview.transform) || g.gameObject == winPreview.gameObject)
                     continue;
                 g.raycastTarget = false;
             }

             // --- FIX: SET SIZE EXPLICITLY TO DISABLE AUTO-RESIZE ---
             layer.SetSize(700, 800);
             layerPreview.SetSize(700, 800);

             // Set Position
             var rectMain = winMain.GetComponent<RectTransform>();
             var rectPreview = winPreview.GetComponent<RectTransform>();
             rectMain.anchoredPosition = new Vector2(-360, 0);
             rectPreview.anchoredPosition = new Vector2(360, 0);

             // Sync Closing
             bool closing = false;
             OnKill(layer, () => {
                if (closing) return;
                closing = true;
                if (layerPreview != null) layerPreview.Close();
             });
             OnKill(layerPreview, () => {
                 if (closing) return;
                 closing = true;
                 if (layer != null) layer.Close();
             });

             // REFLECTION: Disable 'numbering' on Preview
             try {
                 var pNumbering = typeof(BaseList).GetField("numbering", BindingFlags.Public | BindingFlags.Instance);
                 if (pNumbering != null) {
                     pNumbering.SetValue(layerPreview.list, false);
                 } else {
                     var f = layerPreview.list.GetType().GetField("numbering", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.FlattenHierarchy);
                     if (f != null) f.SetValue(layerPreview.list, false);
                 }

                 var pUseKey = layerPreview.list.GetType().GetField("useKey", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                 if (pUseKey != null) pUseKey.SetValue(layerPreview.list, false);
             } catch {}


             var profile = RelocatorManager.Instance.GetProfile(container);

             // --- REFRESH LOGIC ---
             Action refresh = null;
             refresh = () => {
                 // Update Settings List
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

                  // Refreshes the UIList content without re-showing/adding buttons
                  layer.list.List();


                  // Update Preview List
                  var matches = RelocatorManager.Instance.GetMatches(container).ToList();
                  int count = matches.Count;
                  string countStr = count >= 100 ? "100+" : count.ToString();
                  winPreview.SetCaption(GetText(LangKey.Preview) + " (" + countStr + ")");

                  if (count == 0)
                  {
                      layerPreview.SetList2(
                          new List<string> { GetText(LangKey.NoMatches) },
                          (s) => s,
                          (s, b) => {},
                          (s, b) => { b.SetMainText(s); },
                          false
                      );
                  }
                  else
                  {
                      layerPreview.SetList2<Thing>(
                          matches,
                          (t) => { return t != null ? t.Name : ""; },
                          (t, b) => { EClass.Sound.Play("click"); },
                          (t, b) => {
                             if (t == null) return;

                             string richText = t.Name;
                             if (t.Num > 1) richText += " x" + t.Num;

                             Card p = t.parent as Card;
                             string extra = "";
                             if (p != null) extra += "(" + p.Name + ") ";
                             if (t.category != null) extra += t.category.GetName();
                             if (t.encLV > 0) extra += " +" + t.encLV;
                             if (t.rarity > 0) extra += " [" + t.rarity + "]";

                             string finalHtml = richText + " <size=11><color=#808080>" + extra + "</color></size>";

                             if (b.text1 != null) {
                                b.text1.supportRichText = true;
                                b.text1.text = finalHtml;
                                b.text1.horizontalOverflow = HorizontalWrapMode.Overflow;
                                b.text1.verticalOverflow = VerticalWrapMode.Truncate;
                                b.text1.resizeTextForBestFit = false;
                             } else {
                                b.SetMainText(finalHtml);
                             }

                             b.DisableIcon();
                             if (b.image1 != null) b.image1.SetActive(false);
                             if (b.text2 != null) b.text2.gameObject.SetActive(false);

                             // NATIVE TOOLTIP FIX
                             UIButton btn = b.button1 != null ? b.button1 : b.GetComponentInChildren<UIButton>();
                             if (btn != null)
                             {
                                 btn.SetTooltip((tooltip) => {
                                      // Correct Native Pattern: Use WriteNote for Things/Cards
                                      if (t != null && tooltip.note != null) {
                                          t.WriteNote(tooltip.note);
                                      }
                                 }, true);
                             }
                          },
                          false
                      );

                      // RE-ENFORCE SIZE AFTER SetList2 (just in case SetList2 alters it)
                      layerPreview.SetSize(700, 800);
                  }
             };

             // --- ONE TIME SETUP ---
             // Add Buttons Only Once
             AddButtons(layer, profile, container, refresh);

             // Show Layers Only Once
             layer.Show(false);
             // layerPreview is shown implicitly by SetList2 or we can call it here,
             // but SetList2 calls List() which builds it.
             // We ensure it's visible.
             // layerPreview.Show(false); // SetList2 calls this internally effectively? No, SetList2 calls list.List().
             // Actually, LayerList.SetList2 does NOT call Show()! It sets callbacks and runs list.List().
             // So we must call Show() at least once or ensure the layer is open.
             // Since we added it via 'AddLayer', it is open.

             // Initial Refresh
             refresh();
        }

        private static void OnKill(ELayer layer, Action action) {
             layer.onKill.AddListener(() => action());
        }


        private static void AddButtons(LayerList layer, RelocationProfile profile, Thing container, Action refresh)
        {
             layer.windows[0].AddBottomButton(GetText(LangKey.AddFilter), () => {
                 var menu = EClass.ui.CreateContextMenu("ContextMenu");
                 // ... (Menu Logic)
                 menu.AddButton(GetText(LangKey.Text), () => {
                     Dialog.InputName("Enter Text/Tag", "", (cancel, text) => {
                         if (!cancel && !string.IsNullOrEmpty(text)) {
                             profile.Filters.Add(new RelocationFilter { Text = text });
                             refresh();
                         }
                     });
                 });
                 // ... Check other menu items
                 menu.AddButton(GetText(LangKey.Enchant), () => {
                     ShowEnchantPicker((ele) => {
                         Dialog.InputName("Amount (e.g. >=10)", "", (c2, val) => {
                              if (!c2) {
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

             layer.windows[0].AddBottomButton(GetText(LangKey.Settings), () => {
                 var menu = EClass.ui.CreateContextMenu("ContextMenu");
                 string scopeText = GetText(LangKey.Scope) + ": " + (profile.Scope == RelocationProfile.FilterScope.Inventory ? GetText(LangKey.Inventory) : GetText(LangKey.Zone));
                 menu.AddButton(scopeText, () => {
                    if (profile.Scope == RelocationProfile.FilterScope.Inventory)
                        profile.Scope = RelocationProfile.FilterScope.Zone;
                    else
                        profile.Scope = RelocationProfile.FilterScope.Inventory;
                    refresh();
                 });
                 string hotbarText = GetText(LangKey.ExcludeHotbar) + ": " + (profile.ExcludeHotbar ? GetText(LangKey.ON) : GetText(LangKey.OFF));
                 menu.AddButton(hotbarText, () => {
                     profile.ExcludeHotbar = !profile.ExcludeHotbar;
                     refresh();
                 });
                 menu.Show();
             });

             layer.windows[0].AddBottomButton(GetText(LangKey.Execute), () => {
                 RelocatorManager.Instance.ExecuteRelocation(container);
                 Msg.Say(string.Format(GetText(LangKey.Msg_Relocated), ""));
                 layer.Close();
             });
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

        private static void ShowCategoryPicker(Action<string> onSelect)
        {
            var menu = EClass.ui.CreateContextMenu("ContextMenu");
            var roots = EClass.sources.categories.rows.Where(r => r.parent == null).OrderBy(r => r.id).ToList();

            foreach(var root in roots) {
                AddCategoryToMenu(menu, root, onSelect);
            }
            menu.Show();
        }

        private static void AddCategoryToMenu(UIContextMenu menu, SourceCategory.Row cat, Action<string> onSelect)
        {
            if (cat.children.Count > 0) {
               menu.AddButton(cat.GetName() + " >", () => {
                   var subMenu = EClass.ui.CreateContextMenu("ContextMenu");
                   subMenu.AddButton(GetText(LangKey.All) + cat.GetName(), () => onSelect(cat.id));
                   foreach(var child in cat.children) {
                       AddCategoryToMenu(subMenu, child, onSelect);
                   }
                   subMenu.Show();
               });
            } else {
                 menu.AddButton(cat.GetName(), () => onSelect(cat.id));
            }
        }

        private static void ShowEnchantPicker(Action<SourceElement.Row> onConfirm)
        {
            var layer = EClass.ui.AddLayer<LayerList>();
            layer.windows[0].SetCaption(GetText(LangKey.SelectEnchant));

            var sources = new List<SourceElement.Row>();
            foreach(var row in EClass.sources.elements.rows)
            {
                if (string.IsNullOrEmpty(row.alias)) continue;
                bool isEnc = row.IsWeaponEnc || row.IsShieldEnc;
                if (!string.IsNullOrEmpty(row.encSlot) && row.encSlot != "global") isEnc = true;

                if (isEnc)
                {
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
