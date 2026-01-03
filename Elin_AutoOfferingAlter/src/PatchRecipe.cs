using HarmonyLib;
using System.Collections.Generic;
using UnityEngine;

namespace Elin_AutoOfferingAlter
{
    [HarmonyPatch]
    public class PatchRecipe
    {
        // Patch SourceManager.Init to inject our custom item BEFORE the game builds recipes.
        // This allows the game to naturally discover the item and generate a valid recipe for it.
        [HarmonyPrefix]
        [HarmonyPatch(typeof(SourceManager), "Init")]
        public static void Prefix_SourceManager_Init(SourceManager __instance)
        {
            try
            {
                ModUtilRegister.RegisterFromBase(__instance.things, "chest6", Plugin.ID_OFFERING_BOX, row =>
                {
                    row.name_JP = "信仰の箱";
                    row.name = "Offering Box";
                    row.factory = new string[] { "self" };
                    row.recipeKey = new string[] { "*" };
                    row.detail_JP = "眠りにつくたび、中身を自動的に信仰する神へ捧げる不思議な箱。";
                    row.detail = "A mysterious box that automatically offers its contents to your god whenever you sleep.";
                });
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogError("Error in Prefix_SourceManager_Init: " + e.Message);
            }
        }

        // Keep the Craft patch to apply specific tags and names
        [HarmonyPostfix]
        [HarmonyPatch(typeof(Recipe), "Craft")]
        public static void Postfix_Craft(Recipe __instance, ref Thing __result)
        {
            if (__result == null) return;

            if (__instance.id == Plugin.ID_OFFERING_BOX)
            {
                __result.c_idDeity = Plugin.ID_OFFERING_BOX;
                __result.c_altName = "信仰の箱";
                if (ModConfig.EnableLog.Value) Plugin.Log.LogInfo("Crafted Offering Box!");
            }
        }
    }

    [HarmonyPatch(typeof(Player))]
    public class PatchPlayer
    {
        [HarmonyPostfix]
        [HarmonyPatch("OnLoad")]
        public static void Postfix_OnLoad(Player __instance)
        {
            ModUtilRegister.LearnRecipe(Plugin.ID_OFFERING_BOX);
        }

        [HarmonyPostfix]
        [HarmonyPatch("OnStartNewGame")]
        public static void Postfix_OnStartNewGame(Player __instance)
        {
            ModUtilRegister.LearnRecipe(Plugin.ID_OFFERING_BOX);
        }
    }
}
