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

        // ダメージログのフォーマット
        public static string FormatDamageLog(long damage, string targetName, string attackerName)
        {
            string num = FormatNumber(damage);
            string langCode = Lang.langCode;

            switch (ModConfig.DetailLevel.Value)
            {
                case ModConfig.LogDetailLevel.WithTarget:
                    if (langCode == "JP")
                        return $"[ {targetName} に {num} ダメージ！ ]";
                    if (langCode == "CN")
                        return $"[ {targetName} 受到 {num} 伤害！ ]";
                    return $"[ {targetName} took {num} damage! ]";

                default: // NumberOnly
                    if (langCode == "JP")
                        return $"[ {num} ダメージ ]";
                    if (langCode == "CN")
                        return $"[ {num} 伤害 ]";
                    return $"[ {num} damage ]";
            }
        }

        // 回復ログのフォーマット
        public static string FormatHealLog(long healed, string targetName, string healerName)
        {
            string num = FormatNumber(healed);
            string langCode = Lang.langCode;

            switch (ModConfig.DetailLevel.Value)
            {
                case ModConfig.LogDetailLevel.WithTarget:
                    if (langCode == "JP")
                        return $"[ {targetName} が {num} 回復 ]";
                    if (langCode == "CN")
                        return $"[ {targetName} 恢复 {num} ]";
                    return $"[ {targetName} recovered {num} ]";

                default: // NumberOnly
                    if (langCode == "JP")
                        return $"[ {num} 回復 ]";
                    if (langCode == "CN")
                        return $"[ 恢复 {num} ]";
                    return $"[ {num} recovered ]";
            }
        }

        // デバフログのフォーマット
        public static string FormatDebuffLog(string conditionDetail, string targetName, string inflicterName)
        {
            string langCode = Lang.langCode;

            switch (ModConfig.DetailLevel.Value)
            {
                case ModConfig.LogDetailLevel.WithTarget:
                    if (langCode == "JP")
                        return $"[ {targetName} は {conditionDetail} を受けた ]";
                    if (langCode == "CN")
                        return $"[ {targetName} 受到 {conditionDetail} ]";
                    return $"[ {targetName} affected by {conditionDetail} ]";

                default: // NumberOnly
                    return $"[ {conditionDetail} ]";
            }
        }

        // バフログのフォーマット
        public static string FormatBuffLog(string conditionDetail, string targetName, string casterName)
        {
            string langCode = Lang.langCode;

            switch (ModConfig.DetailLevel.Value)
            {
                case ModConfig.LogDetailLevel.WithTarget:
                    if (langCode == "JP")
                        return $"[ {targetName} が {conditionDetail} を得た ]";
                    if (langCode == "CN")
                        return $"[ {targetName} 获得 {conditionDetail} ]";
                    return $"[ {targetName} gained {conditionDetail} ]";

                default: // NumberOnly
                    return $"[ {conditionDetail} ]";
            }
        }

        // Legacy compatibility
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
