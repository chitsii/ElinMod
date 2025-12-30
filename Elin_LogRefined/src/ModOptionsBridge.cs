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

        [ModCfgToggle(titleId: "EnableCommentary", tooltipId: "EnableCommentary_tooltip")]
        public ConfigEntry<bool> EnableCommentary;

        public ModOptionsBridge()
        {
            EnableMod = ModConfig.EnableMod;
            ShowDamageLog = ModConfig.ShowDamageLog;
            ShowHealLog = ModConfig.ShowHealLog;
            ShowConditionLog = ModConfig.ShowConditionLog;
            FormatMode = ModConfig.FormatMode;
            EnableCommentary = ModConfig.EnableCommentary;
        }

        public void SetTranslations(ModOptionController controller)
        {
            controller.SetTranslation(Plugin.ModGuid, "Log Refined", "Log Refined", "Log Refined");

            // Config keys
            controller.SetTranslation("EnableMod", "Enable Mod", "Modを有効化", "启用模组");
            controller.SetTranslation("ShowDamageLog", "Show Damage Log", "ダメージログを表示", "显示伤害日志");
            controller.SetTranslation("ShowHealLog", "Show Heal Log", "回復ログを表示", "显示治疗日志");
            controller.SetTranslation("ShowConditionLog", "Show Condition Log", "状態異常ログを表示", "显示状态异常日志");
            controller.SetTranslation("FormatMode", "Format", "単位", "单位"); // Dropdown label
            controller.SetTranslation("EnableCommentary", "Enable Live Commentary", "熱血実況モードを有効化", "启用热血实况模式");

            // Enum choices
            // Assuming "NumberFormat" is the enum type name
            controller.SetTranslation("NumberFormat.None", "None (1,234)", "なし (1,234)", "无 (1,234)");
            controller.SetTranslation("NumberFormat.Kilo", "Kilo (1.2k)", "キロ (1.2k)", "千 (1.2k)");
            controller.SetTranslation("NumberFormat.Million", "Million (1.2M)", "ミリオン (1.2M)", "百万 (1.2M)");
            // Backup in case class name acts as prefix
            controller.SetTranslation("ModConfig.NumberFormat.None", "None (1,234)", "なし (1,234)", "无 (1,234)");
            controller.SetTranslation("ModConfig.NumberFormat.Kilo", "Kilo (1.2k)", "キロ (1.2k)", "千 (1.2k)");
            controller.SetTranslation("ModConfig.NumberFormat.Million", "Million (1.2M)", "ミリオン (1.2M)", "百万 (1.2M)");

            // Tooltips
            controller.SetTranslation("EnableMod_tooltip", "Toggle the entire mod functionality.", "Mod全体の機能を切り替えます。", "切换整个模组的功能。");
            controller.SetTranslation("ShowDamageLog_tooltip", "Display damage numbers in the log.", "ログにダメージ数値を表示します。", "在日志中显示伤害数值。");
            controller.SetTranslation("ShowHealLog_tooltip", "Display healing numbers in the log.", "ログに回復数値を表示します。", "在日志中显示治疗数值。");
            controller.SetTranslation("ShowConditionLog_tooltip", "Display detailed buff/debuff effects.", "バフ・デバフの詳細効果を表示します。", "显示增益/减益的详细效果。");
            controller.SetTranslation("FormatMode_tooltip", "Choose how to format large numbers.", "大きな数値の表示形式を選択します。", "选择大数值的显示格式。");
            controller.SetTranslation("EnableCommentary_tooltip", "Adds spicy commentary to the logs!", "ログに実況コメントを追加し、戦場を盛り上げます！", "在日志中添加实况评论，让战场更热闹！");
        }
    }
}
