using BepInEx.Configuration;
using System;

namespace Elin_LogRefined
{
    public static class ModConfig
    {
        public enum NumberFormat
        {
            None,
            Kilo,
            Million
        }

        public enum LogDetailLevel
        {
            NumberOnly,       // [ 999 ダメージ ]
            WithTarget        // [ XXX が 999 ダメージを受けた ]
        }

        public static ConfigEntry<bool> EnableMod;
        public static ConfigEntry<bool> ShowDamageLog;
        public static ConfigEntry<bool> ShowHealLog;
        public static ConfigEntry<bool> ShowConditionLog;
        public static ConfigEntry<NumberFormat> FormatMode;
        public static ConfigEntry<LogDetailLevel> DetailLevel;
        public static ConfigEntry<bool> EnableCommentary;
        public static ConfigEntry<bool> GenerateTemplates;

        public static void LoadConfig(ConfigFile config)
        {
            EnableMod = config.Bind("General", "EnableMod", true, "Enable the mod.");
            ShowDamageLog = config.Bind("Damage", "ShowDamageLog", true, "Show damage values in log.");
            ShowHealLog = config.Bind("Heal", "ShowHealLog", true, "Show healing values in log.");
            ShowConditionLog = config.Bind("Condition", "ShowConditionLog", true, "Show condition details (buff/debuff) in log.");
            FormatMode = config.Bind("Format", "FormatMode", NumberFormat.None, "Number formatting mode.");
            DetailLevel = config.Bind("Format", "DetailLevel", LogDetailLevel.NumberOnly, "Log detail level.");
            EnableCommentary = config.Bind("Extra", "EnableCommentary", true, "Enable live commentary mode (combat only).");
            GenerateTemplates = config.Bind("Extra", "GenerateTemplates", false, "Turn ON to generate template files.");

            // Subscribe to the GenerateTemplates toggle
            GenerateTemplates.SettingChanged += OnGenerateTemplatesChanged;
        }

        private static void OnGenerateTemplatesChanged(object sender, System.EventArgs e)
        {
            if (GenerateTemplates.Value)
            {
                // Reset to OFF first to prevent re-triggering
                GenerateTemplates.Value = false;

                Action onComplete = () =>
                {
                    Dialog.YesNo(
                        "Templates created. Open folder?\nテンプレートを作成しました。フォルダを開きますか？",
                        () => CommentaryData.OpenCommentaryDir()
                    );
                };

                // Check if files exist and prompt
                if (CommentaryData.TemplateFilesExist())
                {
                    Dialog.YesNo(
                        "Template files already exist. Overwrite with defaults?\nテンプレートファイルが既に存在します。上書きしますか？",
                        () =>
                        {
                            CommentaryData.GenerateTemplateFiles(true);
                            onComplete();
                        }
                    );
                }
                else
                {
                    CommentaryData.GenerateTemplateFiles(false);
                    onComplete();
                }
            }
        }
    }
}
