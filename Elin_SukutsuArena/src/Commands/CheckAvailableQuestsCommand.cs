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
        }
    }
}
