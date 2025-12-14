using System;
using System.Collections.Generic;

namespace Elin_ItemRelocator
{
    public static class RelocatorLang
    {
        public enum LangKey
        {
            Settings, AddFilter, Preview, Execute, Scope, ExcludeHotbar, Rarity, Quality, Category, Text, Enchant, Remove, Edit, Enable, Disable, Title, Operator, Msg_Relocated, Inventory, Zone, ON, OFF, NoMatches, SelectEnchant, RelocatorCaption, DisabledSuffix, All, EditSearchText, EditCategoryID, EditQuality, Msg_ContainerFull, Msg_RelocatedResult, Msg_NoMatchLog,
            SortLabel, SortDefault, SortPriceAsc, SortPriceDesc, SortMagAsc, SortMagDesc,
            CatAll, CatWeapon, CatArmor,
            SavePreset, LoadPreset, PresetName, Msg_Saved, Msg_Loaded,
            Presets, Rename, Delete, Msg_Renamed, Msg_Deleted, Msg_FileExists, Msg_RenamePrompt,
            Parent, Move, Msg_Moved, AddRule, NewRuleName
        }

        private static Dictionary<LangKey, string[]> _dict = new Dictionary<LangKey, string[]>
        {
            { LangKey.Settings, new[] { "Settings", "設定" } },
            { LangKey.AddFilter, new[] { "Add Filter", "フィルタ追加" } },
            { LangKey.Preview, new[] { "Preview", "プレビュー" } },
            { LangKey.Execute, new[] { "Relocate", "再配置" } },
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
            { LangKey.Msg_NoMatchLog, new[] { "No matching items found.", "条件に合うアイテムが見つからない。" } },
            { LangKey.SortLabel, new[] { "Sort: ", "並び替え: " } },
            { LangKey.SortDefault, new[] { "Default", "初期設定" } },
            { LangKey.SortPriceAsc, new[] { "Price (Low to High)", "価格 (安い順)" } },
            { LangKey.SortPriceDesc, new[] { "Price (High to Low)", "価格 (高い順)" } },
            { LangKey.SortMagAsc, new[] { "Enchant (Weak to Strong)", "エンチャント強度 (弱い順)" } },
            { LangKey.SortMagDesc, new[] { "Enchant (Strong to Weak)", "エンチャント強度 (強い順)" } },
            { LangKey.CatAll, new[] { "General", "汎用" } },
            { LangKey.CatWeapon, new[] { "Weapon Specific", "武器特有" } },
            { LangKey.CatArmor, new[] { "Armor Specific", "防具特有" } },
            { LangKey.SavePreset, new[] { "Save Preset", "プリセット保存" } },
            { LangKey.LoadPreset, new[] { "Load Preset", "プリセット読込" } },
            { LangKey.PresetName, new[] { "Preset Name", "プリセット名" } },
            { LangKey.Msg_Saved, new[] { "Preset saved: {0}", "プリセットを保存しました: {0}" } },
            { LangKey.Msg_Loaded, new[] { "Preset loaded.", "プリセットを読み込みました。" } },
            { LangKey.Presets, new[] { "Presets", "プリセット" } },
            { LangKey.Rename, new[] { "Rename", "名前変更" } },
            { LangKey.Delete, new[] { "Delete", "削除" } },
            { LangKey.Msg_Renamed, new[] { "Renamed preset to {0}.", "プリセット名を {0} に変更しました。" } },
            { LangKey.Msg_Deleted, new[] { "Deleted preset: {0}", "プリセット {0} を削除しました。" } },
            { LangKey.Msg_FileExists, new[] { "Preset already exists.", "同名のプリセットが既に存在します。" } },
            { LangKey.Msg_RenamePrompt, new[] { "Enter new name", "新しい名前を入力" } },
            { LangKey.Parent, new[] { "Location", "場所" } },
            { LangKey.Move, new[] { "Move", "転送" } },
            { LangKey.Msg_Moved, new[] { "Moved {0}.", "{0}を転送しました。" } },
            { LangKey.AddRule, new[] { "Add Rule", "ルール追加" } },
            { LangKey.NewRuleName, new[] { "Rule Name", "ルール名" } }
        };

        public static string GetText(LangKey key)
        {
            int idx = (Lang.langCode == "JP") ? 1 : 0;
            if (_dict.ContainsKey(key)) return _dict[key][idx];
            return key.ToString();
        }
    }
}
