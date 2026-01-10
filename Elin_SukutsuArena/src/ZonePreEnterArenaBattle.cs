using System.Collections.Generic;
using UnityEngine;
using Elin_SukutsuArena;

/// <summary>
/// アリーナ戦闘前のボス配置イベント
/// 戦闘マップに入った時にボスをスポーンさせる
/// </summary>
public class ZonePreEnterArenaBattle : ZonePreEnterEvent
{
    // ステージ設定
    public string stageId = "";
    public BattleStageData stageData = null;

    public override void Execute()
    {
        Debug.Log("[SukutsuArena] ZonePreEnterArenaBattle.Execute()");

        if (stageData == null)
        {
            Debug.LogError($"[SukutsuArena] stageData is null for stage: {stageId}");
            return;
        }

        // 既存のモブを掃除（プレイヤーと仲間以外）
        ClearExistingCharas();

        // プレイヤーの位置（中心のはず）
        Point centerPos = EClass._map.GetCenterPos();

        List<Chara> enemies = new List<Chara>();

        Debug.Log($"[SukutsuArena] Using stageData for stage: {stageId}");
        SpawnEnemiesFromStageData(centerPos, enemies);

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
        bool isJP = EClass.core.config.lang == "JP";
        string displayName = isJP ? stageData.DisplayNameJp : stageData.DisplayNameEn;
        Msg.Say($"{displayName} 開始！");
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

        // ========================================
        // 特殊キャラクター処理
        // ========================================

        // 影の自己: プレイヤーのステータスをコピー
        if (config.CharaId == "sukutsu_shadow_self")
        {
            ApplyShadowSelfStats(enemy);
        }

        // ボスキャラクター: 耐久（END）を10倍に設定してHP増加
        if (config.IsBoss)
        {
            ApplyBossEnduranceBoost(enemy);
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
        Debug.Log($"[SukutsuArena] Spawned: {enemy.Name} (Lv.{enemy.LV}, {config.Rarity}, Boss={config.IsBoss}) at {pos}");

        return enemy;
    }

    /// <summary>
    /// 影の自己にプレイヤーのステータスをコピー
    /// </summary>
    private void ApplyShadowSelfStats(Chara shadow)
    {
        var pc = EClass.pc;
        if (pc == null) return;

        Debug.Log($"[SukutsuArena] Applying Shadow Self stats from player...");

        // プレイヤーの主要ステータスをコピー
        // Element IDs: STR=70, END=71, DEX=73, PER=74, LER=75, WIL=76, MAG=77, CHA=79
        int[] mainStats = { 70, 71, 73, 74, 75, 76, 77, 79 };
        foreach (int statId in mainStats)
        {
            var pcElement = pc.elements.GetElement(statId);
            if (pcElement != null)
            {
                int pcValue = pcElement.ValueWithoutLink;
                shadow.elements.SetBase(statId, pcValue);
                Debug.Log($"[SukutsuArena] Shadow: Set stat {statId} = {pcValue}");
            }
        }

        // 戦闘関連ステータスもコピー
        // DV=152, PV=153
        int[] combatStats = { 152, 153 };
        foreach (int statId in combatStats)
        {
            var pcElement = pc.elements.GetElement(statId);
            if (pcElement != null)
            {
                int pcValue = pcElement.ValueWithoutLink;
                shadow.elements.SetBase(statId, pcValue);
                Debug.Log($"[SukutsuArena] Shadow: Set combat stat {statId} = {pcValue}");
            }
        }

        // ========================================
        // プレイヤーの外見（PCC）をコピー
        // ========================================
        CopyPlayerAppearance(shadow, pc);

        // ========================================
        // プレイヤーの装備をコピー
        // ========================================
        CopyPlayerEquipment(shadow, pc);

        // ========================================
        // アイテムドロップ無効化
        // ========================================
        shadow.noMove = false;  // 動けるようにはしておく
        // 装備品は全てisNPCProperty=trueでドロップ防止済み（CopyPlayerEquipmentで設定）
        Debug.Log($"[SukutsuArena] Shadow: Item drops disabled (via isNPCProperty)");

        // 影の名前をカスタマイズ（プレイヤー名を含める）
        shadow.c_altName = $"影の{pc.Name}";

        Debug.Log($"[SukutsuArena] Shadow Self stats applied. Name: {shadow.c_altName}");
    }

    /// <summary>
    /// プレイヤーの外見（PCC）を影にコピー
    /// </summary>
    private void CopyPlayerAppearance(Chara shadow, Chara pc)
    {
        Debug.Log($"[SukutsuArena] Copying player appearance to shadow...");

        try
        {
            // PCCデータをコピー（キャラチップの外見）
            if (pc.pccData != null)
            {
                shadow.pccData = pc.pccData;
                Debug.Log($"[SukutsuArena] Shadow: Copied pccData");
            }

            // 生物学的情報をコピー（性別のみ確実にアクセス可能）
            if (pc.bio != null && shadow.bio != null)
            {
                shadow.bio.SetGender(pc.bio.gender);
                shadow.bio.height = pc.bio.height;
                shadow.bio.weight = pc.bio.weight;
                Debug.Log($"[SukutsuArena] Shadow: Copied bio data (gender={pc.bio.gender})");
            }

            // スキンIDをコピー
            shadow.idSkin = pc.idSkin;
            Debug.Log($"[SukutsuArena] Shadow: Copied idSkin={pc.idSkin}");

            // レンダラーをリフレッシュ
            shadow.Refresh();
            Debug.Log($"[SukutsuArena] Shadow appearance copy complete");
        }
        catch (System.Exception ex)
        {
            Debug.LogWarning($"[SukutsuArena] Failed to copy appearance: {ex.Message}");
        }
    }

    /// <summary>
    /// プレイヤーの装備を影にコピー
    /// </summary>
    private void CopyPlayerEquipment(Chara shadow, Chara pc)
    {
        Debug.Log($"[SukutsuArena] Copying player equipment to shadow...");

        // 影の既存アイテムを全削除
        shadow.things.DestroyAll();

        // プレイヤーの装備スロットをイテレート（武器・防具のみ）
        // コンテナスロット(elementId=44)は除外
        foreach (var slot in pc.body.slots)
        {
            if (slot.thing == null) continue;

            // コンテナスロット(44)をスキップ
            if (slot.elementId == 44) continue;

            try
            {
                // 装備のコピーを作成
                Thing copy = slot.thing.Duplicate(1);
                if (copy != null)
                {
                    // コピーした装備はNPCプロパティとしてマーク（ドロップ防止）
                    copy.isNPCProperty = true;

                    // 影に装備させる
                    shadow.AddThing(copy);
                    shadow.body.Equip(copy);

                    Debug.Log($"[SukutsuArena] Shadow equipped: {copy.Name} in slot {slot.element?.alias ?? "unknown"}");
                }
            }
            catch (System.Exception ex)
            {
                Debug.LogWarning($"[SukutsuArena] Failed to copy equipment: {slot.thing.Name} - {ex.Message}");
            }
        }

        // 装備後にステータスを再計算
        shadow.Refresh();
        Debug.Log($"[SukutsuArena] Shadow equipment copy complete");
    }

    /// <summary>
    /// ボスキャラクターの耐久を10倍に設定
    /// </summary>
    private void ApplyBossEnduranceBoost(Chara boss)
    {
        // Element ID: END = 71
        const int END_ELEMENT_ID = 71;
        const int BOSS_ENDURANCE_MULTIPLIER = 10;

        var endElement = boss.elements.GetElement(END_ELEMENT_ID);
        int currentEnd = endElement?.ValueWithoutLink ?? 10;
        int boostedEnd = currentEnd * BOSS_ENDURANCE_MULTIPLIER;

        boss.elements.SetBase(END_ELEMENT_ID, boostedEnd);

        Debug.Log($"[SukutsuArena] Boss Endurance Boost: {boss.Name} END {currentEnd} -> {boostedEnd} (x{BOSS_ENDURANCE_MULTIPLIER})");
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
                    Debug.Log($"[SukutsuArena] Playing as BGM with haltPlaylist");
                    LayerDrama.haltPlaylist = true;  // ゾーンBGMによる上書きを防止
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
