using HarmonyLib;

namespace Elin_AutoOfferingAlter
{
    [HarmonyPatch(typeof(ConSleep))]
    public class PatchConSleep
    {
        [HarmonyPostfix]
        [HarmonyPatch("OnRemoved")]
        public static void Postfix_OnRemoved(ConSleep __instance)
        {
            if (__instance.owner.IsPC && __instance.slept)
            {
                if (ModConfig.EnableLog.Value)
                {
                    Plugin.Log.LogInfo("[Elin_AutoOfferingAlter] Woke up. Checking for offerings...");
                }

                int processedCount = 0;

                // 1. Check Player Inventory
                foreach (Thing t in EClass.pc.things)
                {
                    if (t.id == Plugin.ID_OFFERING_BOX && t.IsContainer)
                    {
                         OfferLogic.Process(t);
                         processedCount++;
                    }
                }

                if (ModConfig.EnableLog.Value && processedCount > 0)
                {
                    Plugin.Log.LogInfo("[Elin_AutoOfferingAlter] Processed " + processedCount + " offering boxes.");
                }
            }
        }
    }
}
