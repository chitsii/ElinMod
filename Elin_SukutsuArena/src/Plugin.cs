using BepInEx;
using HarmonyLib;
using UnityEngine;
using System.Reflection;
using System.Collections;
using Elin_SukutsuArena.Core;

namespace Elin_SukutsuArena;

/// <summary>
/// 巣窟アリーナ Mod プラグインエントリ
/// </summary>
[BepInPlugin(ModGuid, "Sukutsu Arena", "0.1.0")]
public class Plugin : BaseUnityPlugin
{
    public const string ModGuid = "tishi.elin.sukutsu_arena";
    public const string ZoneId = "sukutsu_arena";

    private void Awake()
    {
        new Harmony(ModGuid).PatchAll();
        Debug.Log("[SukutsuArena] Plugin loaded.");
#if DEBUG
        Debug.Log("[SukutsuArena] Debug Keys:");
        Debug.Log("[SukutsuArena]   F9: Arena status (rank/flags/quests)");
        Debug.Log("[SukutsuArena]   F11: Complete next available quest");
        Debug.Log("[SukutsuArena]   F12: Cycle rank up");
#endif
    }

#if DEBUG
    private void Update()
    {
        // ゲームがロードされていない場合はスキップ
        if (EMono.core == null || EMono.game == null) return;

        // F9: アリーナステータス表示
        if (Input.GetKeyDown(KeyCode.F9))
        {
            ShowArenaStatus();
        }

        // F11: 次の利用可能なクエストを完了
        if (Input.GetKeyDown(KeyCode.F11))
        {
            CompleteNextQuest();
        }

        // F12: ランクを1つ上げる
        if (Input.GetKeyDown(KeyCode.F12))
        {
            CycleRankUp();
        }
    }
#endif

    /// <summary>
    /// CWLのManagedゾーンからSourceZone.Rowを取得
    /// 公開APIを優先し、非公開フィールドはフォールバックとして使用
    /// </summary>
    private static bool TryGetCwlManagedZone(string zoneId, out SourceZone.Row row)
    {
        row = null;
        try
        {
            var customZoneType = AccessTools.TypeByName("Cwl.API.Custom.CustomZone");
            if (customZoneType == null)
            {
                Debug.Log("[SukutsuArena] CWL CustomZone type not found");
                return false;
            }

            // 1. 公開プロパティを優先
            var managedProp = customZoneType.GetProperty("Managed", BindingFlags.Static | BindingFlags.Public);
            if (managedProp != null)
            {
                var managed = managedProp.GetValue(null) as IDictionary;
                if (managed != null && managed.Contains(zoneId))
                {
                    row = managed[zoneId] as SourceZone.Row;
                    return row != null;
                }
            }

            // 2. 公開フィールドを試す
            var managedFieldPublic = customZoneType.GetField("Managed", BindingFlags.Static | BindingFlags.Public);
            if (managedFieldPublic != null)
            {
                var managed = managedFieldPublic.GetValue(null) as IDictionary;
                if (managed != null && managed.Contains(zoneId))
                {
                    row = managed[zoneId] as SourceZone.Row;
                    return row != null;
                }
            }

            // 3. フォールバック: 非公開フィールド（警告付き）
            var managedFieldNonPublic = customZoneType.GetField("Managed", BindingFlags.Static | BindingFlags.NonPublic);
            if (managedFieldNonPublic != null)
            {
                Debug.LogWarning("[SukutsuArena] Using non-public CWL field - may break with CWL updates");
                var managed = managedFieldNonPublic.GetValue(null) as IDictionary;
                if (managed != null && managed.Contains(zoneId))
                {
                    row = managed[zoneId] as SourceZone.Row;
                    return row != null;
                }
            }

            return false;
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"[SukutsuArena] CWL access failed: {ex.Message}");
            return false;
        }
    }

    private static void InjectZoneData()
    {
        if (EMono.sources.zones.map.ContainsKey(ZoneId))
        {
            return;
        }

        Debug.Log($"[SukutsuArena] Injecting zone data from CWL Managed...");

        if (TryGetCwlManagedZone(ZoneId, out var row))
        {
            EMono.sources.zones.rows.Add(row);
            EMono.sources.zones.map[ZoneId] = row;
            Debug.Log($"[SukutsuArena] Successfully injected {ZoneId} from CustomZone!");
        }
        else
        {
            Debug.LogError($"[SukutsuArena] Failed to inject: ZoneId not in CWL Managed.");
        }
    }

    private void EnterZone()
    {
        var zone = EMono.world?.region?.FindZone(ZoneId);
        if (zone == null)
        {
            Debug.LogError($"[SukutsuArena] Zone '{ZoneId}' not found. Try F7 first.");
            Msg.Say($"[SukutsuArena] ゾーンが見つかりません。F7で生成してください。");
            return;
        }

        Debug.Log($"[SukutsuArena] Entering zone '{ZoneId}'...");
        Msg.Say($"[SukutsuArena] ゾーン '{zone.Name}' に入ります...");
        EMono.player.MoveZone(zone);
    }

#if DEBUG
    private void ShowArenaStatus()
    {
        Debug.Log("[SukutsuArena] === Arena Status ===");

        // フラグ状態を表示
        var ctx = ArenaContext.I;
        Debug.Log($"  Rank: {ctx.Player.Rank}");
        Debug.Log($"  Phase: {ctx.Player.CurrentPhase}");
        Debug.Log($"  Karma: {ctx.Player.Karma}");
        Debug.Log($"  Contribution: {ctx.Player.Contribution}");
        Debug.Log($"  Rel.Lily: {ctx.Rel.Lily}");
        Debug.Log($"  Rel.Balgas: {ctx.Rel.Balgas}");
        Debug.Log($"  Rel.Zek: {ctx.Rel.Zek}");

        // クエスト状態を表示
        ArenaQuestManager.Instance.DebugLogQuestState();

        // 画面にも表示
        var rank = ctx.Player.Rank;
        var gladiator = ctx.Storage.GetInt("sukutsu_gladiator") != 0;
        Msg.Say($"[Arena] Rank: {rank}, Gladiator: {gladiator}");
        Msg.Say($"[Arena] Lily: {ctx.Rel.Lily}, Balgas: {ctx.Rel.Balgas}");

        var available = ArenaQuestManager.Instance.GetAvailableQuests();
        if (available.Count > 0)
        {
            Msg.Say($"[Arena] Available Quests: {available.Count}");
            foreach (var quest in available)
            {
                Msg.Say($"  - {quest.QuestId}: {quest.DisplayNameJP}");
            }
        }
        else
        {
            Msg.Say("[Arena] No quests available");
        }
    }

    private void CycleRankUp()
    {
        var ctx = ArenaContext.I;
        var currentRank = ctx.Player.Rank;
        var nextRank = currentRank + 1;

        // 最大ランクを超えないようにする
        if (nextRank > Flags.Rank.S)
        {
            nextRank = Flags.Rank.Unranked;
        }

        ctx.Player.Rank = nextRank;
        Debug.Log($"[SukutsuArena] Rank changed: {currentRank} -> {nextRank}");
        Msg.Say($"[Arena] Rank: {currentRank} -> {nextRank}");

        // 闘士登録も確認
        if (ctx.Storage.GetInt("sukutsu_gladiator") == 0)
        {
            ctx.Storage.SetInt("sukutsu_gladiator", 1);
            Msg.Say("[Arena] Gladiator status set to true");
        }

        // デバッグ用: 前提クエストを完了済みにする
        CompletePrerequisiteQuests(nextRank);
    }

    /// <summary>
    /// 指定ランクまでの前提クエストを全て完了済みにする（デバッグ用）
    /// </summary>
    private void CompletePrerequisiteQuests(Flags.Rank rank)
    {
        // 常にオープニングを完了
        ArenaQuestManager.Instance.CompleteQuest("01_opening");

        // ランクに応じて昇格試験クエストを完了
        if (rank >= Flags.Rank.G)
        {
            ArenaQuestManager.Instance.CompleteQuest("02_rank_up_G");
        }
        if (rank >= Flags.Rank.F)
        {
            ArenaQuestManager.Instance.CompleteQuest("04_rank_up_F");
        }
        if (rank >= Flags.Rank.E)
        {
            ArenaQuestManager.Instance.CompleteQuest("06_rank_up_E");
        }
        if (rank >= Flags.Rank.D)
        {
            ArenaQuestManager.Instance.CompleteQuest("10_rank_up_D");
        }
        if (rank >= Flags.Rank.C)
        {
            ArenaQuestManager.Instance.CompleteQuest("09_rank_up_C");
        }
        if (rank >= Flags.Rank.B)
        {
            ArenaQuestManager.Instance.CompleteQuest("11_rank_up_B");
        }

        Debug.Log($"[SukutsuArena] Prerequisite quests completed for rank {rank}");
        Msg.Say($"[Arena] Prerequisite quests completed");
    }

    private void CompleteNextQuest()
    {
        var available = ArenaQuestManager.Instance.GetAvailableQuests();
        if (available.Count == 0)
        {
            Debug.Log("[SukutsuArena] No quests available to complete.");
            Msg.Say("[Arena] No quests available");
            return;
        }

        var quest = available[0];
        ArenaQuestManager.Instance.CompleteQuest(quest.QuestId);
        Debug.Log($"[SukutsuArena] Completed quest: {quest.QuestId}");
        Msg.Say($"[Arena] Completed: {quest.QuestId}");
        Msg.Say($"[Arena] ({quest.DisplayNameJP})");
    }
#endif

    /// <summary>
    /// Region.CheckRandomSites でゾーンが存在しなければ生成する
    /// </summary>
    [HarmonyPatch(typeof(Region), nameof(Region.CheckRandomSites))]
    public static class CheckRandomSitesPatch
    {
        [HarmonyPostfix]
        public static void Postfix(Region __instance)
        {
            // まずデータを注入
            InjectZoneData();

            if (__instance.FindZone(ZoneId) != null)
            {
                return;
            }

            Debug.Log($"[SukutsuArena] Creating zone '{ZoneId}'...");
            try
            {
                SpatialGen.Create(ZoneId, __instance, register: true, x: -99999, y: -99999, 0);
                Debug.Log($"[SukutsuArena] Zone '{ZoneId}' created successfully!");
            }
            catch (System.Exception ex)
            {
                Debug.LogError($"[SukutsuArena] Failed to create zone: {ex}");
            }
        }
    }
}
