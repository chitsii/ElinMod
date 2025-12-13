using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace Elin_ItemRelocator
{
    public static class RelocatorPickers
    {
        public static void ShowCategoryPicker(Action<string> onSelect)
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
                   subMenu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.All) + cat.GetName(), () => onSelect(cat.id));
                   foreach(var child in cat.children) {
                       AddCategoryToMenu(subMenu, child, onSelect);
                   }
                   subMenu.Show();
               });
            } else {
                 menu.AddButton(cat.GetName(), () => onSelect(cat.id));
            }
        }

        public static void ShowEnchantPicker(Action<SourceElement.Row> onConfirm)
        {
            var layer = EClass.ui.AddLayer<LayerList>();
            layer.windows[0].SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.SelectEnchant));

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

            // Note: Since this creates a LayerList, we use SetList (or SetList2) logic.
            // Using basic SetList for simplicity as it was in original code.
            layer.SetList(sources, (row) => row.GetName() + " (" + row.alias + ")", (idx, val) => {
                onConfirm(sources[idx]);
                layer.Close();
            }, true);
        }
    }
}
