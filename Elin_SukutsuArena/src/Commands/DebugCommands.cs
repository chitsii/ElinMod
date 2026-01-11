using Elin_SukutsuArena.Core;
using UnityEngine;

namespace Elin_SukutsuArena.Commands
{
    /// <summary>
    /// debug_log_flags()
    /// 全フラグをログ出力
    /// </summary>
    public class DebugLogFlagsCommand : IArenaCommand
    {
        public string Name => "debug_log_flags";

        public void Execute(ArenaContext ctx, DramaManager drama, string[] args)
        {
            Debug.Log("[ArenaFlags] === Current Flag State ===");
            Debug.Log($"  Motivation: {ctx.Player.GetMotivation()?.ToString() ?? "null"}");
            Debug.Log($"  Rank: {ctx.Player.Rank}");
            Debug.Log($"  Phase: {ctx.Player.CurrentPhase}");
            Debug.Log($"  Karma: {ctx.Player.Karma}");
            Debug.Log($"  Contribution: {ctx.Player.Contribution}");
            Debug.Log($"  Fugitive: {ctx.Player.IsFugitive}");
            Debug.Log($"  NullChip: {ctx.Player.HasNullChip}");
            Debug.Log($"  LilyTrueNameKnown: {ctx.Player.KnowsLilyTrueName}");
            Debug.Log($"  BottleChoice: {ctx.Player.GetBottleChoice()?.ToString() ?? "null"}");
            Debug.Log($"  KainSoulChoice: {ctx.Player.GetKainSoulChoice()?.ToString() ?? "null"}");
            Debug.Log($"  BalgasChoice: {ctx.Player.GetBalgasChoice()?.ToString() ?? "null"}");
            Debug.Log("[ArenaFlags] === End ===");
        }
    }

    /// <summary>
    /// debug_log_quests()
    /// クエスト状態をログ出力
    /// </summary>
    public class DebugLogQuestsCommand : IArenaCommand
    {
        public string Name => "debug_log_quests";

        public void Execute(ArenaContext ctx, DramaManager drama, string[] args)
        {
            ArenaQuestManager.Instance.DebugLogQuestState();
        }
    }
}
