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
        Debug.Log("[SukutsuArena] Press F6 to show debug info, F7 to force create zone, F8 to enter zone.");
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
