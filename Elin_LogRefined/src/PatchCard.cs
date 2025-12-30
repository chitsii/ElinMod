using HarmonyLib;
using UnityEngine;
using System;

namespace Elin_LogRefined
{
    [HarmonyPatch(typeof(Card))]
    public class PatchCard
    {
        [HarmonyPatch("DamageHP", new Type[] { typeof(long), typeof(int), typeof(int), typeof(AttackSource), typeof(Card), typeof(bool), typeof(Thing), typeof(Chara) })]
        [HarmonyPrefix]
        public static void DamageHP_Prefix(Card __instance, out int __state)
        {
            __state = __instance.hp;
        }

        [HarmonyPatch("DamageHP", new Type[] { typeof(long), typeof(int), typeof(int), typeof(AttackSource), typeof(Card), typeof(bool), typeof(Thing), typeof(Chara) })]
        [HarmonyPostfix]
        public static void DamageHP_Postfix(Card __instance, int __state)
        {
            if (!ModConfig.EnableMod.Value || !ModConfig.ShowDamageLog.Value)
            {
                return;
            }

            int damage = __state - __instance.hp;
            if (damage <= 0)
            {
                return;
            }

            bool isRelatedToPC = __instance.IsPC || __instance.IsPCFaction || EClass.pc.CanSee(__instance);

            if (isRelatedToPC)
            {
                EClass.core.actionsNextFrame.Add(() =>
                {
                    if (__instance == null) return;

                    Msg.SetColor(Msg.colors.Negative);
                    string text = $"( {RefinedLogUtil.FormatNumber(damage)} {RefinedLogUtil.GetText("damage")} ) ";
                    Msg.SayRaw(text);

                    if (ModConfig.EnableCommentary.Value)
                    {
                        Msg.SetColor(Msg.colors.Talk);
                        string comment = CommentaryData.GetRandomDamage();
                        Msg.SayRaw(comment + " ");
                    }
                });
            }
        }

        [HarmonyPatch("HealHP")]
        [HarmonyPrefix]
        public static void HealHP_Prefix(Card __instance, out int __state)
        {
            __state = __instance.hp;
        }

        [HarmonyPatch("HealHP")]
        [HarmonyPostfix]
        public static void HealHP_Postfix(Card __instance, int __state)
        {
            if (!ModConfig.EnableMod.Value || !ModConfig.ShowHealLog.Value)
            {
                return;
            }

            int healed = __instance.hp - __state;
            if (healed <= 0)
            {
                return;
            }

            bool isRelatedToPC = __instance.IsPC || __instance.IsPCFaction || EClass.pc.CanSee(__instance);

            if (isRelatedToPC)
            {
                Msg.SetColor(Msg.colors.MutateGood);
                string text = $"( {RefinedLogUtil.FormatNumber(healed)} {RefinedLogUtil.GetText("heal")} ) ";
                Msg.SayRaw(text);

                if (ModConfig.EnableCommentary.Value)
                {
                    Msg.SetColor(Msg.colors.Talk);
                    string comment = CommentaryData.GetRandomHeal();
                    Msg.SayRaw(comment + " ");
                }
            }
        }
    }
}
