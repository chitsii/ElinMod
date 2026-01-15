using UnityEngine;

namespace Elin_SukutsuArena.Conditions
{
    /// <summary>
    /// 痛覚遮断薬の毒効果（デメリット）
    /// elementsはExcel側で設定、Tick()で毎ターンダメージ
    /// </summary>
    public class ConSukutsuPoison : Condition
    {
        public override ConditionType Type => ConditionType.Debuff;

        public override Emo2 EmoIcon => Emo2.poison;

        /// <summary>
        /// 自然回復を阻止
        /// </summary>
        public override bool PreventRegen => true;

        public override int GetPhase() => 0;

        public override void Tick()
        {
            // 毎ターン5分の1の確率でダメージ（バニラと同じ）
            if (EClass.rnd(5) == 0)
            {
                int damage = EClass.rnd(owner.END / 10 + 2) + 1;
                owner.DamageHP(damage, AttackSource.Condition);
            }

            // 毎ターン持続時間を1減らす
            Mod(-1);
        }

        public override void OnStart()
        {
            Debug.Log($"[SukutsuArena] ConSukutsuPoison started on {owner.Name}, value={value}");
        }

        public override void PlayEffect()
        {
            if (!Condition.ignoreEffect)
            {
                owner.PlaySound("curse");
                owner.PlayEffect("curse");
            }
        }
    }
}
