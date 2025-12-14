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
            var layer = EClass.ui.AddLayer<LayerList>();
            layer.windows[0].SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Category));
            layer.windows[0].setting.allowResize = true;

            // Set Size
            try { layer.SetSize(500, 700); } catch {}

            var roots = EClass.sources.categories.rows.Where(r => r.parent == null).OrderBy(r => r.id).ToList();
            HashSet<string> expanded = new HashSet<string>();

            // Recursive function to build the view list
            Action refresh = null;
            refresh = () => {
                var viewList = new List<SourceCategory.Row>();

                // Helper to add rows (Delegate for C# 5)
                Action<IEnumerable<SourceCategory.Row>, int> addRows = null;
                addRows = (rows, depth) => {
                    foreach(var cat in rows) {
                        viewList.Add(cat);
                        // If expanded, add children
                        if (expanded.Contains(cat.id) && cat.children.Count > 0) {
                            addRows(cat.children, depth + 1);
                        }
                    }
                };
                addRows(roots, 0);

                layer.SetList(viewList, (cat) => {
                    // Formatter: Indent based on depth?
                    // We need to know depth here or store it.
                    // Simple hack: Check parent chain or just use the fact we build it in order.
                    // Actually, SetList just takes item. We can query item property.

                    int depth = 0;
                    var p = cat.parent;
                    while(p != null) { depth++; p = p.parent; }

                    string prefix = "";
                    if (depth > 0) prefix = new string(' ', depth * 4); // Indent

                    string marker = "";
                    if (cat.children.Count > 0) {
                        marker = expanded.Contains(cat.id) ? "[-] " : "[+] ";
                    } else {
                        marker = " -  ";
                    }

                    return prefix + marker + cat.GetName();
                }, (idx, val) => {
                    var selectedCat = viewList[idx];
                    if (selectedCat.children.Count > 0) {
                        // Toggle
                        if (expanded.Contains(selectedCat.id)) expanded.Remove(selectedCat.id);
                        else expanded.Add(selectedCat.id);

                        // Play sound
                        EClass.Sound.Play("click");

                        // Refresh list (Rebuild)
                        refresh();
                    } else {
                         // Select
                         onSelect(selectedCat.id);
                         layer.Close();
                    }
                }, false);
            };

            // Initial Draw
            refresh();
        }

        // Removed old AddCategoryToMenu helper
        private static void AddCategoryToMenu_Removed(UIContextMenu menu, SourceCategory.Row cat, Action<string> onSelect) {}

        public static void ShowEnchantPicker(Action<SourceElement.Row> onConfirm)
        {
            var layer = EClass.ui.AddLayer<LayerList>();
            layer.windows[0].SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.SelectEnchant));
            layer.windows[0].setting.allowResize = true;
            // Widen window
            var rt = layer.windows[0].GetComponent<RectTransform>();
            rt.sizeDelta = new Vector2(600, 800);


            var sources = new List<SourceElement.Row>();

            foreach(var row in EClass.sources.elements.rows)
            {
                if (string.IsNullOrEmpty(row.alias)) continue;

                // --- Robust Filter based on Game Logic ---

                // 1. Must be a valid enchant candidate (Has slot or is specific enc type)
                bool isEnc = row.IsWeaponEnc || row.IsShieldEnc;
                if (!string.IsNullOrEmpty(row.encSlot) && row.encSlot != "global") isEnc = true;

                if (!isEnc) continue;

                // 2. Must be naturally generating (Chance > 0)
                if (row.chance <= 0) continue;
                if (row.tag.Contains("noRandomEnc")) continue;

                // 3. Strict Category Whitelist
                if (row.category != "attribute" &&
                    row.category != "resist" &&
                    row.category != "skill" &&
                    row.category != "enchant")
                {
                    continue;
                }

                // 4. Exclude non-enchant types that might accidentally match (Safety)
                // Note: 'isSkill' enchants (e.g. Mining +1) ARE valid, so we DO NOT exclude them.
                if (row.isSpell) continue;
                if (row.isTrait) continue;

                sources.Add(row);
            }

            sources.Sort((a,b) => a.id - b.id);

            // Note: Since this creates a LayerList, we use SetList (or SetList2) logic.
            // Using basic SetList for simplicity as it was in original code.
            layer.SetList(sources, (row) => row.GetName() + " (" + row.alias + ")", (idx, val) => {
                onConfirm(sources[idx]);
                layer.Close();
            }, true);

            // --- Window Sizing ---
            // Use built-in SetSize if available, fallback to manual Ref
            try {
                layer.SetSize(900, 800); // 3 Columns (280*3=840 + spacing)
            } catch (Exception e) {
                 Debug.LogError("[Relocator] SetSize failed: " + e.Message);
            }

            // --- Grid Layout Injection ---
            try {
                // Find the LayoutGroup. It is likely on the 'Content' object of the ScrollRect.
                LayoutGroup targetLayout = null;

                // 1. Check UIList._layoutItems (if public) or direct component
                targetLayout = layer.list.GetComponent<LayoutGroup>();

                // 2. Search deeper (Content)
                if (targetLayout == null) {
                    targetLayout = layer.list.GetComponentInChildren<LayoutGroup>(true);
                }

                if (targetLayout != null) {
                    // Debug.Log("[Relocator] Found LayoutGroup on: " + targetLayout.gameObject.name);
                    GameObject layoutObj = targetLayout.gameObject;

                    UnityEngine.Object.DestroyImmediate(targetLayout);

                    var grid = layoutObj.AddComponent<GridLayoutGroup>();
                    // 3 Columns configuration
                    // Width 280 * 3 = 840. Window Width 900.
                    grid.cellSize = new Vector2(280, 28);
                    grid.spacing = new Vector2(10, 2);
                    grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
                    grid.constraintCount = 3;
                    // grid.childAlignment = TextAnchor.UpperLeft;

                    // Force rebuild
                     ContentSizeFitter fitter = layoutObj.GetComponent<ContentSizeFitter>();
                    if (fitter) {
                        fitter.enabled = false;
                        fitter.enabled = true;
                    }
                } else {
                    Debug.LogError("[Relocator] Could not find LayoutGroup to replace!");
                }
            } catch (Exception e) {
                Debug.LogError("[Relocator] Failed to inject Grid Layout: " + e.Message);
            }
            // -----------------------------
        }
        public static void ShowPresetPicker(Action<string> onSelect)
        {
            var layer = EClass.ui.AddLayer<LayerList>();
            layer.SetSize(400, 600);
            layer.windows[0].SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Presets));

            Action refresh = null;
            refresh = () => {
                // Safety check: ensure layer is still alive
                if (layer == null || layer.gameObject == null) return;

                var presets = RelocatorManager.Instance.GetPresetList();

                try {
                    layer.SetList2<string>(
                        presets,
                        (n) => n,
                        (n, b) => { // On Row Click
                            onSelect(n);
                            layer.Close();
                        },
                        (n, b) => { // On Instantiate
                             b.SetMainText(n);

                             // Helper to attach/update Menu Button
                             Transform t = b.transform.Find("BtnPresetMenu");
                             Button btnMenu = null;

                             if (t == null) {
                                 // Create Button
                                 var go = new GameObject("BtnPresetMenu");
                                 go.transform.SetParent(b.transform, false);

                                 var sourceText = b.GetComponentInChildren<Text>();

                                 var txt = go.AddComponent<Text>();
                                 txt.text = "[▼More]";
                                 if (sourceText != null) {
                                     txt.font = sourceText.font;
                                     txt.fontSize = sourceText.fontSize;
                                 } else {
                                     // Fallback
                                     txt.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
                                     txt.fontSize = 14;
                                 }
                                 txt.alignment = TextAnchor.MiddleCenter;
                                 txt.color = Color.white;

                                 var rt = go.GetComponent<RectTransform>();
                                 rt.anchorMin = new Vector2(1, 0);
                                 rt.anchorMax = new Vector2(1, 1);
                                 rt.pivot = new Vector2(1, 0.5f);
                                 rt.sizeDelta = new Vector2(80, 0);
                                 rt.anchoredPosition = new Vector2(-10, 0);

                                 btnMenu = go.AddComponent<Button>();
                                 btnMenu.targetGraphic = txt;

                                 var colors = btnMenu.colors;
                                 colors.normalColor = new Color(0.45f, 0.55f, 0.7f, 1f);
                                 colors.highlightedColor = new Color(0.2f, 0.4f, 1f, 1f);
                                 colors.pressedColor = new Color(0.1f, 0.2f, 0.6f, 1f);
                                 colors.selectedColor = colors.normalColor;
                                 colors.colorMultiplier = 1f;
                                 btnMenu.colors = colors;
                             } else {
                                 btnMenu = t.GetComponent<Button>();
                             }

                             // Update Listener specific to this 'n'
                             btnMenu.onClick.RemoveAllListeners();
                             btnMenu.onClick.AddListener(() => {
                                 // Show Context Menu
                                 RelocatorMenu.Create()
                                     .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Rename), () => {
                                         Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_RenamePrompt), n, (cancel, text) => {
                                             if (!cancel && !string.IsNullOrEmpty(text) && text != n) {
                                                 RelocatorManager.Instance.RenamePreset(n, text);
                                                 if (layer != null && layer.gameObject != null) refresh();
                                             }
                                         });
                                     })
                                     .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Delete), () => {
                                         RelocatorManager.Instance.DeletePreset(n);
                                         if (layer != null && layer.gameObject != null) refresh();
                                     })
                                     .Show();
                             });
                        }
                    );
                } catch (Exception ex) {
                    Debug.LogError("[Relocator] Error refreshing preset list: " + ex);
                }
            };

            refresh();
        }
    }


}
