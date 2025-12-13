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
        // ====================================================================
        // Main Entry Point
        // ====================================================================
        public static void Open(Thing container)
        {
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

             // 2. Create Preview Layer
             var _preview = EClass.ui.AddLayer<LayerList>();
             var winPreview = _preview.windows[0];
             winPreview.SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Preview));

             // Interaction Fix (Raycast blocking)
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
             _preview.SetSize(700, 800);

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

             // Disable Numbering (a, b, c) on Preview List - REVERTED as per user request
             // Keys will be shown normally.

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
                      var menu = EClass.ui.CreateContextMenu("ContextMenu");
                      menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Edit), () => EditFilter(currentFilter, profile, onRefresh));
                      menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Remove), () => { profile.Filters.Remove(currentFilter); onRefresh(); });
                      menu.AddButton(currentFilter.Enabled ? RelocatorLang.GetText(RelocatorLang.LangKey.Disable) : RelocatorLang.GetText(RelocatorLang.LangKey.Enable), () => { currentFilter.Enabled = !currentFilter.Enabled; onRefresh(); });
                      menu.Show();
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
              layer.windows[0].SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Preview) + " (" + countStr + ")");

              if (count == 0)
              {
                  layer.SetList2(
                      new List<string> { RelocatorLang.GetText(RelocatorLang.LangKey.NoMatches) },
                      (s) => s,
                      (s, b) => {},
                      (s, b) => { b.SetMainText(s); },
                      false
                  );
              }
              else
              {
                  layer.SetList2<Thing>(
                      matches,
                      (t) => { return t != null ? t.Name : ""; },
                      (t, b) => { EClass.Sound.Play("click"); },
                      (t, b) => OnInstantiatePreviewItem(t, b),
                      false
                  );

                  // Re-apply size constraints after list population
                  layer.SetSize(700, 800);
              }
        }

        private static void OnInstantiatePreviewItem(Thing t, ItemGeneral b)
        {
             if (t == null) return;

             // Build Rich Text
             string richText = t.Name;
             if (t.Num > 1) richText += " x" + t.Num;

             string extra = "";
             Card p = t.parent as Card;
             if (p != null) extra += "(" + p.Name + ") ";
             if (t.category != null) extra += t.category.GetName();
             if (t.encLV > 0) extra += " +" + t.encLV;
             if (t.rarity > 0) extra += " [" + t.rarity + "]";

             string finalHtml = richText + " <size=11><color=#808080>" + extra + "</color></size>";

             // Apply Text
             if (b.text1 != null) {
                b.text1.supportRichText = true;
                b.text1.text = finalHtml;
                b.text1.horizontalOverflow = HorizontalWrapMode.Overflow;
                b.text1.verticalOverflow = VerticalWrapMode.Truncate;
                b.text1.resizeTextForBestFit = false;
             } else {
                b.SetMainText(finalHtml);
             }

             // Hide Icon & Subtext
             b.DisableIcon();
             if (b.image1 != null) b.image1.SetActive(false);
             if (b.text2 != null) b.text2.gameObject.SetActive(false);

             // Native Tooltip Setup
             UIButton btn = b.button1 != null ? b.button1 : b.GetComponentInChildren<UIButton>();
             if (btn != null)
             {
                 btn.SetTooltip((tooltip) => {
                      if (t != null && tooltip.note != null) {
                          t.WriteNote(tooltip.note);
                      }
                 }, true);
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
             var menu = EClass.ui.CreateContextMenu("ContextMenu");

             menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Text), () => {
                 Dialog.InputName("Enter Text/Tag", "", (cancel, text) => {
                     if (!cancel && !string.IsNullOrEmpty(text)) {
                         profile.Filters.Add(new RelocationFilter { Text = text });
                         refresh();
                     }
                 });
             });

             menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Enchant), () => {
                 RelocatorPickers.ShowEnchantPicker((ele) => {
                     Dialog.InputName("Amount (e.g. >=10)", "", (c2, val) => {
                          if (!c2) {
                              string filterText = "@" + ele.GetName(); // Updated: Use @ + Localized Name

                              if (!string.IsNullOrEmpty(val))
                              {
                                  if (char.IsDigit(val[0])) val = ">=" + val;
                                  filterText += val;
                              }

                              profile.Filters.Add(new RelocationFilter { Text = filterText });
                              refresh();
                          }
                      });
                 });
             });

             menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Category), () => {
                 RelocatorPickers.ShowCategoryPicker((id) => {
                     profile.Filters.Add(new RelocationFilter { CategoryId = id });
                     refresh();
                 });
             });

             menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Rarity), () => {
                  var rareMenu = EClass.ui.CreateContextMenu("ContextMenu");
                  var updateList = Lang.GetList("quality");
                  for(int i=0; i<updateList.Length; i++) {
                      int r = i - 1;
                      string text = updateList[i] + " (" + r + ")";
                      rareMenu.AddButton(text, () => {
                          ShowOperatorMenu(op => {
                              profile.Filters.Add(new RelocationFilter { Rarity = r, RarityOp = op });
                              refresh();
                          });
                      });
                  }
                  rareMenu.Show();
             });

             menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Quality), () => {
                  Dialog.InputName("Enter Quality (e.g. >=2)\nSupported: ==, >=, <=, <, >, !=", "", (cancel, text) => {
                      if (!cancel && !string.IsNullOrEmpty(text)) {
                          profile.Filters.Add(new RelocationFilter { Quality = text });
                          refresh();
                      }
                  });
              });

             menu.Show();
        }

        private static void ShowSettingsMenu(RelocationProfile profile, Action refresh)
        {
             var menu = EClass.ui.CreateContextMenu("ContextMenu");
             string scopeText = RelocatorLang.GetText(RelocatorLang.LangKey.Scope) + ": " + (profile.Scope == RelocationProfile.FilterScope.Inventory ? RelocatorLang.GetText(RelocatorLang.LangKey.Inventory) : RelocatorLang.GetText(RelocatorLang.LangKey.Zone));
             menu.AddButton(scopeText, () => {
                if (profile.Scope == RelocationProfile.FilterScope.Inventory)
                    profile.Scope = RelocationProfile.FilterScope.Zone;
                else
                    profile.Scope = RelocationProfile.FilterScope.Inventory;
                refresh();
             });
             string hotbarText = RelocatorLang.GetText(RelocatorLang.LangKey.ExcludeHotbar) + ": " + (profile.ExcludeHotbar ? RelocatorLang.GetText(RelocatorLang.LangKey.ON) : RelocatorLang.GetText(RelocatorLang.LangKey.OFF));
             menu.AddButton(hotbarText, () => {
                 profile.ExcludeHotbar = !profile.ExcludeHotbar;
                 refresh();
             });
             menu.Show();
        }

        private static void EditFilter(RelocationFilter filter, RelocationProfile profile, Action refresh)
        {
            if (!string.IsNullOrEmpty(filter.Text))
            {
                 Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.EditSearchText), filter.Text, (cancel, text) => {
                      if (!cancel) {
                          filter.Text = text;
                          refresh();
                      }
                 });
            }
            else if (!string.IsNullOrEmpty(filter.CategoryId))
            {
                 Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.EditCategoryID), filter.CategoryId, (cancel, text) => {
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
              var opMenu = EClass.ui.CreateContextMenu("ContextMenu");
              string[] ops = new string[] { ">=", "=", "<=", ">", "<", "!=" };
              foreach(var op in ops) {
                  opMenu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Operator) + ": " + op, () => onSelect(op));
              }
              opMenu.Show();
        }
    }
}
