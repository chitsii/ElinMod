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
# Actor IDs (Character IDs for CWL drama files)
# ============================================================================

class Actors:
    """
    キャラクターID定数

    これらのIDはCWLドラマファイルのactor列で使用され、
    ゲーム内のキャラクターIDと一致する必要がある。
    """
    # プレイヤー
    PC = "pc"

    # アリーナNPC
    LILY = "sukutsu_receptionist"       # リリィ（受付嬢）
    BALGAS = "sukutsu_arena_master"     # バルガス（アリーナマスター）
    ZEK = "sukutsu_shady_merchant"      # ゼク（怪しい商人）
    ASTAROTH = "sukutsu_grandmaster"    # アスタロト（グランドマスター）


# ============================================================================
# Quest IDs (Single Source of Truth for quest identifiers)
# ============================================================================

class QuestIds:
    """
    クエストID定数

    全てのクエストIDをここで一元管理。
    シナリオファイル、quest_dependencies.py、C#コードで使用する。
    """
    # === メインストーリー ===
    OPENING = "01_opening"                  # オープニング

    # === ランク昇格試験 ===
    RANK_UP_G = "02_rank_up_G"              # ランクG昇格（屑肉の洗礼）
    RANK_UP_F = "04_rank_up_F"              # ランクF昇格（凍土の魔犬）
    RANK_UP_E = "06_rank_up_E"              # ランクE昇格（錆びついた英雄カイン）
    RANK_UP_D = "10_rank_up_D"              # ランクD昇格（銅貨稼ぎの洗礼）
    RANK_UP_C = "09_rank_up_C"              # ランクC昇格（闘技場の鴉）
    RANK_UP_B = "11_rank_up_B"              # ランクB昇格（虚無の処刑人ヌル）
    RANK_UP_A = "12_rank_up_A"              # ランクA昇格（影との戦い）
    RANK_UP_S = "15_vs_balgas"              # ランクS昇格（バルガス戦）

    # === ゼクルート ===
    ZEK_INTRO = "03_zek_intro"              # ゼク初遭遇
    ZEK_STEAL_BOTTLE = "05_2_zek_steal_bottle"    # 器すり替え提案
    ZEK_STEAL_SOULGEM = "06_2_zek_steal_soulgem"  # カイン魂の選択

    # === キャラクターイベント ===
    LILY_EXPERIMENT = "05_1_lily_experiment"  # リリィの私的依頼
    LILY_PRIVATE = "08_lily_private"          # リリィの私室招待
    LILY_REAL_NAME = "16_lily_real_name"      # リリィの真名告白
    BALGAS_TRAINING = "09_balgas_training"    # バルガスの特別訓練
    UPPER_EXISTENCE = "07_upper_existence"    # 高次元存在の真実

    # === 後半メインストーリー ===
    MAKUMA = "12_makuma"                    # ヌルの記憶チップ
    MAKUMA2 = "13_makuma2"                  # 虚空の心臓製作
    VS_GRANDMASTER_1 = "17_vs_grandmaster_1"  # アスタロト初遭遇・逃亡
    LAST_BATTLE = "18_last_battle"          # 最終決戦


# ============================================================================
# Flag Integer Values (for dialogFlags which only accepts integers)
# ============================================================================

class FlagValues:
    """
    フラグ値定数（dialogFlagsは整数のみ対応）

    各フラグの取り得る値を定数として定義。
    シナリオファイルではこれらの定数を使用してset_flag/branch_ifを呼び出す。
    """

    # --- Boolean Flags (True/False) ---
    FALSE = 0
    TRUE = 1

    class BottleChoice:
        """共鳴瓶の選択（05_2_zek_steal_bottle）"""
        # Enum ordinals are 0-based: BottleChoice enum has 2 values
        REFUSED = 0   # 拒否
        SWAPPED = 1   # すり替えた

    class KainSoulChoice:
        """カインの魂の選択（06_2_zek_steal_soulgem）"""
        # Enum ordinals are 0-based: KainSoulChoice enum has 2 values
        RETURNED = 0  # バルガスに返した
        SOLD = 1      # ゼクに売った

    class LilyBottleConfession:
        """瓶すり替え発覚時の告白（13_makuma2）"""
        # Enum ordinals are 0-based: LilyBottleConfession enum has 3 values
        CONFESSED = 0   # 正直に告白
        BLAMED_ZEK = 1  # ゼクのせいにした
        DENIED = 2      # 否定した

    class KainSoulConfession:
        """カイン魂売却発覚時の告白（13_makuma2）"""
        # Enum ordinals are 0-based: KainSoulConfession enum has 2 values
        CONFESSED = 0  # 正直に告白
        LIED = 1       # 嘘をついた

    class BalgasChoice:
        """バルガス戦での選択（15_vs_balgas）"""
        # Enum ordinals are 0-based: BalgasChoice enum has 2 values
        SPARED = 0     # 見逃した
        KILLED = 1     # 倒した

    class LilyTrueName:
        """リリィの真名（16_lily_real_name）"""
        # Boolean flag uses TRUE = 1
        KNOWN = 1      # 真名を知っている

    class Ending:
        """エンディング選択（18_last_battle）"""
        # Enum ordinals are 0-based: Ending enum has 3 values
        RETURN_TO_SURFACE = 0     # 地上に戻る
        REBUILD_ARENA = 1         # アリーナを再建
        CHALLENGE_OBSERVERS = 2   # 観客に挑む

    class Motivation:
        """プレイヤーの動機"""
        GREED = 0       # 強欲
        BATTLE_LUST = 1 # 戦闘狂
        NIHILISM = 2    # 虚無
        ARROGANCE = 3   # 傲慢

    class Phase:
        """ストーリーフェーズ"""
        # Enum ordinals are 0-based: Phase enum has 6 values
        PROLOGUE = 0      # ゲーム開始〜初戦
        INITIATION = 1    # Rank G〜F
        RISING = 2        # Rank E〜D
        AWAKENING = 3     # Rank C〜B
        CONFRONTATION = 4 # Rank A
        CLIMAX = 5        # 逃亡〜最終決戦


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


class Phase(Enum):
    """ストーリーフェーズ（クエスト依存関係管理用）"""
    PROLOGUE = "prologue"           # 0: ゲーム開始〜初戦
    INITIATION = "initiation"       # 1: Rank G〜F (チュートリアル完了)
    RISING = "rising"               # 2: Rank E〜D (カイン戦、観客介入導入)
    AWAKENING = "awakening"         # 3: Rank C〜B (英雄残党、ヌル戦、真名イベント)
    CONFRONTATION = "confrontation" # 4: Rank A (アスタロト対決、裏切り発覚)
    CLIMAX = "climax"               # 5: 逃亡〜最終決戦

    def __ge__(self, other):
        if not isinstance(other, Phase):
            return NotImplemented
        order = list(Phase)
        return order.index(self) >= order.index(other)

    def __gt__(self, other):
        if not isinstance(other, Phase):
            return NotImplemented
        order = list(Phase)
        return order.index(self) > order.index(other)

    def __le__(self, other):
        if not isinstance(other, Phase):
            return NotImplemented
        order = list(Phase)
        return order.index(self) <= order.index(other)

    def __lt__(self, other):
        if not isinstance(other, Phase):
            return NotImplemented
        order = list(Phase)
        return order.index(self) < order.index(other)


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

    current_phase = EnumFlag(
        key="player.current_phase",
        enum_type=Phase,
        default=Phase.PROLOGUE,
        description="現在のストーリーフェーズ"
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
        Phase,
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
    CURRENT_PHASE = PlayerFlags.current_phase.full_key
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
