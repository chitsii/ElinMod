using HarmonyLib;
using UnityEngine;
using System.Linq;
using DG.Tweening;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// アリーナ関連のHarmonyパッチまとめ
    /// </summary>
    public static class ArenaZonePatches
    {
        // 自動開始対象のクエストタイプ
        private static readonly string[] AutoStartQuestTypes = new[]
        {
            "main_story",
            "character_event",
            "side_quest"
        };

        // 一度のセッションで開始済みのクエストを追跡（連続トリガー防止）
        private static string lastTriggeredQuestId = null;

        /// <summary>
        /// クエスト完了時にトラッキングをリセット（次のクエストが自動開始可能になる）
        /// </summary>
        public static void ResetQuestTriggerTracking()
        {
            lastTriggeredQuestId = null;
            Debug.Log("[SukutsuArena] Quest trigger tracking reset");
        }

        /// <summary>
        /// ゾーンがアクティブになった時のパッチ
        /// アリーナから敗北・勝利して戻った時に自動でアリーナマスターと会話を開始
        /// ストーリークエストの自動開始
        /// </summary>
        [HarmonyPatch(typeof(Zone), nameof(Zone.Activate))]
        public static class ArenaZoneActivatePatch
        {
            [HarmonyPostfix]
            public static void Postfix(Zone __instance)
            {
                // 戦闘結果からの帰還かチェック
                bool isReturningFromBattle = EClass.player.dialogFlags.ContainsKey("sukutsu_auto_dialog")
                    && EClass.player.dialogFlags["sukutsu_auto_dialog"] > 0;

                // 戦闘結果の自動会話処理
                if (isReturningFromBattle)
                {
                    HandleBattleResultDialog();
                    return; // 戦闘帰還時はストーリークエストをスキップ
                }

                // ストーリークエストの自動開始（アリーナゾーンのみ）
                if (__instance.id == Plugin.ZoneId)
                {
                    CheckAndTriggerStoryQuest();
                }
            }

            /// <summary>
            /// 戦闘結果後の自動会話処理
            /// </summary>
            private static void HandleBattleResultDialog()
            {
                if (!EClass.player.dialogFlags.ContainsKey("sukutsu_auto_dialog"))
                    return;

                int masterUid = EClass.player.dialogFlags["sukutsu_auto_dialog"];
                if (masterUid <= 0)
                    return;

                Debug.Log($"[SukutsuArena] Auto-dialog triggered for master UID: {masterUid}");

                // フラグをクリア
                EClass.player.dialogFlags["sukutsu_auto_dialog"] = 0;

                // アリーナマスターを探す
                Chara master = EClass.game.cards.Find(masterUid) as Chara;
                if (master == null || !master.ExistsOnMap)
                {
                    foreach (var c in EClass._map.charas)
                    {
                        if (c.id == "sukutsu_arena_master")
                        {
                            master = c;
                            break;
                        }
                    }
                }

                if (master != null && master.ExistsOnMap)
                {
                    Debug.Log($"[SukutsuArena] Showing dialog with {master.Name}");
                    master.ShowDialog();
                }
                else
                {
                    Debug.LogWarning($"[SukutsuArena] Arena Master not found");
                }
            }

            /// <summary>
            /// 条件を満たしたストーリークエストを自動開始
            /// </summary>
            private static void CheckAndTriggerStoryQuest()
            {
                // 闘士未登録なら何もしない
                if (!ArenaFlagManager.GetBool("sukutsu_gladiator"))
                    return;

                // 戦闘結果表示中はスキップ
                if (ArenaFlagManager.GetInt("sukutsu_arena_result") != 0)
                    return;

                // ランクアップ結果表示中はスキップ
                if (ArenaFlagManager.GetInt("sukutsu_is_rank_up_result") != 0)
                    return;

                var availableQuests = ArenaQuestManager.Instance.GetAvailableQuests();

                // 自動開始対象のクエストをフィルタリング
                var storyQuest = availableQuests
                    .Where(q => AutoStartQuestTypes.Contains(q.QuestType))
                    .Where(q => q.QuestId != lastTriggeredQuestId) // 連続トリガー防止
                    .OrderByDescending(q => q.Priority)
                    .FirstOrDefault();

                if (storyQuest == null)
                {
                    Debug.Log("[SukutsuArena] No story quest available for auto-start");
                    return;
                }

                Debug.Log($"[SukutsuArena] Auto-starting story quest: {storyQuest.QuestId} ({storyQuest.DramaId})");
                lastTriggeredQuestId = storyQuest.QuestId;

                // 少し遅延させてからドラマを開始（ゾーン遷移の完了を待つ）
                DOVirtual.DelayedCall(0.5f, () =>
                {
                    TriggerQuestDrama(storyQuest);
                });
            }

            /// <summary>
            /// クエストのドラマを開始
            /// </summary>
            private static void TriggerQuestDrama(QuestDefinition quest)
            {
                // ドラマファイル名は "drama_{dramaId}" 形式
                string dramaName = $"drama_{quest.DramaId}";
                Debug.Log($"[SukutsuArena] Triggering drama: {dramaName}");

                try
                {
                    // ドラマIDに基づいて対応するキャラクターを見つける
                    string targetCharaId = GetQuestTargetChara(quest.QuestId);
                    Chara targetChara = null;

                    if (!string.IsNullOrEmpty(targetCharaId))
                    {
                        foreach (var c in EClass._map.charas)
                        {
                            if (c.id == targetCharaId)
                            {
                                targetChara = c;
                                break;
                            }
                        }
                    }

                    if (targetChara != null)
                    {
                        Debug.Log($"[SukutsuArena] Starting dialog with {targetChara.Name} for quest {quest.QuestId}");
                        // キャラクターのShowDialogを使用してドラマを開始（actorが正しく設定される）
                        targetChara.ShowDialog(dramaName);
                    }
                    else
                    {
                        Debug.Log($"[SukutsuArena] Target character not found, starting drama directly: {dramaName}");
                        // キャラクターが見つからない場合は直接開始（フォールバック）
                        LayerDrama.Activate(dramaName, null, null, null, null, null);
                    }
                }
                catch (System.Exception ex)
                {
                    Debug.LogError($"[SukutsuArena] Failed to trigger drama: {ex}");
                }
            }

            /// <summary>
            /// クエストIDに対応する対話相手のキャラクターIDを取得
            /// </summary>
            private static string GetQuestTargetChara(string questId)
            {
                // クエストIDに基づいて対話相手を決定
                return questId switch
                {
                    // オープニング（リリィがナビゲーター）
                    "01_opening" => "sukutsu_receptionist",

                    // ゼク関連
                    "03_zek_intro" => "sukutsu_shady_merchant",
                    "05_2_zek_steal_bottle" => "sukutsu_shady_merchant",
                    "06_2_zek_steal_soulgem" => "sukutsu_shady_merchant",

                    // リリィ関連
                    "05_1_lily_experiment" => "sukutsu_receptionist",
                    "08_lily_private" => "sukutsu_receptionist",
                    "16_lily_real_name" => "sukutsu_receptionist",

                    // バルガス関連
                    "09_balgas_training" => "sukutsu_arena_master",
                    "15_vs_balgas" => "sukutsu_arena_master",

                    // メインストーリー（リリィが語り手）
                    "07_upper_existence" => "sukutsu_receptionist",
                    "12_makuma" => "sukutsu_receptionist",
                    "13_makuma2" => "sukutsu_receptionist",
                    "17_vs_grandmaster_1" => "sukutsu_arena_master",
                    "18_last_battle" => "sukutsu_arena_master",

                    _ => null
                };
            }
        }

        /// <summary>
        /// アリーナ戦闘ゾーンでは自動復活（ゲームオーバー回避）を有効にするパッチ
        /// </summary>
        [HarmonyPatch(typeof(Zone), "get_ShouldAutoRevive")]
        public static class ArenaZoneRevivePatch
        {
            [HarmonyPostfix]
            public static void Postfix(Zone __instance, ref bool __result)
            {
                if (__instance.instance is ZoneInstanceArenaBattle)
                {
                    // アリーナバトル中は強制的に復活可能（ゲームオーバーにならない）
                    // 実際の復活処理と退出はZoneEventArenaBattle.OnCharaDieで行う
                    __result = true;
                }
            }
        }
    }
}
