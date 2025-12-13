using Newtonsoft.Json;
using System;
using System.Linq;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;
using UnityEngine.UI;

namespace Elin_ItemRelocator
{
    [BepInPlugin(ID, TITLE, VERSION)]
    public class Elin_ItemRelocator : BaseUnityPlugin
    {
        public const string ID = "Elin_ItemRelocator";
        public const string TITLE = "Item Relocator";
        public const string VERSION = "1.0.0";

        public static Elin_ItemRelocator Instance { get; private set; }
        internal new static ManualLogSource Logger;

        private void Awake()
        {
            Instance = this;
            Logger = base.Logger;
            var harmony = new Harmony(ID);
            harmony.PatchAll();
        }

        [HarmonyPatch(typeof(Game), "OnLoad")]
        class PatchGameLoad
        {
            static void Postfix()
            {
                RelocatorManager.Instance.Init();
            }
        }

        [HarmonyPatch(typeof(Game), "Save")]
        class PatchGameSave
        {
            static void Postfix()
            {
                RelocatorManager.Instance.Save();
            }
        }

        [HarmonyPatch(typeof(UIInventory), "RefreshMenu")]
        class PatchUIInventory
        {
            static void Postfix(UIInventory __instance)
            {
                if (__instance.window == null) return;

                // Allow injection on player containers too (IsPlayerContainer returns true for held chests)

                var owner = __instance.owner;
                if (owner == null) return;
                if (owner.Container == null) return;

                Thing containerThing = owner.Container.Thing;
                if (containerThing == null)
                {
                    // Skip Chara containers (main backpack)
                    if (owner.Container.isChara) return;
                    return;
                }

                if (!containerThing.trait.IsContainer) return;

                // Use buttonShared (Lock) as per user screenshot (Lock button exists)
                // If buttonShared is null, fallback to buttonSort
                UIButton anchorBtn = __instance.window.buttonShared;

                if (anchorBtn == null)
                {
                    anchorBtn = __instance.window.buttonSort;
                }

                if (anchorBtn == null) return;

                Transform parent = anchorBtn.transform.parent;
                Transform existing = parent.Find("ButtonRelocate");
                if (existing != null) return;

                UIButton btnRelocate = UnityEngine.Object.Instantiate(anchorBtn, parent);
                btnRelocate.gameObject.name = "ButtonRelocate";
                btnRelocate.transform.SetAsLastSibling();

                btnRelocate.onClick.RemoveAllListeners();
                btnRelocate.onClick.AddListener(() =>
                {
                    RelocatorUI.Open(containerThing);
                });

                // Customize Appearance
                if (btnRelocate.icon != null)
                {
                    btnRelocate.icon.color = new Color(0.6f, 0.5f, 1f); // Purple tint
                }

                if (btnRelocate.mainText != null)
                {
                   btnRelocate.mainText.SetActive(true);
                   btnRelocate.mainText.SetText(RelocatorUI.GetText(RelocatorUI.LangKey.Execute));
                }
                else
                {
                    // Fallback: Try to find text component
                    var t = btnRelocate.GetComponentInChildren<UIText>(true);
                    if (t != null)
                    {
                        t.SetActive(true);
                        t.SetText(RelocatorUI.GetText(RelocatorUI.LangKey.Execute));
                    }
                }

                // Set tooltip if possible (UIButton might have tooltip property or Component)
                // btnRelocate.Tooltip = RelocatorUI.GetText(RelocatorUI.LangKey.Title);

                btnRelocate.gameObject.SetActive(true);
                LayoutRebuilder.ForceRebuildLayoutImmediate(parent as RectTransform);
            }
        }
    }
}
