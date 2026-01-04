using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Newtonsoft.Json;
using UnityEngine;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// クエスト管理クラス
    /// quest_definitions.jsonを読み込み、フラグ条件に基づいて利用可能なクエストを判定
    /// </summary>
    public class ArenaQuestManager
    {
        private static ArenaQuestManager _instance;
        public static ArenaQuestManager Instance => _instance ?? (_instance = new ArenaQuestManager());

        private List<QuestDefinition> allQuests = new List<QuestDefinition>();

        private const string QuestDefinitionsPath = "Package/quest_definitions.json";
        private const string QuestCompletedFlagPrefix = "sukutsu_quest_done_";

        /// <summary>
        /// クエスト完了フラグのキーを生成
        /// </summary>
        private static string GetQuestCompletedFlagKey(string questId)
        {
            return QuestCompletedFlagPrefix + questId;
        }

        /// <summary>
        /// クエストが完了済みかどうかをdialogFlagsから確認
        /// </summary>
        public bool IsQuestCompleted(string questId)
        {
            string flagKey = GetQuestCompletedFlagKey(questId);
            return EClass.player.dialogFlags.ContainsKey(flagKey)
                && EClass.player.dialogFlags[flagKey] == 1;
        }

        /// <summary>
        /// クエストを完了済みとしてマーク（dialogFlagsに保存）
        /// </summary>
        private void MarkQuestCompleted(string questId)
        {
            string flagKey = GetQuestCompletedFlagKey(questId);
            EClass.player.dialogFlags[flagKey] = 1;
            Debug.Log($"[ArenaQuest] Marked quest as completed in dialogFlags: {flagKey}");
        }

        // Enum mappings for string-to-int conversion
        private static readonly Dictionary<string, Dictionary<string, int>> EnumMappings = new Dictionary<string, Dictionary<string, int>>
        {
            {
                "chitsii.arena.player.rank", new Dictionary<string, int>
                {
                    { "unranked", 0 },
                    { "G", 1 },
                    { "F", 2 },
                    { "E", 3 },
                    { "D", 4 },
                    { "C", 5 },
                    { "B", 6 },
                    { "A", 7 },
                    { "S", 8 }
                }
            }
        };

        private ArenaQuestManager()
        {
            LoadQuestDefinitions();
        }

        /// <summary>
        /// quest_definitions.jsonを読み込み
        /// </summary>
        private void LoadQuestDefinitions()
        {
            try
            {
                var modPath = Path.GetDirectoryName(typeof(Plugin).Assembly.Location);
                var jsonPath = Path.Combine(modPath, QuestDefinitionsPath);

                if (!File.Exists(jsonPath))
                {
                    Debug.LogError($"[ArenaQuest] Quest definitions not found: {jsonPath}");
                    return;
                }

                var json = File.ReadAllText(jsonPath);
                var questDataList = JsonConvert.DeserializeObject<List<QuestData>>(json);

                allQuests.Clear();
                foreach (var data in questDataList)
                {
                    allQuests.Add(new QuestDefinition(data));
                }

                Debug.Log($"[ArenaQuest] Loaded {allQuests.Count} quest definitions");
            }
            catch (Exception ex)
            {
                Debug.LogError($"[ArenaQuest] Failed to load quest definitions: {ex}");
            }
        }

        /// <summary>
        /// 利用可能なクエストを取得
        /// </summary>
        public List<QuestDefinition> GetAvailableQuests()
        {
            var available = new List<QuestDefinition>();

            int completedCount = allQuests.Count(q => IsQuestCompleted(q.QuestId));
            Debug.Log($"[ArenaQuest] Checking {allQuests.Count} quests, {completedCount} completed");

            foreach (var quest in allQuests)
            {
                // Already completed
                if (IsQuestCompleted(quest.QuestId))
                {
                    Debug.Log($"[ArenaQuest]   {quest.QuestId}: Already completed");
                    continue;
                }

                // Check required quests
                bool missingPrerequisite = false;
                foreach (var reqQuestId in quest.RequiredQuests)
                {
                    if (!IsQuestCompleted(reqQuestId))
                    {
                        Debug.Log($"[ArenaQuest]   {quest.QuestId}: Missing prerequisite {reqQuestId}");
                        missingPrerequisite = true;
                        break;
                    }
                }
                if (missingPrerequisite) continue;

                // Check required flags
                bool flagsFailed = false;
                foreach (var flagCondition in quest.RequiredFlags)
                {
                    if (!CheckFlagCondition(flagCondition))
                    {
                        Debug.Log($"[ArenaQuest]   {quest.QuestId}: Flag condition failed: {flagCondition.FlagKey} {flagCondition.Operator} {flagCondition.Value}");
                        flagsFailed = true;
                        break;
                    }
                }
                if (flagsFailed) continue;

                Debug.Log($"[ArenaQuest]   {quest.QuestId}: AVAILABLE");
                available.Add(quest);
            }

            // Sort by priority (higher first)
            available.Sort((a, b) => b.Priority.CompareTo(a.Priority));
            return available;
        }

        /// <summary>
        /// 特定のクエストが利用可能かチェック
        /// </summary>
        public bool IsQuestAvailable(string questId)
        {
            return GetAvailableQuests().Any(q => q.QuestId == questId);
        }

        /// <summary>
        /// クエストを開始 (現時点では利用可能性のチェックのみ)
        /// </summary>
        public bool StartQuest(string questId)
        {
            if (!IsQuestAvailable(questId))
            {
                Debug.LogWarning($"[ArenaQuest] Cannot start quest '{questId}' - not available");
                return false;
            }

            Debug.Log($"[ArenaQuest] Starting quest: {questId}");
            return true;
        }

        /// <summary>
        /// クエストを完了
        /// </summary>
        public void CompleteQuest(string questId)
        {
            Debug.Log($"[ArenaQuest] CompleteQuest called for: {questId}");

            var quest = allQuests.FirstOrDefault(q => q.QuestId == questId);
            if (quest == null)
            {
                Debug.LogError($"[ArenaQuest] Quest not found: {questId}");
                Debug.LogError($"[ArenaQuest] Available quest IDs: {string.Join(", ", allQuests.Select(q => q.QuestId))}");
                return;
            }

            if (IsQuestCompleted(questId))
            {
                Debug.LogWarning($"[ArenaQuest] Quest already completed: {questId}");
                return;
            }

            MarkQuestCompleted(questId);
            int completedCount = allQuests.Count(q => IsQuestCompleted(q.QuestId));
            Debug.Log($"[ArenaQuest] Marked quest as completed. Total completed: {completedCount}");

            // Apply completion flags
            foreach (var kvp in quest.CompletionFlags)
            {
                Debug.Log($"[ArenaQuest] Setting completion flag: {kvp.Key} = {kvp.Value}");
                SetFlagFromJson(kvp.Key, kvp.Value);
            }

            // 次のクエストが自動開始できるようにトラッキングをリセット
            ArenaZonePatches.ResetQuestTriggerTracking();

            Debug.Log($"[ArenaQuest] Successfully completed quest: {questId}");
        }

        /// <summary>
        /// フラグ条件をチェック
        /// </summary>
        private bool CheckFlagCondition(FlagCondition condition)
        {
            var currentValue = GetFlagValueAsObject(condition.FlagKey);

            // Handle different value types
            if (condition.Value is long || condition.Value is int)
            {
                // Integer comparison
                int currentInt = Convert.ToInt32(currentValue);
                int expectedInt = Convert.ToInt32(condition.Value);

                return condition.Operator switch
                {
                    "==" => currentInt == expectedInt,
                    "!=" => currentInt != expectedInt,
                    ">=" => currentInt >= expectedInt,
                    ">" => currentInt > expectedInt,
                    "<=" => currentInt <= expectedInt,
                    "<" => currentInt < expectedInt,
                    _ => false
                };
            }
            else if (condition.Value is string)
            {
                // String comparison - check if this is an enum flag
                string expectedStr = condition.Value.ToString();

                // Try to find enum mapping for this flag
                if (EnumMappings.ContainsKey(condition.FlagKey))
                {
                    var mapping = EnumMappings[condition.FlagKey];
                    if (mapping.ContainsKey(expectedStr))
                    {
                        // Convert string enum to int and compare
                        int currentInt = Convert.ToInt32(currentValue);
                        int expectedInt = mapping[expectedStr];

                        Debug.Log($"[ArenaQuest] Enum comparison: {condition.FlagKey} current={currentInt} expected={expectedInt} ('{expectedStr}')");

                        return condition.Operator switch
                        {
                            "==" => currentInt == expectedInt,
                            "!=" => currentInt != expectedInt,
                            ">=" => currentInt >= expectedInt,
                            ">" => currentInt > expectedInt,
                            "<=" => currentInt <= expectedInt,
                            "<" => currentInt < expectedInt,
                            _ => false
                        };
                    }
                }

                // Fallback to string comparison
                string currentStr = currentValue?.ToString() ?? "";
                return condition.Operator switch
                {
                    "==" => currentStr == expectedStr,
                    "!=" => currentStr != expectedStr,
                    _ => false
                };
            }
            else if (condition.Value is bool)
            {
                // Boolean comparison
                bool currentBool = Convert.ToBoolean(currentValue);
                bool expectedBool = (bool)condition.Value;

                return condition.Operator switch
                {
                    "==" => currentBool == expectedBool,
                    "!=" => currentBool != expectedBool,
                    _ => false
                };
            }

            return false;
        }

        /// <summary>
        /// フラグ値を取得 (ArenaFlagManagerのラッパー)
        /// </summary>
        private object GetFlagValueAsObject(string flagKey)
        {
            // Use ArenaFlagManager to get the raw int value
            return ArenaFlagManager.GetInt(flagKey, 0);
        }

        /// <summary>
        /// フラグをJSONの値から設定
        /// </summary>
        private void SetFlagFromJson(string flagKey, object value)
        {
            if (value is long || value is int)
            {
                ArenaFlagManager.SetInt(flagKey, Convert.ToInt32(value));
            }
            else if (value is bool)
            {
                ArenaFlagManager.SetBool(flagKey, (bool)value);
            }
            else if (value is string)
            {
                // For string enums, convert to int using mapping
                string strValue = value.ToString();

                if (EnumMappings.ContainsKey(flagKey))
                {
                    var mapping = EnumMappings[flagKey];
                    if (mapping.ContainsKey(strValue))
                    {
                        int intValue = mapping[strValue];
                        Debug.Log($"[ArenaQuest] Setting enum flag: {flagKey} = {intValue} ('{strValue}')");
                        ArenaFlagManager.SetInt(flagKey, intValue);
                        return;
                    }
                }

                Debug.LogWarning($"[ArenaQuest] String flag value has no mapping: {flagKey} = {value}");
            }
        }

        /// <summary>
        /// クエスト定義を取得
        /// </summary>
        public QuestDefinition GetQuest(string questId)
        {
            return allQuests.FirstOrDefault(q => q.QuestId == questId);
        }

        /// <summary>
        /// デバッグ: 全クエスト状態をログ出力
        /// </summary>
        public void DebugLogQuestState()
        {
            Debug.Log("[ArenaQuest] === Quest State ===");
            Debug.Log($"  Total Quests: {allQuests.Count}");

            int completedCount = allQuests.Count(q => IsQuestCompleted(q.QuestId));
            Debug.Log($"  Completed: {completedCount}");

            // 完了済みクエストを表示
            var completedQuests = allQuests.Where(q => IsQuestCompleted(q.QuestId)).ToList();
            foreach (var quest in completedQuests)
            {
                Debug.Log($"    [DONE] {quest.QuestId}");
            }

            var available = GetAvailableQuests();
            Debug.Log($"  Available: {available.Count}");

            foreach (var quest in available)
            {
                Debug.Log($"    - {quest.QuestId} ({quest.QuestType}) [Priority: {quest.Priority}]");
            }

            Debug.Log("[ArenaQuest] === End ===");
        }
    }

    /// <summary>
    /// クエスト定義 (JSON deserialize用)
    /// </summary>
    [Serializable]
    public class QuestData
    {
        public string questId;
        public string questType;
        public string dramaId;
        public string displayNameJP;
        public string displayNameEN;
        public string description;
        public List<FlagConditionData> requiredFlags = new List<FlagConditionData>();
        public List<string> requiredQuests = new List<string>();
        public Dictionary<string, object> completionFlags = new Dictionary<string, object>();
        public List<string> branchChoices = new List<string>();
        public List<string> blocksQuests = new List<string>();
        public int priority;
    }

    [Serializable]
    public class FlagConditionData
    {
        public string flagKey;
        [JsonProperty("operator")]
        public string op;
        public object value;
    }

    /// <summary>
    /// クエスト定義 (内部使用)
    /// </summary>
    public class QuestDefinition
    {
        public string QuestId { get; }
        public string QuestType { get; }
        public string DramaId { get; }
        public string DisplayNameJP { get; }
        public string DisplayNameEN { get; }
        public string Description { get; }
        public List<FlagCondition> RequiredFlags { get; }
        public List<string> RequiredQuests { get; }
        public Dictionary<string, object> CompletionFlags { get; }
        public List<string> BranchChoices { get; }
        public List<string> BlocksQuests { get; }
        public int Priority { get; }

        public QuestDefinition(QuestData data)
        {
            QuestId = data.questId;
            QuestType = data.questType;
            DramaId = data.dramaId;
            DisplayNameJP = data.displayNameJP;
            DisplayNameEN = data.displayNameEN;
            Description = data.description;
            RequiredFlags = data.requiredFlags.Select(f => new FlagCondition(f)).ToList();
            RequiredQuests = data.requiredQuests;
            CompletionFlags = data.completionFlags;
            BranchChoices = data.branchChoices;
            BlocksQuests = data.blocksQuests;
            Priority = data.priority;
        }
    }

    /// <summary>
    /// フラグ条件
    /// </summary>
    public class FlagCondition
    {
        public string FlagKey { get; }
        public string Operator { get; }
        public object Value { get; }

        public FlagCondition(FlagConditionData data)
        {
            FlagKey = data.flagKey;
            Operator = data.op;
            Value = data.value;
        }
    }
}
