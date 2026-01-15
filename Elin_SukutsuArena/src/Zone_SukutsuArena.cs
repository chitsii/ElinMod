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

    /// <summary>
    /// 建築を明示的に禁止
    /// </summary>
    public override bool RestrictBuild => true;

    /// <summary>
    /// ワールドマップから入場時、マップ中央に配置
    /// </summary>
    public override ZoneTransition.EnterState RegionEnterState => ZoneTransition.EnterState.Center;

    public override void OnGenerateMap()
    {
        base.OnGenerateMap();
        Debug.Log("[SukutsuArena] OnGenerateMap called. (NPCs should be placed via Map Editor)");
    }

    /// <summary>
    /// ゾーンに入った時に呼ばれる
    /// オープニングイベントをトリガー
    /// </summary>
    public override void OnBeforeSimulate()
    {
        base.OnBeforeSimulate();

        // BGMはExcelのidPlaylist列で設定（Lobby_Normal）

        // アリーナNPCのhomeZoneが正しく設定されているか確認
        EnsureNpcHomeZones();

        // ストーリー進行に応じてNPCの表示/非表示を制御
        HandleNpcVisibility();

        // 初回訪問時のみオープニングドラマを再生
        // dialogFlags でフラグを管理（CWLと同じ）
        bool openingSeen = EClass.player.dialogFlags.ContainsKey("sukutsu_opening_seen")
            && EClass.player.dialogFlags["sukutsu_opening_seen"] != 0;

        if (!openingSeen)
        {
            Debug.Log("[SukutsuArena] First visit detected. Triggering opening drama...");
            TriggerOpeningDrama();
        }
    }

    /// <summary>
    /// アリーナNPCのhomeZoneが正しく設定されているか確認
    /// CWLのaddZone_タグで設定済みだが、古いセーブデータ対策として残す
    /// ペット解放時にhomeZoneへ自動帰還するために必要
    /// </summary>
    private void EnsureNpcHomeZones()
    {
        var arenaNpcIds = new[] {
            "sukutsu_receptionist",    // Lily
            "sukutsu_arena_master",    // Balgas
            "sukutsu_shady_merchant",  // Zek
            "sukutsu_null",            // Nul
            "sukutsu_astaroth"         // Astaroth
        };

        foreach (var npcId in arenaNpcIds)
        {
            var npc = EClass._map.charas.Find(c => c.id == npcId);
            if (npc != null && npc.IsGlobal && npc.homeZone != this)
            {
                Debug.Log($"[SukutsuArena] Setting homeZone for {npcId}");
                npc.homeZone = this;
            }
        }
    }

    private void TriggerOpeningDrama()
    {
        // リリィ（受付嬢）を探してドラマを開始
        var lily = EClass._map.charas.Find(c => c.id == "sukutsu_receptionist");
        if (lily != null)
        {
            // CWLドラマを開始
            // ShowDialog(book, step) で呼び出し
            // book = "drama_sukutsu_opening" (CWLがマッピング)
            lily.ShowDialog("drama_sukutsu_opening", "main");
        }
        else
        {
            Debug.LogWarning("[SukutsuArena] Lily not found. Cannot trigger opening drama.");
        }
    }

    /// <summary>
    /// ストーリー進行に応じてNPCの表示/非表示を制御
    /// 特定のクエスト完了やストーリーフラグに基づいてNPCを"somewhere"ゾーンに移動
    /// </summary>
    private void HandleNpcVisibility()
    {
        var qm = ArenaQuestManager.Instance;
        var flags = EClass.player.dialogFlags;

        // フラグチェック用ヘルパー
        bool HasFlag(string key) => flags.ContainsKey(key) && flags[key] != 0;

        // Zek: 02_rank_up_G完了後に表示、それまでは非表示
        bool rankGCompleted = qm?.IsQuestCompleted("02_rank_up_G") ?? false;
        if (rankGCompleted)
        {
            ShowNpcInArena("sukutsu_shady_merchant");
        }
        else
        {
            HideNpcToSomewhere("sukutsu_shady_merchant");
        }

        // バルガス死亡またはリリィ離反ルート
        bool balgasDead = HasFlag("balgas_dead");
        bool lilyBetrayed = HasFlag("lily_betrayed");

        // Nul: エピローグ完了後は表示、Bランク試験～エピローグ間は非表示
        // バルガス死亡またはリリィ離反ルートでは常に非表示
        bool epilogueCompleted = qm?.IsQuestCompleted("19_epilogue") ?? false;
        bool rankBCompleted = qm?.IsQuestCompleted("12_rank_b_trial") ?? false;
        if (balgasDead || lilyBetrayed)
        {
            HideNpcToSomewhere("sukutsu_null");
        }
        else if (epilogueCompleted)
        {
            ShowNpcInArena("sukutsu_null");
        }
        else if (rankBCompleted)
        {
            HideNpcToSomewhere("sukutsu_null");
        }

        // Astaroth: 最終戦完了 OR バルガス死亡 OR リリィ離反
        if ((qm?.IsQuestCompleted("18_last_battle") ?? false) || balgasDead || lilyBetrayed)
        {
            HideNpcToSomewhere("sukutsu_astaroth");
        }

        // Balgas: バルガス死亡ルート
        if (balgasDead)
        {
            HideNpcToSomewhere("sukutsu_arena_master");
        }

        // Lily: リリィ離反ルート
        if (lilyBetrayed)
        {
            HideNpcToSomewhere("sukutsu_receptionist");
        }
    }

    /// <summary>
    /// NPCを"somewhere"ゾーンに移動して非表示にする
    /// ペット化されている場合はスキップ
    /// </summary>
    private void HideNpcToSomewhere(string npcId)
    {
        var npc = EClass._map.charas.Find(c => c.id == npcId);
        if (npc == null)
        {
            Debug.Log($"[SukutsuArena] HideNpc: {npcId} not found in map");
            return;
        }

        // ペット化されている場合はスキップ
        if (npc.IsPCParty || npc.master == EClass.pc)
        {
            Debug.Log($"[SukutsuArena] {npcId} is in party, skipping hide");
            return;
        }

        Debug.Log($"[SukutsuArena] Hiding {npcId} to somewhere zone (currentZone={npc.currentZone?.id ?? "null"})");
        npc.MoveZone("somewhere");
    }

    /// <summary>
    /// NPCをアリーナに表示する（"somewhere"から戻す）
    /// </summary>
    private void ShowNpcInArena(string npcId)
    {
        // 既にこのゾーンにいる場合は何もしない
        var existingNpc = EClass._map.charas.Find(c => c.id == npcId);
        if (existingNpc != null)
            return;

        // グローバルキャラから探す
        Chara npc = null;
        foreach (var c in EClass.game.cards.globalCharas.Values)
        {
            if (c.id == npcId)
            {
                npc = c;
                break;
            }
        }
        if (npc == null)
            return;

        // "somewhere"にいる場合のみ移動
        if (npc.currentZone?.id == "somewhere")
        {
            Debug.Log($"[SukutsuArena] Showing {npcId} in arena");
            npc.MoveZone(this);
        }
    }
}
