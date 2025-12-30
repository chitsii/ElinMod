using System.Globalization;

namespace Elin_LogRefined
{
    public static class RefinedLogUtil
    {
        public static string FormatNumber(long num)
        {
            if (ModConfig.FormatMode.Value == ModConfig.NumberFormat.Million && num >= 1000000)
            {
                double m = num / 1000000.0;
                return m.ToString("#,0.#") + "M";
            }
            if ((ModConfig.FormatMode.Value == ModConfig.NumberFormat.Kilo || ModConfig.FormatMode.Value == ModConfig.NumberFormat.Million) && num >= 1000 && num < 1000000)
            {
                double k = num / 1000.0;
                return k.ToString("#,0.#") + "k";
            }
            return num.ToString("#,0");
        }

        public static string GetText(string key)
        {
            if (Lang.langCode == "JP")
            {
                if (key == "damage") return "ダメージ！";
                if (key == "heal") return "回復";
            }
            if (Lang.langCode == "CN")
            {
                if (key == "damage") return "伤害！";
                if (key == "heal") return "恢复";
            }
            if (key == "heal") return "recovered";
            return key;
        }
    }
}
