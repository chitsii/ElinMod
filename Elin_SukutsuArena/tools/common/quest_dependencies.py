"""
Quest Dependency Management System

This module defines the quest flow and dependencies for the Sukutsu Arena mod.
It provides a clear structure for quest progression based on flags.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
from flag_definitions import Keys


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
        quest_id="01_opening",
        quest_type=QuestType.MAIN_STORY,
        drama_id="sukutsu_opening",
        display_name_jp="異次元の闘技場への到着",
        display_name_en="Arrival at the Dimensional Arena",
        description="プレイヤーがアリーナに到着し、リリィとバルガスに出会う",
        required_flags=[],
        required_quests=[],
        completion_flags={
            Keys.RANK: "unranked",
            Keys.REL_LILY: 30,
            Keys.REL_BALGAS: 20,
            Keys.REL_ZEK: 0,
        },
        priority=1000,
    ),

    # ========================================
    # ランク昇格試験
    # ========================================
    QuestDefinition(
        quest_id="02_rank_up_G",
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_G",
        display_name_jp="ランクG昇格試験",
        display_name_en="Rank G Promotion Trial",
        description="最初の試練を突破し、ランクGを獲得する",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "unranked"),
        ],
        required_quests=["01_opening"],
        completion_flags={
            Keys.RANK: "G",
        },
        priority=900,
    ),

    QuestDefinition(
        quest_id="04_rank_up_F",
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_F",
        display_name_jp="ランクF昇格試験（凍土の魔犬）",
        display_name_en="Rank F Promotion Trial (Frozen Hound)",
        description="凍土の魔犬を倒し、ランクFを獲得する",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "G"),
        ],
        required_quests=["02_rank_up_G"],
        completion_flags={
            Keys.RANK: "F",
        },
        priority=900,
    ),

    QuestDefinition(
        quest_id="06_rank_up_E",
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_E",
        display_name_jp="ランクE昇格試験（錆びついた英雄カイン）",
        display_name_en="Rank E Promotion Trial (Rusted Hero Kain)",
        description="錆びついた英雄カインを倒し、ランクEを獲得する",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "F"),
        ],
        required_quests=["04_rank_up_F"],
        completion_flags={
            Keys.RANK: "E",
        },
        priority=900,
    ),

    QuestDefinition(
        quest_id="10_rank_up_D",
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_D",
        display_name_jp="ランクD昇格試験（銅貨稼ぎの洗礼）",
        display_name_en="Rank D Promotion Trial (Copper Earner's Baptism)",
        description="観客の介入を避けながら戦い、ランクDを獲得する",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "E"),
        ],
        required_quests=["06_rank_up_E"],
        completion_flags={
            Keys.RANK: "D",
        },
        priority=900,
    ),

    QuestDefinition(
        quest_id="09_rank_up_C",
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_C",
        display_name_jp="ランクC昇格試験（闘技場の鴉）",
        display_name_en="Rank C Promotion Trial (Arena Crow)",
        description="堕ちた英雄たちを解放し、ランクCを獲得する",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "D"),
        ],
        required_quests=["10_rank_up_D"],
        completion_flags={
            Keys.RANK: "C",
        },
        priority=900,
    ),

    QuestDefinition(
        quest_id="11_rank_up_B",
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_B",
        display_name_jp="ランクB昇格試験（暗殺者ヌル）",
        display_name_en="Rank B Promotion Trial (Assassin Null)",
        description="暗殺者ヌルを倒し、ランクBを獲得する",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "C"),
        ],
        required_quests=["09_rank_up_C"],
        completion_flags={
            Keys.RANK: "B",
        },
        priority=900,
    ),

    QuestDefinition(
        quest_id="14_rank_up_A",
        quest_type=QuestType.RANK_UP,
        drama_id="rank_up_A",
        display_name_jp="ランクA昇格試験（影との戦い）",
        display_name_en="Rank A Promotion Trial (Shadow Battle)",
        description="自分の影（第二のヌル）を倒し、ランクAを獲得する",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "B"),
        ],
        required_quests=["11_rank_up_B", "13_makuma2"],
        completion_flags={
            Keys.RANK: "A",
        },
        priority=900,
    ),

    QuestDefinition(
        quest_id="15_rank_up_S",
        quest_type=QuestType.RANK_UP,
        drama_id="vs_balgas",
        display_name_jp="ランクS昇格試験（バルガス全盛期との一騎打ち）",
        display_name_en="Rank S Promotion Trial (Duel with Prime Balgas)",
        description="バルガスの全盛期の姿と戦い、ランクSを獲得する",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "A"),
        ],
        required_quests=["14_rank_up_A"],
        completion_flags={
            Keys.RANK: "S",
        },
        branch_choices=["balgas_choice"],
        priority=900,
    ),

    # ========================================
    # キャラクターイベント
    # ========================================
    QuestDefinition(
        quest_id="03_zek_intro",
        quest_type=QuestType.CHARACTER_EVENT,
        drama_id="zek_intro",
        display_name_jp="影歩きの邂逅",
        display_name_en="Encounter with the Shadow Walker",
        description="商人ゼクとの初遭遇",
        required_flags=[
            FlagCondition(Keys.RANK, ">=", "G"),
        ],
        required_quests=["02_rank_up_G"],
        completion_flags={
            Keys.REL_ZEK: 10,
        },
        priority=800,
    ),

    QuestDefinition(
        quest_id="05_1_lily_experiment",
        quest_type=QuestType.SIDE_QUEST,
        drama_id="lily_experiment",
        display_name_jp="リリィの私的依頼『残響の器』",
        display_name_en="Lily's Private Request: Vessel of Echoes",
        description="リリィのために虚空の共鳴瓶を製作する",
        required_flags=[
            FlagCondition(Keys.RANK, ">=", "F"),
        ],
        required_quests=["04_rank_up_F"],
        completion_flags={},  # rel.lily +5 は mod_flag で処理
        priority=700,
    ),

    QuestDefinition(
        quest_id="05_2_zek_steal_bottle",
        quest_type=QuestType.SIDE_QUEST,
        drama_id="zek_steal_bottle",
        display_name_jp="ゼクの器すり替え提案",
        display_name_en="Zek's Bottle Swap Proposal",
        description="ゼクが共鳴瓶のすり替えを提案する【重要分岐】",
        required_flags=[
            FlagCondition(Keys.RANK, ">=", "F"),
        ],
        required_quests=["05_1_lily_experiment"],
        completion_flags={},  # bottle_choice は選択で設定
        branch_choices=["bottle_choice"],
        priority=700,
    ),

    QuestDefinition(
        quest_id="06_2_zek_steal_soulgem",
        quest_type=QuestType.SIDE_QUEST,
        drama_id="zek_steal_soulgem",
        display_name_jp="カインの魂の選択",
        display_name_en="Kain's Soul Choice",
        description="カインの魂をゼクに売るか、バルガスに返すか選択する【重要分岐】",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "E"),
        ],
        required_quests=["06_rank_up_E"],
        completion_flags={},  # ランク昇格は10_rank_up_Dで行う
        branch_choices=["kain_soul_choice"],
        priority=850,
    ),

    QuestDefinition(
        quest_id="07_upper_existence",
        quest_type=QuestType.MAIN_STORY,
        drama_id="upper_existence",
        display_name_jp="高次元存在の真実",
        display_name_en="Truth of Higher Dimensional Beings",
        description="観客の正体と闘技場の真実が明らかになる",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "D"),
        ],
        required_quests=["10_rank_up_D"],
        completion_flags={},
        priority=800,
    ),

    QuestDefinition(
        quest_id="08_lily_private",
        quest_type=QuestType.CHARACTER_EVENT,
        drama_id="lily_private",
        display_name_jp="リリィの私室招待",
        display_name_en="Invitation to Lily's Private Room",
        description="リリィの私室に招待される",
        required_flags=[
            FlagCondition(Keys.RANK, ">=", "D"),
            FlagCondition(Keys.REL_LILY, ">=", 40),
        ],
        required_quests=["10_rank_up_D"],
        completion_flags={},
        priority=600,
    ),

    QuestDefinition(
        quest_id="09_balgas_training",
        quest_type=QuestType.CHARACTER_EVENT,
        drama_id="balgas_training",
        display_name_jp="戦士の哲学：鉄を打つ鉄",
        display_name_en="Warrior's Philosophy: Iron Forges Iron",
        description="バルガスから戦士の哲学を学ぶ特別訓練",
        required_flags=[
            FlagCondition(Keys.RANK, ">=", "D"),
            FlagCondition(Keys.REL_BALGAS, ">=", 40),
        ],
        required_quests=["10_rank_up_D"],
        completion_flags={},
        priority=650,
    ),

    QuestDefinition(
        quest_id="12_makuma",
        quest_type=QuestType.MAIN_STORY,
        drama_id="makuma",
        display_name_jp="ヌルの記憶チップとリリィの衣装",
        display_name_en="Null's Memory Chip and Lily's Outfit",
        description="ランクB達成報酬として特別な衣装を授与され、ゼクがヌルの真実を暴露する",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "B"),
        ],
        required_quests=["11_rank_up_B"],
        completion_flags={
            Keys.NULL_CHIP: True,
        },
        priority=850,
    ),

    QuestDefinition(
        quest_id="13_makuma2",
        quest_type=QuestType.MAIN_STORY,
        drama_id="makuma2",
        display_name_jp="虚空の心臓製作【複数分岐統合】",
        display_name_en="Void Core Crafting [Multiple Branch Convergence]",
        description="虚空の心臓を製作し、過去の選択の清算が行われる",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "B"),
        ],
        required_quests=["12_makuma"],
        completion_flags={},
        branch_choices=["lily_bottle_confession", "kain_soul_confession"],
        priority=850,
    ),

    QuestDefinition(
        quest_id="16_lily_real_name",
        quest_type=QuestType.CHARACTER_EVENT,
        drama_id="lily_real_name",
        display_name_jp="リリィの真名告白",
        display_name_en="Lily's True Name Revelation",
        description="リリィが真名『リリアリス』を明かす",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "S"),
            FlagCondition(Keys.BALGAS_CHOICE, "==", "spared"),
            FlagCondition(Keys.REL_LILY, ">=", 50),
        ],
        required_quests=["15_rank_up_S"],
        completion_flags={
            Keys.LILY_TRUE_NAME: "Liliaris",
        },
        # ブロック条件（これらのフラグが立っていると発生しない）
        blocks_quests=[],  # フラグ条件で制御
        priority=600,
    ),

    # ========================================
    # 最終章
    # ========================================
    QuestDefinition(
        quest_id="17_vs_grandmaster_1",
        quest_type=QuestType.MAIN_STORY,
        drama_id="vs_grandmaster_1",
        display_name_jp="アスタロト初遭遇、ゼクによる救出",
        display_name_en="First Astaroth Encounter, Zek's Rescue",
        description="アスタロトが降臨し、ゼクが介入して救出する",
        required_flags=[
            FlagCondition(Keys.RANK, "==", "S"),
        ],
        required_quests=["15_rank_up_S"],
        completion_flags={
            Keys.FUGITIVE: True,
        },
        priority=900,
    ),

    QuestDefinition(
        quest_id="18_last_battle",
        quest_type=QuestType.ENDING,
        drama_id="last_battle",
        display_name_jp="最終決戦：アスタロト撃破",
        display_name_en="Final Battle: Defeat Astaroth",
        description="アスタロトとの最終決戦、複数のエンディング分岐",
        required_flags=[
            FlagCondition(Keys.FUGITIVE, "==", True),
        ],
        required_quests=["17_vs_grandmaster_1"],
        completion_flags={},
        branch_choices=["ending"],
        priority=1000,
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
        available = []

        for quest in self.quests.values():
            # 既に完了済みならスキップ
            if quest.quest_id in completed_quests:
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

    # 利用可能なクエストのテスト
    print("\n=== Testing Quest Availability ===")

    # 初期状態
    current_flags = {
        Keys.RANK: "unranked",
        Keys.REL_LILY: 30,
        Keys.REL_BALGAS: 20,
        Keys.REL_ZEK: 0,
    }
    completed = set()

    print(f"\nInitial state (Rank: unranked):")
    available = graph.get_available_quests(current_flags, completed)
    for quest in available:
        print(f"  - {quest.quest_id}: {quest.display_name_jp}")

    # ランクG取得後
    current_flags[Keys.RANK] = "G"
    completed.add("01_opening")
    completed.add("02_rank_up_G")

    print(f"\nAfter Rank G (completed: {len(completed)} quests):")
    available = graph.get_available_quests(current_flags, completed)
    for quest in available:
        print(f"  - {quest.quest_id}: {quest.display_name_jp}")

    # クエストチェーンの表示
    print("\n=== Quest Chain to Final Battle ===")
    chain = graph.get_quest_chain("18_last_battle")
    print(f"Total quests in chain: {len(chain)}")
    for i, q_id in enumerate(chain, 1):
        quest = graph.quests[q_id]
        print(f"  {i}. {q_id}: {quest.display_name_jp}")

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
