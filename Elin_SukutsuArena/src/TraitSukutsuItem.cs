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
        /// 親クラスの IdEffect をオーバーライド
        /// カスタム効果IDはバニラの EffectId 列挙型に存在しないため、
        /// デフォルト値を返して列挙型変換エラーを回避
        /// </summary>
        public override EffectId IdEffect => global::EffectId.Drink;

        /// <summary>
        /// 効果ID（item_definitions.py の EFFECT_DEFINITIONS キーに対応）
        /// trait列の2番目のパラメータで指定
        /// </summary>
        public string CustomEffectId => GetParam(1) ?? "";

        /// <summary>
        /// 飲んだ時の処理
        /// </summary>
        public override void OnDrink(Chara c)
        {
            Debug.Log($"[SukutsuArena] TraitSukutsuItem.OnDrink: CustomEffectId={CustomEffectId}");

            switch (CustomEffectId)
            {
                case "kiss_of_inferno":
                    ApplyKissOfInferno(c);
                    break;

                case "frost_ward":
                    ApplyConditionByAlias(c, "ConSukutsuResCold", -15);
                    break;

                case "mind_ward":
                    ApplyConditionByAlias(c, "ConSukutsuResDarkness", -15);
                    break;

                case "chaos_ward":
                    ApplyConditionByAlias(c, "ConSukutsuResChaos", -15);
                    break;

                case "sound_ward":
                    ApplyConditionByAlias(c, "ConSukutsuResSound", -15);
                    break;

                case "impact_ward":
                    ApplyConditionByAlias(c, "ConSukutsuResImpact", -15);
                    break;

                case "bleed_ward":
                    ApplyConditionByAlias(c, "ConSukutsuResCut", -15);
                    break;

                case "painkiller":
                    ApplyPainkiller(c);
                    break;

                case "stimulant":
                    ApplyStimulant(c);
                    break;

                default:
                    Debug.LogWarning($"[SukutsuArena] Unknown effect ID: {CustomEffectId}, falling back to base");
                    base.OnDrink(c);
                    break;
            }
        }

        /// <summary>
        /// 万難のエリクサー効果
        /// - 複数耐性バフ（一時的）
        /// - カルマ-30
        /// </summary>
        private void ApplyKissOfInferno(Chara c)
        {
            // 演出
            c.PlaySound("curse");
            c.PlayEffect("curse");

            // 付与する耐性Condition（alias）
            string[] conditionAliases = new string[]
            {
                "ConSukutsuResCold",
                "ConSukutsuResDarkness",
                "ConSukutsuResChaos",
                "ConSukutsuResSound",
                "ConSukutsuResImpact",
                "ConSukutsuResCut",
            };

            // 長めの持続時間
            int power = 2000;

            foreach (string alias in conditionAliases)
            {
                c.AddCondition(Condition.Create(alias, power));
            }

            Debug.Log($"[SukutsuArena] Applied Kiss of Inferno buffs ({conditionAliases.Length} resistances) to {c.Name}");

            // カルマ減少（PCのみ）
            if (c.IsPC)
            {
                EClass.player.ModKarma(-30);
            }
        }

        /// <summary>
        /// Condition aliasを使ってバフを付与
        /// </summary>
        private void ApplyConditionByAlias(Chara c, string conditionAlias, int karmaChange)
        {
            try
            {
                Debug.Log($"[SukutsuArena] ApplyConditionByAlias: {conditionAlias}");

                // 演出
                c.PlaySound("buff");
                c.PlayEffect("buff");

                // Conditionを付与（power = 500 → 約27ターン持続）
                int power = 500;
                c.AddCondition(Condition.Create(conditionAlias, power));

                Debug.Log($"[SukutsuArena] Applied {conditionAlias} to {c.Name}");

                // カルマ減少（PCのみ）
                if (c.IsPC && karmaChange != 0)
                {
                    EClass.player.ModKarma(karmaChange);
                }
            }
            catch (System.Exception ex)
            {
                Debug.LogError($"[SukutsuArena] ApplyConditionByAlias EXCEPTION: {ex.Message}\n{ex.StackTrace}");
            }
        }

        /// <summary>
        /// 痛覚遮断薬効果
        /// - 物理ダメージ軽減（PVバフ、一時的）
        /// - 強力な毒状態付与
        /// </summary>
        private void ApplyPainkiller(Chara c)
        {
            // 演出
            c.PlaySound("curse");
            c.PlayEffect("curse");

            // PVを一時的に上昇
            // power = 800 → 約33ターン持続
            int power = 800;
            c.AddCondition(Condition.Create("ConSukutsuPVBuff", power));

            // 強力な毒状態付与（power = 500で強力な毒）
            c.AddCondition<ConPoison>(500);

            Debug.Log($"[SukutsuArena] Applied Painkiller (PV buff + strong poison) to {c.Name}");

            // カルマ減少
            if (c.IsPC)
            {
                EClass.player.ModKarma(-10);
            }
        }

        /// <summary>
        /// 禁断の覚醒剤効果
        /// - ブースト状態付与
        /// - 後遺症として強力な出血（ブーストより長く持続）
        /// </summary>
        private void ApplyStimulant(Chara c)
        {
            // 演出
            c.PlaySound("boost2");
            c.PlayEffect("buff");

            // ブースト状態付与（power = 200 → 約30ターン）
            c.AddCondition<ConBoost>(200);

            // 強力な出血状態付与（ブーストより長く持続）
            // Conditionを直接作成してvalueを設定
            var bleed = Condition.Create<ConBleed>(1);
            bleed.value = 50;  // 50ターン持続
            c.AddCondition(bleed);

            Debug.Log($"[SukutsuArena] Applied Stimulant (Boost + Bleed value={bleed.value}) to {c.Name}");

            // カルマ減少
            if (c.IsPC)
            {
                EClass.player.ModKarma(-15);
            }
        }

    }
}
