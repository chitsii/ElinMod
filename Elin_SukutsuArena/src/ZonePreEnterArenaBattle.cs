using System.Collections.Generic;
using UnityEngine;
using Elin_SukutsuArena;

/// <summary>
/// アリーナ戦闘前のボス配置イベント
/// 戦闘マップに入った時にボスをスポーンさせる
/// </summary>
public class ZonePreEnterArenaBattle : ZonePreEnterEvent
{
    public int bossLevel = 50;
    public int bossCount = 1;

    // 固定ボスID（ランクに応じて変更可能）
    public string[] bossIds = new string[] { "hound" };  // デフォルト: 猟犬 (wolf ID無効のため)

    public int stage = 1;  // ステージ番号

    public bool isRankUp = false;

    // 新API用フィールド
    public string stageId = "";
    public BattleStageData stageData = null;

    public override void Execute()
    {
        Debug.Log("[SukutsuArena] ZonePreEnterArenaBattle.Execute()");

        // 既存のモブを掃除（プレイヤーと仲間以外）
        ClearExistingCharas();

        // プレイヤーの位置（中心のはず）
        Point centerPos = EClass._map.GetCenterPos();

        List<Chara> enemies = new List<Chara>();

        // 新API（stageData）が設定されている場合はそれを使用
        if (stageData != null)
        {
            Debug.Log($"[SukutsuArena] Using stageData for stage: {stageId}");
            SpawnEnemiesFromStageData(centerPos, enemies);
        }
        else
        {
            // 旧API（bossIds, bossLevel等）を使用
            Debug.Log($"[SukutsuArena] Using legacy config for stage: {stage}");
            SpawnEnemiesLegacy(centerPos, enemies);
        }

        // 全ての敵を敵対化
        foreach (Chara enemy in enemies)
        {
            enemy.hostility = Hostility.Enemy;
            enemy.c_originalHostility = Hostility.Enemy;
            enemy.SetEnemy(EClass.pc);
            enemy.HealAll();
        }

        // 勝利判定イベントを追加
        EClass._zone.events.Add(new ZoneEventArenaBattle());

        // 開始メッセージ
        if (stageData != null)
        {
            bool isJP = EClass.core.config.lang == "JP";
            string displayName = isJP ? stageData.DisplayNameJp : stageData.DisplayNameEn;
            Msg.Say($"{displayName} 開始！");
        }
        else
        {
            Msg.Say($"ステージ {stage} 開始！");
        }
    }

    /// <summary>
    /// 新API: stageDataから敵を生成
    /// </summary>
    private void SpawnEnemiesFromStageData(Point centerPos, List<Chara> enemies)
    {
        // BGM設定（stageDataから直接取得）
        string bgmPath = stageData?.BgmBattle;
        if (!string.IsNullOrEmpty(bgmPath))
        {
            Debug.Log($"[SukutsuArena] Setting custom BGM from stageData: {bgmPath}");
            PlayCustomBGM(bgmPath);
        }
        else
        {
            // arenaInstanceからも試す（フォールバック）
            var arenaInstance = EClass._zone.instance as ZoneInstanceArenaBattle;
            if (arenaInstance != null && !string.IsNullOrEmpty(arenaInstance.bgmBattle))
            {
                Debug.Log($"[SukutsuArena] Setting custom BGM from arenaInstance: {arenaInstance.bgmBattle}");
                PlayCustomBGM(arenaInstance.bgmBattle);
            }
            else
            {
                Debug.Log($"[SukutsuArena] No custom BGM, using default (102)");
                EClass._zone.SetBGM(102);  // デフォルト戦闘BGM
            }
        }

        int enemyIndex = 0;
        foreach (var enemyConfig in stageData.Enemies)
        {
            for (int i = 0; i < enemyConfig.Count; i++)
            {
                Chara enemy = SpawnSingleEnemy(enemyConfig, centerPos, enemyIndex);
                if (enemy != null)
                {
                    enemies.Add(enemy);
                    enemyIndex++;
                }
            }
        }

        Debug.Log($"[SukutsuArena] Spawned {enemies.Count} enemies from stageData");

        // ギミックの追加
        if (stageData.Gimmicks != null && stageData.Gimmicks.Count > 0)
        {
            foreach (var gimmickConfig in stageData.Gimmicks)
            {
                AddGimmickEvent(gimmickConfig);
            }
        }
    }

    /// <summary>
    /// ギミックイベントを追加
    /// </summary>
    private void AddGimmickEvent(GimmickConfig config)
    {
        if (string.IsNullOrEmpty(config.GimmickType)) return;

        switch (config.GimmickType)
        {
            case "audience_interference":
                var audienceEvent = new ZoneEventAudienceInterference
                {
                    // 基本設定
                    interval = config.Interval,
                    damage = config.Damage,
                    radius = config.Radius,
                    startDelay = config.StartDelay,
                    effectName = config.EffectName,
                    soundName = config.SoundName,
                    // エスカレーション設定
                    enableEscalation = config.EnableEscalation,
                    escalationRate = config.EscalationRate,
                    minInterval = config.MinInterval,
                    maxRadius = config.MaxRadius,
                    radiusGrowthInterval = config.RadiusGrowthInterval,
                    // アイテムドロップ設定
                    enableItemDrop = config.EnableItemDrop,
                    itemDropChance = config.ItemDropChance,
                    // 命中率設定
                    blastRadius = config.BlastRadius,
                    directHitChance = config.DirectHitChance,
                    explosionCount = config.ExplosionCount
                };
                EClass._zone.events.Add(audienceEvent);
                Debug.Log($"[SukutsuArena] Added gimmick: {config.GimmickType} (interval={config.Interval}, damage={config.Damage}, directHit={config.DirectHitChance}, blastRadius={config.BlastRadius})");
                break;

            default:
                Debug.LogWarning($"[SukutsuArena] Unknown gimmick type: {config.GimmickType}");
                break;
        }
    }

    /// <summary>
    /// 単体の敵を生成
    /// </summary>
    private Chara SpawnSingleEnemy(EnemyConfig config, Point centerPos, int index)
    {
        Chara enemy = null;

        // キャラ生成
        try
        {
            enemy = CharaGen.Create(config.CharaId);
        }
        catch
        {
            Debug.LogWarning($"[SukutsuArena] Failed to create enemy: {config.CharaId}");
        }

        // 生成失敗時のフォールバック
        if (enemy == null || enemy.id == "chicken")
        {
            if (enemy != null) enemy.Destroy();

            string fallbackId = (config.Level < 30) ? "putty" : "orc_warrior";
            try
            {
                enemy = CharaGen.Create(fallbackId);
                Debug.LogWarning($"[SukutsuArena] Used fallback: {fallbackId}");
            }
            catch
            {
                enemy = CharaGen.CreateFromFilter("c_neutral", config.Level);
            }
        }

        if (enemy == null) return null;

        // レベル設定
        if (enemy.LV < config.Level)
        {
            enemy.SetLv(config.Level);
        }

        // レアリティ設定
        switch (config.Rarity)
        {
            case "Superior":
                enemy.ChangeRarity(Rarity.Superior);
                break;
            case "Legendary":
                enemy.ChangeRarity(Rarity.Legendary);
                break;
            case "Mythical":
                enemy.ChangeRarity(Rarity.Mythical);
                break;
        }

        // 位置決定
        Point pos;
        if (config.Position == "fixed" && config.PositionX != 0 && config.PositionZ != 0)
        {
            pos = new Point(config.PositionX, config.PositionZ);
        }
        else if (config.Position == "center")
        {
            pos = centerPos;
        }
        else
        {
            pos = GetSpawnPos(centerPos, 3 + (index % 3));
        }

        // マップに追加
        EClass._zone.AddCard(enemy, pos);
        Debug.Log($"[SukutsuArena] Spawned: {enemy.Name} (Lv.{enemy.LV}, {config.Rarity}) at {pos}");

        return enemy;
    }

    /// <summary>
    /// 旧API: bossIds等から敵を生成
    /// </summary>
    private void SpawnEnemiesLegacy(Point centerPos, List<Chara> enemies)
    {
        Debug.Log($"[SukutsuArena] Spawning {bossCount} boss(es) (legacy)");

        // 戦闘BGM設定
        EClass._zone.SetBGM(102);

        for (int i = 0; i < bossCount; i++)
        {
            string bossId = (bossIds != null && i < bossIds.Length) ? bossIds[i] : "hound";
            Chara boss = null;

            try
            {
                boss = CharaGen.Create(bossId);
            }
            catch { }

            if (boss == null || boss.id == "chicken")
            {
                if (boss != null) boss.Destroy();

                string fallbackId = (bossLevel < 30) ? "putty" : "orc_warrior";
                try
                {
                    boss = CharaGen.Create(fallbackId);
                }
                catch
                {
                    boss = CharaGen.CreateFromFilter("c_neutral", bossLevel);
                }
            }

            if (boss.LV < bossLevel)
            {
                boss.SetLv(bossLevel);
            }

            if (stage >= 2)
            {
                boss.ChangeRarity(Rarity.Superior);
            }
            if (stage >= 4)
            {
                boss.ChangeRarity(Rarity.Legendary);
            }

            Point pos = GetSpawnPos(centerPos, 3 + (i % 3));
            EClass._zone.AddCard(boss, pos);
            enemies.Add(boss);

            Debug.Log($"[SukutsuArena] Spawned: {boss.Name} (Lv.{boss.LV}) at {pos}");
        }
    }

    /// <summary>
    /// 中心から指定距離離れた有効な座標を取得
    /// </summary>
    private Point GetSpawnPos(Point center, int distance)
    {
        for (int i = 0; i < 20; i++)
        {
            int dx = EClass.rnd(distance * 2 + 1) - distance;
            int dy = EClass.rnd(distance * 2 + 1) - distance;
            // 距離制限
            if (Mathf.Abs(dx) + Mathf.Abs(dy) < 2) continue; // 近すぎない

            Point p = new Point(center.x + dx, center.z + dy);
            if (p.IsValid && !p.IsBlocked && !p.HasChara)
            {
                return p;
            }
        }
        return center; // 失敗時は中心
    }

    /// <summary>
    /// 既存のキャラを削除（プレイヤー・仲間・特殊NPC以外）
    /// </summary>
    private void ClearExistingCharas()
    {
        List<Chara> toRemove = new List<Chara>();
        foreach (Chara c in EClass._map.charas)
        {
            if (c.IsPC || c.IsPCFaction) continue;
            toRemove.Add(c);
        }

        foreach (Chara c in toRemove)
        {
            c.Destroy();
        }
    }

    /// <summary>
    /// カスタムBGMを再生（ドラマと同じ方式）
    /// </summary>
    /// <param name="bgmPath">BGMパス（例: "BGM/Battle_Kain_Requiem"）</param>
    private void PlayCustomBGM(string bgmPath)
    {
        try
        {
            Debug.Log($"[SukutsuArena] Attempting to play BGM: {bgmPath}");
            var data = SoundManager.current.GetData(bgmPath);
            if (data != null)
            {
                Debug.Log($"[SukutsuArena] Found BGM data, type: {data.GetType().Name}");
                if (data is BGMData bgm)
                {
                    Debug.Log($"[SukutsuArena] Playing as BGM");
                    SoundManager.current.PlayBGM(bgm);
                }
                else
                {
                    Debug.Log($"[SukutsuArena] Data is not BGMData, playing as sound");
                    SoundManager.current.Play(data);
                }
            }
            else
            {
                Debug.LogWarning($"[SukutsuArena] BGM not found: {bgmPath}, using default");
                EClass._zone.SetBGM(102);
            }
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"[SukutsuArena] Error playing BGM: {ex.Message}\n{ex.StackTrace}");
            EClass._zone.SetBGM(102);
        }
    }
}
