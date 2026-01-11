using System.Collections.Generic;

namespace Elin_SukutsuArena.Data
{
    /// <summary>
    /// ドラマスクリプトのジャンプラベル
    /// </summary>
    public enum JumpLabel
    {
        None = 0,

        // ランクアップ系 (11-17)
        StartRankG = 11,
        StartRankF = 12,
        StartRankE = 13,
        StartRankD = 14,
        StartRankC = 15,
        StartRankB = 16,
        StartRankA = 17,

        // ストーリークエスト系 (21-33)
        QuestZekIntro = 21,
        QuestLilyExp = 22,
        QuestZekStealBottle = 23,
        QuestZekStealSoulgem = 24,
        QuestUpperExistence = 25,
        QuestLilyPrivate = 26,
        QuestBalgasTraining = 27,
        QuestMakuma = 28,
        QuestMakuma2 = 29,
        QuestVsBalgas = 30,
        QuestLilyRealName = 31,
        QuestVsGrandmaster1 = 32,
        QuestLastBattle = 33,
    }

    /// <summary>
    /// 文字列ラベルとJumpLabel enumのマッピング
    /// </summary>
    public static class JumpLabelMapping
    {
        private static readonly Dictionary<string, JumpLabel> _labelToEnum = new Dictionary<string, JumpLabel>
        {
            // ランクアップ開始系
            ["start_rank_g"] = JumpLabel.StartRankG,
            ["start_rank_f"] = JumpLabel.StartRankF,
            ["start_rank_e"] = JumpLabel.StartRankE,
            ["start_rank_d"] = JumpLabel.StartRankD,
            ["start_rank_c"] = JumpLabel.StartRankC,
            ["start_rank_b"] = JumpLabel.StartRankB,
            ["start_rank_a"] = JumpLabel.StartRankA,

            // ランクアップクエスト確認系 (同じ値を共有)
            ["quest_rank_up_g"] = JumpLabel.StartRankG,
            ["quest_rank_up_f"] = JumpLabel.StartRankF,
            ["quest_rank_up_e"] = JumpLabel.StartRankE,
            ["quest_rank_up_d"] = JumpLabel.StartRankD,
            ["quest_rank_up_c"] = JumpLabel.StartRankC,
            ["quest_rank_up_b"] = JumpLabel.StartRankB,
            ["quest_rank_up_a"] = JumpLabel.StartRankA,

            // ストーリークエスト系
            ["quest_zek_intro"] = JumpLabel.QuestZekIntro,
            ["start_zek_intro"] = JumpLabel.QuestZekIntro,
            ["quest_lily_exp"] = JumpLabel.QuestLilyExp,
            ["start_lily_experiment"] = JumpLabel.QuestLilyExp,
            ["quest_zek_steal_bottle"] = JumpLabel.QuestZekStealBottle,
            ["start_zek_steal_bottle"] = JumpLabel.QuestZekStealBottle,
            ["quest_zek_steal_soulgem"] = JumpLabel.QuestZekStealSoulgem,
            ["start_zek_steal_soulgem"] = JumpLabel.QuestZekStealSoulgem,
            ["quest_upper_existence"] = JumpLabel.QuestUpperExistence,
            ["quest_lily_private"] = JumpLabel.QuestLilyPrivate,
            ["start_lily_private"] = JumpLabel.QuestLilyPrivate,
            ["quest_balgas_training"] = JumpLabel.QuestBalgasTraining,
            ["quest_makuma"] = JumpLabel.QuestMakuma,
            ["quest_makuma2"] = JumpLabel.QuestMakuma2,
            ["quest_vs_balgas"] = JumpLabel.QuestVsBalgas,
            ["quest_lily_real_name"] = JumpLabel.QuestLilyRealName,
            ["start_lily_real_name"] = JumpLabel.QuestLilyRealName,
            ["quest_vs_grandmaster_1"] = JumpLabel.QuestVsGrandmaster1,
            ["quest_last_battle"] = JumpLabel.QuestLastBattle,
        };

        private static readonly Dictionary<JumpLabel, string> _enumToLabel = new Dictionary<JumpLabel, string>();

        static JumpLabelMapping()
        {
            // 逆引き辞書を構築 (最初に登録されたラベルを優先)
            foreach (var kvp in _labelToEnum)
            {
                if (!_enumToLabel.ContainsKey(kvp.Value))
                {
                    _enumToLabel[kvp.Value] = kvp.Key;
                }
            }
        }

        /// <summary>
        /// 文字列ラベルからJumpLabel enumに変換
        /// </summary>
        public static JumpLabel FromString(string label)
        {
            if (string.IsNullOrEmpty(label)) return JumpLabel.None;
            return _labelToEnum.TryGetValue(label, out var result) ? result : JumpLabel.None;
        }

        /// <summary>
        /// JumpLabel enumから文字列ラベルに変換
        /// </summary>
        public static string ToString(JumpLabel label)
        {
            return _enumToLabel.TryGetValue(label, out var result) ? result : "";
        }

        /// <summary>
        /// 文字列ラベルが登録されているか確認
        /// </summary>
        public static bool IsRegistered(string label)
        {
            return !string.IsNullOrEmpty(label) && _labelToEnum.ContainsKey(label);
        }
    }
}
