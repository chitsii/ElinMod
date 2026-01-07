using System.Collections.Generic;
using UnityEngine;
using Elin_SukutsuArena;

/// <summary>
/// ランダム戦闘の敵配置イベント
/// プレイヤーレベルに応じたランダムなモンスターを配置する
/// </summary>
public class ZonePreEnterRandomBattle : ZonePreEnterEvent
{
    // 難易度設定
    public ArenaDifficulty difficulty = ArenaDifficulty.Normal;
    public int minLevel = 1;
    public int maxLevel = 10;
    public int enemyCount = 3;

    // 敵対的モンスターのフィルター候補
    private static readonly string[] HostileFilters = new[]
    {
        "c_wilds",      // 野生動物
        "c_animal",     // 動物
        "c_undead",     // アンデッド
        "c_goblin",     // ゴブリン
        "c_orc",        // オーク
        "c_dragon",     // ドラゴン
        "c_demon",      // デーモン
        "c_elemental",  // エレメンタル
        "c_slime",      // スライム
        "c_insect",     // 昆虫
        "c_yeek",       // イーク
        "c_troll",      // トロール
        "c_giant",      // 巨人
        "c_minotaur",   // ミノタウロス
        "c_kobold",     // コボルド
        "c_fairy",      // 妖精
        "c_golem",      // ゴーレム
    };

    public override void Execute()
    {
        Debug.Log($"[SukutsuArena] ZonePreEnterRandomBattle.Execute() - difficulty={difficulty}, enemies={enemyCount}, level={minLevel}-{maxLevel}");

        // 既存のモブを掃除（プレイヤーと仲間以外）
        ClearExistingCharas();

        // プレイヤーの位置（中心のはず）
        Point centerPos = EClass._map.GetCenterPos();

        List<Chara> enemies = new List<Chara>();

        // ランダムに敵を生成
        for (int i = 0; i < enemyCount; i++)
        {
            Chara enemy = SpawnRandomEnemy(centerPos, i);
            if (enemy != null)
            {
                enemies.Add(enemy);
            }
        }

        // 全ての敵を敵対化
        foreach (Chara enemy in enemies)
        {
            enemy.hostility = Hostility.Enemy;
            enemy.c_originalHostility = Hostility.Enemy;
            enemy.SetEnemy(EClass.pc);
            enemy.HealAll();
        }

        // BGM設定（デフォルト戦闘BGM）
        EClass._zone.SetBGM(102);

        // 開始メッセージ
        string difficultyName = GetDifficultyName(difficulty);
        Msg.Say($"【{difficultyName}】ランダム戦闘 開始！ 敵{enemies.Count}体");
    }

    /// <summary>
    /// ランダムな敵を1体生成
    /// </summary>
    private Chara SpawnRandomEnemy(Point centerPos, int index)
    {
        // レベルをランダムに決定
        int level = minLevel + EClass.rnd(maxLevel - minLevel + 1);

        Chara enemy = null;

        // フィルターからランダムに選んで敵を生成
        for (int attempt = 0; attempt < 10; attempt++)
        {
            string filter = HostileFilters[EClass.rnd(HostileFilters.Length)];

            try
            {
                enemy = CharaGen.CreateFromFilter(filter, level);
                if (enemy != null && !string.IsNullOrEmpty(enemy.id) && enemy.id != "chicken")
                {
                    break;
                }
            }
            catch
            {
                // フィルターが存在しない場合は無視
            }

            enemy = null;
        }

        // フィルターで生成できなかった場合のフォールバック
        if (enemy == null)
        {
            enemy = CreateFallbackEnemy(level);
        }

        if (enemy == null)
        {
            Debug.LogWarning($"[SukutsuArena] Failed to create random enemy at index {index}");
            return null;
        }

        // レベル調整
        if (enemy.LV < level)
        {
            enemy.SetLv(level);
        }

        // 難易度に応じてレアリティを上げる可能性
        ApplyDifficultyRarity(enemy);

        // 位置決定（中心から離れた場所）
        Point pos = GetSpawnPos(centerPos, 3 + (index % 4));

        // マップに追加
        EClass._zone.AddCard(enemy, pos);
        Debug.Log($"[SukutsuArena] Spawned random enemy: {enemy.Name} (Lv.{enemy.LV}) at {pos}");

        return enemy;
    }

    /// <summary>
    /// フォールバック敵を生成
    /// </summary>
    private Chara CreateFallbackEnemy(int level)
    {
        string[] fallbackIds = level < 20
            ? new[] { "putty", "rat", "kobold", "goblin" }
            : level < 50
                ? new[] { "orc", "orc_warrior", "yeek", "troll" }
                : new[] { "minotaur", "fire_drake", "lich", "demon" };

        string id = fallbackIds[EClass.rnd(fallbackIds.Length)];

        try
        {
            return CharaGen.Create(id);
        }
        catch
        {
            // 最終フォールバック
            return CharaGen.Create("putty");
        }
    }

    /// <summary>
    /// 難易度に応じてレアリティを設定
    /// </summary>
    private void ApplyDifficultyRarity(Chara enemy)
    {
        int rarityRoll = EClass.rnd(100);

        switch (difficulty)
        {
            case ArenaDifficulty.Easy:
                // レアリティ変更なし
                break;

            case ArenaDifficulty.Normal:
                // 10%でSuperior
                if (rarityRoll < 10)
                {
                    enemy.ChangeRarity(Rarity.Superior);
                }
                break;

            case ArenaDifficulty.Hard:
                // 20%でSuperior, 5%でLegendary
                if (rarityRoll < 5)
                {
                    enemy.ChangeRarity(Rarity.Legendary);
                }
                else if (rarityRoll < 25)
                {
                    enemy.ChangeRarity(Rarity.Superior);
                }
                break;

            case ArenaDifficulty.VeryHard:
                // 30%でSuperior, 15%でLegendary, 5%でMythical
                if (rarityRoll < 5)
                {
                    enemy.ChangeRarity(Rarity.Mythical);
                }
                else if (rarityRoll < 20)
                {
                    enemy.ChangeRarity(Rarity.Legendary);
                }
                else if (rarityRoll < 50)
                {
                    enemy.ChangeRarity(Rarity.Superior);
                }
                break;
        }
    }

    /// <summary>
    /// 難易度名を取得
    /// </summary>
    private string GetDifficultyName(ArenaDifficulty diff)
    {
        return diff switch
        {
            ArenaDifficulty.Easy => "簡単",
            ArenaDifficulty.Normal => "普通",
            ArenaDifficulty.Hard => "難しい",
            ArenaDifficulty.VeryHard => "超難",
            _ => "不明"
        };
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

            // 距離制限（近すぎない）
            if (Mathf.Abs(dx) + Mathf.Abs(dy) < 2) continue;

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
}
