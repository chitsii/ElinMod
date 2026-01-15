using System.Collections.Generic;
using System.Linq;
using Elin_SukutsuArena.Core;
using UnityEngine;

namespace Elin_SukutsuArena.Commands
{
    /// <summary>
    /// check_available_quests(npcId)
    /// NPCごとの利用可能クエストをチェックし、フラグを設定
    /// ドラマ側で条件分岐に使用する
    /// </summary>
    public class CheckAvailableQuestsCommand : IArenaCommand
    {
        public string Name => "check_available_quests";

        public void Execute(ArenaContext ctx, DramaManager drama, string[] args)
        {
            string npcId = args.Length > 0 ? args[0] : "";

            Debug.Log($"[CheckAvailableQuests] Checking for NPC: {npcId}");

            // NPCに対応するクエストを取得
            var quests = string.IsNullOrEmpty(npcId)
                ? ArenaQuestManager.Instance.GetAvailableQuests()
                : ArenaQuestManager.Instance.GetQuestsForNpc(npcId);

            // 利用可能クエスト数を設定
            ctx.Storage.SetInt("sukutsu_available_quest_count", quests.Count);

            // 各クエストタイプの有無をフラグに設定
            bool hasRankUp = quests.Any(q => q.QuestType == "rank_up");
            bool hasCharacterEvent = quests.Any(q => q.QuestType == "character_event");
            bool hasSubQuest = quests.Any(q => q.QuestType == "sub_quest");

            ctx.Storage.SetInt("sukutsu_has_rank_up", hasRankUp ? 1 : 0);
            ctx.Storage.SetInt("sukutsu_has_character_event", hasCharacterEvent ? 1 : 0);
            ctx.Storage.SetInt("sukutsu_has_sub_quest", hasSubQuest ? 1 : 0);

            // 最優先のクエストIDを設定（選択肢表示用）
            if (quests.Count > 0)
            {
                var topQuest = quests.OrderByDescending(q => q.Priority).First();
                ctx.Storage.SetInt("sukutsu_top_quest_id", topQuest.QuestId.GetHashCode());

                Debug.Log($"[CheckAvailableQuests] Found {quests.Count} quests, top: {topQuest.QuestId}");
            }
            else
            {
                ctx.Storage.SetInt("sukutsu_top_quest_id", 0);
                Debug.Log("[CheckAvailableQuests] No quests available");
            }

            // ランクアップクエストの番号をマッピング（quest_id -> rank値）
            // Note: クエストIDはflag_definitions.py QuestIdsと一致させること
            var rankUpMapping = new Dictionary<string, int>
            {
                { "02_rank_up_G", 1 },  // QuestIds.RANK_UP_G
                { "04_rank_up_F", 2 },  // QuestIds.RANK_UP_F
                { "06_rank_up_E", 3 },  // QuestIds.RANK_UP_E
                { "10_rank_up_D", 4 },  // QuestIds.RANK_UP_D
                { "09_rank_up_C", 5 },  // QuestIds.RANK_UP_C
                { "11_rank_up_B", 6 },  // QuestIds.RANK_UP_B
                { "12_rank_up_A", 7 },  // QuestIds.RANK_UP_A
            };

            // 次に受けられるランクアップクエストを検索
            var nextRankUp = quests
                .Where(q => q.QuestType == "rank_up" && rankUpMapping.ContainsKey(q.QuestId))
                .OrderBy(q => rankUpMapping[q.QuestId])
                .FirstOrDefault();

            int nextRankUpValue = nextRankUp != null ? rankUpMapping[nextRankUp.QuestId] : 0;
            ctx.Storage.SetInt("sukutsu_next_rank_up", nextRankUpValue);

            Debug.Log($"[CheckAvailableQuests] Next rank up: {nextRankUpValue} ({nextRankUp?.QuestId ?? "none"})");

            // クエスト完了状態からランクを推論し、player.rankを同期
            // 高いランクから順にチェックし、完了済みの最高ランクを現在のランクとする
            int inferredRank = 0;
            // 実際に存在するクエスト完了フラグを列挙
            Debug.Log($"[CheckAvailableQuests] Existing quest_done flags:");
            var questDoneFlags = EClass.player.dialogFlags
                .Where(f => f.Key.Contains("quest_done"))
                .OrderBy(f => f.Key)
                .ToList();
            foreach (var f in questDoneFlags)
            {
                Debug.Log($"  {f.Key} = {f.Value}");
            }

            Debug.Log($"[CheckAvailableQuests] Checking rank up completion status:");
            foreach (var kvp in rankUpMapping.OrderByDescending(x => x.Value))
            {
                string flagKey = $"sukutsu_quest_done_{kvp.Key}";
                bool flagExists = EClass.player.dialogFlags.ContainsKey(flagKey);
                int flagValue = flagExists ? EClass.player.dialogFlags[flagKey] : -1;
                bool isCompleted = ArenaQuestManager.Instance.IsQuestCompleted(kvp.Key);
                Debug.Log($"  {kvp.Key} (rank={kvp.Value}): flagKey={flagKey}, exists={flagExists}, value={flagValue}, completed={isCompleted}");
                if (isCompleted && inferredRank == 0)
                {
                    inferredRank = kvp.Value;
                    // 最高ランクを見つけても、デバッグのため全てログ出力を続ける
                }
            }
            Debug.Log($"[CheckAvailableQuests] Inferred rank: {inferredRank}");

            // 現在のplayer.rankと異なる場合は同期
            int currentRank = ctx.Storage.GetInt("chitsii.arena.player.rank");
            Debug.Log($"[CheckAvailableQuests] Current rank: {currentRank}");
            if (currentRank != inferredRank)
            {
                Debug.Log($"[CheckAvailableQuests] Syncing player.rank: {currentRank} -> {inferredRank}");
                ctx.Storage.SetInt("chitsii.arena.player.rank", inferredRank);
            }
            else
            {
                Debug.Log($"[CheckAvailableQuests] Rank already in sync");
            }
        }
    }
}
