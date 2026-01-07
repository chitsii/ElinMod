using System.Collections.Generic;
using UnityEngine;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// CWL DramaOutcome を継承したドラマアクションクラス
    /// invoke* アクションの param から自動的に呼び出される
    /// </summary>
    public class ArenaDramaActions : DramaOutcome
    {
        /// <summary>
        /// if_flag(flagKey, operatorValue)
        /// フラグ条件が真なら true を返す（jump列でジャンプ）
        /// operatorValue は "==1" のように演算子と値が結合された形式
        /// </summary>
        public static bool if_flag(DramaManager dm, Dictionary<string, string> line, params string[] parameters)
        {
            if (parameters.Length < 2)
            {
                Debug.LogError("[ArenaDrama] if_flag requires 2 args: flagKey, operatorValue");
                return false;
            }

            var flagKey = parameters[0];
            var operatorValue = parameters[1]; // e.g., "==1", ">=50"

            // Parse operator and value from combined string (e.g., "==1")
            string op = null;
            string valueStr = null;

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
                Debug.LogError($"[ArenaDrama] Cannot parse operator from: {operatorValue}");
                return false;
            }

            int currentValue = ArenaFlagManager.GetInt(flagKey, 0);

            if (!int.TryParse(valueStr, out int expectedValue))
            {
                Debug.LogWarning($"[ArenaDrama] Cannot parse value: {valueStr}");
                return false;
            }

            bool condition = op switch
            {
                "==" => currentValue == expectedValue,
                "!=" => currentValue != expectedValue,
                ">=" => currentValue >= expectedValue,
                ">" => currentValue > expectedValue,
                "<=" => currentValue <= expectedValue,
                "<" => currentValue < expectedValue,
                _ => false
            };

            Debug.Log($"[ArenaDrama] if_flag: {flagKey} {op} {expectedValue}, current={currentValue}, result={condition}");
            return condition;
        }

        /// <summary>
        /// complete_quest(questId)
        /// クエストを完了
        /// </summary>
        public static bool complete_quest(DramaManager dm, Dictionary<string, string> line, params string[] parameters)
        {
            if (parameters.Length < 1)
            {
                Debug.LogError("[ArenaDrama] complete_quest requires 1 arg: questId");
                return false;
            }

            var questId = parameters[0];
            Debug.Log($"[ArenaDrama] complete_quest: {questId}");
            ArenaQuestManager.Instance.CompleteQuest(questId);
            return true;
        }

        /// <summary>
        /// start_quest(questId)
        /// クエストを開始
        /// </summary>
        public static bool start_quest(DramaManager dm, Dictionary<string, string> line, params string[] parameters)
        {
            if (parameters.Length < 1)
            {
                Debug.LogError("[ArenaDrama] start_quest requires 1 arg: questId");
                return false;
            }

            var questId = parameters[0];
            Debug.Log($"[ArenaDrama] start_quest: {questId}");
            ArenaQuestManager.Instance.StartQuest(questId);
            return true;
        }

        /// <summary>
        /// check_quest_available(questId, jumpLabel)
        /// クエストが利用可能ならフラグを設定して true を返す
        /// </summary>
        public static bool check_quest_available(DramaManager dm, Dictionary<string, string> line, params string[] parameters)
        {
            if (parameters.Length < 2)
            {
                Debug.LogError("[ArenaDrama] check_quest_available requires 2 args: questId, jumpLabel");
                return false;
            }

            var questId = parameters[0];
            var jumpLabel = parameters[1];

            // 既に他のクエストが見つかっている場合はスキップ
            if (EClass.player.dialogFlags.ContainsKey("sukutsu_quest_found") &&
                EClass.player.dialogFlags["sukutsu_quest_found"] == 1)
            {
                Debug.Log($"[ArenaDrama] Quest already found, skipping check");
                return false;
            }

            bool available = ArenaQuestManager.Instance.IsQuestAvailable(questId);
            Debug.Log($"[ArenaDrama] check_quest_available: {questId} = {available}");

            if (available)
            {
                // クエストが見つかったフラグを設定
                EClass.player.dialogFlags["sukutsu_quest_found"] = 1;
                SetQuestTargetFlag(jumpLabel);
                Debug.Log($"[ArenaDrama] Quest found, setting flags for: {jumpLabel}");
            }

            return available;
        }

        /// <summary>
        /// start_random_battle(difficulty, masterId)
        /// ランダム戦闘を開始
        /// </summary>
        public static bool start_random_battle(DramaManager dm, Dictionary<string, string> line, params string[] parameters)
        {
            if (parameters.Length < 2)
            {
                Debug.LogError("[ArenaDrama] start_random_battle requires 2 args: difficulty, masterId");
                return false;
            }

            if (!int.TryParse(parameters[0], out int difficulty))
            {
                Debug.LogError($"[ArenaDrama] Invalid difficulty: {parameters[0]}");
                return false;
            }

            var masterId = parameters[1];
            Debug.Log($"[ArenaDrama] start_random_battle: difficulty={difficulty}, master={masterId}");

            ArenaManager.StartRandomBattle(difficulty, masterId);
            return true;
        }

        /// <summary>
        /// debug_log_flags()
        /// 全フラグをログ出力
        /// </summary>
        public static bool debug_log_flags(DramaManager dm, Dictionary<string, string> line, params string[] parameters)
        {
            ArenaFlagManager.DebugLogAllFlags();
            return true;
        }

        /// <summary>
        /// debug_log_quests()
        /// 全クエスト状態をログ出力
        /// </summary>
        public static bool debug_log_quests(DramaManager dm, Dictionary<string, string> line, params string[] parameters)
        {
            ArenaQuestManager.Instance.DebugLogQuestState();
            return true;
        }

        /// <summary>
        /// ジャンプ先ラベルに応じてクエストターゲットフラグを設定
        /// </summary>
        private static void SetQuestTargetFlag(string jumpLabel)
        {
            EClass.player.dialogFlags["sukutsu_quest_target"] = jumpLabel.GetHashCode();
            EClass.player.dialogFlags["sukutsu_quest_target_name"] = 0;

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
        }
    }
}
