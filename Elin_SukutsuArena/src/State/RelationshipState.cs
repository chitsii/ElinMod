using Elin_SukutsuArena.Core;
using Elin_SukutsuArena.Flags;

namespace Elin_SukutsuArena.State
{
    /// <summary>
    /// NPC関係値の状態管理
    /// </summary>
    public class RelationshipState
    {
        private readonly IFlagStorage _storage;

        public RelationshipState(IFlagStorage storage)
        {
            _storage = storage;
        }

        /// <summary>リリィとの関係値 (0-100, 初期値30)</summary>
        public int Lily
        {
            get => _storage.GetInt(ArenaFlagKeys.Rellily, 30);
            set => _storage.SetInt(ArenaFlagKeys.Rellily, Clamp(value, 0, 100));
        }

        public void AddLily(int delta) => Lily += delta;

        /// <summary>バルガスとの関係値 (0-100, 初期値20)</summary>
        public int Balgas
        {
            get => _storage.GetInt(ArenaFlagKeys.Relbalgas, 20);
            set => _storage.SetInt(ArenaFlagKeys.Relbalgas, Clamp(value, 0, 100));
        }

        public void AddBalgas(int delta) => Balgas += delta;

        /// <summary>ゼクとの関係値 (0-100, 初期値0)</summary>
        public int Zek
        {
            get => _storage.GetInt(ArenaFlagKeys.Relzek, 0);
            set => _storage.SetInt(ArenaFlagKeys.Relzek, Clamp(value, 0, 100));
        }

        public void AddZek(int delta) => Zek += delta;

        private static int Clamp(int value, int min, int max)
        {
            if (value < min) return min;
            if (value > max) return max;
            return value;
        }
    }
}
