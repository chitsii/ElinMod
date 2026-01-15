namespace Elin_SukutsuArena
{
    /// <summary>
    /// アリーナNPC用Trait（非商人）
    /// メインクエスト完了前はペット化・招待不可
    /// </summary>
    public class TraitSukutsuNPC : TraitUniqueChara
    {
        public override bool CanJoinParty =>
            ArenaQuestManager.Instance?.IsQuestCompleted("18_last_battle") ?? false;

        public override bool CanInvite =>
            ArenaQuestManager.Instance?.IsQuestCompleted("18_last_battle") ?? false;

        public override bool CanJoinPartyResident =>
            (ArenaQuestManager.Instance?.IsQuestCompleted("18_last_battle") ?? false)
            && base.CanJoinPartyResident;
    }

    /// <summary>
    /// アリーナ商人NPC用Trait
    /// 商人機能を維持しつつ、メインクエスト完了前はペット化・招待不可
    /// </summary>
    public class TraitSukutsuMerchant : TraitMerchant
    {
        public override bool CanJoinParty =>
            ArenaQuestManager.Instance?.IsQuestCompleted("18_last_battle") ?? false;

        public override bool CanInvite =>
            ArenaQuestManager.Instance?.IsQuestCompleted("18_last_battle") ?? false;

        public override bool CanJoinPartyResident =>
            (ArenaQuestManager.Instance?.IsQuestCompleted("18_last_battle") ?? false)
            && base.CanJoinPartyResident;
    }
}
