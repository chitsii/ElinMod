using UnityEngine;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// 巣窟アリーナ専用カスタムアイテムTrait
    ///
    /// TraitDrinkを継承し、OnDrinkで代償付き効果を発動。
    /// trait列で "Elin_SukutsuArena.TraitSukutsuItem,効果ID" と指定して使用。
    /// </summary>
    public class TraitSukutsuItem : TraitDrink
    {
        /// <summary>
        /// 効果ID（item_definitions.py の EFFECT_DEFINITIONS キーに対応）
        /// trait列の2番目のパラメータで指定
        /// </summary>
        public string EffectId => GetParam(1) ?? "";

        /// <summary>
        /// 飲んだ時の処理
        /// </summary>
        public override void OnDrink(Chara c)
        {
            Debug.Log($"[SukutsuArena] TraitSukutsuItem.OnDrink: EffectId={EffectId}");

            switch (EffectId)
            {
                case "kiss_of_inferno":
                    ApplyKissOfInferno(c);
                    break;

                case "frost_ward":
                    ApplySingleResistance(c, 951, -15, "frost");  // resCold
                    break;

                case "mind_ward":
                    ApplySingleResistance(c, 953, -15, "mind");   // resDarkness
                    break;

                case "chaos_ward":
                    ApplySingleResistance(c, 959, -15, "chaos");  // resChaos
                    break;

                case "sound_ward":
                    ApplySingleResistance(c, 957, -15, "sound");  // resSound
                    break;

                case "impact_ward":
                    ApplySingleResistance(c, 965, -15, "impact"); // resImpact
                    break;

                case "bleed_ward":
                    ApplySingleResistance(c, 964, -15, "bleed");  // resCut
                    break;

                default:
                    Debug.LogWarning($"[SukutsuArena] Unknown effect ID: {EffectId}, falling back to base");
                    base.OnDrink(c);
                    break;
            }
        }

        /// <summary>
        /// 業火の接吻効果
        /// - 複数耐性バフ（一時的、10000ターン）
        /// - カルマ-30
        /// </summary>
        private void ApplyKissOfInferno(Chara c)
        {
            // 効果メッセージ・演出
            c.Say("drink_cursed", c, owner);
            c.PlaySound("curse");
            c.PlayEffect("curse");

            // バフ持続時間（10000ターン相当のpower）
            // ConBuffStats.EvaluateTurn: return base.EvaluateTurn(p) * 100 / 100
            // Condition.EvaluateTurn: return 5 + (int)Mathf.Sqrt(p)
            // 10000ターン → p = (10000 - 5)^2 = 99,900,025 → 約1億
            // 実用的には power = 100000000 で十分長い
            int buffPower = 100000000;

            // 付与する耐性リスト
            int[] resistanceIds = new int[]
            {
                951,  // resCold (冷気)
                953,  // resDarkness (幻惑)
                959,  // resChaos (混沌)
                957,  // resSound (轟音)
                965,  // resImpact (衝撃)
                964,  // resCut (出血)
            };

            foreach (int elementId in resistanceIds)
            {
                c.AddCondition(Condition.Create(buffPower, delegate (ConBuffStats con)
                {
                    // refVal = element ID, refVal2 = 0 (バフ、222だとデバフ)
                    con.SetRefVal(elementId, 0);
                }));
            }

            Msg.Say("sukutsu_kiss_inferno", c);
            Debug.Log($"[SukutsuArena] Applied Kiss of Inferno buffs ({resistanceIds.Length} resistances) to {c.Name}");

            // カルマ減少（PCのみ）
            if (c.IsPC)
            {
                EClass.player.ModKarma(-30);
                Msg.Say("sukutsu_karma_cost");
            }
        }

        /// <summary>
        /// 単一耐性バフを付与
        /// </summary>
        private void ApplySingleResistance(Chara c, int elementId, int karmaChange, string effectName)
        {
            // 演出
            c.PlaySound("buff");
            c.PlayEffect("buff");

            // バフ持続時間（10000ターン相当）
            int buffPower = 100000000;

            c.AddCondition(Condition.Create(buffPower, delegate (ConBuffStats con)
            {
                con.SetRefVal(elementId, 0);
            }));

            Msg.Say($"sukutsu_{effectName}_ward_effect", c);
            Debug.Log($"[SukutsuArena] Applied {effectName} ward (element {elementId}) to {c.Name}");

            // カルマ減少（PCのみ）
            if (c.IsPC && karmaChange != 0)
            {
                EClass.player.ModKarma(karmaChange);
                Msg.Say("sukutsu_karma_cost_minor");
            }
        }

        /// <summary>
        /// バフ値の計算（ConBuffStats.CalcValue を参考）
        /// </summary>
        private int GetBuffValue(int power)
        {
            // ConBuffStats.CalcValue: return (int)Mathf.Max(5f, Mathf.Sqrt(base.power) * 2f - 15f);
            return (int)Mathf.Max(5f, Mathf.Sqrt(power) * 2f - 15f);
        }
    }
}
