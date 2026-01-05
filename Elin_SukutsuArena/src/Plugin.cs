using BepInEx;
using HarmonyLib;
using UnityEngine;
using System.Reflection;
using System.Collections;

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
        Debug.Log("[SukutsuArena] Debug Keys:");
        Debug.Log("[SukutsuArena]   F6: Zone debug info");
        Debug.Log("[SukutsuArena]   F7: Force create zone");
        Debug.Log("[SukutsuArena]   F8: Enter zone");
        Debug.Log("[SukutsuArena]   F9: Arena status (rank/flags/quests)");
        Debug.Log("[SukutsuArena]   F10: Cycle rank up");
        Debug.Log("[SukutsuArena]   F11: Complete next available quest");

    }

    private void Update()
    {
        // ゲームがロードされていない場合はスキップ
        if (EMono.core == null || EMono.game == null) return;

        // F6: デバッグ情報表示
        if (Input.GetKeyDown(KeyCode.F6))
        {
            ShowDebugInfo();
        }

        // F7: 強制ゾーン生成
        if (Input.GetKeyDown(KeyCode.F7))
        {
            ForceCreateZone();
        }

        // F8: ゾーンに入場
        if (Input.GetKeyDown(KeyCode.F8))
        {
            EnterZone();
        }

        // F9: アリーナステータス表示
        if (Input.GetKeyDown(KeyCode.F9))
        {
            ShowArenaStatus();
        }

        // F10: ランクを1つ上げる
        if (Input.GetKeyDown(KeyCode.F10))
        {
            CycleRankUp();
        }

        // F11: 次の利用可能なクエストを完了
        if (Input.GetKeyDown(KeyCode.F11))
        {
            CompleteNextQuest();
        }
    }

    private void ShowDebugInfo()
    {
        var zone = EMono.world?.region?.FindZone(ZoneId);
        if (zone == null)
        {
            Debug.Log($"[SukutsuArena] Zone '{ZoneId}' NOT FOUND in world.region.");
            Debug.Log($"[SukutsuArena] SourceZone in map: {EMono.sources.zones.map.ContainsKey(ZoneId)}");

            // rows も確認
            var inRows = false;
            foreach (var row in EMono.sources.zones.rows)
            {
                if (row.id == ZoneId)
                {
                    inRows = true;
                    Debug.Log($"[SukutsuArena] Found in rows: id={row.id}, type={row.type}");
                    break;
                }
            }
            if (!inRows)
            {
                Debug.Log($"[SukutsuArena] NOT FOUND in rows either.");
            }

            // CWL Managed 確認
            CheckCwlManaged();

            Msg.Say($"[SukutsuArena] ゾーン '{ZoneId}' が見つかりません。F7で生成を試してください。");
        }
        else
        {
            Debug.Log($"[SukutsuArena] Zone Debug Info:");
            Debug.Log($"  ID: {zone.id}");
            Debug.Log($"  Name: {zone.Name}");
            Debug.Log($"  Position: ({zone.x}, {zone.y})");
            Debug.Log($"  UID: {zone.uid}");
            Debug.Log($"  Type: {zone.GetType().Name}");

            Msg.Say($"[SukutsuArena] ゾーン発見: {zone.Name} ({zone.x}, {zone.y})");
        }
    }

    private void CheckCwlManaged()
    {
        try
        {
            var customZoneType = AccessTools.TypeByName("Cwl.API.Custom.CustomZone");
            if (customZoneType != null)
            {
                var managedField = customZoneType.GetField("Managed", BindingFlags.Static | BindingFlags.NonPublic | BindingFlags.Public);
                if (managedField != null)
                {
                    var managed = managedField.GetValue(null) as IDictionary;
                    if (managed != null && managed.Contains(ZoneId))
                    {
                        Debug.Log($"[SukutsuArena] Found in CWL Managed!");
                    }
                    else
                    {
                        Debug.Log($"[SukutsuArena] NOT FOUND in CWL Managed.");
                    }
                }
            }
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"[SukutsuArena] Failed to check CWL Managed: {ex}");
        }
    }

    private void ForceCreateZone()
    {
        // 生成前にデータ注入を試みる
        InjectZoneData();

        var region = EMono.world?.region;
        if (region == null)
        {
            Debug.LogError("[SukutsuArena] World region not available.");
            Msg.Say("[SukutsuArena] ワールドリージョンが利用できません。");
            return;
        }

        var existingZone = region.FindZone(ZoneId);
        if (existingZone != null)
        {
            Debug.Log($"[SukutsuArena] Zone already exists at ({existingZone.x}, {existingZone.y}).");
            Msg.Say($"[SukutsuArena] ゾーンは既に存在します: ({existingZone.x}, {existingZone.y})");
            return;
        }

        try
        {
            Debug.Log("[SukutsuArena] Attempting to create zone...");
            SpatialGen.Create(ZoneId, region, register: true, x: -99999, y: -99999, 0);

            var newZone = region.FindZone(ZoneId);
            if (newZone != null)
            {
                Debug.Log($"[SukutsuArena] Zone created successfully at ({newZone.x}, {newZone.y})!");
                Msg.Say($"[SukutsuArena] ゾーン生成成功: ({newZone.x}, {newZone.y})");

                // マップを更新
                EMono.scene.elomap?.objmap?.UpdateMeshImmediate();
            }
            else
            {
                Debug.LogError("[SukutsuArena] SpatialGen.Create returned but zone not found.");
                Msg.Say("[SukutsuArena] ゾーン生成失敗: SpatialGen は返ったが見つかりません。");
            }
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"[SukutsuArena] Failed to create zone: {ex}");
            Msg.Say($"[SukutsuArena] ゾーン生成エラー: {ex.Message}");
        }
    }

    private static void InjectZoneData()
    {
        if (EMono.sources.zones.map.ContainsKey(ZoneId))
        {
            return;
        }

        Debug.Log($"[SukutsuArena] Injecting zone data from CWL Managed...");
        try
        {
            var customZoneType = AccessTools.TypeByName("Cwl.API.Custom.CustomZone");
            if (customZoneType != null)
            {
                var managedField = customZoneType.GetField("Managed", BindingFlags.Static | BindingFlags.NonPublic | BindingFlags.Public);
                if (managedField != null)
                {
                    var managed = managedField.GetValue(null) as IDictionary;
                    if (managed != null && managed.Contains(ZoneId))
                    {
                        var row = managed[ZoneId] as SourceZone.Row;
                        if (row != null)
                        {
                            EMono.sources.zones.rows.Add(row);
                            EMono.sources.zones.map[ZoneId] = row;
                            Debug.Log($"[SukutsuArena] Successfully injected {ZoneId} from CustomZone!");
                        }
                    }
                    else
                    {
                        Debug.LogError($"[SukutsuArena] Failed to inject: ZoneId not in CWL Managed.");
                    }
                }
            }
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"[SukutsuArena] Failed to inject zone data: {ex}");
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

    private void ShowArenaStatus()
    {
        Debug.Log("[SukutsuArena] === Arena Status ===");

        // フラグ状態を表示
        ArenaFlagManager.DebugLogAllFlags();

        // クエスト状態を表示
        ArenaQuestManager.Instance.DebugLogQuestState();

        // 画面にも表示
        var rank = ArenaFlagManager.Player.GetRank();
        var gladiator = ArenaFlagManager.GetBool("sukutsu_gladiator");
        Msg.Say($"[Arena] Rank: {rank}, Gladiator: {gladiator}");
        Msg.Say($"[Arena] Lily: {ArenaFlagManager.Rel.Lily}, Balgas: {ArenaFlagManager.Rel.Balgas}");

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
        var currentRank = ArenaFlagManager.Player.GetRank();
        var nextRank = currentRank + 1;

        // 最大ランクを超えないようにする
        if (nextRank > Flags.Rank.S)
        {
            nextRank = Flags.Rank.Unranked;
        }

        ArenaFlagManager.Player.SetRank(nextRank);
        Debug.Log($"[SukutsuArena] Rank changed: {currentRank} -> {nextRank}");
        Msg.Say($"[Arena] Rank: {currentRank} -> {nextRank}");

        // 闘士登録も確認
        if (!ArenaFlagManager.GetBool("sukutsu_gladiator"))
        {
            ArenaFlagManager.SetBool("sukutsu_gladiator", true);
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
