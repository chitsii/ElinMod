using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Linq;

namespace Elin_ItemRelocator {
    // Helper component to make sidebar follow main window
    public class RelocatorSidebarSync : MonoBehaviour {
        public RectTransform target;
        public RectTransform sidebar;
        public Vector2 offset;

        private void LateUpdate() {
            if (target == null || sidebar == null)
                return;
            sidebar.anchoredPosition = target.anchoredPosition + offset;
        }
    }
    public class LayerItemRelocator : ELayer {
        // Wrappers Moved to UI/FilterNode.cs
        // FilterNode and ConditionType are now external

        // ====================================================================
        // Fields
        // ====================================================================
        private static RelocatorTable<Thing> previewTable;
        private static RelocatorAccordion<FilterNode> mainAccordion;
        private static RelocatorSidebar presetSidebar;
        private static Thing currentContainer;

        // ====================================================================
        // Main Entry Point
        // ====================================================================
        public static void Open(Thing container) {
            currentContainer = container;

            // Setup Accordion Logic FIRST
            mainAccordion = RelocatorAccordion<FilterNode>.Create();
            var profile = RelocatorManager.Instance.GetProfile(container);

            // UX: Default Empty Rule for new/empty profiles
            if (profile.Rules.Count == 0) {
                profile.Rules.Add(new RelocationRule { Name = RelocatorLang.GetText(RelocatorLang.LangKey.NewRuleName) + " 1" });
            }

            Action refresh = null;
            // Define Refresh Logic
            refresh = () => {
                // Rebuild Data
                List<FilterNode> roots = new List<FilterNode>();


                if (profile.Rules is not null) {
                    foreach (var r in profile.Rules) {
                        FilterNode node = new() { Rule = r, CondType = ConditionType.None };
                        roots.Add(node);
                        // Default Open: Ensure rule is expanded regardless of state
                        // But we want persistence. Since we override Equals based on Rule,
                        // previously expanded rules remain expanded.
                        // But for FIRST load or New Rule, we should expand it.
                        // 'Expand' method relies on 'Equals'.
                        // If we call Expand(node) it will add it to the set.
                        // Persistence is handled by SetRoots not clearing 'expanded'.
                        // WE WANT TO FORCE EXPAND ALWAYS according to user request?
                        // "Default to open" implies new ones open.
                        // User said: "Adding condition closes rule is bad". Override Equals fixes that.
                        // "Rule default open" -> Let's force expand all on refresh? No, that prevents closing.
                        // But for UX, let's Expand if not already tracked (aka new).
                        // However, since we recreate nodes, we can't easily distinguish 'new' from 'closed'.
                        // Use 'mainAccordion.Expand(node)' which checks 'contains'.
                        mainAccordion.Expand(node);
                    }
                }
                mainAccordion.SetRoots(roots);
                mainAccordion.Refresh();

                RefreshPreview(null, container, profile);
            };

            // Configure Accordion
            mainAccordion.SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Title));

            mainAccordion.SetOnBuildRow((trans, node) => {
                // Settings row logic removed
            });

            mainAccordion.SetChildren((node) => {
                if (node.IsRule) {
                    List<FilterNode> list = [];
                    var r = node.Rule;

                    // Deconstruct Rule into Nodes
                    if (r.CategoryIds.Count > 0) {
                        foreach (var id in r.CategoryIds) {
                            string name = id;
                            var source = EClass.sources.categories.map.TryGetValue(id);
                            if (source is not null)
                                name = source.GetName();
                            list.Add(new() { Rule = r, CondType = ConditionType.Category, CondValue = id, DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Category) + ": " + name });
                        }
                    }
                    if (r.Rarities is { Count: > 0 }) {
                        var qualityNames = Lang.GetList("quality");
                        List<string> display = [];
                        // Sort for nicer display
                        var sorted = r.Rarities.ToList();
                        sorted.Sort();
                        foreach (var rar in sorted) {
                            int idx = rar + 1;
                            if (idx >= 0 && idx < qualityNames.Length)
                                display.Add(qualityNames[idx]);
                            else
                                display.Add(rar.ToString());
                        }
                        list.Add(new() { Rule = r, CondType = ConditionType.Rarity, DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Rarity) + ": " + string.Join(", ", display.ToArray()) });
                    }
                    if (!string.IsNullOrEmpty(r.Quality)) {
                        list.Add(new() { Rule = r, CondType = ConditionType.Quality, DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Quality) + " " + r.Quality });
                    }
                    if (!string.IsNullOrEmpty(r.Text)) {
                        list.Add(new() { Rule = r, CondType = ConditionType.Text, DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Text) + ": " + r.Text });
                    }
                    if (r.Enchants != null && r.Enchants.Count > 0) {
                        foreach (var e in r.Enchants) {
                            list.Add(new() { Rule = r, CondType = ConditionType.Enchant, CondValue = e, DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Enchant) + ": " + e });
                        }
                    }
                    if (r.Weight.HasValue) {
                        list.Add(new() { Rule = r, CondType = ConditionType.Weight, CondValue = r.Weight.Value.ToString(), DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Weight) + " " + (string.IsNullOrEmpty(r.WeightOp) ? ">=" : r.WeightOp) + " " + r.Weight });
                    }

                    // ADD BUTTON
                    // Material
                    if (r.MaterialIds is { Count: > 0 }) {
                        string prefix = r.NotMaterial ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                        HashSet<string> allMats = r.MaterialIds;
                        string displayMat = "";
                        if (allMats.Count <= 3) {
                            List<string> names = [];
                            foreach (var mid in allMats) {
                                var ms = EClass.sources.materials.rows.FirstOrDefault(m => m.alias.Equals(mid, StringComparison.OrdinalIgnoreCase) || m.id.ToString() == mid);
                                names.Add(ms is not null ? ms.GetName() : mid);
                            }
                            displayMat = string.Join(", ", names.ToArray());
                        } else {
                            displayMat = "(" + allMats.Count + ")";
                        }
                        list.Add(new() { Rule = r, CondType = ConditionType.Material, CondValue = "Multi", DisplayText = prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Material) + ": " + displayMat });
                    }

                    // Bless
                    if (r.BlessStates is { Count: > 0 }) {
                        string prefix = r.NotBless ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                        HashSet<int> allStates = r.BlessStates;

                        List<string> names = [];
                        foreach (var b in allStates) {
                            if (b == 1)
                                names.Add(RelocatorLang.GetText(RelocatorLang.LangKey.StateBlessed));
                            else if (b == -1)
                                names.Add(RelocatorLang.GetText(RelocatorLang.LangKey.StateCursed));
                            else if (b == 0)
                                names.Add(RelocatorLang.GetText(RelocatorLang.LangKey.StateNormal));
                            else
                                names.Add(RelocatorLang.GetText(RelocatorLang.LangKey.StateDoomed));
                        }
                        list.Add(new() { Rule = r, CondType = ConditionType.Bless, DisplayText = prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Bless) + ": " + string.Join(", ", names.ToArray()) });
                    }

                    // Stolen
                    if (r.IsStolen.HasValue) {
                        string prefix = r.NotStolen ? RelocatorLang.GetText(RelocatorLang.LangKey.Not) + " " : "";
                        list.Add(new() { Rule = r, CondType = ConditionType.Stolen, DisplayText = prefix + RelocatorLang.GetText(RelocatorLang.LangKey.Stolen) + ": " + (r.IsStolen.Value ? "Yes" : "No") });
                    }

                    // Identified
                    if (r.IsIdentified.HasValue) {
                        string val = r.IsIdentified.Value
                            ? RelocatorLang.GetText(RelocatorLang.LangKey.StateIdentified)
                            : RelocatorLang.GetText(RelocatorLang.LangKey.StateUnidentified);
                        list.Add(new() { Rule = r, CondType = ConditionType.Identified, DisplayText = RelocatorLang.GetText(RelocatorLang.LangKey.Identified) + ": " + val });
                    }

                    // ADD BUTTON
                    list.Add(new() { Rule = r, CondType = ConditionType.AddButton, DisplayText = " + " });

                    return list;
                }
                return null;
            });

            mainAccordion.SetText((node) => {
                if (node.IsRule) {
                    string status = node.Rule.Enabled ? "" : " (Disabled)";
                    return node.Rule.Name + " (" + node.Rule.GetConditionList().Count + ")" + status;
                }
                return node.DisplayText;
            });

            mainAccordion.SetGetBackgroundColor((node) => {
                if (node.IsRule) {
                    return new(0.85f, 0.82f, 0.75f, 1f);
                }
                if (node.IsAddButton) {
                    return Color.clear;
                }
                return Color.clear;
            });

            mainAccordion.SetOnSelect((node) => {
                if (node.IsAddButton) {
                    RuleEditor.ShowAddConditionMenu(node.Rule, refresh);
                } else if (node.IsCondition) {
                    RuleEditor.EditRuleCondition(node, refresh);
                }
            });

            mainAccordion.SetOnRightClick((node) => {
                if (node.IsRule) {
                    var menu = RelocatorMenu.Create();
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Rename), () => {
                        Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.NewRuleName), node.Rule.Name, (c, text) => {
                            if (!c && !string.IsNullOrEmpty(text)) { node.Rule.Name = text; refresh(); }
                        }, (Dialog.InputType)0);
                    })
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Remove), () => {
                            Dialog.YesNo(RelocatorLang.GetText(RelocatorLang.LangKey.Delete) + "?", () => { profile.Rules.Remove(node.Rule); refresh(); });
                        })
                        .AddButton(node.Rule.Enabled ? RelocatorLang.GetText(RelocatorLang.LangKey.Disable) : RelocatorLang.GetText(RelocatorLang.LangKey.Enable), () => { node.Rule.Enabled = !node.Rule.Enabled; refresh(); })
                        .Show();
                }
            });



            mainAccordion.SetOnBuildRowExtra((node, rowGO) => {
                if (node.IsCondition) {
                    // Negation Button
                    bool isNegated = false;
                    Action toggleNegation = null;

                    switch (node.CondType) {
                    case ConditionType.Category:
                        isNegated = node.Rule.NegatedCategoryIds is not null && node.Rule.NegatedCategoryIds.Contains(node.CondValue);
                        toggleNegation = () => {
                            if (node.Rule.NegatedCategoryIds is null)
                                node.Rule.NegatedCategoryIds = [];
                            if (node.Rule.NegatedCategoryIds.Contains(node.CondValue))
                                node.Rule.NegatedCategoryIds.Remove(node.CondValue);
                            else
                                node.Rule.NegatedCategoryIds.Add(node.CondValue);
                            refresh();
                        };
                        break;

                    case ConditionType.Quality:
                        isNegated = node.Rule.NotQuality;
                        toggleNegation = () => { node.Rule.NotQuality = !node.Rule.NotQuality; refresh(); };
                        break;
                    case ConditionType.Text:
                        isNegated = node.Rule.NotText;
                        toggleNegation = () => { node.Rule.NotText = !node.Rule.NotText; refresh(); };
                        break;
                    case ConditionType.Weight:
                        isNegated = node.Rule.NotWeight;
                        toggleNegation = () => { node.Rule.NotWeight = !node.Rule.NotWeight; refresh(); };
                        break;
                    }

                    if (toggleNegation != null) {
                        var btnNeg = CreateTinyButton(rowGO.transform, RelocatorLang.GetText(RelocatorLang.LangKey.Not), toggleNegation);
                        var txtNeg = btnNeg.GetComponentInChildren<Text>();
                        var imgNeg = btnNeg.GetComponent<Image>();
                        if (isNegated) {
                            if (txtNeg)
                                txtNeg.color = Color.red; /*Red for Negated*/
                            if (imgNeg)
                                imgNeg.color = new Color(1f, 0.8f, 0.8f);
                        } else {
                            if (txtNeg)
                                txtNeg.color = SkinManager.CurrentColors.textDefault;
                            if (imgNeg)
                                imgNeg.color = new Color(0.9f, 0.9f, 0.9f);
                        }
                    }

                    // Remove Button (Updated Signature)
                    var btnRemove = CreateTinyButton(rowGO.transform, "x", () => {
                        Dialog.YesNo(RelocatorLang.GetText(RelocatorLang.LangKey.Delete) + "?", () => {
                            switch (node.CondType) {
                            case ConditionType.Category:
                                node.Rule.CategoryIds.Remove(node.CondValue);
                                break;
                            case ConditionType.Rarity:
                                node.Rule.Rarities = [];
                                break;
                            case ConditionType.Quality:
                                node.Rule.Quality = null;
                                break;
                            case ConditionType.Text:
                                node.Rule.Text = null;
                                break;
                            case ConditionType.Enchant:
                                node.Rule.Enchants.Remove(node.CondValue);
                                break;
                            case ConditionType.Weight:
                                node.Rule.Weight = null;
                                break;
                            case ConditionType.Material:
                                node.Rule.MaterialIds = null;
                                break;
                            case ConditionType.Bless:
                                node.Rule.BlessStates = null;
                                break;
                            case ConditionType.Stolen:
                                node.Rule.IsStolen = null;
                                break;
                            }
                            refresh();
                        });
                    });
                }
            });

            // 1. Setup Sidebar
            presetSidebar = RelocatorSidebar.Create()
                .SetCaption(RelocatorLang.GetText(RelocatorLang.LangKey.Presets))
                .SetOnSelect((name) => {
                    var loaded = RelocatorManager.Instance.LoadPreset(name);
                    if (loaded is not null) {
                        profile.Rules = loaded.Rules;
                        profile.Scope = loaded.Scope;
                        profile.ExcludeHotbar = loaded.ExcludeHotbar;
                        profile.SortMode = loaded.SortMode;
                        refresh();
                        Msg.Say(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Loaded));
                    }
                })
                .SetOnRightClick((name) => {
                    RelocatorMenu.Create()
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Rename), () => {
                            Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_RenamePrompt), name, (c, text) => {
                                if (!c && !string.IsNullOrEmpty(text)) {
                                    RelocatorManager.Instance.RenamePreset(name, text);
                                    refresh();
                                }
                            }, (Dialog.InputType)0);
                        })
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Delete), () => {
                            Dialog.YesNo(RelocatorLang.GetText(RelocatorLang.LangKey.Delete) + "?", () => {
                                RelocatorManager.Instance.DeletePreset(name);
                                refresh();
                            });
                        })
                        .Show();
                })
                .SetOnAdd(() => {
                    Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.PresetName), "", (c, text) => {
                        if (!c && !string.IsNullOrEmpty(text)) {
                            RelocatorManager.Instance.SavePreset(text, profile);
                            refresh();
                        }
                    }, (Dialog.InputType)0);
                });

            // 2. Setup Preview Table
            previewTable = RelocatorTable<Thing>.Create()
                .SetShowHeader(true)
                .SetPreferredHeight(800)
                .SetOnSelect((t) => {
                    var menu = RelocatorMenu.Create();
                    menu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Move), () => {
                        if (currentContainer is not null) {
                            RelocatorManager.Instance.RelocateSingleThing(t, currentContainer);
                            if (previewTable is not null)
                                previewTable.Refresh();
                        }
                    });
                    menu.Show();
                })
                .AddColumn(RelocatorLang.GetText(RelocatorLang.LangKey.Text), 350, (t, cell) => {
                    var txt = cell.GetComponentInChildren<Text>();
                    if (!txt) {
                        GameObject g = new("Text");
                        g.transform.SetParent(cell.transform, false);
                        txt = g.AddComponent<Text>();
                        txt.font = SkinManager.Instance.fontSet.ui.source.font;
                        txt.color = SkinManager.CurrentColors.textDefault;
                        txt.alignment = TextAnchor.MiddleLeft;
                        txt.resizeTextForBestFit = true;
                        txt.resizeTextMinSize = 10;
                        txt.resizeTextMaxSize = 13;
                        txt.horizontalOverflow = HorizontalWrapMode.Wrap;
                        txt.verticalOverflow = VerticalWrapMode.Truncate;
                        txt.raycastTarget = false;
                        var rt = txt.rectTransform;
                        rt.anchorMin = Vector2.zero;
                        rt.anchorMax = Vector2.one;
                        rt.sizeDelta = Vector2.zero;
                    }
                    txt.text = t?.Name ?? "";
                    var rowBtn = cell.transform.parent.GetComponentInChildren<UIButton>();
                    if (rowBtn) {
                        var field = typeof(UIButton).GetField("tooltip", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic);
                        if (field != null)
                            field.SetValue(rowBtn, null);
                        rowBtn.SetTooltip((tooltip) => {
                            if (t is not null && tooltip.note is not null)
                                t.WriteNote(tooltip.note);
                        }, true);
                    }
                })
                .AddTextColumn(RelocatorLang.GetText(RelocatorLang.LangKey.Category), 100, t => t is { category: not null } ? t.category.GetName() : "")
                .AddTextColumn(RelocatorLang.GetText(RelocatorLang.LangKey.Parent), 100, t => {
                    if (t is null || t.parent is null)
                        return "";
                    if (t.parent == EClass.pc.things)
                        return RelocatorLang.GetText(RelocatorLang.LangKey.Inventory);
                    if (t.parent == EClass._map.things)
                        return RelocatorLang.GetText(RelocatorLang.LangKey.Zone);
                    return t.parent is Card c ? c.Name : t.parent.ToString();
                })
                .AddTextColumn(RelocatorLang.GetText(RelocatorLang.LangKey.Details), 250, t => {
                    if (t == null)
                        return "";

                    // Show value based on current sort mode
                    switch (profile.SortMode) {
                    case RelocationProfile.ResultSortMode.PriceAsc:
                    case RelocationProfile.ResultSortMode.PriceDesc:
                        // Price
                        return t.GetPrice().ToString() + " gp";

                    case RelocationProfile.ResultSortMode.TotalWeightAsc:
                    case RelocationProfile.ResultSortMode.TotalWeightDesc:
                        // Total Weight
                        return (t.ChildrenAndSelfWeight * t.Num * 0.001f).ToString("0.0") + "s";

                    case RelocationProfile.ResultSortMode.UnitWeightAsc:
                    case RelocationProfile.ResultSortMode.UnitWeightDesc:
                        // Unit Weight
                        return (t.SelfWeight * 0.001f).ToString("0.0") + "s";

                    case RelocationProfile.ResultSortMode.TotalEnchantMagDesc:
                        int totalMag = 0;
                        if (t.elements != null && t.elements.dict != null) {
                            foreach (var e in t.elements.dict.Values) {
                                if (e.Value > 0)
                                    totalMag += e.Value;
                            }
                        }
                        return "Total Mag: " + totalMag;

                    case RelocationProfile.ResultSortMode.EnchantMagAsc:
                    case RelocationProfile.ResultSortMode.EnchantMagDesc:
                        // Enchant Magnitude
                        List<int> targetEleIds = RelocatorManager.Instance.GetTargetEnchantIDs(profile);
                        int val = 0;
                        foreach (int id in targetEleIds) {
                            val += t.elements.Value(id);
                        }
                        return "Mag: " + val;

                    case RelocationProfile.ResultSortMode.UidAsc:
                    case RelocationProfile.ResultSortMode.UidDesc:
                        return "UID: " + t.uid;

                    default:
                        // Default View: Show simplified info (Weight + ID status)
                        string info = "";
                        if (t.SelfWeight > 0)
                            info += (t.SelfWeight * 0.001f).ToString("0.0") + "s ";
                        if (!t.IsIdentified)
                            info += "(UnID) ";
                        return info;
                    }
                });

            // Initialize Layers (Main and Preview)
            LayerList layerMain, layerPreview, layerSidebar;
            InitLayers(out layerMain, out layerPreview, out layerSidebar);

            // Refine refresh to update sidebar
            var oldRefresh = refresh;
            refresh = () => {
                oldRefresh();
                if (presetSidebar != null) {
                    presetSidebar.SetItems(RelocatorManager.Instance.GetPresetList());
                    presetSidebar.Refresh();
                }
            };

            // Restore Footer Buttons ("Settings", "Execute", "Add Rule")
            // "Add Rule" stays in Accordion? No, user said "Except Add Filter".
            // "Add Filter" is gone. We have "Add Rule".
            // Let's put ALL main actions in Footer for consistency.
            var win = layerMain.windows[0];
            win.AddBottomButton(RelocatorLang.GetText(RelocatorLang.LangKey.AddRule), () => {
                Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.NewRuleName), RelocatorLang.GetText(RelocatorLang.LangKey.NewRuleName), (c, text) => {
                    if (!c && !string.IsNullOrEmpty(text)) {
                        profile.Rules.Add(new() { Name = text });
                        refresh();
                    }
                }, (Dialog.InputType)0);
            });
            // Reset Button (Clear current rule conditions)
            win.AddBottomButton(RelocatorLang.GetText(RelocatorLang.LangKey.ResetRules), () => {
                Dialog.YesNo(RelocatorLang.GetText(RelocatorLang.LangKey.ResetRulesConfirm), () => {
                    // Logic: "Erase editing search rule/condition (Initialize All)"
                    // If this means "Reset Profile Rules to Empty", use:
                    // profile.Rules.Clear();
                    // But user said "editing...". If there's a selected rule, maybe just that one?
                    // "すべて初期化する" (Initialize All) usually implies a full reset of the current context.
                    // Given the "Relocator" context, I'll reset the entire profile rules list to be safe/thorough,
                    // OR just the conditions of the rules? No, deleting rules is "Reset".
                    // Actually, "Rules & Conditions".
                    // I will Clear profile.Rules.
                    profile.Rules.Clear();
                    refresh();
                    Msg.Say(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_RulesCleared));
                });
            });
            win.AddBottomButton(RelocatorLang.GetText(RelocatorLang.LangKey.Settings), () => ShowSettingsMenu(profile, refresh));
            win.AddBottomButton(RelocatorLang.GetText(RelocatorLang.LangKey.Execute), () => {
                RelocatorManager.Instance.ExecuteRelocation(container);
                Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Relocated), ""));
                if (mainAccordion != null)
                    mainAccordion.Close();
            });

            // Initial Data Load
            refresh();
        }

        // ====================================================================
        // Layer Initialization & Setup
        // ====================================================================
        private static void InitLayers(out LayerList main, out LayerList preview, out LayerList sidebar) {
            // 1. Create Main Layer via Accordion
            var _main = mainAccordion.Show();
            var winMain = _main.windows[0];

            // 2. Create Preview Layer (Table)
            var _preview = previewTable.Show();
            var winPreview = _preview.windows[0];

            // 3. Create Sidebar (Last = Topmost)
            var _sidebar = presetSidebar.Show();
            var winSidebar = _sidebar.windows[0];

            // Disable full-screen raycast blocking for all layers to allow clicking through to others
            DisableLayerBlocker(_main, winMain);
            DisableLayerBlocker(_preview, winPreview);
            DisableLayerBlocker(_sidebar, winSidebar);

            // =================================================================================
            // DYNAMIC LAYOUT CALCULATION (Center Group)
            // =================================================================================
            // Define Component Widths
            float widthSidebar = 200f; // Increased from 160f
            float widthMain = 580f;
            float widthPreview = 840f; // Increased to accommodate new columns (was 640f)
            float gap = 10f;

            // Calculate Total Width and Starting X for centering
            // Group: [Sidebar] [Gap] [Main] [Gap] [Preview]
            float totalWidth = widthSidebar + gap + widthMain + gap + widthPreview;
            float startX = -(totalWidth / 2f); // Left edge of the group

            // Calculate Center X for each component
            // 1. Sidebar Center: StartX + (W/2)
            float xSidebar = startX + (widthSidebar / 2f);

            // 2. Main Center: StartX + SidebarW + Gap + (W/2)
            float xMain = startX + widthSidebar + gap + (widthMain / 2f);

            // 3. Preview Center: StartX + SidebarW + Gap + MainW + Gap + (W/2)
            float xPreview = startX + widthSidebar + gap + widthMain + gap + (widthPreview / 2f);

            // Apply Widths to Components (via new APIs)
            presetSidebar.SetPreferredWidth(widthSidebar);
            // mainAccordion.SetPreferredWidth(widthMain); // Accordion relies on MainLayer setting size below
            previewTable.SetPreferredWidth(widthPreview);

            // Apply Sizes & Positions
            winMain.setting.allowResize = true;
            winPreview.setting.allowResize = true;

            _main.SetSize(widthMain, 800);

            var rectMain = winMain.GetComponent<RectTransform>();
            var rectPreview = winPreview.GetComponent<RectTransform>();
            var rectSidebar = winSidebar.GetComponent<RectTransform>();

            rectMain.anchoredPosition = new Vector2(xMain, 0);
            rectPreview.anchoredPosition = new Vector2(xPreview, 0);
            rectSidebar.anchoredPosition = new Vector2(xSidebar, 0);

            // Implementation of Sidebar Following Main Window
            var sync = _sidebar.gameObject.AddComponent<RelocatorSidebarSync>();
            sync.target = winMain.GetComponent<RectTransform>();
            sync.sidebar = winSidebar.GetComponent<RectTransform>();
            sync.offset = rectSidebar.anchoredPosition - rectMain.anchoredPosition;

            // Synced Closing Logic
            bool closing = false;
            OnKill(_main, () => {
                if (closing)
                    return;
                closing = true;
                if (mainAccordion != null)
                    mainAccordion.Close();
                if (_preview != null)
                    _preview.Close();
                if (_sidebar != null)
                    _sidebar.Close();
            });
            OnKill(_preview, () => {
                if (closing)
                    return;
                closing = true;
                if (_main != null)
                    _main.Close();
                if (_sidebar != null)
                    _sidebar.Close();
            });
            OnKill(_sidebar, () => {
                if (closing)
                    return;
                closing = true;
                if (_main != null)
                    _main.Close();
                if (_preview != null)
                    _preview.Close();
            });

            main = _main;
            preview = _preview;
            sidebar = _sidebar;
        }

        private static void DisableLayerBlocker(ELayer layer, Window win) {
            foreach (var g in layer.GetComponentsInChildren<Graphic>(true)) {
                if (g.transform.IsChildOf(win.transform) || g.gameObject == win.gameObject)
                    continue;
                g.raycastTarget = false;
            }
        }

        private static void OnKill(ELayer layer, Action action) {
            layer.onKill.AddListener(() => action());
        }

        public override void OnRightClick() {
            // This is actually not called since we use LayerList prefab
            // Handled via Harmony patch in Mod.cs
        }

        // ====================================================================
        // Refresh Logic
        // ====================================================================
        private static void RefreshPreview(LayerList layer, Thing container, RelocationProfile profile) {
            if (container == null)
                return;

            // Limit preview search to 2000
            List<Thing> matches = RelocatorManager.Instance.GetMatches(container, 2000).ToList();

            // Sorting is handled by Manager.GetMatches

            int count = matches.Count;
            string countStr = count >= 2000 ? "2000+" : count.ToString();

            if (previewTable != null) {
                string caption = RelocatorLang.GetText(RelocatorLang.LangKey.Preview) + " (" + countStr + ")";
                // Limit display to 200 items to avoid UI lag (Optimized: 100 -> 200)
                if (count > 200) {
                    caption += " [Display Limit: 200]";
                    previewTable.SetDataSource(matches.Take(200).ToList());
                } else {
                    previewTable.SetDataSource(matches);
                }
                previewTable.SetCaption(caption);
                previewTable.Refresh();
            }
        }

        private static void ShowSettingsMenu(RelocationProfile profile, Action refresh) {
            string currentScope = RelocatorLang.GetText(RelocatorLang.LangKey.Inventory); // Default
            if (profile.Scope == RelocationProfile.FilterScope.Both)
                currentScope = RelocatorLang.GetText(RelocatorLang.LangKey.ScopeBoth);
            else if (profile.Scope == RelocationProfile.FilterScope.ZoneOnly)
                currentScope = RelocatorLang.GetText(RelocatorLang.LangKey.Zone);

            RelocatorMenu.Create()
                .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.Scope) + ": " + currentScope, (child) => {
                    child
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Inventory), () => {
                             profile.Scope = RelocationProfile.FilterScope.Inventory;
                             refresh();
                         })
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Zone), () => { // Zone Only
                             profile.Scope = RelocationProfile.FilterScope.ZoneOnly;
                             refresh();
                         })
                         .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.ScopeBoth), () => { // Both
                             profile.Scope = RelocationProfile.FilterScope.Both;
                             refresh();
                         });
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
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortMagDesc), () => { profile.SortMode = RelocationProfile.ResultSortMode.EnchantMagDesc; refresh(); })
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortTotalEnchantMagDesc), () => { profile.SortMode = RelocationProfile.ResultSortMode.TotalEnchantMagDesc; refresh(); })
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortWeightAsc), () => { profile.SortMode = RelocationProfile.ResultSortMode.TotalWeightAsc; refresh(); })
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortWeightDesc), () => { profile.SortMode = RelocationProfile.ResultSortMode.TotalWeightDesc; refresh(); })
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortUnitWeightAsc), () => { profile.SortMode = RelocationProfile.ResultSortMode.UnitWeightAsc; refresh(); })
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortUnitWeightDesc), () => { profile.SortMode = RelocationProfile.ResultSortMode.UnitWeightDesc; refresh(); })
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortUidAsc), () => { profile.SortMode = RelocationProfile.ResultSortMode.UidAsc; refresh(); })
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SortUidDesc), () => { profile.SortMode = RelocationProfile.ResultSortMode.UidDesc; refresh(); });
                })
                .AddSeparator()
                .AddChild(RelocatorLang.GetText(RelocatorLang.LangKey.Presets), (child) => {
                    child
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.SavePreset), () => {
                            Dialog.InputName(RelocatorLang.GetText(RelocatorLang.LangKey.PresetName), "", (c, text) => {
                                if (!c && !string.IsNullOrEmpty(text)) {
                                    RelocatorManager.Instance.SavePreset(text, profile);
                                }
                            }, (Dialog.InputType)0);
                        })
                        .AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.LoadPreset), () => {
                            RelocatorPickers.ShowPresetPicker((name) => {
                                var loaded = RelocatorManager.Instance.LoadPreset(name);
                                if (loaded is not null) {
                                    profile.Rules = loaded.Rules;
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

        private static void ShowOperatorMenu(Action<string> onSelect) {
            var opMenu = RelocatorMenu.Create();
            string[] ops = [">=", "=", "<=", ">", "<", "!="];
            foreach (var op in ops) {
                opMenu.AddButton(RelocatorLang.GetText(RelocatorLang.LangKey.Operator) + ": " + op, () => onSelect(op));
            }
            opMenu.Show();
        }


        private static Button CreateTinyButton(Transform parent, string label, Action onClick) {
            var btnGO = new GameObject("Btn_" + label);
            btnGO.transform.SetParent(parent, false);
            var le = btnGO.AddComponent<LayoutElement>();
            le.minWidth = 24;
            le.preferredWidth = 24;
            le.minHeight = 24;
            le.preferredHeight = 24;

            var img = btnGO.AddComponent<Image>();
            img.color = new Color(0.8f, 0.8f, 0.8f);

            var btn = btnGO.AddComponent<Button>();
            btn.targetGraphic = img;
            btn.onClick.AddListener(() => onClick());

            var txtGO = new GameObject("Text");
            txtGO.transform.SetParent(btnGO.transform, false);
            var txt = txtGO.AddComponent<Text>();
            Font f = null;
            if (SkinManager.Instance is { fontSet.ui.source: not null }) {
                f = SkinManager.Instance.fontSet.ui.source.font;
            }
            if (f is null)
                f = UnityEngine.Resources.GetBuiltinResource<Font>("Arial.ttf"); // Fallback

            txt.font = f;
            txt.fontSize = 12;
            txt.text = label;
            txt.alignment = TextAnchor.MiddleCenter;

            Color c = Color.black;
            if (SkinManager.CurrentColors is not null)
                c = SkinManager.CurrentColors.textDefault;
            txt.color = c;
            txt.rectTransform.anchorMin = Vector2.zero;
            txt.rectTransform.anchorMax = Vector2.one;
            txt.rectTransform.sizeDelta = Vector2.zero;
            txt.rectTransform.offsetMin = Vector2.zero;
            txt.rectTransform.offsetMax = Vector2.zero;

            return btn;
        }



        private static string GetSortText(RelocationProfile.ResultSortMode mode) => mode switch {
            RelocationProfile.ResultSortMode.Default => RelocatorLang.GetText(RelocatorLang.LangKey.SortDefault),
            RelocationProfile.ResultSortMode.PriceAsc => RelocatorLang.GetText(RelocatorLang.LangKey.SortPriceAsc),
            RelocationProfile.ResultSortMode.PriceDesc => RelocatorLang.GetText(RelocatorLang.LangKey.SortPriceDesc),
            RelocationProfile.ResultSortMode.EnchantMagAsc => RelocatorLang.GetText(RelocatorLang.LangKey.SortMagAsc),
            RelocationProfile.ResultSortMode.EnchantMagDesc => RelocatorLang.GetText(RelocatorLang.LangKey.SortMagDesc),
            RelocationProfile.ResultSortMode.TotalEnchantMagDesc => RelocatorLang.GetText(RelocatorLang.LangKey.SortTotalEnchantMagDesc),
            RelocationProfile.ResultSortMode.TotalWeightAsc => RelocatorLang.GetText(RelocatorLang.LangKey.SortWeightAsc),
            RelocationProfile.ResultSortMode.TotalWeightDesc => RelocatorLang.GetText(RelocatorLang.LangKey.SortWeightDesc),
            RelocationProfile.ResultSortMode.UnitWeightAsc => RelocatorLang.GetText(RelocatorLang.LangKey.SortUnitWeightAsc),
            RelocationProfile.ResultSortMode.UnitWeightDesc => RelocatorLang.GetText(RelocatorLang.LangKey.SortUnitWeightDesc),
            RelocationProfile.ResultSortMode.UidAsc => RelocatorLang.GetText(RelocatorLang.LangKey.SortUidAsc),
            RelocationProfile.ResultSortMode.UidDesc => RelocatorLang.GetText(RelocatorLang.LangKey.SortUidDesc),
            _ => mode.ToString()
        };
    }
}
