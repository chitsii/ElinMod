using System;
using Elin_SukutsuArena.Core;
using Elin_SukutsuArena.Flags;

namespace Elin_SukutsuArena.State
{
    /// <summary>
    /// プレイヤーの状態管理
    /// </summary>
    public class PlayerState
    {
        private readonly IFlagStorage _storage;

        public PlayerState(IFlagStorage storage)
        {
            _storage = storage;
        }

        // --- Motivation ---
        public Motivation? GetMotivation()
        {
            var value = _storage.GetInt(ArenaFlagKeys.Motivation, -1);
            if (value < 0 || value >= 4) return null;
            return (Motivation)value;
        }

        public void SetMotivation(Motivation motivation)
        {
            _storage.SetInt(ArenaFlagKeys.Motivation, (int)motivation);
        }

        // --- Rank ---
        public Rank Rank
        {
            get
            {
                var value = _storage.GetInt(ArenaFlagKeys.Rank, 0);
                if (value < 0 || value > 15) return Rank.Unranked;
                return (Rank)value;
            }
            set => _storage.SetInt(ArenaFlagKeys.Rank, (int)value);
        }

        public bool IsRankAtLeast(Rank minRank)
        {
            return Rank >= minRank;
        }

        // --- Phase ---
        public Phase CurrentPhase
        {
            get
            {
                var value = _storage.GetInt(ArenaFlagKeys.CurrentPhase, 0);
                if (value < 0 || value > 5) return Phase.Prologue;
                return (Phase)value;
            }
            set => _storage.SetInt(ArenaFlagKeys.CurrentPhase, (int)value);
        }

        // --- Karma ---
        public int Karma
        {
            get => _storage.GetInt(ArenaFlagKeys.Karma);
            set => _storage.SetInt(ArenaFlagKeys.Karma, Clamp(value, -100, 100));
        }

        public void AddKarma(int delta) => Karma += delta;

        // --- Contribution ---
        public int Contribution
        {
            get => _storage.GetInt(ArenaFlagKeys.Contribution);
            set => _storage.SetInt(ArenaFlagKeys.Contribution, Clamp(value, 0, 1000));
        }

        public void AddContribution(int delta) => Contribution += delta;

        // --- Boolean Flags ---
        public bool IsFugitive
        {
            get => GetBool(ArenaFlagKeys.FugitiveStatus);
            set => SetBool(ArenaFlagKeys.FugitiveStatus, value);
        }

        public bool HasNullChip
        {
            get => GetBool(ArenaFlagKeys.NullChipObtained);
            set => SetBool(ArenaFlagKeys.NullChipObtained, value);
        }

        public bool IsLilyTrustRebuilding
        {
            get => GetBool(ArenaFlagKeys.LilyTrustRebuilding);
            set => SetBool(ArenaFlagKeys.LilyTrustRebuilding, value);
        }

        public bool IsLilyHostile
        {
            get => GetBool(ArenaFlagKeys.LilyHostile);
            set => SetBool(ArenaFlagKeys.LilyHostile, value);
        }

        public bool IsBalgasTrustBroken
        {
            get => GetBool(ArenaFlagKeys.BalgasTrustBroken);
            set => SetBool(ArenaFlagKeys.BalgasTrustBroken, value);
        }

        public bool KnowsLilyTrueName
        {
            get => GetBool(ArenaFlagKeys.LilyTrueName);
            set => SetBool(ArenaFlagKeys.LilyTrueName, value);
        }

        // --- Choice Flags ---
        public BottleChoice? GetBottleChoice()
        {
            var value = _storage.GetInt(ArenaFlagKeys.BottleChoice, -1);
            if (value < 0 || value >= 2) return null;
            return (BottleChoice)value;
        }

        public void SetBottleChoice(BottleChoice choice)
        {
            _storage.SetInt(ArenaFlagKeys.BottleChoice, (int)choice);
        }

        public KainSoulChoice? GetKainSoulChoice()
        {
            var value = _storage.GetInt(ArenaFlagKeys.KainSoulChoice, -1);
            if (value < 0 || value >= 2) return null;
            return (KainSoulChoice)value;
        }

        public void SetKainSoulChoice(KainSoulChoice choice)
        {
            _storage.SetInt(ArenaFlagKeys.KainSoulChoice, (int)choice);
        }

        public BalgasChoice? GetBalgasChoice()
        {
            var value = _storage.GetInt(ArenaFlagKeys.BalgasChoice, -1);
            if (value < 0 || value >= 2) return null;
            return (BalgasChoice)value;
        }

        public void SetBalgasChoice(BalgasChoice choice)
        {
            _storage.SetInt(ArenaFlagKeys.BalgasChoice, (int)choice);
        }

        public LilyBottleConfession? GetLilyBottleConfession()
        {
            var value = _storage.GetInt(ArenaFlagKeys.LilyBottleConfession, -1);
            if (value < 0 || value >= 3) return null;
            return (LilyBottleConfession)value;
        }

        public void SetLilyBottleConfession(LilyBottleConfession choice)
        {
            _storage.SetInt(ArenaFlagKeys.LilyBottleConfession, (int)choice);
        }

        public KainSoulConfession? GetKainSoulConfession()
        {
            var value = _storage.GetInt(ArenaFlagKeys.KainSoulConfession, -1);
            if (value < 0 || value >= 2) return null;
            return (KainSoulConfession)value;
        }

        public void SetKainSoulConfession(KainSoulConfession choice)
        {
            _storage.SetInt(ArenaFlagKeys.KainSoulConfession, (int)choice);
        }

        public Ending? GetEnding()
        {
            var value = _storage.GetInt(ArenaFlagKeys.Ending, -1);
            if (value < 0 || value >= 3) return null;
            return (Ending)value;
        }

        public void SetEnding(Ending ending)
        {
            _storage.SetInt(ArenaFlagKeys.Ending, (int)ending);
        }

        // --- Scenario Condition Helpers ---

        /// <summary>
        /// リリィの真名開示条件をチェック
        /// </summary>
        public bool CanShowLilyTrueName()
        {
            if (Rank != Rank.S) return false;
            if (GetBalgasChoice() != BalgasChoice.Spared) return false;

            var confession = GetLilyBottleConfession();
            if (confession == LilyBottleConfession.BlamedZek || confession == LilyBottleConfession.Denied) return false;
            if (IsLilyHostile) return false;

            return true;
        }

        /// <summary>
        /// 最終決戦でのバルガス参戦条件をチェック
        /// </summary>
        public bool CanBalgasJoinFinalBattle()
        {
            return !IsBalgasTrustBroken && GetBalgasChoice() == BalgasChoice.Spared;
        }

        /// <summary>
        /// 最終決戦でのリリィ参戦条件をチェック
        /// </summary>
        public bool CanLilyJoinFinalBattle()
        {
            return !IsLilyHostile;
        }

        // --- Private Helpers ---
        private bool GetBool(string key)
        {
            return _storage.GetInt(key) != 0;
        }

        private void SetBool(string key, bool value)
        {
            _storage.SetInt(key, value ? 1 : 0);
        }

        private static int Clamp(int value, int min, int max)
        {
            if (value < min) return min;
            if (value > max) return max;
            return value;
        }
    }
}
