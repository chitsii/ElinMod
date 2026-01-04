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
        Debug.Log("[SukutsuArena] OnGenerateMap called. (NPCs should be placed via Map Editor)");
    }

    /// <summary>
    /// ゾーンに入った時に呼ばれる
    /// オープニングイベントをトリガー
    /// </summary>
    public override void OnBeforeSimulate()
    {
        base.OnBeforeSimulate();

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
}
