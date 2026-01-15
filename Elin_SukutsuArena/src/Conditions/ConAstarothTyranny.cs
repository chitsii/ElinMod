namespace Elin_SukutsuArena.Conditions
{
    /// <summary>
    /// アスタロトの権能「時の独裁」
    /// 速度を大幅に低下させる（elementsはExcel側で設定）
    /// </summary>
    public class ConAstarothTyranny : Condition
    {
        public override string Name => "tyranny_of_time".lang();

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
