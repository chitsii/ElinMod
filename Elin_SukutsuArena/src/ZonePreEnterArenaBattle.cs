using System.Collections.Generic;
using UnityEngine;

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

    public override void Execute()
    {
        Debug.Log("[SukutsuArena] ZonePreEnterArenaBattle.Execute()");

        // 既存のモブを掃除（プレイヤーと仲間以外）
        ClearExistingCharas();

        // プレイヤーの位置（中心のはず）
        Point centerPos = EClass._map.GetCenterPos();

        // 敵のスポーン起点（中心から少し離す）
        Point spawnBaseInfo = centerPos.GetNearestPoint(allowBlock: false, allowChara: false) ?? centerPos;

        // 少しランダムに散らすためのオフセット用
        int attempts = 0;

        Debug.Log($"[SukutsuArena] Spawning {bossCount} boss(es) near {spawnBaseInfo}");

        // 戦闘BGM設定
        EClass._zone.SetBGM(102);  // 戦闘BGM

        List<Chara> enemies = new List<Chara>();

        for (int i = 0; i < bossCount; i++)
        {
            // ボス生成
            string bossId = (bossIds != null && i < bossIds.Length) ? bossIds[i] : "hound";
            Chara boss = null;

            // IDで直接生成を試みる
            try
            {
                boss = CharaGen.Create(bossId);
            }
            catch
            {
                // 失敗したらnullのまま
            }

            // 生成失敗、またはチキン（無効IDのフォールバック）になってしまった場合のリトライ
            if (boss == null || boss.id == "chicken")
            {
                if (boss != null) boss.Destroy(); // チキンなら消す

                string fallbackId = (bossLevel < 30) ? "putty" : "orc_warrior";
                try
                {
                    boss = CharaGen.Create(fallbackId);
                }
                catch
                {
                    // それでもダメならランダム生成
                    boss = CharaGen.CreateFromFilter("c_neutral", bossLevel);
                }
            }

            // レベル設定
            if (boss.LV < bossLevel)
            {
                boss.SetLv(bossLevel);
            }

            // レアリティ設定（ステージに応じて）
            // ステージ1は通常、2以降は強力に
            if (stage >= 2)
            {
                boss.ChangeRarity(Rarity.Superior);
            }
            if (stage >= 4) // ボス
            {
                boss.ChangeRarity(Rarity.Legendary);
            }

            // スポーン位置決定（中心から距離2-5の範囲）
            Point pos = GetSpawnPos(centerPos, 3 + (i % 3));

            // マップに追加
            EClass._zone.AddCard(boss, pos);
            enemies.Add(boss);

            Debug.Log($"[SukutsuArena] Spawned: {boss.Name} (Lv.{boss.LV}) at {pos}");
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

        Msg.Say($"ステージ {stage} 開始！");
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
}
