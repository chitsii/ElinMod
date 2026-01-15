namespace Elin_SukutsuArena.Conditions
{
    /// <summary>
    /// アスタロトの権能「終焉の削除命令」
    /// 魔力を大幅に低下させ、MPを0にする（elementsはExcel側で設定）
    /// </summary>
    public class ConAstarothDeletion : Condition
    {
        public override string Name => "deletion_command".lang();

        public override ConditionType Type => ConditionType.Debuff;

        public override int GetPhase() => 0;

        public override void SetOwner(Chara _owner, bool onDeserialize = false)
        {
            base.SetOwner(_owner);
            // MPを0にする
            owner.mana.value = 0;
        }

        public override void OnRefresh()
        {
            base.OnRefresh();
            // 常にMPを0に維持
            owner.mana.value = 0;
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
