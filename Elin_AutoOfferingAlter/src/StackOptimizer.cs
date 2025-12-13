using System;
using UnityEngine;

namespace Elin_AutoOfferingAlter
{
    public static class StackOptimizer
    {
        // Executes the offering process for a stack of items, splitting them optimally.
        // onOffer: Callback function that takes the (possibly split) item and performs the offering.
        public static void OptimizeAndOffer(Thing t, Religion faith, Action<Thing> onOffer)
        {
            if (t.Num <= 1)
            {
                onOffer(t);
                return;
            }

            // Calculate value of a single unit
            int unitVal = faith.GetOfferingValue(t, 1);
            if (unitVal <= 0)
            {
                // No value, just offer all
                onOffer(t);
                return;
            }

            // Determine optimal batch size (target >= 1500)
            // User rules:
            // - Limit per offering "time" (batch) is 3000.
            // - "1500" is the sweet spot (1 Faith point).
            // - "1400 is lossy".
            // - Prefer slightly over 1500 if exact 1500 isn't possible (e.g. 1600).
            // - Unit val is clamped to 1000 max.

            int targetVal = 1500;
            int maxVal = 3000;

            int batchSize = 1;

            // Logically find smallest N where N * unitVal >= 1500
            // N = Ceil(1500 / unitVal)
            batchSize = (targetVal + unitVal - 1) / unitVal;

            // Ensure we don't exceed maxVal if possible (though with unitVal<=1000, 2 units is 2000 <= 3000, so mostly safe)
            // If unitVal is somehow > 1500 (e.g. special multiplier?), then batchSize would be 1.
            if (batchSize * unitVal > maxVal)
            {
                // If the single unit is huge (shouldn't happen with 1000 cap), or calc is weird.
                // Fallback to ensuring < 3000
                batchSize = Math.Max(1, maxVal / unitVal);
            }

            // Strategy: "Digest remainder first"
            // total items = t.Num
            // remainder = t.Num % batchSize

            int remainder = t.Num % batchSize;

            if (ModConfig.EnableLog.Value)
            {
                Plugin.Log.LogInfo(string.Format("Optimizer: Item={0}, UnitVal={1}, BatchSize={2}, Qty={3}, Remainder={4}",
                    t.Name, unitVal, batchSize, t.Num, remainder));
            }

            // 1. Offer Remainder
            if (remainder > 0)
            {
                // If the stack is just the remainder (remainder == t.Num), we just offer it.
                // But since we are inside t.Num (loop), we split off the remainder.
                if (remainder < t.Num)
                {
                   Thing splitThing = t.Split(remainder);
                   onOffer(splitThing);
                }
                else
                {
                   // Entire stack is remainder (less than 1 batch)
                   onOffer(t);
                   return;
                }
            }

            // 2. Offer Batches
            // t now contains a multiple of batchSize
            while (t.Num > 0)
            {
                if (t.Num > batchSize)
                {
                    Thing splitThing = t.Split(batchSize);
                    onOffer(splitThing);
                }
                else
                {
                    // Last batch (should be equal to batchSize)
                    onOffer(t);
                    break;
                }
            }
        }
    }
}
