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
import os


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


def parse_jump_label_mapping_cs(filepath: str) -> Dict[str, int]:
    """
    JumpLabelMapping.cs をパースしてラベル→値のマッピングを抽出

    Args:
        filepath: JumpLabelMapping.cs のパス

    Returns:
        {"label_name": value, ...}
    """
    import re

    result = {}

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # JumpLabel enum の値を抽出
        enum_values = {}
        enum_match = re.search(r'public enum JumpLabel\s*\{([^}]+)\}', content, re.DOTALL)
        if enum_match:
            enum_body = enum_match.group(1)
            for line in enum_body.split('\n'):
                line = line.strip()
                if '=' in line:
                    match = re.match(r'(\w+)\s*=\s*(\d+)', line)
                    if match:
                        name, value = match.groups()
                        enum_values[name] = int(value)

        # _labelToEnum の辞書エントリを抽出
        dict_match = re.search(r'_labelToEnum\s*=\s*new\s+Dictionary[^{]+\{([^;]+)\};', content, re.DOTALL)
        if dict_match:
            dict_body = dict_match.group(1)
            # ["label"] = JumpLabel.XXX パターンを抽出
            for match in re.finditer(r'\["([^"]+)"\]\s*=\s*JumpLabel\.(\w+)', dict_body):
                label, enum_name = match.groups()
                if enum_name in enum_values:
                    result[label] = enum_values[enum_name]

    except Exception as e:
        print(f"Warning: Could not parse {filepath}: {e}")

    return result


def validate_jump_label_sync() -> ValidationResult:
    """
    Python側のJUMP_LABELSとC#側のJumpLabelMappingの同期を検証
    """
    import os
    result = ValidationResult()

    try:
        from flag_definitions import JUMP_LABELS
    except ImportError as e:
        result.add_warning("IMPORT_ERROR", f"Could not import JUMP_LABELS: {e}")
        return result

    # C#ファイルのパスを計算
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csharp_path = os.path.join(script_dir, "..", "..", "src", "Data", "JumpLabelMapping.cs")

    if not os.path.exists(csharp_path):
        result.add_warning("FILE_NOT_FOUND", f"JumpLabelMapping.cs not found at: {csharp_path}")
        return result

    csharp_labels = parse_jump_label_mapping_cs(csharp_path)

    if not csharp_labels:
        result.add_warning("PARSE_FAILED", "Could not parse any labels from JumpLabelMapping.cs")
        return result

    # Python側のラベルがC#側に存在するか確認
    for label, value in JUMP_LABELS.items():
        if label not in csharp_labels:
            result.add_error(
                "MISSING_LABEL",
                f"Label '{label}' not found in JumpLabelMapping.cs",
                suggestion=f'Add: ["{label}"] = JumpLabel.XXX,'
            )
        elif csharp_labels[label] != value:
            result.add_error(
                "LABEL_VALUE_MISMATCH",
                f"Label '{label}' value mismatch: Python={value}, C#={csharp_labels[label]}"
            )

    # C#側にあってPython側にないラベルは警告（必須ではない）
    for label, value in csharp_labels.items():
        if label not in JUMP_LABELS:
            result.add_warning(
                "EXTRA_CSHARP_LABEL",
                f"Label '{label}' in C# but not in Python JUMP_LABELS (value={value})"
            )

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


def validate_drama_quest_sync() -> ValidationResult:
    """
    ドラマファイルで使用されているクエストIDが
    quest_dependencies.pyに定義されているか検証
    """
    import os
    import re

    result = ValidationResult()

    # quest_dependencies.pyから定義済みクエストIDを取得
    try:
        from quest_dependencies import QUEST_DEFINITIONS
        defined_quest_ids = set()
        for quest in QUEST_DEFINITIONS:
            defined_quest_ids.add(quest.quest_id)
    except ImportError as e:
        result.add_warning("IMPORT_ERROR", f"Could not import quest_dependencies: {e}")
        return result

    # ドラマファイルからQuestEntryで使用されているクエストIDを抽出
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scenarios_dir = os.path.join(script_dir, "scenarios")

    drama_files = [
        ("00_lily.py", "LILY_QUESTS"),
        ("00_zek.py", "ZEK_QUESTS"),
        ("00_arena_master.py", "AVAILABLE_QUESTS"),
    ]

    drama_quest_ids = set()

    for filename, list_name in drama_files:
        filepath = os.path.join(scenarios_dir, filename)
        if not os.path.exists(filepath):
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # QuestEntry(QuestIds.XXX, ...) パターンを抽出
            pattern = r'QuestEntry\s*\(\s*QuestIds\.(\w+)'
            matches = re.findall(pattern, content)

            for match in matches:
                # flag_definitions.pyからQuestIdsを取得して実際の値に変換
                try:
                    from flag_definitions import QuestIds
                    quest_id = getattr(QuestIds, match, None)
                    if quest_id:
                        drama_quest_ids.add((quest_id, filename, match))
                except:
                    pass

        except Exception as e:
            result.add_warning("FILE_READ_ERROR", f"Could not read {filename}: {e}")

    # 不一致を検出
    for quest_id, filename, attr_name in drama_quest_ids:
        if quest_id not in defined_quest_ids:
            result.add_error(
                "MISSING_QUEST_DEFINITION",
                f"Quest 'QuestIds.{attr_name}' ({quest_id}) used in {filename} but not defined in quest_dependencies.py",
                suggestion="Add parent quest definition to QUEST_DEFINITIONS"
            )

    return result


def validate_custom_zone_maps() -> ValidationResult:
    """
    カスタムゾーン定義とマップファイルの整合性を検証

    検証項目:
    1. battle_stages.json の zoneType がカスタムゾーン（field_fine, field_snow等）の場合、
       対応するマップファイルが存在するか確認
    2. Zone_*.cs ファイルが存在するか確認
    3. create_zone_excel.py で定義されているゾーンIDの一覧取得
    """
    import json

    result = ValidationResult()

    # パス設定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", "..")
    battle_stages_path = os.path.join(project_root, "Package", "battle_stages.json")
    maps_dir = os.path.join(project_root, "LangMod", "JP", "Maps")
    src_dir = os.path.join(project_root, "src")

    # カスタムゾーンとマップファイルのマッピング
    # Zone_*.cs の MAP_FILE_NAME 定数に対応
    CUSTOM_ZONE_MAP_FILES = {
        "field_fine": "chitsii_battle_field_fine.z",
        "field_snow": "chitsii_battle_field_snow.z",
    }

    # カスタムゾーンとC#クラスのマッピング
    CUSTOM_ZONE_CLASSES = {
        "field_fine": "Zone_FieldFine.cs",
        "field_snow": "Zone_FieldSnow.cs",
    }

    # ゲーム組み込みゾーン（検証不要）
    BUILTIN_ZONES = {"field", "dungeon", "town", "ntyris"}

    # 1. battle_stages.json のバリデーション
    if not os.path.exists(battle_stages_path):
        result.add_warning("FILE_NOT_FOUND", f"battle_stages.json not found at: {battle_stages_path}")
        return result

    try:
        with open(battle_stages_path, 'r', encoding='utf-8') as f:
            battle_stages = json.load(f)
    except Exception as e:
        result.add_error("JSON_PARSE_ERROR", f"Failed to parse battle_stages.json: {e}")
        return result

    # 使用されているカスタムゾーンを収集
    used_custom_zones = set()
    stage_categories = ["rankUpStages", "normalStages", "debugStages"]

    for category in stage_categories:
        stages = battle_stages.get(category, {})
        for stage_id, stage_data in stages.items():
            zone_type = stage_data.get("zoneType", "")
            if zone_type and zone_type not in BUILTIN_ZONES:
                used_custom_zones.add((zone_type, stage_id, category))

    # 2. カスタムゾーンに対応するマップファイルの存在確認
    for zone_type, stage_id, category in used_custom_zones:
        # マップファイルチェック
        if zone_type in CUSTOM_ZONE_MAP_FILES:
            map_file = CUSTOM_ZONE_MAP_FILES[zone_type]
            map_path = os.path.join(maps_dir, map_file)
            if not os.path.exists(map_path):
                result.add_error(
                    "MISSING_MAP_FILE",
                    f"Map file '{map_file}' not found for zoneType '{zone_type}'",
                    location=f"{category}/{stage_id}",
                    suggestion=f"Create map file at: LangMod/JP/Maps/{map_file}"
                )
        else:
            result.add_error(
                "UNKNOWN_ZONE_TYPE",
                f"Unknown custom zoneType '{zone_type}' used",
                location=f"{category}/{stage_id}",
                suggestion="Add zone to CUSTOM_ZONE_MAP_FILES in validation.py, or use builtin zone"
            )

    # 3. C#クラスファイルの存在確認
    for zone_type in set(z[0] for z in used_custom_zones):
        if zone_type in CUSTOM_ZONE_CLASSES:
            cs_file = CUSTOM_ZONE_CLASSES[zone_type]
            cs_path = os.path.join(src_dir, cs_file)
            if not os.path.exists(cs_path):
                result.add_error(
                    "MISSING_ZONE_CLASS",
                    f"C# class file '{cs_file}' not found for zoneType '{zone_type}'",
                    suggestion=f"Create {cs_file} in src/ directory"
                )

    # 4. 定義済みだが未使用のカスタムゾーンを警告
    defined_custom_zones = set(CUSTOM_ZONE_MAP_FILES.keys())
    used_zone_types = set(z[0] for z in used_custom_zones)
    unused_zones = defined_custom_zones - used_zone_types

    for zone_type in unused_zones:
        # マップファイルが存在する場合のみ警告（未使用でもファイルがなければ問題なし）
        map_file = CUSTOM_ZONE_MAP_FILES.get(zone_type)
        if map_file:
            map_path = os.path.join(maps_dir, map_file)
            if os.path.exists(map_path):
                result.add_warning(
                    "UNUSED_CUSTOM_ZONE",
                    f"Custom zone '{zone_type}' is defined but not used in any stage",
                    suggestion="Consider using this zone in battle_stages.json or remove the map file"
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

    # 2. ジャンプラベル同期チェック
    label_result = validate_jump_label_sync()
    if label_result.has_errors:
        all_passed = False
        all_errors.extend(label_result.errors)
    all_warnings.extend(label_result.warnings)

    # 3. ドラマ-クエスト整合性チェック
    drama_quest_result = validate_drama_quest_sync()
    if drama_quest_result.has_errors:
        all_passed = False
        all_errors.extend(drama_quest_result.errors)
    all_warnings.extend(drama_quest_result.warnings)

    # 4. クエスト定義チェック
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

    # 5. 報酬定義チェック
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

    # 6. カスタムゾーン・マップファイル整合性チェック
    zone_map_result = validate_custom_zone_maps()
    if zone_map_result.has_errors:
        all_passed = False
        all_errors.extend(zone_map_result.errors)
    all_warnings.extend(zone_map_result.warnings)

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
