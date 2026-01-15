namespace Elin_SukutsuArena.Conditions
{
    /// <summary>
    /// アスタロトの権能「因果の拒絶」
    /// 筋力を大幅に低下させる（elementsはExcel側で設定）
    /// </summary>
    public class ConAstarothDenial : Condition
    {
        public override string Name => "denial_of_causality".lang();

        public override ConditionType Type => ConditionType.Debuff;

        public override int GetPhase() => 0;

        public override void PlayEffect()
        {
            if (!Condition.ignoreEffect)
            {
                owner.PlaySound("debuff");
                owner.PlayEffect("debuff");
            }
        }
    }
}
