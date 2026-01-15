using Newtonsoft.Json;
using UnityEngine;

/// <summary>
/// アリーナ戦闘用のゾーンインスタンス
/// 戦闘終了後にプレイヤーを元の場所に戻し、報酬を付与する
/// </summary>
public class ZoneInstanceArenaBattle : ZoneInstance
{
    [JsonProperty]
    public int uidMaster;

    [JsonProperty]
    public int returnX;

    [JsonProperty]
    public int returnZ;

    [JsonProperty]
    public int rewardPlat = 10;

    [JsonProperty]
    public bool isRankUp = false;

    [JsonProperty]
    public string stageId = "";

    [JsonProperty]
    public string bgmBattle = "";

    [JsonProperty]
    public string bgmVictory = "";

    public override ZoneTransition.EnterState ReturnState => ZoneTransition.EnterState.Exact;

    /// <summary>
    /// ゾーン離脱時の処理
    /// </summary>
    public override void OnLeaveZone()
    {
        Debug.Log($"[SukutsuArena] OnLeaveZone called, stageId={stageId}");

        // 勝利判定はZoneEventArenaBattleで行われ、フラグが立っているはず
        int result = EClass.player.dialogFlags.ContainsKey("sukutsu_arena_result")
            ? EClass.player.dialogFlags["sukutsu_arena_result"] : 0;

        if (result == 1) // 勝利
        {
            Debug.Log("[SukutsuArena] Victory processed");

            GiveReward();
            ScheduleAutoDialog();
        }
        else
        {
            // 敗北（死亡または逃走）
            // 既に勝利フラグがない場合のみ敗北とする
            Debug.Log("[SukutsuArena] Defeat or flee");
            EClass.player.dialogFlags["sukutsu_arena_result"] = 2;  // 敗北
            Msg.Say("アリーナから撤退した...");

            // 帰還後に自動会話
            ScheduleAutoDialog();
        }

        // クエストバトル（sukutsu_quest_battle != 0）が優先
        // isRankUpよりも明示的に設定されたsukutsu_quest_battleを優先する
        // 注意: フラグのクリアはドラマ側で行う（quest_battle_result_checkの後）
        int questBattle = EClass.player.dialogFlags.ContainsKey("sukutsu_quest_battle")
            ? EClass.player.dialogFlags["sukutsu_quest_battle"] : 0;

        if (questBattle != 0)
        {
            // クエストバトル結果として処理
            EClass.player.dialogFlags["sukutsu_is_quest_battle_result"] = 1;
            EClass.player.dialogFlags["sukutsu_is_rank_up_result"] = 0;
            Debug.Log($"[SukutsuArena] Quest battle result flag set, questBattle={questBattle}");
        }
        else if (isRankUp)
        {
            // ランクアップ戦結果として処理
            EClass.player.dialogFlags["sukutsu_is_rank_up_result"] = 1;
            EClass.player.dialogFlags["sukutsu_is_quest_battle_result"] = 0;
        }
        else
        {
            // 通常バトル
            EClass.player.dialogFlags["sukutsu_is_rank_up_result"] = 0;
            EClass.player.dialogFlags["sukutsu_is_quest_battle_result"] = 0;
        }

        // マスターIDを使って後処理などがあればここで行う
    }

    public void LeaveZone()
    {
        Zone zone = EClass.game.spatials.Find(uidZone) as Zone;
        if (zone != null)
        {
            EClass.pc.MoveZone(zone, new ZoneTransition
            {
                state = ZoneTransition.EnterState.Exact,
                x = returnX,
                z = returnZ
            });
        }
        else
        {
            // フォールバック
            Zone fallbackZone = EClass.game.spatials.Find("sukutsu_arena") as Zone;
            if (fallbackZone != null)
            {
                EClass.pc.MoveZone(fallbackZone, ZoneTransition.EnterState.Center);
            }
        }
    }

    /// <summary>
    /// 帰還後にアリーナマスターとの会話を自動開始するよう予約
    /// </summary>
    private void ScheduleAutoDialog()
    {
        // Harmonyパッチが読み取る自動会話フラグを設定
        EClass.player.dialogFlags["sukutsu_auto_dialog"] = uidMaster;
        Debug.Log($"[SukutsuArena] Scheduled auto-dialog flag for master UID: {uidMaster}");
    }

    /// <summary>
    /// 報酬付与
    /// </summary>
    private void GiveReward()
    {
        // 結果フラグはドラマ側でクリアするのでここではクリアしない
        // EClass.player.dialogFlags["sukutsu_arena_result"] = 0;

        // ステージクリア報酬
        Thing plat = ThingGen.Create("plat");
        plat.SetNum(rewardPlat);
        EClass.pc.Pick(plat);

        Msg.Say($"勝利の報酬としてプラチナコイン {rewardPlat} 枚を獲得した！");

        // ステージ進行は廃止 - クエストシステムで管理
        // ランクアップはクエスト完了時にのみ発生
    }
}
