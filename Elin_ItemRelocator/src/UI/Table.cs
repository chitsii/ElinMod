using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace Elin_ItemRelocator
{
    public class RelocatorTable<T>
    {
        private List<ColumnDef> columns = new List<ColumnDef>();
        private IEnumerable<T> data;
        private string caption = "Table";
        private Action<T> onSelectRow; // Optional row click handler
        private bool showHeader = true;
        private float preferredHeight = 800;
        private LayerList _layer; // Persistent layer reference

        public class ColumnDef
        {
             public string Header;
             public float Width;
             public Action<T, GameObject> Binder;
        }

        private RelocatorTable() { }

        public static RelocatorTable<T> Create()
        {
            return new RelocatorTable<T>();
        }

        public RelocatorTable<T> SetCaption(string text)
        {
            this.caption = text;
            return this;
        }

        public RelocatorTable<T> SetDataSource(IEnumerable<T> dataSource)
        {
            this.data = dataSource;
            return this;
        }

        public RelocatorTable<T> SetOnSelect(Action<T> onSelect)
        {
            this.onSelectRow = onSelect;
            return this;
        }

        public RelocatorTable<T> SetShowHeader(bool show)
        {
            this.showHeader = show;
            return this;
        }

        public RelocatorTable<T> SetPreferredHeight(float h)
        {
            this.preferredHeight = h;
            return this;
        }

        public RelocatorTable<T> AddColumn(string header, float width, Action<T, GameObject> onBind)
        {
            columns.Add(new ColumnDef { Header = header, Width = width, Binder = onBind });
            return this;
        }

        // Helper for simple text column
        public RelocatorTable<T> AddTextColumn(string header, float width, Func<T, string> textSelector, Action<Text> configureText = null)
        {
            return AddColumn(header, width, (item, cell) => {
                 // Try to reuse existing Text or add new
                 var t = cell.GetComponent<Text>();
                 if (!t) {
                     t = cell.AddComponent<Text>();
                     t.font = SkinManager.Instance.fontSet.ui.source.font;
                     Color c = Color.black;
                     if (SkinManager.CurrentColors != null) c = SkinManager.CurrentColors.textDefault;
                     t.color = c;
                     t.alignment = TextAnchor.MiddleLeft;
                     t.resizeTextForBestFit = true;
                     t.resizeTextMinSize = 8;
                     t.resizeTextMaxSize = 13;
                     t.horizontalOverflow = HorizontalWrapMode.Wrap;
                     t.verticalOverflow = VerticalWrapMode.Truncate;
                 }

                 t.text = textSelector(item);
                 if (configureText != null) configureText(t);
            });
        }

        public LayerList Show()
        {
             if (data == null) data = new List<T>();

             // 1. Create or Reuse Layer
             bool isNew = false;
             if (_layer == null || _layer.gameObject == null) {
                _layer = EClass.ui.AddLayer<LayerList>();
                isNew = true;
             }
             var layer = _layer;

             if (isNew) {
                 layer.windows[0].SetCaption(caption);
                 layer.windows[0].setting.allowResize = true;

                 // 2. Calculate Window Size
                 float totalWidth = columns.Sum(c => c.Width) + 60; // Padding
                 if (totalWidth < 400) totalWidth = 400; // Min width
                 try { layer.SetSize(totalWidth, preferredHeight); } catch {}

                 // 3. Headers
                 if (showHeader)
                 {
                     // Create Header Row
                     var headerRow = new GameObject("HeaderRow");
                     var trans = headerRow.AddComponent<RectTransform>();

                     // Place header inside the scrollable content area
                     trans.SetParent(layer.list.transform.parent, false);
                     trans.SetSiblingIndex(layer.list.transform.GetSiblingIndex());

                     // Set height for LayoutElement reference
                     trans.sizeDelta = new Vector2(0, 24);

                     // Setup Layout
                     var hlg = headerRow.AddComponent<HorizontalLayoutGroup>();
                     hlg.childControlWidth = true;
                     hlg.childControlHeight = true;
                     hlg.childForceExpandWidth = false;
                     hlg.childForceExpandHeight = true;
                     hlg.spacing = 5;
                     hlg.padding = new RectOffset(5, 5, 5, 5);

                     // Height for Header
                     var le = headerRow.AddComponent<LayoutElement>();
                     le.minHeight = 24; // Compact
                     le.preferredHeight = 24;
                     le.flexibleHeight = 0;

                     // Create Header Cells
                     foreach(var col in columns) {
                         var cell = new GameObject("Header_" + col.Header);
                         cell.transform.SetParent(headerRow.transform, false);

                         var cellLe = cell.AddComponent<LayoutElement>();
                         cellLe.preferredWidth = col.Width;
                         cellLe.minWidth = col.Width;

                         // Add Text
                         var t = cell.AddComponent<Text>();
                          t.text = col.Header;
                          t.font = SkinManager.Instance.fontSet.ui.source.font;
                          Color hc = Color.black;
                          if (SkinManager.CurrentColors != null) hc = SkinManager.CurrentColors.textDefault;
                          t.color = hc;
                         t.fontStyle = FontStyle.Bold;
                         t.alignment = TextAnchor.MiddleLeft;
                         t.resizeTextForBestFit = true;
                         t.resizeTextMinSize = 8;
                         t.resizeTextMaxSize = 13;
                     }

                     // Background for Header
                     var img = headerRow.AddComponent<Image>();
                     img.color = new Color(0.9f, 0.9f, 0.9f, 0.5f);
                 }
             } else {
                 // Update persistent properties on refresh
                 layer.windows[0].SetCaption(caption);
             }

             // 4. Populate List
             layer.SetList2(data.ToList(),
                (t) => "", // Main Text (Unused)
                (t, b) => { // On Click
                    if (onSelectRow != null) {
                        onSelectRow(t);
                    }
                },
                (t, b) => { // On Instantiate / Bind
                    // b is ItemGeneral
                    b.SetMainText(""); // Clear default
                    b.DisableIcon();
                    b.refObj = t; // Fix for equipment comparison patch NRE

                    // Setup Horizontal Layout for the ROW
                    var hlg = b.GetComponent<HorizontalLayoutGroup>();
                    if(!hlg) {
                        hlg = b.gameObject.AddComponent<HorizontalLayoutGroup>();
                        hlg.childControlWidth = true;
                        hlg.childControlHeight = true;
                        hlg.childForceExpandWidth = false;
                        hlg.childForceExpandHeight = true;
                        hlg.spacing = 5;
                        hlg.padding = new RectOffset(5, 5, 2, 2);
                    }

                     // Set compact Row Height
                     // Remove ContentSizeFitter if it exists (conflicts with height control)
                    var csf = b.GetComponent<ContentSizeFitter>();
                    if (csf) UnityEngine.Object.DestroyImmediate(csf);

                    var le = b.GetComponent<LayoutElement>();
                    if (!le) le = b.gameObject.AddComponent<LayoutElement>();
                    le.minHeight = 24;
                    le.preferredHeight = 24;
                    le.flexibleHeight = 0;

                     // Destroy previous custom cells
                     var toDestroy = new List<GameObject>();
                     foreach(Transform child in b.transform) {
                         if (child.name.StartsWith("Cell_")) toDestroy.Add(child.gameObject);
                     }
                     foreach(var g in toDestroy) UnityEngine.Object.DestroyImmediate(g);

                     // --- Smart Hide & Button Setup ---
                     // Find the interactive button for this row
                     var btn = b.GetComponent<UIButton>() ?? b.GetComponentInChildren<UIButton>();
                     Graphic btnTarget = btn ? btn.targetGraphic : null;

                     if (btn) {
                        btn.enabled = true;
                        // Ensure the hit target (background) is visible
                        if (btnTarget) {
                            btnTarget.enabled = true;
                            btnTarget.gameObject.SetActive(true);
                        }

                        // If button is a child object, remove it from the HorizontalLayoutGroup flow
                        // and stretch it to cover the entire row area.
                        if (btn.gameObject != b.gameObject) {
                            var leBtn = btn.GetComponent<LayoutElement>();
                            if (!leBtn) leBtn = btn.gameObject.AddComponent<LayoutElement>();
                            leBtn.ignoreLayout = true;

                            var rtBtn = btn.transform as RectTransform;
                            if (rtBtn) {
                                rtBtn.anchorMin = Vector2.zero;
                                rtBtn.anchorMax = Vector2.one;
                                rtBtn.offsetMin = Vector2.zero;
                                rtBtn.offsetMax = Vector2.zero;
                            }
                        }
                     }

                     // Hide unrelated Texts
                     foreach(var txt in b.GetComponentsInChildren<Text>(true)) {
                         txt.enabled = false;
                     }

                     // Hide unrelated Images (icons etc), preserving the Button Target
                     foreach(var img in b.GetComponentsInChildren<Image>(true)) {
                         if (img.gameObject == b.gameObject) continue; // Keep root
                         if (btnTarget != null && img == btnTarget) continue; // Keep hit target
                         img.enabled = false;
                     }

                    // Create Cells
                    int i = 0;
                    foreach(var col in columns) {
                        var cell = new GameObject("Cell_" + i);
                        cell.transform.SetParent(b.transform, false);

                        var cellLe = cell.AddComponent<LayoutElement>();
                        cellLe.preferredWidth = col.Width;
                        cellLe.minWidth = col.Width;
                        cellLe.flexibleWidth = 0;

                        // Execute Binder
                        col.Binder(t, cell);

                        i++;
                    }
                },
                false // highlight
             );

             return layer;
        }

        public void Refresh()
        {
            Show();
        }
    }
}
