namespace Elin_SukutsuArena.Conditions
{
    /// <summary>
    /// アスタロトの権能「時の独裁」
    /// 速度を大幅に低下させる
    /// </summary>
    public class ConAstarothTyranny : Condition
    {
        public override string Name => "tyranny_of_time".lang();

        public override ConditionType Type => ConditionType.Debuff;

        public override bool UseElements => true;

        public override int GetPhase() => 0;

        public override void SetOwner(Chara _owner, bool onDeserialize = false)
        {
            base.SetOwner(_owner);
            // Element 79 = Speed, -1000で大幅減速
            elements.SetBase(79, -1000);
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
