using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Newtonsoft.Json;
using UnityEngine;
using Elin_SukutsuArena.Core;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// ストーリーフェーズ（クエスト依存関係管理用）
    /// </summary>
    public enum StoryPhase
    {
        Prologue = 0,      // ゲーム開始〜初戦
        Initiation = 1,    // Rank G〜F
        Rising = 2,        // Rank E〜D
        Awakening = 3,     // Rank C〜B
        Confrontation = 4, // Rank A
        Climax = 5         // 逃亡〜最終決戦
    }

    /// <summary>
    /// クエスト管理クラス
    /// quest_definitions.jsonを読み込み、フラグ条件に基づいて利用可能なクエストを判定
    /// フェーズベースの依存関係管理をサポート
    /// </summary>
    public class ArenaQuestManager
    {
        private static ArenaQuestManager _instance;
        public static ArenaQuestManager Instance => _instance ?? (_instance = new ArenaQuestManager());

        private List<QuestDefinition> allQuests = new List<QuestDefinition>();

        private const string QuestDefinitionsPath = "Package/quest_definitions.json";
        private const string QuestCompletedFlagPrefix = "sukutsu_quest_done_";
        private const string CurrentPhaseFlagKey = "chitsii.arena.player.current_phase";

        /// <summary>
        /// NPCクエスト更新イベント（マーカー管理用）
        /// </summary>
        public event Action OnQuestStateChanged;

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

        // Enum mappings for string-to-int conversion (auto-generated from ArenaEnumMappings.cs)
        private static readonly Dictionary<string, Dictionary<string, int>> EnumMappings = ArenaEnumMappings.Mappings;

        /// <summary>
        /// 現在のストーリーフェーズを取得
        /// </summary>
        public StoryPhase GetCurrentPhase()
        {
            int phaseValue = ArenaContext.I.Storage.GetInt(CurrentPhaseFlagKey, 0);
            if (Enum.IsDefined(typeof(StoryPhase), phaseValue))
            {
                return (StoryPhase)phaseValue;
            }
            return StoryPhase.Prologue;
        }

        /// <summary>
        /// ストーリーフェーズを設定
        /// </summary>
        public void SetCurrentPhase(StoryPhase phase)
        {
            int oldPhase = ArenaContext.I.Storage.GetInt(CurrentPhaseFlagKey, 0);
            int newPhase = (int)phase;

            if (oldPhase != newPhase)
            {
                ArenaContext.I.Storage.SetInt(CurrentPhaseFlagKey, newPhase);
                Debug.Log($"[ArenaQuest] Phase advanced: {(StoryPhase)oldPhase} -> {phase}");
                OnQuestStateChanged?.Invoke();
            }
        }

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
        /// 利用可能なクエストを取得（フェーズベース依存関係を考慮）
        /// </summary>
        public List<QuestDefinition> GetAvailableQuests()
        {
            var available = new List<QuestDefinition>();
            var currentPhase = GetCurrentPhase();

            int completedCount = allQuests.Count(q => IsQuestCompleted(q.QuestId));
            Debug.Log($"[ArenaQuest] Checking {allQuests.Count} quests, {completedCount} completed, Phase: {currentPhase}");

            foreach (var quest in allQuests)
            {
                // 詳細ログ（アリーナマスターのクエストのみ）
                bool isArenaMasterQuest = quest.QuestGiver == "sukutsu_arena_master";

                // Already completed
                if (IsQuestCompleted(quest.QuestId))
                {
                    if (isArenaMasterQuest) Debug.Log($"[ArenaQuest] {quest.QuestId}: SKIP (completed)");
                    continue;
                }

                // Phase check: quest must be in current or earlier phase
                if (quest.Phase > currentPhase)
                {
                    if (isArenaMasterQuest) Debug.Log($"[ArenaQuest] {quest.QuestId}: SKIP (phase {quest.Phase} > current {currentPhase})");
                    continue;
                }

                // Check required quests
                bool missingPrerequisite = false;
                string missingQuestId = null;
                foreach (var reqQuestId in quest.RequiredQuests)
                {
                    if (!IsQuestCompleted(reqQuestId))
                    {
                        missingPrerequisite = true;
                        missingQuestId = reqQuestId;
                        break;
                    }
                }
                if (missingPrerequisite)
                {
                    if (isArenaMasterQuest) Debug.Log($"[ArenaQuest] {quest.QuestId}: SKIP (missing prerequisite: {missingQuestId})");
                    continue;
                }

                // Check required flags
                bool flagsFailed = false;
                string failedFlag = null;
                foreach (var flagCondition in quest.RequiredFlags)
                {
                    if (!CheckFlagCondition(flagCondition))
                    {
                        flagsFailed = true;
                        failedFlag = $"{flagCondition.FlagKey} {flagCondition.Operator} {flagCondition.Value}";
                        break;
                    }
                }
                if (flagsFailed)
                {
                    if (isArenaMasterQuest) Debug.Log($"[ArenaQuest] {quest.QuestId}: SKIP (flag failed: {failedFlag})");
                    continue;
                }

                if (isArenaMasterQuest) Debug.Log($"[ArenaQuest] {quest.QuestId}: AVAILABLE");
                available.Add(quest);
            }

            // Sort by priority (higher first)
            available.Sort((a, b) => b.Priority.CompareTo(a.Priority));
            return available;
        }

        /// <summary>
        /// 自動発動クエストを取得（ゾーン入場時に発動）
        /// </summary>
        public List<QuestDefinition> GetAutoTriggerQuests()
        {
            return GetAvailableQuests().Where(q => q.AutoTrigger).ToList();
        }

        /// <summary>
        /// 特定NPCが持つ利用可能なクエストを取得
        /// </summary>
        public List<QuestDefinition> GetQuestsForNpc(string npcId)
        {
            return GetAvailableQuests().Where(q => q.QuestGiver == npcId).ToList();
        }

        /// <summary>
        /// クエストを持っているNPCのIDリストを取得（マーカー表示用）
        /// </summary>
        public List<string> GetNpcsWithQuests()
        {
            return GetAvailableQuests()
                .Where(q => !string.IsNullOrEmpty(q.QuestGiver))
                .Select(q => q.QuestGiver)
                .Distinct()
                .ToList();
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

            // Advance phase if this quest triggers phase advancement
            if (quest.AdvancesPhase.HasValue)
            {
                SetCurrentPhase(quest.AdvancesPhase.Value);
            }

            // 次のクエストが自動開始できるようにトラッキングをリセット
            ArenaZonePatches.ResetQuestTriggerTracking();

            // Notify listeners (for NPC marker updates)
            OnQuestStateChanged?.Invoke();

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
        /// フラグ値を取得
        /// </summary>
        private object GetFlagValueAsObject(string flagKey)
        {
            return ArenaContext.I.Storage.GetInt(flagKey, 0);
        }

        /// <summary>
        /// フラグをJSONの値から設定
        /// </summary>
        private void SetFlagFromJson(string flagKey, object value)
        {
            var storage = ArenaContext.I.Storage;

            if (value is long || value is int)
            {
                storage.SetInt(flagKey, Convert.ToInt32(value));
            }
            else if (value is bool)
            {
                storage.SetInt(flagKey, (bool)value ? 1 : 0);
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
                        storage.SetInt(flagKey, intValue);
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
        /// デバッグ: 全クエストを完了済みにする
        /// </summary>
        public void DebugCompleteAllQuests()
        {
            Debug.Log("[ArenaQuest] DEBUG: Completing all quests...");
            int count = 0;
            foreach (var quest in allQuests)
            {
                if (!IsQuestCompleted(quest.QuestId))
                {
                    MarkQuestCompleted(quest.QuestId);
                    count++;
                }
            }
            // フェーズを最終段階に
            SetCurrentPhase(StoryPhase.Climax);
            Debug.Log($"[ArenaQuest] DEBUG: Completed {count} quests, set phase to Climax");
            OnQuestStateChanged?.Invoke();
        }

        /// <summary>
        /// デバッグ: 全クエスト状態をログ出力
        /// </summary>
        public void DebugLogQuestState()
        {
            Debug.Log("[ArenaQuest] === Quest State ===");
            Debug.Log($"  Total Quests: {allQuests.Count}");
            Debug.Log($"  Current Phase: {GetCurrentPhase()}");

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
                string marker = quest.AutoTrigger ? "[AUTO]" : !string.IsNullOrEmpty(quest.QuestGiver) ? $"[{quest.QuestGiver}]" : "";
                Debug.Log($"    - {quest.QuestId} ({quest.Phase}) {marker} [Priority: {quest.Priority}]");
            }

            // NPCクエスト情報
            var npcsWithQuests = GetNpcsWithQuests();
            if (npcsWithQuests.Count > 0)
            {
                Debug.Log($"  NPCs with quests: {string.Join(", ", npcsWithQuests)}");
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

        // Phase system fields
        public string phase;
        public int phaseOrdinal;
        public string questGiver;
        public bool autoTrigger;
        public string advancesPhase;
        public int advancesPhaseOrdinal = -1;

        // Requirements
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

        // Phase system properties
        public StoryPhase Phase { get; }
        public string QuestGiver { get; }
        public bool AutoTrigger { get; }
        public StoryPhase? AdvancesPhase { get; }

        // Requirements
        public List<FlagCondition> RequiredFlags { get; }
        public List<string> RequiredQuests { get; }
        public Dictionary<string, object> CompletionFlags { get; }
        public List<string> BranchChoices { get; }
        public List<string> BlocksQuests { get; }
        public int Priority { get; }

        // Convenience properties
        public bool IsAutoTrigger => AutoTrigger && string.IsNullOrEmpty(QuestGiver);
        public bool IsNpcQuest => !string.IsNullOrEmpty(QuestGiver);

        public QuestDefinition(QuestData data)
        {
            QuestId = data.questId;
            QuestType = data.questType;
            DramaId = data.dramaId;
            DisplayNameJP = data.displayNameJP;
            DisplayNameEN = data.displayNameEN;
            Description = data.description;

            // Parse phase ordinal to enum
            Phase = (StoryPhase)data.phaseOrdinal;
            QuestGiver = data.questGiver;
            AutoTrigger = data.autoTrigger;

            // Parse advances phase (-1 means null/no advancement)
            if (data.advancesPhaseOrdinal >= 0 && Enum.IsDefined(typeof(StoryPhase), data.advancesPhaseOrdinal))
            {
                AdvancesPhase = (StoryPhase)data.advancesPhaseOrdinal;
            }
            else
            {
                AdvancesPhase = null;
            }

            RequiredFlags = data.requiredFlags?.Select(f => new FlagCondition(f)).ToList() ?? new List<FlagCondition>();
            RequiredQuests = data.requiredQuests ?? new List<string>();
            CompletionFlags = data.completionFlags ?? new Dictionary<string, object>();
            BranchChoices = data.branchChoices ?? new List<string>();
            BlocksQuests = data.blocksQuests ?? new List<string>();
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
