using BepInEx.Configuration;

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

        public static ConfigEntry<bool> EnableMod;
        public static ConfigEntry<bool> ShowDamageLog;
        public static ConfigEntry<bool> ShowHealLog;
        public static ConfigEntry<bool> ShowConditionLog;
        public static ConfigEntry<NumberFormat> FormatMode;
        public static ConfigEntry<bool> EnableCommentary;

        public static void LoadConfig(ConfigFile config)
        {
            EnableMod = config.Bind("General", "EnableMod", true, "Enable the mod.");
            ShowDamageLog = config.Bind("Damage", "ShowDamageLog", true, "Show damage values in log.");
            ShowHealLog = config.Bind("Heal", "ShowHealLog", true, "Show healing values in log.");
            ShowConditionLog = config.Bind("Condition", "ShowConditionLog", true, "Show condition details (buff/debuff) in log.");
            FormatMode = config.Bind("Format", "FormatMode", NumberFormat.None, "Number formatting mode.");
            EnableCommentary = config.Bind("Extra", "EnableCommentary", true, "Enable live commentary mode.");
        }
    }
}
