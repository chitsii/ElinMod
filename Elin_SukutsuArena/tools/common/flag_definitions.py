"""
Arena Flag Definitions - Single Source of Truth

This module defines all flags used in the Sukutsu Arena mod.
Import this module in scenarios.py and generate_flags.py for type-safe access.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Type, Any

# ============================================================================
# Prefix
# ============================================================================
PREFIX = "chitsii.arena"


# ============================================================================
# Enum Definitions
# ============================================================================

class Motivation(Enum):
    """プレイヤーの動機選択"""
    GREED = "greed"
    BATTLE_LUST = "battle_lust"
    NIHILISM = "nihilism"
    ARROGANCE = "arrogance"


class Rank(Enum):
    """闘技場ランク（昇順）"""
    UNRANKED = "unranked"
    G = "G"
    F = "F"
    E = "E"
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    S = "S"
    SS = "SS"
    SSS = "SSS"
    U = "U"
    Z = "Z"
    GOD_SLAYER = "god_slayer"
    SINGULARITY = "singularity"
    VOID_KING = "void_king"

    def __ge__(self, other):
        if not isinstance(other, Rank):
            return NotImplemented
        order = list(Rank)
        return order.index(self) >= order.index(other)

    def __gt__(self, other):
        if not isinstance(other, Rank):
            return NotImplemented
        order = list(Rank)
        return order.index(self) > order.index(other)

    def __le__(self, other):
        if not isinstance(other, Rank):
            return NotImplemented
        order = list(Rank)
        return order.index(self) <= order.index(other)

    def __lt__(self, other):
        if not isinstance(other, Rank):
            return NotImplemented
        order = list(Rank)
        return order.index(self) < order.index(other)


class BottleChoice(Enum):
    """共鳴瓶の選択（scenario/05_2）"""
    REFUSED = "refused"
    SWAPPED = "swapped"


class KainSoulChoice(Enum):
    """カインの魂の選択（scenario/06_2）"""
    RETURNED = "returned"
    SOLD = "sold"


class BalgasChoice(Enum):
    """バルガス戦の選択（scenario/15）"""
    SPARED = "spared"
    KILLED = "killed"


class LilyBottleConfession(Enum):
    """瓶すり替え発覚時の告白（scenario/13）"""
    CONFESSED = "confessed"
    BLAMED_ZEK = "blamed_zek"
    DENIED = "denied"


class KainSoulConfession(Enum):
    """カイン魂売却発覚時の告白（scenario/13）"""
    CONFESSED = "confessed"
    LIED = "lied"


class Ending(Enum):
    """エンディング選択（scenario/18）"""
    RETURN_TO_SURFACE = "return_to_surface"
    REBUILD_ARENA = "rebuild_arena"
    CHALLENGE_OBSERVERS = "challenge_observers"


# ============================================================================
# Flag Definition Classes
# ============================================================================

@dataclass
class FlagDef:
    """Base class for flag definitions"""
    key: str
    description: str = ""

    @property
    def full_key(self) -> str:
        return f"{PREFIX}.{self.key}"


@dataclass
class EnumFlag(FlagDef):
    """Enum型フラグ"""
    enum_type: Type[Enum] = None
    default: Optional[Enum] = None


@dataclass
class IntFlag(FlagDef):
    """整数型フラグ"""
    default: int = 0
    min_value: int = -100
    max_value: int = 100


@dataclass
class BoolFlag(FlagDef):
    """真偽値型フラグ"""
    default: bool = False


@dataclass
class StringFlag(FlagDef):
    """文字列型フラグ"""
    default: Optional[str] = None


# ============================================================================
# Flag Instances - Player State
# ============================================================================

class PlayerFlags:
    """プレイヤー状態フラグ"""

    motivation = EnumFlag(
        key="player.motivation",
        enum_type=Motivation,
        default=None,
        description="プレイヤーの動機選択"
    )

    rank = EnumFlag(
        key="player.rank",
        enum_type=Rank,
        default=Rank.UNRANKED,
        description="現在の闘技場ランク"
    )

    karma = IntFlag(
        key="player.karma",
        default=0,
        min_value=-100,
        max_value=100,
        description="カルマ値（善悪度）"
    )

    contribution = IntFlag(
        key="player.contribution",
        default=0,
        min_value=0,
        max_value=1000,
        description="闘技場貢献度（ランクアップ条件）"
    )

    fugitive_status = BoolFlag(
        key="player.fugitive_status",
        default=False,
        description="逃亡者状態（scenario/17以降）"
    )

    lily_true_name = StringFlag(
        key="player.lily_true_name",
        default=None,
        description="リリィの真名（獲得済みの場合）"
    )

    null_chip_obtained = BoolFlag(
        key="player.null_chip_obtained",
        default=False,
        description="ヌルの記憶チップ入手済み"
    )

    lily_trust_rebuilding = BoolFlag(
        key="player.lily_trust_rebuilding",
        default=False,
        description="リリィとの信頼再構築中"
    )

    ending = EnumFlag(
        key="player.ending",
        enum_type=Ending,
        default=None,
        description="選択したエンディング"
    )

    # === 重要選択フラグ ===
    bottle_choice = EnumFlag(
        key="player.bottle_choice",
        enum_type=BottleChoice,
        default=None,
        description="共鳴瓶すり替えの選択"
    )

    kain_soul_choice = EnumFlag(
        key="player.kain_soul_choice",
        enum_type=KainSoulChoice,
        default=None,
        description="カインの魂の選択"
    )

    balgas_choice = EnumFlag(
        key="player.balgas_choice",
        enum_type=BalgasChoice,
        default=None,
        description="バルガス戦での選択"
    )

    lily_bottle_confession = EnumFlag(
        key="player.lily_bottle_confession",
        enum_type=LilyBottleConfession,
        default=None,
        description="瓶すり替え発覚時の告白"
    )

    kain_soul_confession = EnumFlag(
        key="player.kain_soul_confession",
        enum_type=KainSoulConfession,
        default=None,
        description="カイン魂売却発覚時の告白"
    )

    # === 状態フラグ ===
    lily_hostile = BoolFlag(
        key="player.lily_hostile",
        default=False,
        description="リリィ敵対状態"
    )

    balgas_trust_broken = BoolFlag(
        key="player.balgas_trust_broken",
        default=False,
        description="バルガスとの信頼崩壊"
    )


# ============================================================================
# Flag Instances - Relationship Values
# ============================================================================

class RelFlags:
    """NPC関係値フラグ"""

    lily = IntFlag(
        key="rel.lily",
        default=30,
        min_value=0,
        max_value=100,
        description="リリィとの関係値"
    )

    balgas = IntFlag(
        key="rel.balgas",
        default=20,
        min_value=0,
        max_value=100,
        description="バルガスとの関係値"
    )

    zek = IntFlag(
        key="rel.zek",
        default=0,
        min_value=0,
        max_value=100,
        description="ゼクとの関係値"
    )


# ============================================================================
# Helper Functions
# ============================================================================

def get_all_flags() -> List[FlagDef]:
    """Get all defined flags as a flat list"""
    flags = []

    for name in dir(PlayerFlags):
        if not name.startswith('_'):
            attr = getattr(PlayerFlags, name)
            if isinstance(attr, FlagDef):
                flags.append(attr)

    for name in dir(RelFlags):
        if not name.startswith('_'):
            attr = getattr(RelFlags, name)
            if isinstance(attr, FlagDef):
                flags.append(attr)

    return flags


def get_all_enums() -> List[Type[Enum]]:
    """Get all defined enums"""
    return [
        Motivation,
        Rank,
        BottleChoice,
        KainSoulChoice,
        BalgasChoice,
        LilyBottleConfession,
        KainSoulConfession,
        Ending,
    ]


# ============================================================================
# Convenience Shortcuts (for scenarios.py)
# ============================================================================

# Flag key shortcuts
class Keys:
    """Quick access to full flag keys for use in scenarios"""
    # Player
    MOTIVATION = PlayerFlags.motivation.full_key
    RANK = PlayerFlags.rank.full_key
    KARMA = PlayerFlags.karma.full_key
    CONTRIBUTION = PlayerFlags.contribution.full_key
    FUGITIVE = PlayerFlags.fugitive_status.full_key
    LILY_TRUE_NAME = PlayerFlags.lily_true_name.full_key
    NULL_CHIP = PlayerFlags.null_chip_obtained.full_key
    LILY_TRUST_REBUILD = PlayerFlags.lily_trust_rebuilding.full_key
    ENDING = PlayerFlags.ending.full_key

    # Choices
    BOTTLE_CHOICE = PlayerFlags.bottle_choice.full_key
    KAIN_SOUL_CHOICE = PlayerFlags.kain_soul_choice.full_key
    BALGAS_CHOICE = PlayerFlags.balgas_choice.full_key
    LILY_BOTTLE_CONFESSION = PlayerFlags.lily_bottle_confession.full_key
    KAIN_SOUL_CONFESSION = PlayerFlags.kain_soul_confession.full_key

    # States
    LILY_HOSTILE = PlayerFlags.lily_hostile.full_key
    BALGAS_TRUST_BROKEN = PlayerFlags.balgas_trust_broken.full_key

    # Relationships
    REL_LILY = RelFlags.lily.full_key
    REL_BALGAS = RelFlags.balgas.full_key
    REL_ZEK = RelFlags.zek.full_key


# ============================================================================
# Unit Tests
# ============================================================================

if __name__ == "__main__":
    print("=== Flag Definitions Test ===\n")

    # Test all flags are accessible
    all_flags = get_all_flags()
    print(f"Total flags defined: {len(all_flags)}")

    for flag in all_flags:
        print(f"  - {flag.full_key} ({type(flag).__name__})")

    print(f"\nTotal enums defined: {len(get_all_enums())}")
    for enum_type in get_all_enums():
        print(f"  - {enum_type.__name__}: {[e.value for e in enum_type]}")

    # Test Rank comparison
    print("\n=== Rank Comparison Test ===")
    assert Rank.S > Rank.A, "S should be greater than A"
    assert Rank.A >= Rank.A, "A should be >= A"
    assert Rank.G < Rank.F, "G should be less than F"
    assert Rank.UNRANKED <= Rank.G, "UNRANKED should be <= G"
    print("All rank comparisons passed!")

    # Test Keys
    print("\n=== Keys Test ===")
    print(f"MOTIVATION key: {Keys.MOTIVATION}")
    print(f"REL_LILY key: {Keys.REL_LILY}")

    print("\n=== All Tests Passed! ===")
