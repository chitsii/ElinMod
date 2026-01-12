namespace Elin_SukutsuArena.Conditions
{
    /// <summary>
    /// アスタロトの権能「因果の拒絶」
    /// 筋力を大幅に低下させる
    /// </summary>
    public class ConAstarothDenial : Condition
    {
        public override string Name => "denial_of_causality".lang();

        public override ConditionType Type => ConditionType.Debuff;

        public override bool UseElements => true;

        public override int GetPhase() => 0;

        public override void SetOwner(Chara _owner, bool onDeserialize = false)
        {
            base.SetOwner(_owner);
            // Element 70 = STR, -1000で物理攻撃力大幅低下
            elements.SetBase(70, -1000);
            elements.SetParent(owner);
        }

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
