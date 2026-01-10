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
                    // 戦闘結果ダイアログを直接指定（NpcQuestDialogPatchをバイパス）
                    // これによりクエストドラマではなく結果ダイアログが表示される
                    Debug.Log($"[SukutsuArena] Showing battle result dialog with {master.Name}");
                    master.ShowDialog("drama_sukutsu_arena_master");
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
                if (Core.ArenaContext.I.Storage.GetInt("sukutsu_gladiator") == 0)
                    return;

                // 戦闘結果表示中はスキップ
                if (Core.ArenaContext.I.Storage.GetInt("sukutsu_arena_result") != 0)
                    return;

                // ランクアップ結果表示中はスキップ
                if (Core.ArenaContext.I.Storage.GetInt("sukutsu_is_rank_up_result") != 0)
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

        // NpcQuestDialogPatchNoArgs は削除されました
        // クエスト選択はドラマファイル内の選択肢で対応します
        // 理由: return false で他Modと競合するリスクが高いため

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
