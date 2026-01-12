using UnityEngine;
using Elin_SukutsuArena;

/// <summary>
/// アリーナ戦闘進行監視イベント
/// 敵の全滅を監視し、勝利時にゾーン移動を行う
/// </summary>
public class ZoneEventArenaBattle : ZoneEvent
{
    private float checkTimer;
    private bool isGameFinished;
    private float victoryTimer = -1f;

    public override void OnTick()
    {
        // 戦闘中の帰還を禁止
        if (EClass.player.returnInfo != null)
        {
            EClass.player.returnInfo = null;
            Msg.Say("戦闘中は帰還できない！");
        }

        // 勝利後の待機処理
        if (victoryTimer >= 0f)
        {
            victoryTimer -= Core.delta;
            if (victoryTimer <= 0f)
            {
                var arenaInstance = EClass._zone.instance as ZoneInstanceArenaBattle;
                if (arenaInstance != null)
                {
                    arenaInstance.LeaveZone();
                }
                else
                {
                    // フォールバック（通常ありえない）
                    Zone zone = EClass.game.spatials.Find("sukutsu_arena") as Zone;
                    if (zone != null)
                    {
                        EClass.pc.MoveZone(zone, new ZoneTransition
                        {
                            state = ZoneTransition.EnterState.Center
                        });
                    }
                }
                victoryTimer = -1f; // 完了
            }
            return;
        }

        if (isGameFinished) return;

        checkTimer += Core.delta;
        if (checkTimer < 1.0f) return;
        checkTimer = 0f;

        // 敵の生存確認
        bool enemyExists = false;
        foreach (Chara c in EClass._map.charas)
        {
            if (c.IsHostile() && !c.isDead && !c.IsPC && !c.IsPCFaction)
            {
                enemyExists = true;
                break;
            }
        }

        if (!enemyExists)
        {
            // 勝利処理
            isGameFinished = true;

            // ゾーンインスタンスを取得してフラグ設定
            var arenaInstance = EClass._zone.instance as ZoneInstanceArenaBattle;
            if (arenaInstance != null)
            {
                EClass.player.dialogFlags["sukutsu_arena_result"] = 1; // 勝利フラグ

                // 貢献度システムは廃止 - クエストシステムで進行を管理

                // ログとエフェクト
                Msg.Say("敵を殲滅した！");

                EClass.Sound.Play("quest_complete");
                PlayVictoryBGM(arenaInstance);

                // 少し待ってから帰還 (3秒後にタイマーで実行)
                victoryTimer = 3.0f;
            }
        }
    }

    public override void OnCharaDie(Chara c)
    {
        if (c.IsPC)
        {
            // 敗北処理
            var arenaInstance = EClass._zone.instance as ZoneInstanceArenaBattle;
            if (arenaInstance != null)
            {
                // 注意: ここで直接フラグを設定するか、LeaveZoneで設定するか
                // ZoneInstanceArenaBattle.OnLeaveZone はフラグなしなら敗北とするロジックになっているので
                // ここで特に設定しなくても良いが、念の為
                EClass.player.dialogFlags["sukutsu_arena_result"] = 2; // 敗北

                // 自動会話フラグもここで確実にセットする
                EClass.player.dialogFlags["sukutsu_auto_dialog"] = arenaInstance.uidMaster;

                Msg.Say("このままではやられてしまう！アリーナから撤退した...");

                // 強制復活 (HP全快、メッセージなし)
                c.Revive(null, false);

                // 退出
                arenaInstance.LeaveZone();
            }
        }
    }

    /// <summary>
    /// 勝利BGMを再生（カスタムBGM対応）
    /// </summary>
    private void PlayVictoryBGM(ZoneInstanceArenaBattle arenaInstance)
    {
        if (arenaInstance != null && !string.IsNullOrEmpty(arenaInstance.bgmVictory))
        {
            try
            {
                Debug.Log($"[SukutsuArena] Playing victory BGM: {arenaInstance.bgmVictory}");
                var data = SoundManager.current.GetData(arenaInstance.bgmVictory);
                if (data != null && data is BGMData bgm)
                {
                    LayerDrama.haltPlaylist = true;  // ゾーンBGMによる上書きを防止
                    SoundManager.current.PlayBGM(bgm);
                    return;
                }
            }
            catch (System.Exception ex)
            {
                Debug.LogWarning($"[SukutsuArena] Failed to play victory BGM: {ex.Message}");
            }
        }
        // フォールバック
        EClass._zone.SetBGM(106);
    }
}
