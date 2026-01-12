using System.IO;
using System.Reflection;
using UnityEngine;

namespace Elin_SukutsuArena;

/// <summary>
/// 通常フィールド用カスタムゾーン
/// カスタムマップ chitsii_battle_field_fine.z を読み込む
/// </summary>
public class Zone_FieldFine : Zone_Field
{
    /// <summary>
    /// 敵の自然発生を無効化
    /// Zone_Field は PrespawnRate = 1.2f だが、アリーナ戦闘では不要
    /// </summary>
    public override float PrespawnRate => 0f;

    private const string MAP_FILE_NAME = "chitsii_battle_field_fine.z";

    /// <summary>
    /// カスタムマップファイルのパス
    /// LangMod/JP/Maps/chitsii_battle_field_fine.z を読み込む
    /// </summary>
    public override string pathExport
    {
        get
        {
            string modPath = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            string customMap = Path.Combine(modPath, "LangMod/JP/Maps", MAP_FILE_NAME);

            if (File.Exists(customMap))
            {
                Debug.Log($"[SukutsuArena] Loading custom field map: {customMap}");
                return customMap;
            }

            Debug.LogWarning($"[SukutsuArena] Custom map not found: {customMap}, falling back to default");
            return base.pathExport;
        }
    }
}
