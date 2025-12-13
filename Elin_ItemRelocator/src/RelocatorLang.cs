using System;
using System.Collections.Generic;

namespace Elin_ItemRelocator
{
    public static class RelocatorLang
    {
        public enum LangKey
        {
            Settings, AddFilter, Preview, Execute, Scope, ExcludeHotbar, Rarity, Quality, Category, Text, Enchant, Remove, Edit, Enable, Disable, Title, Operator, Msg_Relocated, Inventory, Zone, ON, OFF, NoMatches, SelectEnchant, RelocatorCaption, DisabledSuffix, All, EditSearchText, EditCategoryID, EditQuality, Msg_ContainerFull, Msg_RelocatedResult, Msg_NoMatchLog
        }

        private static Dictionary<LangKey, string[]> _dict = new Dictionary<LangKey, string[]>
        {
            { LangKey.Settings, new[] { "Settings", "設定" } },
            { LangKey.AddFilter, new[] { "Add Filter", "フィルタ追加" } },
            { LangKey.Preview, new[] { "Preview", "プレビュー" } },
            { LangKey.Execute, new[] { "Relocate", "実行" } },
            { LangKey.Scope, new[] { "Scope", "範囲" } },
            { LangKey.ExcludeHotbar, new[] { "Exclude Hotbar", "ツールベルト除外" } },
            { LangKey.Rarity, new[] { "Rarity", "レアリティ" } },
            { LangKey.Quality, new[] { "Quality", "品質" } },
            { LangKey.Category, new[] { "Category", "カテゴリ" } },
            { LangKey.Text, new[] { "Text (Name/Tag)", "テキスト (名前/タグ)" } },
            { LangKey.Enchant, new[] { "Enchant", "エンチャント" } },
            { LangKey.Remove, new[] { "Remove", "削除" } },
            { LangKey.Edit, new[] { "Edit", "編集" } },
            { LangKey.Enable, new[] { "Enable", "有効" } },
            { LangKey.Disable, new[] { "Disable", "無効" } },
            { LangKey.Title, new[] { "Item Relocator", "アイテムリロケータ" } },
            { LangKey.Operator, new[] { "Operator", "演算子" } },
            { LangKey.Msg_Relocated, new[] { "Relocated {0} items.", "{0}個のアイテムを移動しました。" } },
            { LangKey.Inventory, new[] { "Inventory", "インベントリ" } },
            { LangKey.Zone, new[] { "Zone", "ゾーン" } },
            { LangKey.ON, new[] { "ON", "ON" } },
            { LangKey.OFF, new[] { "OFF", "OFF" } },
            { LangKey.NoMatches, new[] { "No matches found.", "該当なし" } },
            { LangKey.SelectEnchant, new[] { "Select Enchant", "エンチャント選択" } },
            { LangKey.RelocatorCaption, new[] { "Relocator: {0} [{1}] (Matches: {2})", "リロケータ: {0} [{1}] (合致: {2})" } },
            { LangKey.DisabledSuffix, new[] { " (Disabled)", " (無効)" } },
            { LangKey.All, new[] { "All ", "すべて選択 " } },
            { LangKey.EditSearchText, new[] { "Edit Search Text", "検索テキスト編集" } },
            { LangKey.EditCategoryID, new[] { "Edit Category ID", "カテゴリID編集" } },
            { LangKey.EditQuality, new[] { "Edit Quality (e.g. >=2)", "品質設定 (例: >=2)" } },
            { LangKey.Msg_ContainerFull, new[] { "Container is full.", "コンテナが一杯です。" } },
            { LangKey.Msg_RelocatedResult, new[] { "Relocated {0} stacks to {1}.", "{0}個のスタックを{1}に移動した。" } },
            { LangKey.Msg_NoMatchLog, new[] { "No matching items found.", "条件に合うアイテムが見つからない。" } }
        };

        public static string GetText(LangKey key)
        {
            int idx = (Lang.langCode == "JP") ? 1 : 0;
            if (_dict.ContainsKey(key)) return _dict[key][idx];
            return key.ToString();
        }
    }
}
