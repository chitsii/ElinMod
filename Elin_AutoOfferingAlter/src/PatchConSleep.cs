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

                // Scan inventory (excluding equipped items to avoid duplication)
                foreach (Thing t in EClass.pc.things)
                {
                    if (!t.isEquipped && t.id == Plugin.ID_OFFERING_BOX && t.IsContainer)
                    {
                        OfferLogic.Process(t);
                    }
                }

                // Scan body slots (for equipped Offering Boxes)
                foreach (BodySlot slot in EClass.pc.body.slots)
                {
                    if (slot.thing != null && slot.thing.id == Plugin.ID_OFFERING_BOX && slot.thing.IsContainer)
                    {
                        OfferLogic.Process(slot.thing);
                    }
                }
            }
        }
    }
}
