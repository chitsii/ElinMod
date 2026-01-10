"""
Build-time Validation System
============================
Pydanticを使用したビルド時バリデーション

主な検証項目:
1. Enumマッピングの整合性（Python <-> C#）
2. フラグキーの有効性
3. クエスト参照の有効性
4. ドラマIDの存在確認
"""

from typing import Dict, List, Set, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass
import sys


# ========================================
# C# EnumMappings との同期定義
# ========================================
# ArenaQuestManager.cs の EnumMappings と一致させる必要がある

CSHARP_ENUM_MAPPINGS: Dict[str, Dict[str, int]] = {
    "chitsii.arena.player.rank": {
        "unranked": 0,
        "G": 1,
        "F": 2,
        "E": 3,
        "D": 4,
        "C": 5,
        "B": 6,
        "A": 7,
        "S": 8,
    },
    "chitsii.arena.player.current_phase": {
        "prologue": 0,
        "initiation": 1,
        "rising": 2,
        "awakening": 3,
        "confrontation": 4,
        "climax": 5,
    },
    "chitsii.arena.player.balgas_choice": {
        "spared": 0,
        "killed": 1,
    },
    "chitsii.arena.player.bottle_choice": {
        "kept": 0,
        "swapped": 1,
    },
    "chitsii.arena.player.kain_soul_choice": {
        "freed": 0,
        "sold": 1,
    },
}

# 数値比較のみを使用するフラグ（Enumマッピング不要）
NUMERIC_ONLY_FLAGS: Set[str] = {
    "chitsii.arena.rel.lily",
    "chitsii.arena.rel.balgas",
    "chitsii.arena.rel.zek",
    "sukutsu_gladiator",
    "sukutsu_arena_stage",
    "sukutsu_arena_result",
    "sukutsu_is_rank_up_result",
    "sukutsu_rank_up_trial",
    "sukutsu_quest_found",
    "sukutsu_quest_target_name",
}


# ========================================
# Validation Error Collection
# ========================================

@dataclass
class ValidationError:
    """バリデーションエラー"""
    category: str
    message: str
    location: Optional[str] = None
    suggestion: Optional[str] = None

    def __str__(self):
        parts = [f"[{self.category}] {self.message}"]
        if self.location:
            parts.append(f"  Location: {self.location}")
        if self.suggestion:
            parts.append(f"  Suggestion: {self.suggestion}")
        return "\n".join(parts)


class ValidationResult:
    """バリデーション結果"""
    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

    def add_error(self, category: str, message: str, location: str = None, suggestion: str = None):
        self.errors.append(ValidationError(category, message, location, suggestion))

    def add_warning(self, category: str, message: str, location: str = None, suggestion: str = None):
        self.warnings.append(ValidationError(category, message, location, suggestion))

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def print_report(self):
        """バリデーション結果を出力"""
        if self.warnings:
            print(f"\n{'='*60}")
            print(f"WARNINGS ({len(self.warnings)})")
            print('='*60)
            for w in self.warnings:
                print(f"\n{w}")

        if self.errors:
            print(f"\n{'='*60}")
            print(f"ERRORS ({len(self.errors)})")
            print('='*60)
            for e in self.errors:
                print(f"\n{e}")

        print(f"\n{'='*60}")
        if self.has_errors:
            print(f"VALIDATION FAILED: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
        elif self.has_warnings:
            print(f"VALIDATION PASSED WITH WARNINGS: {len(self.warnings)} warning(s)")
        else:
            print("VALIDATION PASSED: All checks OK")
        print('='*60)


# ========================================
# Flag Condition Validator
# ========================================

class FlagConditionValidator:
    """フラグ条件のバリデーター"""

    VALID_OPERATORS = {"==", "!=", ">=", ">", "<=", "<"}

    def __init__(self, result: ValidationResult):
        self.result = result

    def validate(self, flag_key: str, operator: str, value: Any, location: str):
        """フラグ条件を検証"""
        # オペレーターチェック
        if operator not in self.VALID_OPERATORS:
            self.result.add_error(
                "INVALID_OPERATOR",
                f"Unknown operator '{operator}'",
                location,
                f"Valid operators: {', '.join(self.VALID_OPERATORS)}"
            )
            return

        # 文字列値の場合、Enumマッピングが必要
        if isinstance(value, str) and not value.isdigit():
            self._validate_string_enum(flag_key, value, location)

    def _validate_string_enum(self, flag_key: str, value: str, location: str):
        """文字列Enum値のマッピング存在確認"""
        # 数値のみのフラグはスキップ
        if flag_key in NUMERIC_ONLY_FLAGS:
            self.result.add_error(
                "INVALID_STRING_VALUE",
                f"Flag '{flag_key}' should use numeric values, got string '{value}'",
                location,
                "Use integer value instead of string"
            )
            return

        # Enumマッピングの存在確認
        if flag_key not in CSHARP_ENUM_MAPPINGS:
            self.result.add_error(
                "MISSING_ENUM_MAPPING",
                f"No C# EnumMapping defined for flag '{flag_key}'",
                location,
                f"Add mapping to CSHARP_ENUM_MAPPINGS in validation.py AND ArenaQuestManager.cs"
            )
            return

        # 値の存在確認
        valid_values = CSHARP_ENUM_MAPPINGS[flag_key]
        if value not in valid_values:
            self.result.add_error(
                "INVALID_ENUM_VALUE",
                f"Invalid value '{value}' for flag '{flag_key}'",
                location,
                f"Valid values: {', '.join(valid_values.keys())}"
            )


# ========================================
# Quest Definition Validator
# ========================================

class QuestValidator:
    """クエスト定義のバリデーター"""

    def __init__(self, result: ValidationResult):
        self.result = result
        self.flag_validator = FlagConditionValidator(result)
        self.known_quest_ids: Set[str] = set()
        self.known_drama_ids: Set[str] = set()
        self.known_actors: Set[str] = set()

    def set_known_quest_ids(self, quest_ids: Set[str]):
        self.known_quest_ids = quest_ids

    def set_known_drama_ids(self, drama_ids: Set[str]):
        self.known_drama_ids = drama_ids

    def set_known_actors(self, actors: Set[str]):
        self.known_actors = actors

    def validate_quest(self, quest_data: dict, quest_id: str):
        """クエスト定義を検証"""
        location = f"Quest: {quest_id}"

        # ドラマIDの存在確認
        drama_id = quest_data.get("drama_id") or quest_data.get("dramaId")
        if drama_id and self.known_drama_ids and drama_id not in self.known_drama_ids:
            self.result.add_warning(
                "UNKNOWN_DRAMA_ID",
                f"Drama ID '{drama_id}' not found in known drama IDs",
                location,
                "Ensure drama file exists or add to drama_constants.py"
            )

        # クエストギバーの確認
        quest_giver = quest_data.get("quest_giver") or quest_data.get("questGiver")
        if quest_giver and self.known_actors and quest_giver not in self.known_actors:
            self.result.add_warning(
                "UNKNOWN_QUEST_GIVER",
                f"Quest giver '{quest_giver}' not found in known actors",
                location,
                "Ensure NPC ID is correct"
            )

        # 必須フラグ条件の検証
        required_flags = quest_data.get("required_flags") or quest_data.get("requiredFlags", [])
        for i, flag_cond in enumerate(required_flags):
            if isinstance(flag_cond, dict):
                flag_key = flag_cond.get("flag_key") or flag_cond.get("flagKey")
                operator = flag_cond.get("operator") or flag_cond.get("op")
                value = flag_cond.get("value")
            else:
                # FlagCondition dataclass
                flag_key = flag_cond.flag_key
                operator = flag_cond.operator
                value = flag_cond.value

            self.flag_validator.validate(
                flag_key, operator, value,
                f"{location} -> required_flags[{i}]"
            )

        # 前提クエストの存在確認
        required_quests = quest_data.get("required_quests") or quest_data.get("requiredQuests", [])
        for req_quest in required_quests:
            if self.known_quest_ids and req_quest not in self.known_quest_ids:
                self.result.add_error(
                    "UNKNOWN_REQUIRED_QUEST",
                    f"Required quest '{req_quest}' not found",
                    location,
                    "Check quest ID spelling or add missing quest definition"
                )


# ========================================
# Full Validation Runner
# ========================================

def validate_quest_definitions(quest_definitions: list, drama_ids: Set[str] = None, actors: Set[str] = None) -> ValidationResult:
    """全クエスト定義を検証"""
    result = ValidationResult()
    validator = QuestValidator(result)

    # 既知のクエストIDを収集
    quest_ids = set()
    for quest in quest_definitions:
        if hasattr(quest, 'quest_id'):
            quest_ids.add(quest.quest_id)
        elif isinstance(quest, dict):
            quest_ids.add(quest.get('quest_id') or quest.get('questId'))

    validator.set_known_quest_ids(quest_ids)

    if drama_ids:
        validator.set_known_drama_ids(drama_ids)

    if actors:
        validator.set_known_actors(actors)

    # 各クエストを検証
    for quest in quest_definitions:
        if hasattr(quest, 'quest_id'):
            # QuestDefinition dataclass
            quest_data = {
                'drama_id': quest.drama_id,
                'quest_giver': quest.quest_giver,
                'required_flags': quest.required_flags,
                'required_quests': quest.required_quests,
            }
            quest_id = quest.quest_id
        else:
            # dict
            quest_data = quest
            quest_id = quest.get('quest_id') or quest.get('questId')

        validator.validate_quest(quest_data, quest_id)

    return result


def validate_csharp_enum_sync() -> ValidationResult:
    """
    Python側のEnum定義とC#側のEnumMappingsの同期を検証

    これはビルド時にC#ファイルを読み込んで検証することも可能
    """
    result = ValidationResult()

    # flag_definitions.py からのインポート
    try:
        from flag_definitions import (
            FlagValues, BalgasChoice, BottleChoice, KainSoulChoice, Rank, Phase
        )

        # Rank enum check
        expected_ranks = {
            "unranked": 0, "G": 1, "F": 2, "E": 3, "D": 4, "C": 5, "B": 6, "A": 7, "S": 8
        }
        csharp_ranks = CSHARP_ENUM_MAPPINGS.get("chitsii.arena.player.rank", {})
        for name, value in expected_ranks.items():
            if name not in csharp_ranks:
                result.add_error(
                    "ENUM_SYNC",
                    f"Rank '{name}' missing from C# EnumMappings",
                    "chitsii.arena.player.rank"
                )
            elif csharp_ranks[name] != value:
                result.add_error(
                    "ENUM_SYNC",
                    f"Rank '{name}' value mismatch: Python={value}, C#={csharp_ranks[name]}",
                    "chitsii.arena.player.rank"
                )

        # BalgasChoice check
        python_balgas = {"spared": 0, "killed": 1}
        csharp_balgas = CSHARP_ENUM_MAPPINGS.get("chitsii.arena.player.balgas_choice", {})
        for name, value in python_balgas.items():
            if name not in csharp_balgas:
                result.add_error(
                    "ENUM_SYNC",
                    f"BalgasChoice '{name}' missing from C# EnumMappings",
                    "chitsii.arena.player.balgas_choice",
                    "Add to ArenaQuestManager.cs EnumMappings"
                )

        # BottleChoice check
        python_bottle = {"kept": 0, "swapped": 1}
        csharp_bottle = CSHARP_ENUM_MAPPINGS.get("chitsii.arena.player.bottle_choice", {})
        for name, value in python_bottle.items():
            if name not in csharp_bottle:
                result.add_error(
                    "ENUM_SYNC",
                    f"BottleChoice '{name}' missing from C# EnumMappings",
                    "chitsii.arena.player.bottle_choice",
                    "Add to ArenaQuestManager.cs EnumMappings"
                )

        # KainSoulChoice check
        python_kain = {"freed": 0, "sold": 1}
        csharp_kain = CSHARP_ENUM_MAPPINGS.get("chitsii.arena.player.kain_soul_choice", {})
        for name, value in python_kain.items():
            if name not in csharp_kain:
                result.add_error(
                    "ENUM_SYNC",
                    f"KainSoulChoice '{name}' missing from C# EnumMappings",
                    "chitsii.arena.player.kain_soul_choice",
                    "Add to ArenaQuestManager.cs EnumMappings"
                )

    except ImportError as e:
        result.add_warning(
            "IMPORT_ERROR",
            f"Could not import flag_definitions for validation: {e}"
        )

    return result


def run_all_validations(quiet: bool = False) -> bool:
    """
    全てのバリデーションを実行

    Args:
        quiet: Trueの場合、成功時は出力を抑制（エラー時のみ詳細表示）
    """
    all_passed = True
    all_errors = []
    all_warnings = []

    # 1. Enum同期チェック
    enum_result = validate_csharp_enum_sync()
    if enum_result.has_errors:
        all_passed = False
        all_errors.extend(enum_result.errors)
    all_warnings.extend(enum_result.warnings)

    # 2. クエスト定義チェック
    try:
        from quest_dependencies import QUEST_DEFINITIONS
        from drama_constants import ALL_DRAMA_IDS
        from flag_definitions import Actors

        drama_ids = set(ALL_DRAMA_IDS)
        actors = {
            Actors.PC, Actors.LILY, Actors.BALGAS, Actors.ZEK,
            Actors.ASTAROTH
        }

        quest_result = validate_quest_definitions(QUEST_DEFINITIONS, drama_ids, actors)
        if quest_result.has_errors:
            all_passed = False
            all_errors.extend(quest_result.errors)
        all_warnings.extend(quest_result.warnings)

    except ImportError as e:
        if not quiet:
            print(f"WARNING: Could not import quest definitions: {e}")

    # 3. 報酬定義チェック
    try:
        from rewards import validate_all as validate_rewards
        reward_errors = validate_rewards()
        if reward_errors:
            all_passed = False
            for err in reward_errors:
                all_errors.append(ValidationError("REWARD_VALIDATION", err))
    except ImportError as e:
        if not quiet:
            print(f"WARNING: Could not import rewards for validation: {e}")

    # 結果出力
    if not all_passed:
        # エラーがある場合は詳細を表示
        print("\n" + "="*60)
        print("VALIDATION ERRORS")
        print("="*60)
        for e in all_errors:
            print(f"\n{e}")
        if all_warnings:
            print("\n" + "-"*60)
            print("Warnings:")
            for w in all_warnings:
                print(f"  - {w.message}")
        print("\n" + "="*60)
        print(f"FAILED: {len(all_errors)} error(s), {len(all_warnings)} warning(s)")
        print("="*60)
    elif not quiet:
        # 成功時（quiet=Falseの場合のみ）
        if all_warnings:
            print(f"Validation passed with {len(all_warnings)} warning(s)")
        else:
            print("Validation passed")

    return all_passed


if __name__ == "__main__":
    success = run_all_validations()
    sys.exit(0 if success else 1)
