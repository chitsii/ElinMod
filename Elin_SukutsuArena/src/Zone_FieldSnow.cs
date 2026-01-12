using System.IO;
using System.Reflection;
using UnityEngine;

namespace Elin_SukutsuArena;

/// <summary>
/// 雪原フィールド用カスタムゾーン
/// Zone_Field を継承し、IsSnowZone を true にオーバーライド
/// カスタムマップ chitsii_battle_field_snow.z を読み込む
/// </summary>
public class Zone_FieldSnow : Zone_Field
{
    /// <summary>
    /// 敵の自然発生を無効化
    /// Zone_Field は PrespawnRate = 1.2f だが、アリーナ戦闘では不要
    /// </summary>
    public override float PrespawnRate => 0f;

    private const string MAP_FILE_NAME = "chitsii_battle_field_snow.z";

    /// <summary>
    /// 雪原ゾーンとして認識させる
    /// - IsSnowCovered => true (雪タイル)
    /// - IDSceneTemplate => "Snow" (雪のライティング)
    /// これにより季節に関係なく常に冬の見た目になる
    /// </summary>
    public override bool IsSnowZone => true;

    /// <summary>
    /// カスタムマップファイルのパス
    /// LangMod/JP/Maps/chitsii_battle_field_snow.z を読み込む
    /// </summary>
    public override string pathExport
    {
        get
        {
            string modPath = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            string customMap = Path.Combine(modPath, "LangMod/JP/Maps", MAP_FILE_NAME);

            if (File.Exists(customMap))
            {
                Debug.Log($"[SukutsuArena] Loading custom snow map: {customMap}");
                return customMap;
            }

            Debug.LogWarning($"[SukutsuArena] Custom map not found: {customMap}, falling back to default");
            return base.pathExport;
        }
    }
}
