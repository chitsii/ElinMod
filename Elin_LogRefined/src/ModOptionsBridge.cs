using BepInEx.Configuration;
using EvilMask.Elin.ModOptions;
using EvilMask.Elin.ModOptions.UI;

namespace Elin_LogRefined
{
    public class ModOptionsBridge
    {
        [ModCfgToggle(titleId: "EnableMod", tooltipId: "EnableMod_tooltip")]
        public ConfigEntry<bool> EnableMod;

        [ModCfgToggle(titleId: "ShowDamageLog", tooltipId: "ShowDamageLog_tooltip")]
        public ConfigEntry<bool> ShowDamageLog;

        [ModCfgToggle(titleId: "ShowHealLog", tooltipId: "ShowHealLog_tooltip")]
        public ConfigEntry<bool> ShowHealLog;

        [ModCfgToggle(titleId: "ShowConditionLog", tooltipId: "ShowConditionLog_tooltip")]
        public ConfigEntry<bool> ShowConditionLog;

        [ModCfgDropdown(titleId: "FormatMode")]
        public ConfigEntry<ModConfig.NumberFormat> FormatMode;

        [ModCfgDropdown(titleId: "DetailLevel")]
        public ConfigEntry<ModConfig.LogDetailLevel> DetailLevel;

        [ModCfgToggle(titleId: "EnableCommentary", tooltipId: "EnableCommentary_tooltip")]
        public ConfigEntry<bool> EnableCommentary;

        [ModCfgToggle(titleId: "GenerateTemplates", tooltipId: "GenerateTemplates_tooltip")]
        public ConfigEntry<bool> GenerateTemplates;

        public ModOptionsBridge()
        {
            EnableMod = ModConfig.EnableMod;
            ShowDamageLog = ModConfig.ShowDamageLog;
            ShowHealLog = ModConfig.ShowHealLog;
            ShowConditionLog = ModConfig.ShowConditionLog;
            FormatMode = ModConfig.FormatMode;
            DetailLevel = ModConfig.DetailLevel;
            EnableCommentary = ModConfig.EnableCommentary;
            GenerateTemplates = ModConfig.GenerateTemplates;
        }

        public void SetTranslations(ModOptionController controller)
        {
            controller.SetTranslation(Plugin.ModGuid, "Log Refined", "Log Refined", "Log Refined");

            // Config keys
            controller.SetTranslation("EnableMod", "Enable Mod", "Modを有効化", "启用模组");
            controller.SetTranslation("ShowDamageLog", "Show Damage Log", "ダメージログを表示", "显示伤害日志");
            controller.SetTranslation("ShowHealLog", "Show Heal Log", "回復ログを表示", "显示治疗日志");
            controller.SetTranslation("ShowConditionLog", "Show Condition Log", "状態異常ログを表示", "显示状态异常日志");
            controller.SetTranslation("FormatMode", "Unit", "単位", "单位");
            controller.SetTranslation("DetailLevel", "Detail", "詳細度", "详细程度");
            controller.SetTranslation("EnableCommentary", "Commentary (Combat)", "実況モード (戦闘中のみ)", "实况模式 (仅战斗)");

            // NumberFormat enum
            controller.SetTranslation("NumberFormat.None", "None (1,234)", "なし (1,234)", "无 (1,234)");
            controller.SetTranslation("NumberFormat.Kilo", "Kilo (1.2k)", "キロ (1.2k)", "千 (1.2k)");
            controller.SetTranslation("NumberFormat.Million", "Million (1.2M)", "ミリオン (1.2M)", "百万 (1.2M)");

            // LogDetailLevel enum
            controller.SetTranslation("LogDetailLevel.NumberOnly", "Number Only", "数値のみ", "仅数值");
            controller.SetTranslation("LogDetailLevel.WithTarget", "With Target", "対象者あり", "含目标");

            // Tooltips
            controller.SetTranslation("EnableMod_tooltip", "Toggle the entire mod functionality.", "Mod全体の機能を切り替えます。", "切换整个模组的功能。");
            controller.SetTranslation("ShowDamageLog_tooltip", "Display damage numbers in the log.", "ログにダメージ数値を表示します。", "在日志中显示伤害数值。");
            controller.SetTranslation("ShowHealLog_tooltip", "Display healing numbers in the log.", "ログに回復数値を表示します。", "在日志中显示治疗数值。");
            controller.SetTranslation("ShowConditionLog_tooltip", "Display detailed buff/debuff effects.", "バフ・デバフの詳細効果を表示します。", "显示增益/减益的详细效果。");
            controller.SetTranslation("FormatMode_tooltip", "Choose how to format large numbers.", "大きな数値の表示形式を選択します。", "选择大数值的显示格式。");
            controller.SetTranslation("EnableCommentary_tooltip",
                "Adds spicy commentary to the logs! (To Customize Commentary, enable following setting: 'Setup Custom Commentary')",
                "ログに実況コメントを追加し、戦場を盛り上げます！ (セリフのカスタマイズするには、次の設定'カスタムセリフ用テンプレートを初期化'をトグルして下さい)",
                "在日志中添加实况评论，让战场更热闹！ (要自定义台词，请启用'创建自定义台词模板'设置)"
            );

            controller.SetTranslation("GenerateTemplates", "Setup Custom Commentary", "カスタムセリフ用テンプレートを初期化", "创建自定义台词模板");
            controller.SetTranslation("GenerateTemplates_tooltip",
                "ON to create editable template files in the [commentary] folder. Once created, your custom lines are preserved even when the mod is updated. Please restart the game after editing the template files.",
                "ONにすると[commentary]フォルダに独自のセリフを記述できるテンプレートファイルを作成します。作成されたファイルはModの更新後も保持されます。テンプレートファイル編集後はゲームを再起動して下さい。",
                "打开后在 [commentary] 文件夹中创建可编辑的模板文件。创建后，即使模组更新，您的自定义台词也会保留。编辑模板文件后请重启游戏。"
            );
        }
    }
}
