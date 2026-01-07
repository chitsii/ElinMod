using HarmonyLib;
using UnityEngine;
using System;
using System.Collections.Generic;
using System.Linq;
using DG.Tweening;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// アリーナ関連のHarmonyパッチまとめ
    /// フェーズベースのクエスト管理とNPCマーカーをサポート
    /// </summary>
    public static class ArenaZonePatches
    {
        // 一度のセッションで開始済みのクエストを追跡（連続トリガー防止）
        private static string lastTriggeredQuestId = null;

        /// <summary>
        /// ゾーンがアリーナかどうかを判定
        /// </summary>
        public static bool IsArenaZone(Zone zone)
        {
            if (zone == null) return false;
            return zone.id == Plugin.ZoneId ||
                   zone.id?.Contains("sukutsu") == true ||
                   zone.id?.Contains("arena") == true;
        }

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
        /// 自動発動クエストの開始とNPCマーカーの更新
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
                    return; // 戦闘帰還時は自動クエストをスキップ
                }

                // アリーナゾーンの処理
                if (IsArenaZone(__instance))
                {
                    // NPCマーカーをリフレッシュ
                    DOVirtual.DelayedCall(0.3f, () =>
                    {
                        ArenaQuestMarkerManager.Instance.RefreshAllMarkers();
                    });

                    // 自動発動クエストのチェックと開始
                    CheckAndTriggerAutoQuest();
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

                // デバッグ: ドラマ開始前のフラグ状態を確認
                int arenaResult = EClass.player.dialogFlags.ContainsKey("sukutsu_arena_result")
                    ? EClass.player.dialogFlags["sukutsu_arena_result"] : -1;
                int isRankUpResult = EClass.player.dialogFlags.ContainsKey("sukutsu_is_rank_up_result")
                    ? EClass.player.dialogFlags["sukutsu_is_rank_up_result"] : -1;
                int rankUpTrial = EClass.player.dialogFlags.ContainsKey("sukutsu_rank_up_trial")
                    ? EClass.player.dialogFlags["sukutsu_rank_up_trial"] : -1;
                Debug.Log($"[SukutsuArena] PRE-DIALOG FLAGS: arena_result={arenaResult}, is_rank_up_result={isRankUpResult}, rank_up_trial={rankUpTrial}");

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
                    // 戦闘結果ダイアログを直接指定
                    // NpcQuestDialogPatchNoArgsがスキップするようにフラグを設定
                    Debug.Log($"[SukutsuArena] Showing battle result dialog with {master.Name}");
                    Debug.Log($"[SukutsuArena] FLAGS BEFORE DRAMA: arena_result={ArenaFlagManager.GetInt("sukutsu_arena_result")}, is_rank_up_result={ArenaFlagManager.GetInt("sukutsu_is_rank_up_result")}, rank_up_trial={ArenaFlagManager.GetInt("sukutsu_rank_up_trial")}");
                    // 戦闘結果ダイアログ中フラグを設定（NpcQuestDialogPatchがスキップするため）
                    ArenaFlagManager.SetBool("sukutsu_showing_battle_result", true);
                    master.ShowDialog("drama_sukutsu_arena_master", "main");
                }
                else
                {
                    Debug.LogWarning($"[SukutsuArena] Arena Master not found");
                }
            }

            /// <summary>
            /// 自動発動クエストをチェックして開始（フェーズベース）
            /// </summary>
            private static void CheckAndTriggerAutoQuest()
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

                // 自動発動クエストを取得（フェーズと条件でフィルタリング済み）
                var autoQuests = ArenaQuestManager.Instance.GetAutoTriggerQuests();

                // 連続トリガー防止と優先度でフィルタリング
                var quest = autoQuests
                    .Where(q => q.QuestId != lastTriggeredQuestId)
                    .OrderByDescending(q => q.Priority)
                    .FirstOrDefault();

                if (quest == null)
                {
                    Debug.Log("[SukutsuArena] No auto-trigger quest available");
                    return;
                }

                Debug.Log($"[SukutsuArena] Auto-triggering quest: {quest.QuestId} (Phase: {quest.Phase}, Drama: {quest.DramaId})");
                lastTriggeredQuestId = quest.QuestId;

                // 少し遅延させてからドラマを開始（ゾーン遷移の完了を待つ）
                DOVirtual.DelayedCall(0.5f, () =>
                {
                    TriggerQuestDrama(quest);
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
                    string targetCharaId = GetQuestTargetChara(quest);
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
            /// クエストに対応する対話相手のキャラクターIDを取得
            /// quest_giverを優先し、未定義の場合はフォールバック
            /// </summary>
            private static string GetQuestTargetChara(QuestDefinition quest)
            {
                // quest_giverが設定されていればそれを使用
                if (!string.IsNullOrEmpty(quest.QuestGiver))
                {
                    return quest.QuestGiver;
                }

                // 自動発動クエスト（quest_giver = null）の場合はフォールバック
                return quest.QuestId switch
                {
                    // オープニング（リリィがナビゲーター）
                    "01_opening" => "sukutsu_receptionist",

                    // メインストーリー（リリィが語り手）
                    "13_makuma2" => "sukutsu_receptionist",
                    "17_escape" => "sukutsu_arena_master",
                    "18_last_battle" => "sukutsu_arena_master",

                    // デフォルトはリリィ
                    _ => "sukutsu_receptionist"
                };
            }
        }

        /// <summary>
        /// NPC会話開始時（引数なし）にクエストを持っているかチェックし、クエストドラマを優先するパッチ
        /// ShowDialog()オーバーロードをパッチ（プレイヤーがNPCをクリックした時に呼ばれる）
        ///
        /// 注意: character_eventタイプのクエストのみ強制開始する
        /// rank_upクエストは通常のNPCダイアログで選択できるようにする
        /// </summary>
        [HarmonyPatch(typeof(Chara), nameof(Chara.ShowDialog), new Type[] { })]
        public static class NpcQuestDialogPatchNoArgs
        {
            // NPCクリックで自動開始すべきクエストタイプ
            private static readonly HashSet<string> AutoStartQuestTypes = new HashSet<string>
            {
                "character_event",  // キャラクターイベント（ゼク初遭遇など）
                "side_quest"        // サイドクエスト
            };

            [HarmonyPrefix]
            public static bool Prefix(Chara __instance)
            {
                Debug.Log($"[NpcQuestDialog] ShowDialog() called: NPC={__instance?.id}");

                // 戦闘結果ダイアログ表示中はスキップ（HandleBattleResultDialogから呼ばれた場合）
                if (ArenaFlagManager.GetBool("sukutsu_showing_battle_result"))
                {
                    Debug.Log($"[NpcQuestDialog] SKIP: Battle result dialog in progress");
                    ArenaFlagManager.SetBool("sukutsu_showing_battle_result", false); // フラグをクリア
                    return true; // 元のShowDialogを実行
                }

                // アリーナゾーン外ではスキップ
                if (!IsArenaZone(EClass._zone))
                {
                    Debug.Log($"[NpcQuestDialog] SKIP: Not in arena zone (zone={EClass._zone?.id})");
                    return true;
                }

                // アリーナNPCかチェック
                string npcId = __instance.id;
                if (!IsArenaNpc(npcId))
                {
                    Debug.Log($"[NpcQuestDialog] SKIP: Not an arena NPC ({npcId})");
                    return true;
                }

                // このNPCが利用可能なクエストを持っているかチェック
                Debug.Log($"[NpcQuestDialog] Checking quests for NPC: {npcId}");
                var allQuests = ArenaQuestManager.Instance.GetQuestsForNpc(npcId);
                Debug.Log($"[NpcQuestDialog] GetQuestsForNpc returned: {allQuests?.Count ?? 0} quests");

                if (allQuests == null || allQuests.Count == 0)
                {
                    Debug.Log($"[NpcQuestDialog] SKIP: No quests for NPC {npcId}");
                    return true;
                }

                // 自動開始すべきクエストタイプのみフィルタリング
                // rank_up, main_storyなどはNPCダイアログ内で選択させる
                var autoStartQuests = allQuests
                    .Where(q => AutoStartQuestTypes.Contains(q.QuestType))
                    .OrderByDescending(q => q.Priority)
                    .ToList();

                Debug.Log($"[NpcQuestDialog] Auto-start eligible quests: {autoStartQuests.Count} (types: {string.Join(",", AutoStartQuestTypes)})");

                if (autoStartQuests.Count == 0)
                {
                    Debug.Log($"[NpcQuestDialog] SKIP: No auto-start quests for NPC {npcId}");
                    return true;
                }

                var quest = autoStartQuests.First();
                Debug.Log($"[SukutsuArena] NPC {npcId} has auto-start quest: {quest.QuestId} (type: {quest.QuestType}), starting quest drama");

                // クエストドラマを開始（通常会話をスキップ）
                string dramaName = $"drama_{quest.DramaId}";
                Debug.Log($"[NpcQuestDialog] Starting drama: {dramaName}");
                __instance.ShowDialog(dramaName);

                return false; // 通常会話をスキップ
            }
        }

        /// <summary>
        /// アリーナNPCかどうかを判定（共通メソッド）
        /// </summary>
        private static bool IsArenaNpc(string npcId)
        {
            return npcId == "sukutsu_receptionist" ||
                   npcId == "sukutsu_arena_master" ||
                   npcId == "sukutsu_shady_merchant" ||
                   npcId == "sukutsu_grandmaster";
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

        /// <summary>
        /// ダイアログ終了時にマーカーをリフレッシュするパッチ
        /// </summary>
        [HarmonyPatch(typeof(LayerDrama), nameof(LayerDrama.OnKill))]
        public static class DramaEndMarkerRefreshPatch
        {
            [HarmonyPostfix]
            public static void Postfix()
            {
                Debug.Log("[ArenaMarker] Drama layer closed, refreshing markers");

                // 少し遅延させてリフレッシュ（ダイアログ終了処理完了後）
                DOVirtual.DelayedCall(0.1f, () =>
                {
                    if (IsArenaZone(EClass._zone))
                    {
                        ArenaQuestMarkerManager.Instance.RefreshAllMarkers();
                    }
                });
            }
        }

        /// <summary>
        /// TickConditionsの直後にマーカーを設定するパッチ
        /// TickConditionsでemoIconがnoneにリセットされるので、直後に再設定する
        /// これにより点滅を防ぐ
        /// </summary>
        [HarmonyPatch(typeof(Chara), nameof(Chara.TickConditions))]
        public static class CharaTickConditionsMarkerPatch
        {
            [HarmonyPostfix]
            public static void Postfix(Chara __instance)
            {
                try
                {
                    // アリーナゾーン外ではスキップ
                    if (!IsArenaZone(EClass._zone)) return;

                    // このキャラがクエストマーカーを持つべきかチェック
                    var npcsWithQuests = ArenaQuestMarkerManager.Instance.GetNpcsWithQuestsList();
                    if (npcsWithQuests == null || !npcsWithQuests.Contains(__instance.id)) return;

                    // emoIcon = Emo2.hint で「！」マーカーを直接表示
                    // TickConditionsでnoneにリセットされた直後に設定するので点滅しない
                    __instance.emoIcon = Emo2.hint;
                }
                catch
                {
                    // 静かに失敗
                }
            }
        }
    }
}
