using System.Collections.Generic;
using UnityEngine;

namespace Elin_AutoOfferingAlter
{
    public static class OfferLogic
    {
        public static void Process(Thing container)
        {
            if (EClass.pc.faith == EClass.game.religions.Eyth)
            {
                // Eyth doesn't usually accept offerings in the same way, or it's complicated.
                // For safety and simplicity, skip if no faith (Eyth is default/no faith).
                // Or if user wants to support Eyth offering (e.g. specialized items),
                // TraitAltar might handle it, but typically it returns false for CanOffer.
                // Let's rely on TraitAltar.CanOffer.
            }

            // Create a dummy altar trait wrapper
            TraitAltar fakeAltar = new TraitAltar();
            fakeAltar.SetOwner(container);

            // Log if enabled
            if (ModConfig.EnableLog.Value)
            {
                Plugin.Log.LogInfo(string.Format("[Elin_AutoOfferingAlter] Processing container: {0} (UID:{1})", container.Name, container.uid));
            }

            // Iterate through items in the container.
            // MUST copy the list because OnOffer destroys items, modifying the collection during iteration.
            List<Thing> thingsToProcess = new List<Thing>();
            foreach (Thing t in container.things)
            {
                thingsToProcess.Add(t);
            }

            foreach (Thing t in thingsToProcess)
            {
                if (fakeAltar.CanOffer(t))
                {
                    // Prepare renaming once for this stack
                    string originalName = container.c_altName;

                    // Force the fake altar to have the player's faith as its deity
                    fakeAltar.SetDeity(EClass.pc.faith.id);

                    // Setup name for message
                    string godName = EClass.pc.faith.Name;

                    // Optimization: Rename container temporarily so messages say "You offer to [God]"
                    // We do this around the entire stack processing to avoid flickering/overhead.
                    container.c_altName = godName;

                    try
                    {
                        // Use Optimizer to handle stack splitting
                        StackOptimizer.OptimizeAndOffer(t, fakeAltar.Deity, (itemToOffer) =>
                        {
                            if (ModConfig.EnableLog.Value)
                            {
                                Plugin.Log.LogInfo(string.Format("[Elin_AutoOfferingAlter] Offering item: {0} (x{1})", itemToOffer.Name, itemToOffer.Num));
                            }
                            fakeAltar.OnOffer(EClass.pc, itemToOffer);
                        });
                    }
                    finally
                    {
                        // Restore name
                        container.c_altName = originalName;
                    }
                }
                else
                {
                     // Verbose log for debug
                     // if (ModConfig.EnableLog.Value) Plugin.Log.LogInfo(string.Format("Skipping {0}", t.Name));
                }
            }
        }
    }
}
