using HarmonyLib;
using System;
using System.Collections.Generic;
using UnityEngine;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// DramaManagerへのHarmonyパッチ
    /// 新しいアクション「modInvoke」を追加し、C#メソッド呼び出しを可能にする
    /// focusChara アクションにnullチェックを追加
    /// </summary>
    [HarmonyPatch(typeof(DramaManager))]
    public static class DramaManager_Patch
    {
        /// <summary>
        /// DramaManager.ParseLine の前に focusChara を安全なバージョンに差し替え
        /// </summary>
        [HarmonyPrefix]
        [HarmonyPatch("ParseLine")]
        public static void ParseLine_Prefix(DramaManager __instance, Dictionary<string, string> item)
        {
            try
            {
                if (!item.ContainsKey("action"))
                    return;

                string[] actionParts = item["action"].Split('/');
                string action = actionParts[0];

                // focusChara を安全なバージョンに差し替え
                if (action == "focusChara")
                {
                    string charaId = item.ContainsKey("param") ? item["param"] : "";

                    // 先にキャラの存在をチェック
                    bool charaExists = false;
                    if (EClass._map != null && !string.IsNullOrEmpty(charaId))
                    {
                        foreach (var c in EClass._map.charas)
                        {
                            if (c.id == charaId)
                            {
                                charaExists = true;
                                break;
                            }
                        }
                    }

                    if (!charaExists)
                    {
                        Debug.LogWarning($"[ArenaFocusChara] Character not found on map: {charaId}, replacing with safe wait");
                        // キャラがいない場合は wait アクションに差し替え（元のfocusCharaの代わり）
                        item["action"] = "wait";
                        item["param"] = "0.1";
                    }
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[ArenaPatch] Error in ParseLine_Prefix: {ex}");
            }
        }

        /// <summary>
        /// DramaManager.ParseLine の後にカスタムアクションを処理
        /// </summary>
        [HarmonyPostfix]
        [HarmonyPatch("ParseLine")]
        public static void ParseLine_Postfix(DramaManager __instance, Dictionary<string, string> item)
        {
            try
            {
                // アクションを取得
                if (!item.ContainsKey("action"))
                    return;

                string[] actionParts = item["action"].Split('/');
                string action = actionParts[0];

                // modInvoke または invoke* の場合のみ処理
                if (action != "modInvoke" && action != "invoke*")
                    return;

                // パラメータを取得
                string param = item.ContainsKey("param") ? item["param"] : "";
                if (string.IsNullOrEmpty(param))
                {
                    Debug.LogError("[ArenaModInvoke] Missing param for modInvoke action");
                    return;
                }

                // ジャンプ先を取得
                string jump = item.ContainsKey("jump") ? item["jump"] : "";

                // イベントを追加
                __instance.AddEvent(delegate
                {
                    HandleModInvoke(__instance, param, jump);
                });
            }
            catch (Exception ex)
            {
                Debug.LogError($"[ArenaModInvoke] Error in ParseLine_Postfix: {ex}");
            }
        }

        /// <summary>
        /// modInvoke アクションのハンドラ
        /// </summary>
        private static void HandleModInvoke(DramaManager manager, string param, string jump)
        {
            try
            {
                Debug.Log($"[ArenaModInvoke] HandleModInvoke: param='{param}', jump='{jump}'");

                // Parse method call: "methodName(arg1, arg2)"
                var openParen = param.IndexOf('(');
                if (openParen < 0)
                {
                    Debug.LogError($"[ArenaModInvoke] Invalid format: {param}");
                    return;
                }

                var methodName = param.Substring(0, openParen).Trim();
                var argsStr = param.Substring(openParen + 1, param.Length - openParen - 2); // Remove '(' and ')'
                var args = ParseArgs(argsStr);

                Debug.Log($"[ArenaModInvoke] Method: {methodName}, Args: [{string.Join(", ", args)}]");

                // Dispatch to appropriate handler
                bool handled = DispatchMethod(manager, methodName, args, jump);

                if (!handled)
                {
                    Debug.LogWarning($"[ArenaModInvoke] Unknown method: {methodName}");
                }
                else
                {
                    Debug.Log($"[ArenaModInvoke] Successfully handled: {methodName}");
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[ArenaModInvoke] Error handling modInvoke: {ex}");
            }
        }

        /// <summary>
        /// メソッド名とパラメータに応じてディスパッチ
        /// </summary>
        private static bool DispatchMethod(DramaManager manager, string methodName, List<string> args, string defaultJump)
        {
            switch (methodName)
            {
                // Quest Management
                case "check_quest_available":
                    return HandleCheckQuestAvailable(manager, args, defaultJump);

                case "start_quest":
                    return HandleStartQuest(args);

                case "complete_quest":
                    return HandleCompleteQuest(args);

                // Flag Conditionals (for string enum comparisons)
                case "if_flag":
                    return HandleIfFlag(manager, args, defaultJump);

                // Random Battle
                case "start_random_battle":
                    return HandleStartRandomBattle(args);

                // Debug
                case "debug_log_flags":
                    ArenaFlagManager.DebugLogAllFlags();
                    return true;

                case "debug_log_quests":
                    ArenaQuestManager.Instance.DebugLogQuestState();
                    return true;

                default:
                    return false;
            }
        }

        /// <summary>
        /// check_quest_available(questId, jumpLabel)
        /// クエストが利用可能ならジャンプ先ラベル名をフラグに保存
        /// </summary>
        private static bool HandleCheckQuestAvailable(DramaManager manager, List<string> args, string defaultJump)
        {
            if (args.Count < 1)
            {
                Debug.LogError("[ArenaModInvoke] check_quest_available requires at least 1 arg: questId[, jumpLabel]");
                return false;
            }

            var questId = args[0];
            var jumpLabel = args.Count > 1 ? args[1] : defaultJump;

            Debug.Log($"[ArenaModInvoke] check_quest_available: questId='{questId}', jumpLabel='{jumpLabel}'");

            // 既に他のクエストが見つかっている場合はスキップ
            if (EClass.player.dialogFlags.ContainsKey("sukutsu_quest_found") &&
                EClass.player.dialogFlags["sukutsu_quest_found"] == 1)
            {
                Debug.Log($"[ArenaModInvoke] Quest already found, skipping check");
                return true;
            }

            bool available = ArenaQuestManager.Instance.IsQuestAvailable(questId);
            Debug.Log($"[ArenaModInvoke] Quest '{questId}' available: {available}");

            if (available && !string.IsNullOrEmpty(jumpLabel))
            {
                Debug.Log($"[ArenaModInvoke] Quest found, setting jump target: {jumpLabel}");
                // クエストが見つかったフラグと、ジャンプ先ラベル名をフラグに保存
                EClass.player.dialogFlags["sukutsu_quest_found"] = 1;
                // ジャンプ先ラベル名をハッシュ化して保存（stringは直接保存できないため）
                EClass.player.dialogFlags["sukutsu_quest_target"] = jumpLabel.GetHashCode();
                EClass.player.dialogFlags["sukutsu_quest_target_name"] = 0; // ダミー、実際には使わない

                // 一時的にラベル名を保存する別の方法: quest_typeとして保存
                // ランクアップ系 (11-16)
                if (jumpLabel == "start_rank_g") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 11;
                else if (jumpLabel == "start_rank_f") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 12;
                else if (jumpLabel == "start_rank_e") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 13;
                else if (jumpLabel == "start_rank_d") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 14;
                else if (jumpLabel == "start_rank_c") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 15;
                else if (jumpLabel == "start_rank_b") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 16;
                // クエスト確認用 (同じ値を使用)
                else if (jumpLabel == "quest_rank_up_g") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 11;
                else if (jumpLabel == "quest_rank_up_f") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 12;
                else if (jumpLabel == "quest_rank_up_e") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 13;
                else if (jumpLabel == "quest_rank_up_d") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 14;
                else if (jumpLabel == "quest_rank_up_c") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 15;
                else if (jumpLabel == "quest_rank_up_b") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 16;
                // ストーリー系 (21-33)
                else if (jumpLabel == "quest_zek_intro") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 21;
                else if (jumpLabel == "quest_lily_exp") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 22;
                else if (jumpLabel == "quest_zek_steal_bottle") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 23;
                else if (jumpLabel == "quest_zek_steal_soulgem") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 24;
                else if (jumpLabel == "quest_upper_existence") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 25;
                else if (jumpLabel == "quest_lily_private") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 26;
                else if (jumpLabel == "quest_balgas_training") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 27;
                else if (jumpLabel == "quest_makuma") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 28;
                else if (jumpLabel == "quest_makuma2") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 29;
                else if (jumpLabel == "quest_vs_balgas") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 30;
                else if (jumpLabel == "quest_lily_real_name") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 31;
                else if (jumpLabel == "quest_vs_grandmaster_1") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 32;
                else if (jumpLabel == "quest_last_battle") EClass.player.dialogFlags["sukutsu_quest_target_name"] = 33;

                Debug.Log($"[ArenaModInvoke] Flag set: sukutsu_quest_found=1, target_name={EClass.player.dialogFlags["sukutsu_quest_target_name"]}");
            }
            else if (!available)
            {
                Debug.Log($"[ArenaModInvoke] Quest not available");
            }
            else
            {
                Debug.Log($"[ArenaModInvoke] No jump label specified");
            }

            return true;
        }

        /// <summary>
        /// start_quest(questId)
        /// クエストを開始
        /// </summary>
        private static bool HandleStartQuest(List<string> args)
        {
            if (args.Count < 1)
            {
                Debug.LogError("[ArenaModInvoke] start_quest requires 1 arg: questId");
                return false;
            }

            var questId = args[0];
            ArenaQuestManager.Instance.StartQuest(questId);
            return true;
        }

        /// <summary>
        /// complete_quest(questId)
        /// クエストを完了
        /// </summary>
        private static bool HandleCompleteQuest(List<string> args)
        {
            Debug.Log($"[ArenaModInvoke] HandleCompleteQuest called with {args.Count} args");

            if (args.Count < 1)
            {
                Debug.LogError("[ArenaModInvoke] complete_quest requires 1 arg: questId");
                return false;
            }

            var questId = args[0];
            Debug.Log($"[ArenaModInvoke] Calling CompleteQuest for: {questId}");
            ArenaQuestManager.Instance.CompleteQuest(questId);
            return true;
        }

        /// <summary>
        /// start_random_battle(difficulty, masterId)
        /// ランダム戦闘を開始
        /// difficulty: 1=Easy, 2=Normal, 3=Hard, 4=VeryHard
        /// masterId: アリーナマスターのキャラクターID
        /// </summary>
        private static bool HandleStartRandomBattle(List<string> args)
        {
            if (args.Count < 2)
            {
                Debug.LogError("[ArenaModInvoke] start_random_battle requires 2 args: difficulty, masterId");
                return false;
            }

            if (!int.TryParse(args[0], out int difficulty))
            {
                Debug.LogError($"[ArenaModInvoke] Invalid difficulty: {args[0]}");
                return false;
            }

            var masterId = args[1];
            Debug.Log($"[ArenaModInvoke] Starting random battle: difficulty={difficulty}, master={masterId}");

            ArenaManager.StartRandomBattle(difficulty, masterId);
            return true;
        }

        /// <summary>
        /// if_flag(flagKey, operatorValue[, jumpLabel])
        /// フラグ条件が真ならjumpLabelにジャンプ
        /// operatorValue は "==1" のように演算子と値が結合された形式
        /// </summary>
        private static bool HandleIfFlag(DramaManager manager, List<string> args, string defaultJump)
        {
            if (args.Count < 2)
            {
                Debug.LogError("[ArenaModInvoke] if_flag requires at least 2 args: flagKey, operatorValue[, jumpLabel]");
                return false;
            }

            var flagKey = args[0];
            var operatorValue = args[1]; // e.g., "==1", ">=50"
            var jumpLabel = args.Count > 2 ? args[2] : defaultJump;

            // Parse operator and value from combined string (e.g., "==1")
            string op = null;
            string valueStr = null;

            // Try to find operator at the start
            if (operatorValue.StartsWith("=="))
            {
                op = "==";
                valueStr = operatorValue.Substring(2);
            }
            else if (operatorValue.StartsWith("!="))
            {
                op = "!=";
                valueStr = operatorValue.Substring(2);
            }
            else if (operatorValue.StartsWith(">="))
            {
                op = ">=";
                valueStr = operatorValue.Substring(2);
            }
            else if (operatorValue.StartsWith("<="))
            {
                op = "<=";
                valueStr = operatorValue.Substring(2);
            }
            else if (operatorValue.StartsWith(">"))
            {
                op = ">";
                valueStr = operatorValue.Substring(1);
            }
            else if (operatorValue.StartsWith("<"))
            {
                op = "<";
                valueStr = operatorValue.Substring(1);
            }
            else
            {
                Debug.LogError($"[ArenaModInvoke] Cannot parse operator from: {operatorValue}");
                return false;
            }

            // Get current flag value as int (since dialogFlags stores ints)
            int currentValue = ArenaFlagManager.GetInt(flagKey, 0);

            // Try to parse value as int
            bool condition = false;
            if (int.TryParse(valueStr, out int expectedValue))
            {
                // Integer comparison
                condition = op switch
                {
                    "==" => currentValue == expectedValue,
                    "!=" => currentValue != expectedValue,
                    ">=" => currentValue >= expectedValue,
                    ">" => currentValue > expectedValue,
                    "<=" => currentValue <= expectedValue,
                    "<" => currentValue < expectedValue,
                    _ => false
                };
                Debug.Log($"[ArenaModInvoke] if_flag: {flagKey} {op} {expectedValue}, current={currentValue}, condition={condition}");
            }
            else
            {
                // String comparison (for enum names)
                // This would require mapping enum names to their int values
                Debug.LogWarning($"[ArenaModInvoke] String comparison not fully implemented: {flagKey} {op} {valueStr}");
                Debug.LogWarning($"[ArenaModInvoke] Current value: {currentValue}");
            }

            if (condition && !string.IsNullOrEmpty(jumpLabel))
            {
                Debug.Log($"[ArenaModInvoke] Jumping to: {jumpLabel}");
                manager.sequence.Play(jumpLabel);
            }

            return true;
        }

        /// <summary>
        /// 引数文字列をパースして配列に変換
        /// 例: "arg1, arg2, arg3" -> ["arg1", "arg2", "arg3"]
        /// </summary>
        private static List<string> ParseArgs(string argsStr)
        {
            var args = new List<string>();
            if (string.IsNullOrWhiteSpace(argsStr))
            {
                return args;
            }

            // Simple split by comma (no support for quoted strings with commas yet)
            var parts = argsStr.Split(',');
            foreach (var part in parts)
            {
                args.Add(part.Trim());
            }

            return args;
        }
    }
}
