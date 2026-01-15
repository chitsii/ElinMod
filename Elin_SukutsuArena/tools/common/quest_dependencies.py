"""
Quest Dependency Management System

This module defines the quest flow and dependencies for the Sukutsu Arena mod.
It provides a clear structure for quest progression based on flags.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
from flag_definitions import Keys, Phase, Actors, QuestIds


class QuestType(Enum):
    """クエストの種類"""
    MAIN_STORY = "main_story"          # メインストーリー
    RANK_UP = "rank_up"                # ランク昇格試験
    SIDE_QUEST = "side_quest"          # サイドクエスト
    CHARACTER_EVENT = "character_event" # キャラクターイベント
    ENDING = "ending"                   # エンディング


@dataclass
class FlagCondition:
    """フラグ条件"""
    flag_key: str
    operator: str  # "==", "!=", ">=", ">", "<=", "<"
    value: any

    def __str__(self):
        return f"{self.flag_key} {self.operator} {self.value}"


@dataclass
class QuestDefinition:
    """クエスト定義"""
    quest_id: str
    quest_type: QuestType
    drama_id: str  # 対応するドラマファイルID
    display_name_jp: str
    display_name_en: str
    description: str

    # フェーズベース依存関係
    phase: Phase = Phase.PROLOGUE  # このクエストが利用可能になるフェーズ
    quest_giver: Optional[str] = None  # クエストを与えるNPC (None = 自動発動)
    auto_trigger: bool = False  # ゾーン入場時に自動発動するか
    advances_phase: Optional[Phase] = None  # クリア時にフェーズを進める先

    # 前提条件
    required_flags: List[FlagCondition] = field(default_factory=list)
    required_quests: List[str] = field(default_factory=list)  # 前提クエストID

    # このクエスト完了時に設定されるフラグ
    completion_flags: Dict[str, any] = field(default_factory=dict)

    # このクエストで発生する可能性のある分岐選択
    branch_choices: List[str] = field(default_factory=list)

    # 排他的クエスト（このクエストが完了すると発生しなくなるクエスト）
    blocks_quests: List[str] = field(default_factory=list)

    # 優先度（同時に複数クエストが利用可能な場合の優先順位）
    priority: int = 0


# ========================================
# クエスト定義リスト
# ========================================

QUEST_DEFINITIONS = [
    # ========================================
    # メインストーリー - オープニング
    # ========================================
    QuestDefinition(
        quest_id=QuestIds.OPENING,
        quest_type=QuestType.MAIN_STORY,
        drama_id="sukutsu_opening",
        display_name_jp="異次元の闘技場への到着",
        display_name_en="Arrival at the Dimensional Arena",
        description="プレイヤーがアリーナに到着し、リリィとバルガスに出会う",
        phase=Phase.PROLOGUE,
        quest_giver=None,  # 自動発動
        auto_trigger=True,
        advances_phase=None,  # フェーズ進行なし（初戦勝利で進行）
        required_flags=[],
        required_quests=[],
        completion_flags={
            Keys.RANK: "unranked",
        },
        priority=1000,
    ),

    # ========================================
    # ランク昇格試験
    # ========================================
    QuestDefinition(
        quest_id=QuestIds.RANK_UP_G,
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_G",
        display_name_jp="ランクG昇格試験（屑肉の洗礼）",
        display_name_en="Rank G Promotion Trial (Baptism of Scraps)",
        description="最初の試練を突破し、ランクGを獲得する",
        phase=Phase.PROLOGUE,
        quest_giver=Actors.BALGAS,
        auto_trigger=False,
        advances_phase=Phase.INITIATION,
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.OPENING],
        completion_flags={},  # ランクはクエスト完了から推論
        priority=950,
    ),

    QuestDefinition(
        quest_id=QuestIds.RANK_UP_F,
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_F",
        display_name_jp="ランクF昇格試験（凍土の魔犬）",
        display_name_en="Rank F Promotion Trial (Frozen Hound)",
        description="凍土の魔犬を倒し、ランクFを獲得する",
        phase=Phase.INITIATION,
        quest_giver=Actors.BALGAS,
        auto_trigger=False,
        advances_phase=Phase.RISING,
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.RANK_UP_G],
        completion_flags={},  # ランクはクエスト完了から推論
        priority=900,
    ),

    QuestDefinition(
        quest_id=QuestIds.RANK_UP_E,
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_E",
        display_name_jp="ランクE昇格試験（錆びついた英雄カイン）",
        display_name_en="Rank E Promotion Trial (Rusted Hero Kain)",
        description="錆びついた英雄カインを倒し、ランクEを獲得する",
        phase=Phase.RISING,
        quest_giver=Actors.BALGAS,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.RANK_UP_F],
        completion_flags={},  # ランクはクエスト完了から推論
        priority=900,
    ),

    QuestDefinition(
        quest_id=QuestIds.RANK_UP_D,
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_D",
        display_name_jp="ランクD昇格試験（銅貨稼ぎの洗礼）",
        display_name_en="Rank D Promotion Trial (Copper Earner's Baptism)",
        description="観客の介入を避けながら戦い、ランクDを獲得する",
        phase=Phase.RISING,
        quest_giver=Actors.BALGAS,
        auto_trigger=False,
        advances_phase=Phase.AWAKENING,
        required_flags=[],
        required_quests=[QuestIds.UPPER_EXISTENCE],  # 07講義後に受験可能
        completion_flags={},
        priority=900,
    ),

    QuestDefinition(
        quest_id=QuestIds.RANK_UP_C,
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_C",
        display_name_jp="ランクC昇格試験（闘技場の鴉）",
        display_name_en="Rank C Promotion Trial (Arena Crow)",
        description="堕ちた英雄たちを解放し、ランクCを獲得する",
        phase=Phase.AWAKENING,
        quest_giver=Actors.BALGAS,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],
        required_quests=[QuestIds.BALGAS_TRAINING],  # 09訓練後に受験可能
        completion_flags={},
        priority=900,
    ),

    QuestDefinition(
        quest_id=QuestIds.RANK_UP_B,
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_B",
        display_name_jp="ランクB昇格試験（虚無の処刑人ヌル）",
        display_name_en="Rank B Promotion Trial (Null the Void Executioner)",
        description="虚無の処刑人ヌルを倒し、ランクBを獲得する",
        phase=Phase.AWAKENING,
        quest_giver=Actors.BALGAS,
        auto_trigger=False,
        advances_phase=Phase.CONFRONTATION,
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.RANK_UP_C],
        completion_flags={},  # ランクはクエスト完了から推論
        priority=900,
    ),

    QuestDefinition(
        quest_id=QuestIds.RANK_UP_A,
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_A",
        display_name_jp="ランクA昇格試験（影との戦い）",
        display_name_en="Rank A Promotion Trial (Shadow Battle)",
        description="自分の影（第二のヌル）を倒し、ランクAを獲得する",
        phase=Phase.CONFRONTATION,
        quest_giver=Actors.BALGAS,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.RANK_UP_B],  # MAKUMA2は瓶すり替え時のみなので削除
        completion_flags={},  # ランクはクエスト完了から推論
        priority=900,
    ),

    # ランクS昇格試験 親クエスト（バルガスのドラマから開始）
    QuestDefinition(
        quest_id=QuestIds.RANK_UP_S,
        quest_type=QuestType.RANK_UP,
        drama_id="vs_balgas",
        display_name_jp="Rank S 昇格試験『屠竜者への道』",
        display_name_en="Rank S Trial: Path to Dragon Slayer",
        description="全盛期のバルガスとの最終決戦",
        phase=Phase.CONFRONTATION,
        quest_giver=Actors.BALGAS,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],
        required_quests=[QuestIds.RANK_UP_A],
        completion_flags={},
        priority=910,  # 分岐より少し高い
    ),

    # ランクS昇格分岐クエスト（排他的）
    QuestDefinition(
        quest_id=QuestIds.RANK_UP_S_BALGAS_SPARED,
        quest_type=QuestType.RANK_UP,
        drama_id="vs_balgas",  # 同じドラマ、選択で分岐
        display_name_jp="ランクS昇格：バルガスを見逃す",
        display_name_en="Rank S: Spare Balgas",
        description="バルガスを見逃し、慈悲の道を選んだ",
        phase=Phase.CONFRONTATION,
        quest_giver=Actors.BALGAS,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件なし
        required_quests=[QuestIds.RANK_UP_A, QuestIds.RANK_UP_S],  # 親クエスト必須
        completion_flags={},
        blocks_quests=[QuestIds.RANK_UP_S_BALGAS_KILLED],  # 排他的
        priority=900,
    ),

    QuestDefinition(
        quest_id=QuestIds.RANK_UP_S_BALGAS_KILLED,
        quest_type=QuestType.RANK_UP,
        drama_id="vs_balgas",  # 同じドラマ、選択で分岐
        display_name_jp="ランクS昇格：バルガスを殺す",
        display_name_en="Rank S: Kill Balgas",
        description="観客の命令に従い、バルガスを殺した",
        phase=Phase.CONFRONTATION,
        quest_giver=Actors.BALGAS,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件なし
        required_quests=[QuestIds.RANK_UP_A, QuestIds.RANK_UP_S],  # 親クエスト必須
        completion_flags={},
        blocks_quests=[QuestIds.RANK_UP_S_BALGAS_SPARED, QuestIds.LILY_PRIVATE],  # 排他的、LILY_PRIVATEもブロック
        priority=900,
    ),

    # ========================================
    # キャラクターイベント・サイドクエスト
    # ========================================
    QuestDefinition(
        quest_id=QuestIds.ZEK_INTRO,
        quest_type=QuestType.CHARACTER_EVENT,
        drama_id="zek_intro",
        display_name_jp="影歩きの邂逅",
        display_name_en="Encounter with the Shadow Walker",
        description="商人ゼクとの初遭遇",
        phase=Phase.INITIATION,
        quest_giver=Actors.ZEK,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.RANK_UP_G],
        completion_flags={},  # 関係値はクエスト完了から推論
        priority=800,
    ),

    QuestDefinition(
        quest_id=QuestIds.LILY_EXPERIMENT,
        quest_type=QuestType.SIDE_QUEST,
        drama_id="lily_experiment",
        display_name_jp="リリィの私的依頼『残響の器』",
        display_name_en="Lily's Private Request: Vessel of Echoes",
        description="リリィのために死の共鳴瓶を製作する",
        phase=Phase.INITIATION,
        quest_giver=Actors.LILY,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.RANK_UP_F],
        completion_flags={},
        priority=700,
    ),

    # 瓶すり替え親クエスト（ゼクのドラマから開始）
    QuestDefinition(
        quest_id=QuestIds.ZEK_STEAL_BOTTLE,
        quest_type=QuestType.SIDE_QUEST,
        drama_id="zek_steal_bottle",
        display_name_jp="ゼクの器すり替え",
        display_name_en="Zek's Bottle Swap",
        description="ゼクが共鳴瓶のすり替えを提案してくる",
        phase=Phase.INITIATION,
        quest_giver=Actors.ZEK,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],
        required_quests=[QuestIds.LILY_EXPERIMENT],
        completion_flags={},
        priority=710,  # LILY_EXPERIMENTより少し高い
    ),

    # 瓶すり替え分岐クエスト（排他的）
    QuestDefinition(
        quest_id=QuestIds.ZEK_STEAL_BOTTLE_ACCEPT,
        quest_type=QuestType.SIDE_QUEST,
        drama_id="zek_steal_bottle",  # 同じドラマ、選択で分岐
        display_name_jp="ゼクの器すり替え：応諾",
        display_name_en="Zek's Bottle Swap: Accepted",
        description="ゼクの提案に応じて共鳴瓶をすり替えた",
        phase=Phase.INITIATION,
        quest_giver=Actors.ZEK,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件なし
        required_quests=[QuestIds.LILY_EXPERIMENT, QuestIds.ZEK_STEAL_BOTTLE],
        completion_flags={},
        blocks_quests=[QuestIds.ZEK_STEAL_BOTTLE_REFUSE],  # 排他的
        priority=700,
    ),

    QuestDefinition(
        quest_id=QuestIds.ZEK_STEAL_BOTTLE_REFUSE,
        quest_type=QuestType.SIDE_QUEST,
        drama_id="zek_steal_bottle",  # 同じドラマ、選択で分岐
        display_name_jp="ゼクの器すり替え：拒否",
        display_name_en="Zek's Bottle Swap: Refused",
        description="ゼクの提案を断り、正直にリリィに渡した",
        phase=Phase.INITIATION,
        quest_giver=Actors.ZEK,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件なし
        required_quests=[QuestIds.LILY_EXPERIMENT, QuestIds.ZEK_STEAL_BOTTLE],
        completion_flags={},
        blocks_quests=[QuestIds.ZEK_STEAL_BOTTLE_ACCEPT],  # 排他的
        priority=700,
    ),

    # カイン魂親クエスト（ゼクのドラマから開始）
    QuestDefinition(
        quest_id=QuestIds.ZEK_STEAL_SOULGEM,
        quest_type=QuestType.SIDE_QUEST,
        drama_id="zek_steal_soulgem",
        display_name_jp="カインの魂の行方",
        display_name_en="Fate of Kain's Soul",
        description="ゼクがカインの魂の取引を持ちかけてくる",
        phase=Phase.RISING,
        quest_giver=Actors.ZEK,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],
        required_quests=[QuestIds.RANK_UP_E],
        completion_flags={},
        priority=860,  # 分岐より少し高い
    ),

    # カイン魂分岐クエスト（排他的）
    QuestDefinition(
        quest_id=QuestIds.ZEK_STEAL_SOULGEM_SELL,
        quest_type=QuestType.SIDE_QUEST,
        drama_id="zek_steal_soulgem",  # 同じドラマ、選択で分岐
        display_name_jp="カインの魂：売却",
        display_name_en="Kain's Soul: Sold",
        description="カインの魂をゼクに売った",
        phase=Phase.RISING,
        quest_giver=Actors.ZEK,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件なし
        required_quests=[QuestIds.RANK_UP_E, QuestIds.ZEK_STEAL_SOULGEM],
        completion_flags={},
        blocks_quests=[QuestIds.ZEK_STEAL_SOULGEM_RETURN],  # 排他的
        priority=850,
    ),

    QuestDefinition(
        quest_id=QuestIds.ZEK_STEAL_SOULGEM_RETURN,
        quest_type=QuestType.SIDE_QUEST,
        drama_id="zek_steal_soulgem",  # 同じドラマ、選択で分岐
        display_name_jp="カインの魂：返還",
        display_name_en="Kain's Soul: Returned",
        description="カインの魂をバルガスに返した",
        phase=Phase.RISING,
        quest_giver=Actors.ZEK,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件なし
        required_quests=[QuestIds.RANK_UP_E, QuestIds.ZEK_STEAL_SOULGEM],
        completion_flags={},
        blocks_quests=[QuestIds.ZEK_STEAL_SOULGEM_SELL],  # 排他的
        priority=850,
    ),

    QuestDefinition(
        quest_id=QuestIds.UPPER_EXISTENCE,
        quest_type=QuestType.MAIN_STORY,
        drama_id="upper_existence",
        display_name_jp="高次元存在の真実",
        display_name_en="Truth of Higher Dimensional Beings",
        description="観客の正体と闘技場の真実が明らかになる",
        phase=Phase.RISING,  # RANK_UP_D前なのでRISINGフェーズ
        quest_giver=Actors.BALGAS,  # バルガスに話しかけて開始
        auto_trigger=False,  # 昇格試験を受けようとした時に開始
        advances_phase=None,
        required_flags=[],
        required_quests=[QuestIds.RANK_UP_E],  # RANK_UP_D前に発動
        completion_flags={},
        priority=899,  # RANK_UP_D(900)より先に発動
    ),

    QuestDefinition(
        quest_id=QuestIds.LILY_PRIVATE,
        quest_type=QuestType.CHARACTER_EVENT,
        drama_id="lily_private",
        display_name_jp="リリィの私室招待",
        display_name_en="Invitation to Lily's Private Room",
        description="リリィの私室に招待される",
        phase=Phase.AWAKENING,
        quest_giver=Actors.LILY,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.RANK_UP_D],  # ランクD昇格のみ
        completion_flags={},
        blocks_quests=[],  # バルガス殺害時はArenaQuestManagerでブロック
        priority=600,
    ),

    QuestDefinition(
        quest_id=QuestIds.BALGAS_TRAINING,
        quest_type=QuestType.CHARACTER_EVENT,
        drama_id="balgas_training",
        display_name_jp="戦士の哲学：鉄を打つ鉄",
        display_name_en="Warrior's Philosophy: Iron Forges Iron",
        description="バルガスから戦士の哲学を学ぶ特別訓練",
        phase=Phase.AWAKENING,
        quest_giver=Actors.BALGAS,  # バルガスに話しかけて開始
        auto_trigger=False,  # 自動発動ではない
        advances_phase=None,
        required_flags=[],
        required_quests=[QuestIds.RANK_UP_D],  # ランクD昇格後に受けられる
        completion_flags={},
        priority=899,  # RANK_UP_C(900)より先に発動
    ),

    QuestDefinition(
        quest_id=QuestIds.MAKUMA,
        quest_type=QuestType.MAIN_STORY,
        drama_id="makuma",
        display_name_jp="ヌルの記憶チップとリリィの衣装",
        display_name_en="Null's Memory Chip and Lily's Outfit",
        description="ランクB達成報酬として特別な衣装を授与され、ゼクがヌルの真実を暴露する",
        phase=Phase.CONFRONTATION,
        quest_giver=Actors.LILY,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.RANK_UP_B],
        completion_flags={},  # フラグ設定削除
        priority=850,
    ),

    QuestDefinition(
        quest_id=QuestIds.MAKUMA2,
        quest_type=QuestType.MAIN_STORY,
        drama_id="makuma2",
        display_name_jp="虚空の心臓製作【複数分岐統合】",
        display_name_en="Void Core Crafting [Multiple Branch Convergence]",
        description="虚空の心臓を製作し、過去の選択の清算が行われる",
        phase=Phase.CONFRONTATION,
        quest_giver=Actors.LILY,  # リリィから受注
        auto_trigger=False,  # 手動受注
        advances_phase=None,
        required_flags=[],
        required_quests=[QuestIds.MAKUMA],  # MAKUMAのみ（瓶すり替え選択は内部で分岐）
        completion_flags={},
        priority=850,
    ),

    QuestDefinition(
        quest_id=QuestIds.LILY_REAL_NAME,
        quest_type=QuestType.CHARACTER_EVENT,
        drama_id="lily_real_name",
        display_name_jp="リリィの真名告白",
        display_name_en="Lily's True Name Revelation",
        description="リリィが真名『リリシエル』を明かす",
        phase=Phase.CONFRONTATION,
        quest_giver=Actors.LILY,
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.RANK_UP_S_BALGAS_SPARED],  # バルガス見逃しが必須
        completion_flags={},
        priority=600,
    ),

    # ========================================
    # 最終章
    # ========================================
    # NOTE: VS_ASTAROTH はバルガス戦完了（どちらか）が必要
    # ArenaQuestManager で特別にチェック: RANK_UP_S_BALGAS_SPARED または RANK_UP_S_BALGAS_KILLED
    QuestDefinition(
        quest_id=QuestIds.VS_ASTAROTH,
        quest_type=QuestType.MAIN_STORY,
        drama_id="vs_astaroth",
        display_name_jp="アスタロト初遭遇、ゼクによる救出",
        display_name_en="First Astaroth Encounter, Zek's Rescue",
        description="アスタロトが降臨し、ゼクが介入して救出する",
        phase=Phase.CONFRONTATION,
        quest_giver=None,  # 自動発動
        auto_trigger=True,
        advances_phase=Phase.CLIMAX,  # 逃亡開始でフェーズ進行
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.RANK_UP_A],  # バルガス戦完了はArenaQuestManagerでチェック
        completion_flags={},
        priority=900,
    ),

    QuestDefinition(
        quest_id=QuestIds.LAST_BATTLE,
        quest_type=QuestType.ENDING,
        drama_id="last_battle",
        display_name_jp="最終決戦：アスタロト撃破",
        display_name_en="Final Battle: Defeat Astaroth",
        description="アスタロトとの最終決戦、複数のエンディング分岐",
        phase=Phase.CLIMAX,
        quest_giver=Actors.ZEK,  # ゼクから開始
        auto_trigger=False,
        advances_phase=None,
        required_flags=[],  # フラグ条件削除
        required_quests=[QuestIds.VS_ASTAROTH],
        completion_flags={},
        priority=500,  # サイドクエストより低い優先度（他のクエストを先に表示）
    ),
]


# ========================================
# Quest Dependency Graph
# ========================================

class QuestDependencyGraph:
    """クエスト依存関係グラフ"""

    def __init__(self):
        self.quests: Dict[str, QuestDefinition] = {}
        for quest in QUEST_DEFINITIONS:
            self.quests[quest.quest_id] = quest

    def get_current_phase(self, current_flags: Dict[str, any]) -> Phase:
        """現在のフェーズを取得"""
        phase_value = current_flags.get(Keys.CURRENT_PHASE, 0)
        if isinstance(phase_value, Phase):
            return phase_value
        # 整数値からPhaseに変換
        phase_list = list(Phase)
        if isinstance(phase_value, int) and 0 <= phase_value < len(phase_list):
            return phase_list[phase_value]
        return Phase.PROLOGUE

    def get_available_quests(self, current_flags: Dict[str, any],
                           completed_quests: Set[str]) -> List[QuestDefinition]:
        """
        現在のフラグと完了済みクエストから、利用可能なクエストを取得

        Args:
            current_flags: 現在のフラグ状態
            completed_quests: 完了済みクエストのIDセット

        Returns:
            利用可能なクエストのリスト（優先度順）
        """
        current_phase = self.get_current_phase(current_flags)
        available = []

        for quest in self.quests.values():
            # 既に完了済みならスキップ
            if quest.quest_id in completed_quests:
                continue

            # フェーズチェック（現在のフェーズより先のクエストはスキップ）
            if quest.phase > current_phase:
                continue

            # 前提クエストチェック
            if not all(req_quest in completed_quests
                      for req_quest in quest.required_quests):
                continue

            # フラグ条件チェック
            if not self._check_flag_conditions(quest.required_flags, current_flags):
                continue

            # ブロックされているクエストチェック
            if self._is_blocked(quest, current_flags):
                continue

            available.append(quest)

        # 優先度順にソート
        available.sort(key=lambda q: q.priority, reverse=True)
        return available

    def get_auto_trigger_quests(self, current_flags: Dict[str, any],
                                completed_quests: Set[str]) -> List[QuestDefinition]:
        """
        自動発動クエストのみを取得

        Args:
            current_flags: 現在のフラグ状態
            completed_quests: 完了済みクエストのIDセット

        Returns:
            自動発動可能なクエストのリスト（優先度順）
        """
        available = self.get_available_quests(current_flags, completed_quests)
        return [q for q in available if q.auto_trigger]

    def get_npc_quests(self, npc_id: str, current_flags: Dict[str, any],
                       completed_quests: Set[str]) -> List[QuestDefinition]:
        """
        特定NPCが持つ利用可能なクエストを取得

        Args:
            npc_id: NPCのID（Actors定数）
            current_flags: 現在のフラグ状態
            completed_quests: 完了済みクエストのIDセット

        Returns:
            そのNPCが提供可能なクエストのリスト（優先度順）
        """
        available = self.get_available_quests(current_flags, completed_quests)
        return [q for q in available if q.quest_giver == npc_id]

    def get_all_npc_quests(self, current_flags: Dict[str, any],
                          completed_quests: Set[str]) -> Dict[str, List[QuestDefinition]]:
        """
        全NPCの利用可能クエストをNPC別に取得

        Returns:
            {npc_id: [quests]} の形式
        """
        available = self.get_available_quests(current_flags, completed_quests)
        npc_quests: Dict[str, List[QuestDefinition]] = {}

        for quest in available:
            if quest.quest_giver:
                if quest.quest_giver not in npc_quests:
                    npc_quests[quest.quest_giver] = []
                npc_quests[quest.quest_giver].append(quest)

        return npc_quests

    def _check_flag_conditions(self, conditions: List[FlagCondition],
                               current_flags: Dict[str, any]) -> bool:
        """フラグ条件をチェック"""
        for condition in conditions:
            flag_value = current_flags.get(condition.flag_key)

            if condition.operator == "==":
                if flag_value != condition.value:
                    return False
            elif condition.operator == "!=":
                if flag_value == condition.value:
                    return False
            elif condition.operator == ">=":
                if flag_value is None or flag_value < condition.value:
                    return False
            elif condition.operator == ">":
                if flag_value is None or flag_value <= condition.value:
                    return False
            elif condition.operator == "<=":
                if flag_value is None or flag_value > condition.value:
                    return False
            elif condition.operator == "<":
                if flag_value is None or flag_value >= condition.value:
                    return False

        return True

    def _is_blocked(self, quest: QuestDefinition,
                   current_flags: Dict[str, any]) -> bool:
        """クエストがブロックされているかチェック"""
        # リリィの真名イベントのブロック条件
        if quest.quest_id == "16_lily_real_name":
            bottle_confession = current_flags.get(Keys.LILY_BOTTLE_CONFESSION)
            lily_hostile = current_flags.get(Keys.LILY_HOSTILE, False)

            if bottle_confession in ["blamed_zek", "denied"]:
                return True
            if lily_hostile:
                return True

        return False

    def get_quest_chain(self, quest_id: str) -> List[str]:
        """指定クエストに至るまでのクエストチェーンを取得"""
        quest = self.quests.get(quest_id)
        if not quest:
            return []

        chain = []
        visited = set()

        def _build_chain(q_id: str):
            if q_id in visited:
                return
            visited.add(q_id)

            q = self.quests.get(q_id)
            if not q:
                return

            # 前提クエストを先に追加
            for req_quest in q.required_quests:
                _build_chain(req_quest)

            chain.append(q_id)

        _build_chain(quest_id)
        return chain

    def validate_dependencies(self) -> List[str]:
        """依存関係の妥当性をチェック"""
        errors = []

        for quest in self.quests.values():
            # 前提クエストの存在チェック
            for req_quest in quest.required_quests:
                if req_quest not in self.quests:
                    errors.append(
                        f"Quest '{quest.quest_id}' requires non-existent quest '{req_quest}'"
                    )

            # 循環依存チェック
            if self._has_circular_dependency(quest.quest_id):
                errors.append(
                    f"Quest '{quest.quest_id}' has circular dependency"
                )

        return errors

    def _has_circular_dependency(self, quest_id: str,
                                visited: Set[str] = None) -> bool:
        """循環依存をチェック"""
        if visited is None:
            visited = set()

        if quest_id in visited:
            return True

        visited.add(quest_id)
        quest = self.quests.get(quest_id)
        if not quest:
            return False

        for req_quest in quest.required_quests:
            if self._has_circular_dependency(req_quest, visited.copy()):
                return True

        return False

    def generate_quest_graph_viz(self) -> str:
        """Graphviz形式のクエストグラフを生成（可視化用）"""
        lines = ["digraph QuestFlow {"]
        lines.append('  rankdir=TB;')
        lines.append('  node [shape=box];')

        # クエストタイプごとに色分け
        colors = {
            QuestType.MAIN_STORY: "lightblue",
            QuestType.RANK_UP: "lightgreen",
            QuestType.SIDE_QUEST: "lightyellow",
            QuestType.CHARACTER_EVENT: "lightpink",
            QuestType.ENDING: "lightcoral",
        }

        for quest in self.quests.values():
            color = colors.get(quest.quest_type, "white")
            lines.append(
                f'  "{quest.quest_id}" [label="{quest.display_name_jp}\\n({quest.quest_id})", '
                f'fillcolor="{color}", style=filled];'
            )

        for quest in self.quests.values():
            for req_quest in quest.required_quests:
                lines.append(f'  "{req_quest}" -> "{quest.quest_id}";')

        lines.append("}")
        return "\n".join(lines)


# ========================================
# ユーティリティ関数
# ========================================

def get_quest_graph() -> QuestDependencyGraph:
    """クエスト依存関係グラフのシングルトンインスタンスを取得"""
    return QuestDependencyGraph()


# ========================================
# テスト/検証
# ========================================

def export_quests_to_json(output_path: str):
    """クエスト定義をJSON形式でエクスポート"""
    import json

    quests_data = []
    for quest in QUEST_DEFINITIONS:
        quest_data = {
            "questId": quest.quest_id,
            "questType": quest.quest_type.value,
            "dramaId": quest.drama_id,
            "displayNameJP": quest.display_name_jp,
            "displayNameEN": quest.display_name_en,
            "description": quest.description,
            # Phase system fields
            "phase": quest.phase.value if quest.phase else None,
            "phaseOrdinal": list(Phase).index(quest.phase) if quest.phase else 0,
            "questGiver": quest.quest_giver,
            "autoTrigger": quest.auto_trigger,
            "advancesPhase": quest.advances_phase.value if quest.advances_phase else None,
            "advancesPhaseOrdinal": list(Phase).index(quest.advances_phase) if quest.advances_phase else -1,
            # Legacy fields
            "requiredFlags": [
                {
                    "flagKey": cond.flag_key,
                    "operator": cond.operator,
                    "value": cond.value
                }
                for cond in quest.required_flags
            ],
            "requiredQuests": quest.required_quests,
            "completionFlags": quest.completion_flags,
            "branchChoices": quest.branch_choices,
            "blocksQuests": quest.blocks_quests,
            "priority": quest.priority,
        }
        quests_data.append(quest_data)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(quests_data, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(quests_data)} quests to {output_path}")


if __name__ == "__main__":
    print("=== Quest Dependency System Test ===\n")

    graph = get_quest_graph()

    # 依存関係の検証
    print("Validating quest dependencies...")
    errors = graph.validate_dependencies()
    if errors:
        print("ERRORS FOUND:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("  [OK] All dependencies are valid!")

    # フェーズシステムテスト
    print("\n=== Phase System Test ===")
    print(f"Available phases: {[p.value for p in Phase]}")

    # 利用可能なクエストのテスト
    print("\n=== Testing Quest Availability ===")

    # 初期状態（PROLOGUE）
    current_flags = {
        Keys.RANK: "unranked",
        Keys.CURRENT_PHASE: 0,  # PROLOGUE
    }
    completed = set()

    print(f"\nPhase: PROLOGUE (Rank: unranked)")
    available = graph.get_available_quests(current_flags, completed)
    for quest in available:
        marker = "[AUTO]" if quest.auto_trigger else f"[{quest.quest_giver}]" if quest.quest_giver else ""
        print(f"  - {quest.quest_id}: {quest.display_name_jp} {marker}")

    # 自動発動クエストのテスト
    print("\n=== Auto-Trigger Quests ===")
    auto_quests = graph.get_auto_trigger_quests(current_flags, completed)
    for quest in auto_quests:
        print(f"  - {quest.quest_id}: {quest.display_name_jp}")

    # オープニング完了後
    completed.add("01_opening")
    completed.add("02_first_battle")
    current_flags[Keys.CURRENT_PHASE] = 1  # INITIATION
    current_flags[Keys.RANK] = "unranked"

    print(f"\nPhase: INITIATION (after first battle)")
    # NPC別クエストのテスト
    print("\n=== NPC Quests ===")
    npc_quests = graph.get_all_npc_quests(current_flags, completed)
    for npc_id, quests in npc_quests.items():
        print(f"  {npc_id}:")
        for quest in quests:
            print(f"    - {quest.quest_id}: {quest.display_name_jp}")

    # ランクG→F進行後
    current_flags[Keys.RANK] = "F"
    current_flags[Keys.CURRENT_PHASE] = 2  # RISING
    completed.add("03_rank_up_G")
    completed.add("04_rank_up_F")

    print(f"\nPhase: RISING (Rank: F)")
    available = graph.get_available_quests(current_flags, completed)
    for quest in available:
        marker = "[AUTO]" if quest.auto_trigger else f"[{quest.quest_giver}]" if quest.quest_giver else ""
        print(f"  - {quest.quest_id}: {quest.display_name_jp} {marker}")

    # クエストチェーンの表示
    print("\n=== Quest Chain to Final Battle ===")
    chain = graph.get_quest_chain("18_last_battle")
    print(f"Total quests in chain: {len(chain)}")
    for i, q_id in enumerate(chain, 1):
        quest = graph.quests[q_id]
        phase_name = quest.phase.value if quest.phase else "N/A"
        print(f"  {i}. [{phase_name}] {q_id}: {quest.display_name_jp}")

    # Graphviz出力
    print("\n=== Generating Graphviz Graph ===")
    viz = graph.generate_quest_graph_viz()
    print("Graph generated! Save to quest_graph.dot and run:")
    print("  dot -Tpng quest_graph.dot -o quest_graph.png")

    # JSON出力
    print("\n=== Exporting to JSON ===")
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_output_path = os.path.join(project_root, "Package", "quest_definitions.json")
    os.makedirs(os.path.dirname(json_output_path), exist_ok=True)
    export_quests_to_json(json_output_path)

    print("\n=== Test Complete ===")
