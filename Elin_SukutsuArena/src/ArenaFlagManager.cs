using System;
using Elin_SukutsuArena.Flags;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// アリーナフラグ管理クラス
    /// EClass.player.dialogFlags (Dictionary&lt;string, int&gt;) のラッパーとして、型安全なフラグアクセスを提供
    /// </summary>
    public static class ArenaFlagManager
    {
        // ============================================================================
        // Low-level Access (EClass.player.dialogFlags wrapper)
        // dialogFlags is Dictionary<string, int>
        // ============================================================================

        /// <summary>フラグ値を整数として取得</summary>
        public static int GetInt(string key, int defaultValue = 0)
        {
            if (EClass.player?.dialogFlags == null) return defaultValue;
            return EClass.player.dialogFlags.TryGetValue(key, out var value) ? value : defaultValue;
        }

        /// <summary>フラグ値を整数として設定</summary>
        public static void SetInt(string key, int value)
        {
            if (EClass.player?.dialogFlags == null) return;
            EClass.player.dialogFlags[key] = value;
        }

        /// <summary>整数フラグに加算</summary>
        public static void AddInt(string key, int delta)
        {
            var current = GetInt(key);
            SetInt(key, current + delta);
        }

        /// <summary>フラグ値を真偽値として取得 (0 = false, else = true)</summary>
        public static bool GetBool(string key, bool defaultValue = false)
        {
            if (EClass.player?.dialogFlags == null) return defaultValue;
            if (!EClass.player.dialogFlags.TryGetValue(key, out var value)) return defaultValue;
            return value != 0;
        }

        /// <summary>フラグ値を真偽値として設定 (true = 1, false = 0)</summary>
        public static void SetBool(string key, bool value)
        {
            SetInt(key, value ? 1 : 0);
        }

        /// <summary>フラグが存在するかチェック</summary>
        public static bool HasFlag(string key)
        {
            if (EClass.player?.dialogFlags == null) return false;
            return EClass.player.dialogFlags.ContainsKey(key);
        }

        /// <summary>値をクランプ (.NET 4.x互換)</summary>
        private static int Clamp(int value, int min, int max)
        {
            if (value < min) return min;
            if (value > max) return max;
            return value;
        }

        // ============================================================================
        // Player Flags - Typed Access
        // ============================================================================

        public static class Player
        {
            // --- Motivation (stored as enum ordinal) ---
            public static Motivation? GetMotivation()
            {
                var value = GetInt(ArenaFlagKeys.Motivation, -1);
                if (value < 0 || value >= 4) return null;
                return (Motivation)value;
            }

            public static void SetMotivation(Motivation motivation)
            {
                SetInt(ArenaFlagKeys.Motivation, (int)motivation);
            }

            // --- Rank (stored as enum ordinal) ---
            public static Rank GetRank()
            {
                var value = GetInt(ArenaFlagKeys.Rank, 0);
                if (value < 0 || value > 8) return Rank.Unranked;
                return (Rank)value;
            }

            public static void SetRank(Rank rank)
            {
                SetInt(ArenaFlagKeys.Rank, (int)rank);
            }

            public static bool IsRankAtLeast(Rank minRank)
            {
                return GetRank() >= minRank;
            }

            // --- Karma ---
            public static int GetKarma() => GetInt(ArenaFlagKeys.Karma);
            public static void SetKarma(int value) => SetInt(ArenaFlagKeys.Karma, Clamp(value, -100, 100));
            public static void AddKarma(int delta) => SetKarma(GetKarma() + delta);

            // --- Boolean Flags ---
            public static bool IsFugitive => GetBool(ArenaFlagKeys.FugitiveStatus);
            public static void SetFugitive(bool value) => SetBool(ArenaFlagKeys.FugitiveStatus, value);

            public static bool HasNullChip => GetBool(ArenaFlagKeys.NullChipObtained);
            public static void SetNullChipObtained(bool value) => SetBool(ArenaFlagKeys.NullChipObtained, value);

            public static bool IsLilyTrustRebuilding => GetBool(ArenaFlagKeys.LilyTrustRebuilding);
            public static void SetLilyTrustRebuilding(bool value) => SetBool(ArenaFlagKeys.LilyTrustRebuilding, value);

            public static bool IsLilyHostile => GetBool(ArenaFlagKeys.LilyHostile);
            public static void SetLilyHostile(bool value) => SetBool(ArenaFlagKeys.LilyHostile, value);

            public static bool IsBalgasTrustBroken => GetBool(ArenaFlagKeys.BalgasTrustBroken);
            public static void SetBalgasTrustBroken(bool value) => SetBool(ArenaFlagKeys.BalgasTrustBroken, value);

            // --- LilyTrueName (stored as 1 if known, key in separate string storage if needed) ---
            // Since dialogFlags only stores int, we use 1 = known, 0 = unknown
            public static bool KnowsLilyTrueName => GetBool(ArenaFlagKeys.LilyTrueName);
            public static void SetLilyTrueNameKnown(bool known) => SetBool(ArenaFlagKeys.LilyTrueName, known);

            // --- Choice Flags (stored as enum ordinal, -1 = not chosen) ---
            public static BottleChoice? GetBottleChoice()
            {
                var value = GetInt(ArenaFlagKeys.BottleChoice, -1);
                if (value < 0 || value >= 2) return null;
                return (BottleChoice)value;
            }
            public static void SetBottleChoice(BottleChoice choice)
            {
                SetInt(ArenaFlagKeys.BottleChoice, (int)choice);
            }

            public static KainSoulChoice? GetKainSoulChoice()
            {
                var value = GetInt(ArenaFlagKeys.KainSoulChoice, -1);
                if (value < 0 || value >= 2) return null;
                return (KainSoulChoice)value;
            }
            public static void SetKainSoulChoice(KainSoulChoice choice)
            {
                SetInt(ArenaFlagKeys.KainSoulChoice, (int)choice);
            }

            public static BalgasChoice? GetBalgasChoice()
            {
                var value = GetInt(ArenaFlagKeys.BalgasChoice, -1);
                if (value < 0 || value >= 2) return null;
                return (BalgasChoice)value;
            }
            public static void SetBalgasChoice(BalgasChoice choice)
            {
                SetInt(ArenaFlagKeys.BalgasChoice, (int)choice);
            }

            public static LilyBottleConfession? GetLilyBottleConfession()
            {
                var value = GetInt(ArenaFlagKeys.LilyBottleConfession, -1);
                if (value < 0 || value >= 3) return null;
                return (LilyBottleConfession)value;
            }
            public static void SetLilyBottleConfession(LilyBottleConfession choice)
            {
                SetInt(ArenaFlagKeys.LilyBottleConfession, (int)choice);
            }

            public static KainSoulConfession? GetKainSoulConfession()
            {
                var value = GetInt(ArenaFlagKeys.KainSoulConfession, -1);
                if (value < 0 || value >= 2) return null;
                return (KainSoulConfession)value;
            }
            public static void SetKainSoulConfession(KainSoulConfession choice)
            {
                SetInt(ArenaFlagKeys.KainSoulConfession, (int)choice);
            }

            public static Ending? GetEnding()
            {
                var value = GetInt(ArenaFlagKeys.Ending, -1);
                if (value < 0 || value >= 3) return null;
                return (Ending)value;
            }
            public static void SetEnding(Ending ending)
            {
                SetInt(ArenaFlagKeys.Ending, (int)ending);
            }
        }

        // ============================================================================
        // Relationship Flags
        // ============================================================================

        public static class Rel
        {
            // --- Lily ---
            public static int Lily
            {
                get => GetInt(ArenaFlagKeys.Rellily, 30);
                set => SetInt(ArenaFlagKeys.Rellily, Clamp(value, 0, 100));
            }
            public static void AddLily(int delta) => Lily = Lily + delta;

            // --- Balgas ---
            public static int Balgas
            {
                get => GetInt(ArenaFlagKeys.Relbalgas, 20);
                set => SetInt(ArenaFlagKeys.Relbalgas, Clamp(value, 0, 100));
            }
            public static void AddBalgas(int delta) => Balgas = Balgas + delta;

            // --- Zek ---
            public static int Zek
            {
                get => GetInt(ArenaFlagKeys.Relzek, 0);
                set => SetInt(ArenaFlagKeys.Relzek, Clamp(value, 0, 100));
            }
            public static void AddZek(int delta) => Zek = Zek + delta;
        }

        // ============================================================================
        // Convenience Methods for Scenario Conditions
        // ============================================================================

        /// <summary>
        /// リリィの真名開示条件をチェック
        /// scenario/16の発生条件
        /// </summary>
        public static bool CanShowLilyTrueName()
        {
            // Require: Rank S, Balgas spared, Lily relationship >= 50
            if (Player.GetRank() != Rank.S) return false;
            if (Player.GetBalgasChoice() != BalgasChoice.Spared) return false;
            if (Rel.Lily < 50) return false;

            // Block conditions
            var confession = Player.GetLilyBottleConfession();
            if (confession == LilyBottleConfession.BlamedZek || confession == LilyBottleConfession.Denied) return false;
            if (Player.IsLilyHostile) return false;

            return true;
        }

        /// <summary>
        /// 最終決戦でのバルガス参戦条件をチェック
        /// </summary>
        public static bool CanBalgasJoinFinalBattle()
        {
            return !Player.IsBalgasTrustBroken && Player.GetBalgasChoice() == BalgasChoice.Spared;
        }

        /// <summary>
        /// 最終決戦でのリリィ参戦条件をチェック
        /// </summary>
        public static bool CanLilyJoinFinalBattle()
        {
            return !Player.IsLilyHostile;
        }

        // ============================================================================
        // Debug / Testing
        // ============================================================================

        /// <summary>全フラグをログ出力</summary>
        public static void DebugLogAllFlags()
        {
            UnityEngine.Debug.Log("[ArenaFlags] === Current Flag State ===");
            UnityEngine.Debug.Log($"  Motivation: {Player.GetMotivation()?.ToString() ?? "null"}");
            UnityEngine.Debug.Log($"  Rank: {Player.GetRank()}");
            UnityEngine.Debug.Log($"  Karma: {Player.GetKarma()}");
            UnityEngine.Debug.Log($"  Fugitive: {Player.IsFugitive}");
            UnityEngine.Debug.Log($"  NullChip: {Player.HasNullChip}");
            UnityEngine.Debug.Log($"  LilyTrueNameKnown: {Player.KnowsLilyTrueName}");
            UnityEngine.Debug.Log($"  Rel.Lily: {Rel.Lily}");
            UnityEngine.Debug.Log($"  Rel.Balgas: {Rel.Balgas}");
            UnityEngine.Debug.Log($"  Rel.Zek: {Rel.Zek}");
            UnityEngine.Debug.Log($"  BottleChoice: {Player.GetBottleChoice()?.ToString() ?? "null"}");
            UnityEngine.Debug.Log($"  KainSoulChoice: {Player.GetKainSoulChoice()?.ToString() ?? "null"}");
            UnityEngine.Debug.Log($"  BalgasChoice: {Player.GetBalgasChoice()?.ToString() ?? "null"}");
            UnityEngine.Debug.Log("[ArenaFlags] === End ===");
        }
    }
}
