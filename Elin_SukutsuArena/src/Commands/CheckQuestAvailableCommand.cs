using Elin_SukutsuArena.Core;
using Elin_SukutsuArena.Data;
using UnityEngine;

namespace Elin_SukutsuArena.Commands
{
    /// <summary>
    /// check_quest_available(questId, jumpLabel)
    /// クエストが利用可能かチェックし、利用可能ならジャンプ先を設定
    /// </summary>
    public class CheckQuestAvailableCommand : IArenaCommand
    {
        public string Name => "check_quest_available";

        public void Execute(ArenaContext ctx, DramaManager drama, string[] args)
        {
            if (args.Length < 1)
            {
                Debug.LogError("[CheckQuestAvailable] Requires at least 1 arg: questId[, jumpLabel]");
                return;
            }

            var questId = args[0];
            var jumpLabel = args.Length > 1 ? args[1] : "";

            Debug.Log($"[CheckQuestAvailable] questId='{questId}', jumpLabel='{jumpLabel}'");
            Msg.Say($"[DEBUG] check_quest: {questId}");

            // 既に他のクエストが見つかっている場合はスキップ
            if (ctx.Session.QuestFound)
            {
                Debug.Log("[CheckQuestAvailable] Quest already found, skipping");
                Msg.Say($"[DEBUG] skip (already found)");
                return;
            }

            // ArenaQuestManagerを使用してクエスト可用性をチェック
            bool available = ArenaQuestManager.Instance.IsQuestAvailable(questId);
            Debug.Log($"[CheckQuestAvailable] Quest '{questId}' available: {available}");
            Msg.Say($"[DEBUG] {questId} available={available}");

            if (available && !string.IsNullOrEmpty(jumpLabel))
            {
                ctx.Session.QuestFound = true;
                var target = JumpLabelMapping.FromString(jumpLabel);
                ctx.Session.QuestJumpTarget = target;
                Debug.Log($"[CheckQuestAvailable] Set jump target: {jumpLabel} -> {target} ({(int)target})");
                Msg.Say($"[DEBUG] SET target={jumpLabel} -> {(int)target}");
            }
        }
    }
}
