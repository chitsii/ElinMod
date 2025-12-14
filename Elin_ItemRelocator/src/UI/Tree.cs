using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace Elin_ItemRelocator
{
    public class RelocatorTree<T>
    {
        private List<T> roots = new List<T>();
        private Func<T, IEnumerable<T>> getChildren;
        private Func<T, string> getText;
        private Func<T, string> getDebugText;
        private Action<T> onSelect;
        private Func<T, bool> isSelected;
        private Func<T, bool> isDisabled; // e.g., if parent is selected
        private string caption = "Tree";
        private LayerList _layer;
        private HashSet<T> expanded = new HashSet<T>();
        private List<BottomButtonDef> bottomButtons = new List<BottomButtonDef>();

        // Cache the content transform to avoid accessing destroyed components
        private Transform _contentTrans;

        // Font customization
        private Font uiFont;

        public class BottomButtonDef
        {
            public string Label;
            public Action OnClick;
            public Color? Color;
        }

        private RelocatorTree()
        {
            uiFont = Resources.GetBuiltinResource<Font>("Arial.ttf");
        }

        public static RelocatorTree<T> Create()
        {
            return new RelocatorTree<T>();
        }

        public RelocatorTree<T> SetCaption(string text)
        {
            this.caption = text;
            return this;
        }

        public RelocatorTree<T> SetRoots(IEnumerable<T> roots)
        {
            this.roots = roots.ToList();
            return this;
        }

        public RelocatorTree<T> SetChildren(Func<T, IEnumerable<T>> accessor)
        {
            this.getChildren = accessor;
            return this;
        }

        public RelocatorTree<T> SetText(Func<T, string> selector)
        {
            this.getText = selector;
            return this;
        }

        public RelocatorTree<T> SetDebugText(Func<T, string> selector)
        {
            this.getDebugText = selector;
            return this;
        }

        public RelocatorTree<T> SetOnSelect(Action<T> action)
        {
            this.onSelect = action;
            return this;
        }

        public RelocatorTree<T> SetIsSelected(Func<T, bool> predicate)
        {
            this.isSelected = predicate;
            return this;
        }

        public RelocatorTree<T> SetIsDisabled(Func<T, bool> predicate)
        {
            this.isDisabled = predicate;
            return this;
        }

        public RelocatorTree<T> AddBottomButton(string label, Action onClick, Color? color = null)
        {
            bottomButtons.Add(new BottomButtonDef { Label = label, OnClick = onClick, Color = color });
            return this;
        }

        public LayerList Show()
        {
            bool isNew = false;
            // Robust Layer Creation
            if (_layer == null || _layer.gameObject == null) {
                _layer = EClass.ui.AddLayer<LayerList>();
                if (_layer == null) {
                    Debug.LogError("[RelocatorTree] Failed to create LayerList!");
                    return null;
                }
                isNew = true;
            }
            var layer = _layer;

            if (isNew) {
                if (layer.windows.Count > 0)
                {
                    layer.windows[0].SetCaption(caption ?? "Tree");
                    layer.windows[0].setting.allowResize = true;
                }
                else
                {
                    Debug.LogWarning("[RelocatorTree] LayerList has no windows!");
                }

                try { layer.SetSize(500, 700); } catch {}

                // --- MANUAL SETUP ---
                if (layer.list != null)
                {
                    // Cache Transform BEFORE destroying the UIList component
                    _contentTrans = layer.list.transform;
                    var contentTrans = _contentTrans;

                    // 1. Destroy native UIList (if exists)
                    var nativeList = layer.list.GetComponent<UIList>();
                    if (nativeList) UnityEngine.Object.DestroyImmediate(nativeList);

                    // 2. Setup VLG
                    if (contentTrans != null)
                    {
                        var vlg = contentTrans.GetComponent<VerticalLayoutGroup>();
                        if (!vlg) vlg = contentTrans.gameObject.AddComponent<VerticalLayoutGroup>();
                        vlg.childControlWidth = true;
                        vlg.childControlHeight = true;
                        vlg.childForceExpandWidth = true;
                        vlg.childForceExpandHeight = false;
                        vlg.spacing = 0;
                        vlg.padding = new RectOffset(0,0,0,0);

                        var csf = contentTrans.GetComponent<ContentSizeFitter>();
                        if (!csf) csf = contentTrans.gameObject.AddComponent<ContentSizeFitter>();
                        csf.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
                        csf.horizontalFit = ContentSizeFitter.FitMode.Unconstrained;
                    }
                }
                else
                {
                     Debug.LogError("[RelocatorTree] layer.list is NULL!");
                }
            }

            Refresh();
            return layer;
        }

        public void Refresh()
        {
            if (_layer == null || _layer.gameObject == null) return;
            if (_contentTrans == null) return;

            var contentTrans = _contentTrans;

            // 1. Flatten Data
            var flattened = new List<Tuple<T, int>>(); // Item, Depth

            Action<IEnumerable<T>, int> traverse = null;
            traverse = (items, depth) => {
                if (items == null) return;
                foreach(var item in items) {
                    flattened.Add(Tuple.Create(item, depth));
                    // Check expansion
                    if (expanded.Contains(item)) {
                        var kids = getChildren != null ? getChildren(item) : null;
                        if (kids != null && kids.Any()) {
                            traverse(kids, depth + 1);
                        }
                    }
                }
            };
            traverse(roots, 0);

            // 2. Clear Visuals
            foreach(Transform child in contentTrans) {
                 UnityEngine.Object.Destroy(child.gameObject);
            }
            contentTrans.DetachChildren();

            // 3. Rebuild
            foreach(var tuple in flattened) {
                T item = tuple.Item1;
                int depth = tuple.Item2;

                BuildRow(contentTrans, item, depth);
            }

            // 4. Bottom Buttons
            foreach(var btnDef in bottomButtons) {
                BuildBottomButton(contentTrans, btnDef);
            }

            LayoutRebuilder.ForceRebuildLayoutImmediate(contentTrans as RectTransform);
        }

        private void BuildRow(Transform parent, T item, int depth)
        {
            var rowGO = new GameObject("Row");
            rowGO.transform.SetParent(parent, false);

            var hlg = rowGO.AddComponent<HorizontalLayoutGroup>();
            hlg.childControlWidth = true; hlg.childControlHeight = true;
            hlg.childForceExpandWidth = false; hlg.childForceExpandHeight = true;
            hlg.spacing = 0; hlg.padding = new RectOffset(5, 5, 0, 0);

            var leRow = rowGO.AddComponent<LayoutElement>();
            leRow.minHeight = 28; leRow.preferredHeight = 28; leRow.flexibleHeight = 0;

            // Clicker
            var clickerGO = new GameObject("Clicker");
            clickerGO.transform.SetParent(rowGO.transform, false);
            var leClicker = clickerGO.AddComponent<LayoutElement>();
            leClicker.ignoreLayout = true;
            var imgClicker = clickerGO.AddComponent<Image>();
            imgClicker.color = Color.clear;
            var btnClicker = clickerGO.AddComponent<Button>();
            btnClicker.targetGraphic = imgClicker;
            var rtClicker = clickerGO.GetComponent<RectTransform>();
            rtClicker.anchorMin = Vector2.zero; rtClicker.anchorMax = Vector2.one;
            rtClicker.offsetMin = Vector2.zero; rtClicker.offsetMax = Vector2.zero;
            clickerGO.transform.SetSiblingIndex(0);

            // Spacer
            var spacer = new GameObject("Spacer");
            spacer.transform.SetParent(rowGO.transform, false);
            var leSpacer = spacer.AddComponent<LayoutElement>();
            float indent = depth * 15;
            leSpacer.minWidth = indent; leSpacer.preferredWidth = indent;
            spacer.SetActive(indent > 0);

            // Expand
            var expandGO = new GameObject("Expand");
            expandGO.transform.SetParent(rowGO.transform, false);
            var leExpand = expandGO.AddComponent<LayoutElement>();
            leExpand.minWidth = 24; leExpand.preferredWidth = 24;
            leExpand.minHeight = 24; leExpand.preferredHeight = 24;

            var txtExpand = new GameObject("Text").AddComponent<Text>();
            txtExpand.transform.SetParent(expandGO.transform, false);
            txtExpand.rectTransform.anchorMin = Vector2.zero; txtExpand.rectTransform.anchorMax = Vector2.one;
            txtExpand.font = uiFont; txtExpand.fontSize = 14;
            txtExpand.alignment = TextAnchor.MiddleCenter; txtExpand.color = Color.black; txtExpand.fontStyle = FontStyle.Bold;
            txtExpand.raycastTarget = false;

            var imgExpand = expandGO.AddComponent<Image>();
            // Transparent
            imgExpand.color = Color.clear;
            var btnExpand = expandGO.AddComponent<Button>();
            btnExpand.targetGraphic = imgExpand;

            // Label
            var lblGO = new GameObject("Label");
            lblGO.transform.SetParent(rowGO.transform, false);
            var leLbl = lblGO.AddComponent<LayoutElement>();
            leLbl.flexibleWidth = 1;
            var lbl = lblGO.AddComponent<Text>();
            lbl.font = uiFont; lbl.fontSize = 14; lbl.alignment = TextAnchor.MiddleLeft;
            lbl.resizeTextForBestFit = true; lbl.resizeTextMinSize = 10; lbl.resizeTextMaxSize = 14;
            lbl.raycastTarget = false;

            // Logic
            var kids = getChildren != null ? getChildren(item) : null;
            bool hasKids = kids != null && kids.Any();

            if (hasKids) {
                bool isExp = expanded.Contains(item);
                txtExpand.text = isExp ? "-" : "+";
                btnExpand.onClick.AddListener(() => {
                    if (expanded.Contains(item)) expanded.Remove(item);
                    else expanded.Add(item);
                    EClass.Sound.Play("click");
                    Refresh();
                });
            } else {
                imgExpand.color = Color.clear;
                txtExpand.text = "";
                btnExpand.interactable = false;
            }

            bool disabled = isDisabled != null && isDisabled(item);
            bool selected = isSelected != null && isSelected(item);

            string extra = (getDebugText != null) ? getDebugText(item) : "";
            string name = (getText != null) ? getText(item) : item.ToString();

            if (disabled) {
                lbl.text = "[P] " + name + extra;
                lbl.color = Color.gray;
                btnClicker.enabled = false;
            } else {
                lbl.text = (selected ? "[v] " : "[  ] ") + name + extra;
                lbl.color = selected ? new Color(0, 0, 0.8f) : new Color(0.1f, 0.1f, 0.1f);
                btnClicker.enabled = true;
                btnClicker.onClick.AddListener(() => {
                   if (onSelect != null) {
                       onSelect(item);
                       EClass.Sound.Play("click");
                       Refresh();
                   }
                });
            }
        }

        private void BuildBottomButton(Transform parent, BottomButtonDef def)
        {
            var btnGO = new GameObject("Btn_" + def.Label);
            btnGO.transform.SetParent(parent, false);

            var hlg = btnGO.AddComponent<HorizontalLayoutGroup>();
            hlg.childControlWidth = true; hlg.childControlHeight = true;
            hlg.padding = new RectOffset(10, 10, 5, 5);

            var le = btnGO.AddComponent<LayoutElement>();
            le.minHeight = 40; le.preferredHeight = 40; le.flexibleHeight = 0;

            var bg = btnGO.AddComponent<Image>();
            bg.color = Color.clear; // Default button bg

            var btn = btnGO.AddComponent<Button>();
            btn.targetGraphic = bg;
            btn.onClick.AddListener(() => {
                if (def.OnClick != null) def.OnClick();
            });

            var txtGO = new GameObject("Text");
            txtGO.transform.SetParent(btnGO.transform, false);
            var txt = txtGO.AddComponent<Text>();
            txt.font = uiFont;
            txt.fontSize = 16;
            txt.alignment = TextAnchor.MiddleCenter;
            txt.text = "<b>" + def.Label + "</b>";
            txt.color = def.Color ?? new Color(0.1f, 0.1f, 0.1f);
        }

        public void Close()
        {
            if (_layer != null) _layer.Close();
        }
    }
}
