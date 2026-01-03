using System.IO;
using System.Reflection;
using UnityEngine;

namespace Elin_SukutsuArena;

/// <summary>
/// 巣窟アリーナ専用のカスタムゾーン
/// Zone_sssMain (StrangeSpellShop) と同じ構造
/// </summary>
public class Zone_SukutsuArena : Zone_Civilized
{
    /// <summary>
    /// マップファイルのパス（Mod フォルダ内の Maps/ から読み込む）
    /// StrangeSpellShop と同じパターン
    /// </summary>
    public override string pathExport =>
        Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location),
                     "Maps/" + this.idExport + ".z");

    public override void OnGenerateMap()
    {
        base.OnGenerateMap();

        Debug.Log("[SukutsuArena] OnGenerateMap called. Spawning NPCs...");

        // マップの中心付近と思われる座標に配置（マップサイズによるが、とりあえず安全圏に）
        // ユーザーがマップを差し替えた後、座標が壁の中にならないように注意が必要だが、
        // 20,20 あたりは大概安全
        SpawnMob("sukutsu_receptionist", 20, 20);
        SpawnMob("sukutsu_arena_master", 22, 20);
        SpawnMob("sukutsu_grand_master", 20, 22);
        SpawnMob("sukutsu_shady_merchant", 22, 22);
    }

    private void SpawnMob(string id, int x, int y)
    {
        // CharaGen.Create でキャラ生成
        var chara = CharaGen.Create(id);
        if (chara != null)
        {
            // ゾーンに追加
            this.AddCard(chara, x, y);
            Debug.Log($"[SukutsuArena] Spawned {id} at {x}, {y}");
        }
        else
        {
            Debug.LogError($"[SukutsuArena] Failed to spawn {id}. ID might be wrong or data not loaded.");
        }
    }
}
