namespace Elin_SukutsuArena.Feats;

/// <summary>
/// 闘志（Arena Spirit）フィート
/// 闘技場で戦い抜いた証として得られるフィート。
/// ランクが上がるごとにレベルが上がり、活力が向上する。
/// </summary>
internal class FeatArenaSpirit : Feat
{
    /// <summary>
    /// CWL によって呼び出されるフィート効果適用メソッド
    /// </summary>
    /// <param name="add">フィートのレベル（1-7）</param>
    /// <param name="eleOwner">フィート所有者のElementContainer</param>
    /// <param name="hint">trueの場合はヒント情報収集モード</param>
    internal void _OnApply(int add, ElementContainer eleOwner, bool hint)
    {
        // 活力のみをシンプルに強化
        // Lv1-5: add * 5 (5, 10, 15, 20, 25)
        // Lv6: 30
        // Lv7: 40
        int vigorBonus = add <= 5 ? add * 5 : (add == 6 ? 30 : 40);
        eleOwner.ModBase(62, vigorBonus); // vigor = 62
    }
}
