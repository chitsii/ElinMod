using UnityEngine;

namespace Elin_SukutsuArena;

/// <summary>
/// アリーナバトル管理クラス
/// CWLのevalアクションから呼び出される
/// </summary>
public static class ArenaManager
{
    /// <summary>
    /// ステージ設定
    /// </summary>
    public class StageConfig
    {
        public string[] MonsterIds { get; set; }
        public int[] MonsterLevels { get; set; }
        public int RewardPlat { get; set; }
        public string ZoneType { get; set; } = "field";  // 今後カスタムマップも可能
    }

    /// <summary>
    /// ステージ設定を取得
    /// </summary>
    public static StageConfig GetStageConfig(int stage)
    {
        return stage switch
        {
            1 => new StageConfig
            {
                MonsterIds = new[] { "hound" }, // 猟犬
                MonsterLevels = new[] { 20 },
                RewardPlat = 10,
                ZoneType = "field"
            },
            2 => new StageConfig
            {
                MonsterIds = new[] { "putty_snow" }, // スノーププチ
                MonsterLevels = new[] { 35 },
                RewardPlat = 30,
                ZoneType = "field" // snow ID不明のためfield
            },
            3 => new StageConfig
            {
                MonsterIds = new[] { "skeleton" }, // スケルトン（推測）
                MonsterLevels = new[] { 50 },
                RewardPlat = 50,
                ZoneType = "field" // cave ID不明のためfield
            },
            4 => new StageConfig
            {
                MonsterIds = new[] { "sukutsu_grand_master" },
                MonsterLevels = new[] { 80 },
                RewardPlat = 100,
                ZoneType = "field" // arena ID不明のためfield
            },
            _ => new StageConfig
            {
                MonsterIds = new[] { "hound" },
                MonsterLevels = new[] { 10 },
                RewardPlat = 5,
                ZoneType = "field"
            }
        };
    }

    /// <summary>
    /// 戦闘開始（CWL evalから呼び出し）
    /// </summary>
    /// <param name="master">アリーナマスター</param>
    /// <param name="stage">ステージ番号</param>
    public static void StartBattle(Chara master, int stage)
    {
        Debug.Log($"[SukutsuArena] StartBattle called: master={master?.Name}, stage={stage}");

        if (master == null)
        {
            Debug.LogError("[SukutsuArena] Arena Master is null!");
            return;
        }

        var config = GetStageConfig(stage);

        // 一時戦闘マップを作成
        Zone battleZone = SpatialGen.CreateInstance(config.ZoneType, new ZoneInstanceArenaBattle
        {
            uidMaster = master.uid,
            returnX = master.pos.x,
            returnZ = master.pos.z,
            uidZone = EClass._zone.uid,
            bossCount = config.MonsterIds.Length,
            stage = stage,
            rewardPlat = config.RewardPlat
        });

        // 敵配置イベントを追加
        battleZone.events.AddPreEnter(new ZonePreEnterArenaBattle
        {
            bossLevel = config.MonsterLevels[0],
            bossCount = config.MonsterIds.Length,
            bossIds = config.MonsterIds,
            stage = stage
        });

        Debug.Log($"[SukutsuArena] Created battle zone, moving player...");

        // ダイアログ終了後にゾーン移動
        LayerDrama.Instance?.SetOnKill(() =>
        {
            Debug.Log($"[SukutsuArena] Drama closed, moving to battle zone");
            EClass.pc.MoveZone(battleZone, ZoneTransition.EnterState.Center);
        });
    }
}
