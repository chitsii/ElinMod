using HarmonyLib;

namespace Elin_LogRefined
{
    [HarmonyPatch(typeof(Chara))]
    public class PatchChara
    {
        [HarmonyPatch("AddCondition", typeof(Condition), typeof(bool))]
        [HarmonyPostfix]
        public static void AddCondition_Postfix(Chara __instance, Condition __result)
        {
            if (!ModConfig.EnableMod.Value || !ModConfig.ShowConditionLog.Value)
            {
                return;
            }

            if (__result == null)
            {
                // Condition was not added (e.g., resisted, nullified)
                return;
            }

            bool isRelatedToPC = __instance.IsPC || __instance.IsPCFaction || EClass.pc.CanSee(__instance);
            if (!isRelatedToPC)
            {
                return;
            }

            string detail = "";

            // Checks for conditions with elements (ConBuffStats, ConHero, etc.)
            if (__result.elements != null && __result.elements.dict != null && __result.elements.dict.Count > 0)
            {
                System.Text.StringBuilder sb = new System.Text.StringBuilder();
                bool first = true;
                foreach (var kvp in __result.elements.dict)
                {
                    int eleId = kvp.Key;
                    int val = kvp.Value.Value;
                    if (val == 0) continue;

                    if (!first) sb.Append(", ");

                    // Get element name
                    string statName = EClass.sources.elements.map[eleId].GetName();
                    string sign = val >= 0 ? "+" : "";

                    sb.Append($"{statName} {sign}{RefinedLogUtil.FormatNumber(val)}");
                    first = false;
                }
                detail = sb.ToString();
            }

            // Fallback for ConBuffStats if dict was empty but CalcValue works (shouldn't happen if initialized correctly, but safety)
            if (string.IsNullOrEmpty(detail) && __result is ConBuffStats buffStats)
            {
                int val = buffStats.CalcValue();
                if (buffStats.isDebuff) val = -val; // Apply negative sign for debuffs as CalcValue returns magnitude

                if (val != 0)
                {
                    string sign = val >= 0 ? "+" : "";
                    string statName = EClass.sources.elements.map[buffStats.refVal].GetName();
                    detail = $"{statName} {sign}{RefinedLogUtil.FormatNumber(val)}";
                }
            }

            // Ultimate fallback to condition name
            if (string.IsNullOrEmpty(detail))
            {
                detail = __result.Name;
            }
            else
            {
                // Prepend name if we have details? e.g. "Hero : STR+10"
                detail = $"{__result.Name} : {detail}";
            }

            // Determine color based on Buff/Debuff
            // Use Msg.colors fields
            if (__result.Type == ConditionType.Debuff)
            {
                Msg.SetColor(Msg.colors.Negative);
            }
            else
            {
                Msg.SetColor(Msg.colors.MutateGood);
            }

            Msg.SayRaw($"( {detail} ) ");

            // Apply commentary for Debuffs if enabled
            if (ModConfig.EnableCommentary.Value && __result.Type == ConditionType.Debuff)
            {
                Msg.SetColor(Msg.colors.Talk);
                string comment = CommentaryData.GetRandomDebuff();
                Msg.SayRaw("「" + comment + "」");
            }
        }
    }
}
