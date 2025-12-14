using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace Elin_ItemRelocator
{
    public static class RelocatorPickers
    {
        public static void ShowCategoryPicker(List<string> initialSelection, Action<List<string>> onConfirm)
        {
            HashSet<string> selected = new HashSet<string>();
            if (initialSelection != null) foreach(var s in initialSelection) selected.Add(s);

            var allCats = EClass.sources.categories.rows;
            var roots = allCats.Where(r => r.parent == null).OrderBy(r => r.id).ToList();

            // Using direct class name now that build.bat is fixed
            var tree = RelocatorTree<SourceCategory.Row>.Create();

            tree.SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Category));
            tree.SetRoots(roots);

            tree.SetChildren((SourceCategory.Row cat) => allCats.Where(r => r.parent == cat).OrderBy(r => r.id));
            tree.SetText((SourceCategory.Row cat) => cat.GetName());

            Func<SourceCategory.Row, bool> isParentSelected = null;
            isParentSelected = (SourceCategory.Row c) => {
                 if (c.parent == null) return false;
                 if (selected.Contains(c.parent.id)) return true;
                 return isParentSelected(c.parent);
            };

            tree.SetIsSelected((SourceCategory.Row cat) => selected.Contains(cat.id));
            tree.SetIsDisabled((SourceCategory.Row cat) => isParentSelected(cat));
            tree.SetOnSelect((SourceCategory.Row cat) => {
                if (selected.Contains(cat.id)) selected.Remove(cat.id);
                else selected.Add(cat.id);
            });

            tree.AddBottomButton("[ OK ]", () => {
                onConfirm(selected.ToList());
                tree.Close();
            }, new Color(0.3f, 0.5f, 0));

            tree.Show();
        }

        public static void ShowEnchantPicker(Action<SourceElement.Row> onConfirm)
        {
            var layer = EClass.ui.AddLayer<LayerList>();
            layer.windows[0].SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.SelectEnchant));
            layer.windows[0].setting.allowResize = true;
            try { layer.SetSize(900, 800); } catch {}
            var sources = new List<SourceElement.Row>();
            foreach(var row in EClass.sources.elements.rows) {
                if (string.IsNullOrEmpty(row.alias)) continue;
                bool isEnc = row.IsWeaponEnc || row.IsShieldEnc;
                if (!string.IsNullOrEmpty(row.encSlot) && row.encSlot != "global") isEnc = true;
                if (!isEnc) continue;
                if (row.chance <= 0) continue;
                if (row.tag.Contains("noRandomEnc")) continue;
                if (row.category != "attribute" && row.category != "resist" && row.category != "skill" && row.category != "enchant") continue;
                if (row.isSpell) continue;
                if (row.isTrait) continue;
                sources.Add(row);
            }
            sources.Sort((a,b) => a.id - b.id);
            layer.SetList(sources, (row) => row.GetName() + " (" + row.alias + ")", (idx, val) => {
                onConfirm(sources[idx]);
                layer.Close();
            }, true);
            try {
                LayoutGroup targetLayout = null;
                targetLayout = layer.list.GetComponent<LayoutGroup>();
                if (targetLayout == null) targetLayout = layer.list.GetComponentInChildren<LayoutGroup>(true);
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

        public static void ShowPresetPicker(Action<string> onSelect)
        {
            var layer = EClass.ui.AddLayer<LayerList>();
            layer.SetSize(400, 600);
            layer.windows[0].SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Presets));
            Action refresh = null;
            refresh = () => {
                if (layer == null || layer.gameObject == null) return;
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
                                 if (sourceText != null) { txt.font = sourceText.font; txt.fontSize = sourceText.fontSize; }
                                 else { txt.font = Resources.GetBuiltinResource<Font>("Arial.ttf"); txt.fontSize = 14; }
                                 txt.alignment = TextAnchor.MiddleCenter;
                                 txt.color = Color.white;
                                 var rt = go.GetComponent<RectTransform>();
                                 rt.anchorMin = new Vector2(1, 0); rt.anchorMax = new Vector2(1, 1);
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
                } catch (Exception ex) { Debug.LogError(ex); }
            };
            refresh();
        }
    }
}
