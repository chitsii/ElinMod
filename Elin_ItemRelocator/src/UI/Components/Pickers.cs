using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace Elin_ItemRelocator {
    public static class RelocatorPickers {


        public static void ShowCategoryPicker(List<string> initialSelection, Action<List<string>> onConfirm) {
            HashSet<string> selected = new HashSet<string>();
            if (initialSelection != null)
                foreach (var s in initialSelection)
                    selected.Add(s);

            var allCats = EClass.sources.categories.rows;
            var roots = allCats.Where(r => r.parent == null).OrderBy(r => r.id).ToList();

            var tree = RelocatorTree<SourceCategory.Row>.Create();

            tree.SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Category));
            tree.SetRoots(roots);

            tree.SetChildren((SourceCategory.Row cat) => allCats.Where(r => r.parent == cat).OrderBy(r => r.id));
            tree.SetText((SourceCategory.Row cat) => cat.GetName());

            Func<SourceCategory.Row, bool> isParentSelected = null;
            isParentSelected = (SourceCategory.Row c) => {
                if (c.parent == null)
                    return false;
                if (selected.Contains(c.parent.id))
                    return true;
                return isParentSelected(c.parent);
            };

            tree.SetIsSelected((SourceCategory.Row cat) => selected.Contains(cat.id));
            tree.SetIsDisabled((SourceCategory.Row cat) => isParentSelected(cat));
            tree.SetOnSelect((SourceCategory.Row cat) => {
                if (selected.Contains(cat.id))
                    selected.Remove(cat.id);
                else
                    selected.Add(cat.id);
            });

            tree.AddBottomButton("[ OK ]", () => {
                onConfirm(selected.ToList());
                tree.Close();
            }, new Color(0.3f, 0.5f, 0));

            tree.Show();
        }

        public static void ShowEnchantPicker(int filterMode, Action<SourceElement.Row> onConfirm) {
            var layer = EClass.ui.AddLayer<LayerList>();

            // Caption
            string caption = "";
            switch (filterMode) {
            case 1:
                caption = RelocatorLang.GetText(RelocatorLang.LangKey.SelectEnchant) + " (" + RelocatorLang.GetText(RelocatorLang.LangKey.CatWeapon) + ")";
                break;
            case 2:
                caption = RelocatorLang.GetText(RelocatorLang.LangKey.SelectEnchant) + " (" + RelocatorLang.GetText(RelocatorLang.LangKey.CatArmor) + ")";
                break;
            default:
                caption = RelocatorLang.GetText(RelocatorLang.LangKey.SelectEnchant);
                break;
            }
            layer.windows[0].SetCaption(caption);
            layer.windows[0].setting.allowResize = true;
            try { layer.SetSize(900, 800); } catch { }

            // 1. Gather Valid Enchants & Sort
            var sources = new List<SourceElement.Row>();
            foreach (var row in EClass.sources.elements.rows) {
                if (string.IsNullOrEmpty(row.alias))
                    continue;
                bool isEnc = row.IsWeaponEnc || row.IsShieldEnc;
                if (!string.IsNullOrEmpty(row.encSlot) && row.encSlot != "global")
                    isEnc = true;
                if (!isEnc)
                    continue;
                if (row.chance <= 0)
                    continue;
                if (row.tag.Contains("noRandomEnc"))
                    continue;
                if (row.category != "attribute" && row.category != "resist" && row.category != "skill" && row.category != "enchant")
                    continue;
                if (row.isSpell)
                    continue;
                if (row.isTrait)
                    continue;

                // --- Filter Logic ---
                if (filterMode == 1) { // Weapon
                    if (!(row.IsWeaponEnc || row.encSlot == "weapon"))
                        continue;
                } else if (filterMode == 2) { // Armor
                    bool isWeapon = (row.IsWeaponEnc || row.encSlot == "weapon");
                    if (isWeapon)
                        continue;
                    if (row.encSlot == "all")
                        continue; // Exclude 'all' from armor specific list? Or include? User said "Split", usually implies exclusive or focused.
                                  // But "All" category usually contains general stuff.
                                  // Let's adhere to previous logic:
                                  // Group 0=All, 1=Weapon, 2=Armor.
                                  // If filterMode==0 (All in general), show everything (or just 'all' category?)
                                  // User said "All", "Weapon", "Armor".
                                  // Most likely:
                                  // - Button All: Show General/Common enchants (encSlot == "all" etc).
                                  // - Button Weapon: Weapon specific.
                                  // - Button Armor: Armor specific.
                } else {
                    // Mode 0: General/All
                    if (row.encSlot != "all")
                        continue;
                }

                sources.Add(row);
            }

            // Sort: ID
            sources.Sort((a, b) => a.id - b.id);

            // 2. Display List (3-column grid)
            layer.SetList(sources, (row) => row.GetName() + " (" + row.alias + ")", (idx, val) => {
                onConfirm(sources[idx]);
                layer.Close();
            }, true);

            // Apply Grid Layout
            try {
                LayoutGroup targetLayout = null;
                targetLayout = layer.list.GetComponent<LayoutGroup>();
                if (targetLayout == null)
                    targetLayout = layer.list.GetComponentInChildren<LayoutGroup>(true);
                if (targetLayout != null) {
                    GameObject layoutObj = targetLayout.gameObject;
                    UnityEngine.Object.DestroyImmediate(targetLayout);
                    var grid = layoutObj.AddComponent<GridLayoutGroup>();
                    grid.cellSize = new Vector2(280, 28);
                    grid.spacing = new Vector2(10, 2);
                    grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
                    grid.constraintCount = 3;
                    ContentSizeFitter fitter = layoutObj.GetComponent<ContentSizeFitter>();
                    if (fitter) { fitter.enabled = false; fitter.enabled = true; }
                }
            } catch (Exception e) { Debug.LogError(e.Message); }
        }

        public static void ShowPresetPicker(Action<string> onSelect) {
            var layer = EClass.ui.AddLayer<LayerList>();
            layer.SetSize(400, 600);
            layer.windows[0].SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Presets));
            Action refresh = null;
            refresh = () => {
                if (layer == null || layer.gameObject == null)
                    return;
                var presets = RelocatorManager.Instance.GetPresetList();
                try {
                    layer.SetList2<string>(
                        presets,
                        (n) => n,
                        (n, b) => { onSelect(n); layer.Close(); },
                        (n, b) => {
                            b.SetMainText(n);
                            Transform t = b.transform.Find("BtnPresetMenu");
                            Button btnMenu = null;
                            if (t == null) {
                                var go = new GameObject("BtnPresetMenu");
                                go.transform.SetParent(b.transform, false);
                                var sourceText = b.GetComponentInChildren<Text>();
                                var txt = go.AddComponent<Text>();
                                txt.text = "[▼More]";
                                if (sourceText != null) { txt.font = sourceText.font; txt.fontSize = sourceText.fontSize; } else { txt.font = SkinManager.Instance.fontSet.ui.source.font; txt.fontSize = 14; } // Updated Font
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
                                btnMenu.colors = colors;
                            } else { btnMenu = t.GetComponent<Button>(); }
                            btnMenu.onClick.RemoveAllListeners();
                            btnMenu.onClick.AddListener(() => {
                                RelocatorMenu.Create()
                                    .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Rename), () => {
                                        Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_RenamePrompt), n, (cancel, text) => {
                                            if (!cancel && !string.IsNullOrEmpty(text) && text != n) {
                                                RelocatorManager.Instance.RenamePreset(n, text);
                                                if (layer != null && layer.gameObject != null)
                                                    refresh();
                                            }
                                        });
                                    })
                                    .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Delete), () => {
                                        RelocatorManager.Instance.DeletePreset(n);
                                        if (layer != null && layer.gameObject != null)
                                            refresh();
                                    })
                                    .Show();
                            });
                        }
                    );
                } catch (Exception ex) { Debug.LogError(ex); }
            };
            refresh();
        }

        public static void ShowMaterialPicker(List<string> initialSelection, Action<List<string>> onConfirm) {
            HashSet<string> selected = new HashSet<string>();
            if (initialSelection != null)
                foreach (var s in initialSelection)
                    selected.Add(s);

            // Access materials
            var sources = EClass.sources.materials.rows.Where(r => !string.IsNullOrEmpty(r.alias)).OrderBy(r => r.id).ToList();

            var tree = RelocatorTree<SourceMaterial.Row>.Create();
            tree.SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Material));
            tree.SetRoots(sources);

            tree.SetText((SourceMaterial.Row m) => m.GetName() + " (" + m.alias + ")");
            tree.SetIsSelected((SourceMaterial.Row m) => {
                return selected.Contains(m.alias) || selected.Contains(m.id.ToString());
            });

            tree.SetOnSelect((SourceMaterial.Row m) => {
                string key = m.alias; // Use alias as primary key
                if (selected.Contains(key))
                    selected.Remove(key);
                else
                    selected.Add(key);
            });

            tree.AddBottomButton("[ OK ]", () => {
                onConfirm(selected.ToList());
                tree.Close();
            }, new Color(0.3f, 0.5f, 0));

            tree.Show();
        }

        public static void ShowBlessPicker(List<int> initialSelection, Action<List<int>> onConfirm) {
            HashSet<int> selected = new HashSet<int>();
            if (initialSelection != null)
                foreach (var s in initialSelection)
                    selected.Add(s);

            // Hardcoded sources
            var sources = new List<int> { 0, 1, -1, -2 }; // Normal, Blessed, Cursed, Doomed

            var tree = RelocatorTree<int>.Create();
            tree.SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Bless));
            tree.SetRoots(sources);

            tree.SetText((int b) => {
                if (b == 1)
                    return RelocatorLang.GetText(RelocatorLang.LangKey.StateBlessed);
                if (b == -1)
                    return RelocatorLang.GetText(RelocatorLang.LangKey.StateCursed);
                if (b == 0)
                    return RelocatorLang.GetText(RelocatorLang.LangKey.StateNormal);
                if (b == -2)
                    return RelocatorLang.GetText(RelocatorLang.LangKey.StateDoomed);
                return b.ToString();
            });

            tree.SetIsSelected((int b) => selected.Contains(b));

            tree.SetOnSelect((int b) => {
                if (selected.Contains(b))
                    selected.Remove(b);
                else
                    selected.Add(b);
            });

            tree.AddBottomButton("[ OK ]", () => {
                onConfirm(selected.ToList());
                tree.Close();
            }, new Color(0.3f, 0.5f, 0));

            tree.Show();
        }

        public static void ShowRarityPicker(List<int> initialSelection, Action<List<int>> onConfirm) {
            HashSet<int> selected = new HashSet<int>();
            if (initialSelection != null)
                foreach (var s in initialSelection)
                    selected.Add(s);

            // Access Rarity List (Lang "quality"): index 0 = -1 (Crude), 1 = 0 (Normal)...
            var updateList = Lang.GetList("quality");
            List<int> sources = new List<int>();
            for (int i = 0; i < updateList.Length; i++) {
                sources.Add(i - 1);
            }

            var tree = RelocatorTree<int>.Create();
            tree.SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Rarity));
            tree.SetRoots(sources);

            tree.SetText((int r) => {
                int index = r + 1;
                if (index >= 0 && index < updateList.Length)
                    return updateList[index];
                return r.ToString();
            });

            tree.SetIsSelected((int r) => selected.Contains(r));

            tree.SetOnSelect((int r) => {
                if (selected.Contains(r))
                    selected.Remove(r);
                else
                    selected.Add(r);
            });

            tree.AddBottomButton("[ OK ]", () => {
                onConfirm(selected.ToList());
                tree.Close();
            }, new Color(0.3f, 0.5f, 0));

            tree.Show();
        }

        // General Element Picker (for DNA etc)
        // DNA Content Picker (Tree-based)
        public static void ShowDnaContentPicker(List<string> initialSelection, Action<List<string>> onConfirm) {
            HashSet<string> selected = new HashSet<string>();
            if (initialSelection != null)
                foreach (var s in initialSelection) {
                    // Handle "mining>=5" style strings - extract just the ID part for selection state
                    string id = s;
                    string[] ops = [">=", "<=", "!=", ">", "<", "="];
                    foreach (var o in ops) {
                        int idx = s.IndexOf(o);
                        if (idx > 0) {
                            id = s.Substring(0, idx).Trim();
                            break;
                        }
                    }
                    selected.Add(id);
                }

            // Roots: Categories
            var categories = new List<string> { "attribute", "skill", "feat", "ability", "slot" };

            // Map: Category -> List<SourceElement.Row>
            var map = new Dictionary<string, List<SourceElement.Row>>();
            foreach (var cat in categories)
                map[cat] = new List<SourceElement.Row>();

            foreach (var row in EClass.sources.elements.rows) {
                if (string.IsNullOrEmpty(row.alias))
                    continue;
                if (row.tag.Contains("hidden"))
                    continue;
                if (map.ContainsKey(row.category)) {
                    map[row.category].Add(row);
                }
            }

            // Sort
            foreach (var list in map.Values)
                list.Sort((a, b) => a.id - b.id);

            var tree = RelocatorTree<object>.Create();
            tree.SetCaption("Select DNA Content");
            tree.SetRoots(categories.Cast<object>());

            tree.SetChildren((object obj) => {
                if (obj is string cat && map.ContainsKey(cat)) {
                    return map[cat].Cast<object>();
                }
                return null;
            });

            tree.SetText((object obj) => {
                if (obj is string cat) {
                    if (Enum.TryParse("Cat_" + char.ToUpper(cat[0]) + cat.Substring(1), out RelocatorLang.LangKey key))
                        return RelocatorLang.GetText(key);
                    return cat.ToUpper();
                }
                if (obj is SourceElement.Row row)
                    return row.GetName();
                return obj.ToString();
            });

            tree.SetIsSelected((object obj) => {
                if (obj is SourceElement.Row row)
                    return selected.Contains(row.alias);
                return false;
            });

            tree.SetOnSelect((object obj) => {
                if (obj is SourceElement.Row row) {
                    if (selected.Contains(row.alias))
                        selected.Remove(row.alias);
                    else
                        selected.Add(row.alias);
                }
            });

            tree.AddBottomButton("[ OK ]", () => {
                onConfirm(selected.ToList());
                tree.Close();
            }, new Color(0.3f, 0.5f, 0));

            tree.Show();
        }
    }
}
