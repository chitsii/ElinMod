using System;

/// <summary>
/// アリーナマスター専用のTrait
/// CanBout = true を設定し、会話処理は Harmony パッチで行う
/// </summary>
public class TraitArenaMaster : TraitChara
{
    /// <summary>
    /// 戦闘メニューを表示できるか
    /// バニラの _bout パターンで使われる
    /// </summary>
    public override bool CanBout => true;

    /// <summary>
    /// ユニークNPCとして扱う
    /// </summary>
    public override bool IsUnique => true;
}
