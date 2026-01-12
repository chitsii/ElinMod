using HarmonyLib;
using UnityEngine;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// 虚飾の黄金鎧 - HPダメージの代わりに所持金を消費
    /// </summary>
    public class TraitSukutsuGildedArmor : Trait
    {
        /// <summary>
        /// 所持金1枚あたりの吸収HP
        /// </summary>
        public const int GoldPerHp = 10;

        /// <summary>
        /// キャラクターが虚飾の黄金鎧を装備しているか確認
        /// </summary>
        public static bool IsWearingGildedArmor(Chara c)
        {
            if (c == null || c.body == null) return false;

            foreach (var slot in c.body.slots)
            {
                if (slot.thing != null && slot.thing.id == "sukutsu_gilded_armor")
                {
                    return true;
                }
            }
            return false;
        }

        /// <summary>
        /// 所持金からダメージを吸収し、吸収できた量を返す
        /// </summary>
        public static long AbsorbDamageWithGold(Chara c, long damage)
        {
            if (!c.IsPC) return 0; // PCのみ適用

            // Card.GetCurrency を使用して所持金を取得
            int currentGold = c.GetCurrency("money");
            if (currentGold <= 0) return 0;

            // 吸収可能な最大ダメージ（所持金 ÷ GoldPerHp）
            long maxAbsorb = currentGold / GoldPerHp;
            long actualAbsorb = System.Math.Min(damage, maxAbsorb);

            if (actualAbsorb > 0)
            {
                // 所持金を消費（Card.ModCurrency を使用）
                int goldCost = (int)(actualAbsorb * GoldPerHp);
                c.ModCurrency(-goldCost, "money");

                // 金貨が剥がれ落ちる演出
                c.PlaySound("pay");
                c.PlayEffect("sparkle");

                Debug.Log($"[SukutsuArena] Gilded Armor absorbed {actualAbsorb} damage, cost {goldCost} gold");
            }

            return actualAbsorb;
        }
    }

    /// <summary>
    /// Card.DamageHP のパッチ - 虚飾の黄金鎧の効果を適用
    /// </summary>
    [HarmonyPatch(typeof(Card), nameof(Card.DamageHP), new[] { typeof(long), typeof(int), typeof(int), typeof(AttackSource), typeof(Card), typeof(bool), typeof(Thing), typeof(Chara) })]
    public static class Patch_Card_DamageHP_GildedArmor
    {
        /// <summary>
        /// ダメージ計算前に所持金で吸収
        /// </summary>
        static void Prefix(Card __instance, ref long dmg, int ele, int eleP, AttackSource attackSource)
        {
            // キャラクターでない場合はスキップ
            if (!__instance.isChara) return;

            Chara c = __instance.Chara;
            if (c == null || !c.IsPC) return;

            // 虚飾の黄金鎧を装備しているか確認
            if (!TraitSukutsuGildedArmor.IsWearingGildedArmor(c)) return;

            // 物理ダメージのみ適用（ele == 0 は物理）
            // 元素ダメージ（火、冷気など）は吸収しない
            if (ele != 0) return;

            // 所持金でダメージを吸収
            long absorbed = TraitSukutsuGildedArmor.AbsorbDamageWithGold(c, dmg);
            if (absorbed > 0)
            {
                dmg -= absorbed;
                if (dmg < 0) dmg = 0;

                // メッセージ表示（頻繁すぎないように条件付き）
                if (absorbed >= 10)
                {
                    Msg.Say("sukutsu_gilded_absorb");
                }
            }
        }
    }
}
