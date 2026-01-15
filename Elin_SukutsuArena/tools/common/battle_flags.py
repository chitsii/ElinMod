"""
battle_flags.py - バトル結果フラグの一元管理

バグパターン防止:
  フラグの設定とクリアが別の場所にあると、クリアを忘れてバグになる。
  このモジュールで設定・クリア・分岐を一元管理し、整合性を保証する。

使用例:
  # シナリオ側（バトル開始時）
  from battle_flags import QuestBattleFlags

  builder.step(scene3) \\
      .set_flag(QuestBattleFlags.FLAG_NAME, QuestBattleFlags.UPPER_EXISTENCE) \\
      .set_flag(QuestBattleFlags.RESULT_FLAG, 1) \\
      .start_battle_by_stage("upper_existence_battle")

  # arena_master側（結果処理）
  builder.step(quest_battle_result_upper) \\
      .set_flag(QuestBattleFlags.FLAG_NAME, QuestBattleFlags.NONE) \\  # クリア
      .switch_flag("sukutsu_arena_result", [...])
"""

from typing import Dict, List, TYPE_CHECKING
from enum import IntEnum

if TYPE_CHECKING:
    from drama_builder import DramaBuilder


class QuestBattleType(IntEnum):
    """クエストバトルの種類"""
    NONE = 0
    UPPER_EXISTENCE = 1
    VS_BALGAS = 2
    LAST_BATTLE = 3
    BALGAS_TRAINING = 4


class RankUpTrialType(IntEnum):
    """ランクアップ試験の種類"""
    NONE = 0
    RANK_G = 1
    RANK_F = 2
    RANK_E = 3
    RANK_D = 4
    RANK_C = 5
    RANK_B = 6
    RANK_A = 7


class QuestBattleFlags:
    """
    クエストバトル用フラグ管理

    フラグ:
      sukutsu_quest_battle: バトル種類（QuestBattleType）
      sukutsu_is_quest_battle_result: 結果処理フラグ（1=要処理）

    ライフサイクル:
      1. バトル開始前: set_for_battle() でフラグ設定
      2. バトル終了後: OnLeaveZone() で is_result=1 設定
      3. 結果処理: clear() でフラグクリア、switch_flag で分岐
    """

    FLAG_NAME = "sukutsu_quest_battle"
    RESULT_FLAG = "sukutsu_is_quest_battle_result"

    # 定数（後方互換）
    NONE = QuestBattleType.NONE
    UPPER_EXISTENCE = QuestBattleType.UPPER_EXISTENCE
    VS_BALGAS = QuestBattleType.VS_BALGAS
    LAST_BATTLE = QuestBattleType.LAST_BATTLE
    BALGAS_TRAINING = QuestBattleType.BALGAS_TRAINING

    # クエストIDとの対応
    QUEST_MAPPING: Dict[QuestBattleType, str] = {
        QuestBattleType.UPPER_EXISTENCE: "07_upper_existence",
        QuestBattleType.VS_BALGAS: "15_vs_balgas",
        QuestBattleType.LAST_BATTLE: "18_last_battle",
        QuestBattleType.BALGAS_TRAINING: "09_balgas_training",
    }

    @classmethod
    def set_for_battle(cls, builder: 'DramaBuilder', battle_type: QuestBattleType) -> 'DramaBuilder':
        """
        バトル開始前にフラグを設定

        Args:
            builder: DramaBuilder インスタンス
            battle_type: QuestBattleType の値

        Returns:
            builder（チェーン用）
        """
        return builder \
            .set_flag(cls.FLAG_NAME, int(battle_type)) \
            .set_flag(cls.RESULT_FLAG, 1)

    @classmethod
    def clear(cls, builder: 'DramaBuilder') -> 'DramaBuilder':
        """
        結果処理後にフラグをクリア

        Args:
            builder: DramaBuilder インスタンス

        Returns:
            builder（チェーン用）
        """
        return builder.set_flag(cls.FLAG_NAME, int(cls.NONE))

    @classmethod
    def get_switch_cases(cls, labels: Dict[QuestBattleType, str], fallback: str) -> List[str]:
        """
        switch_flag 用のケースリストを生成

        Args:
            labels: {QuestBattleType: ラベル名} の辞書
            fallback: フォールバック時のラベル名

        Returns:
            switch_flag に渡すリスト
        """
        cases = [fallback]  # 0: NONE
        for battle_type in [cls.UPPER_EXISTENCE, cls.VS_BALGAS, cls.LAST_BATTLE, cls.BALGAS_TRAINING]:
            cases.append(labels.get(battle_type, fallback))
        return cases


class RankUpTrialFlags:
    """
    ランクアップ試験用フラグ管理

    フラグ:
      sukutsu_rank_up_trial: 試験ランク（RankUpTrialType）
      sukutsu_is_rank_up_result: 結果処理フラグ（1=要処理）

    ライフサイクル:
      1. 試験開始前: set_for_trial() でフラグ設定
      2. バトル終了後: OnLeaveZone() で is_result=1 設定
      3. 結果処理: clear() でフラグクリア、switch_flag で分岐
    """

    FLAG_NAME = "sukutsu_rank_up_trial"
    RESULT_FLAG = "sukutsu_is_rank_up_result"

    # 定数（後方互換）
    NONE = RankUpTrialType.NONE
    RANK_G = RankUpTrialType.RANK_G
    RANK_F = RankUpTrialType.RANK_F
    RANK_E = RankUpTrialType.RANK_E
    RANK_D = RankUpTrialType.RANK_D
    RANK_C = RankUpTrialType.RANK_C
    RANK_B = RankUpTrialType.RANK_B
    RANK_A = RankUpTrialType.RANK_A

    # ランク文字列との対応
    RANK_MAPPING: Dict[str, RankUpTrialType] = {
        "G": RankUpTrialType.RANK_G,
        "F": RankUpTrialType.RANK_F,
        "E": RankUpTrialType.RANK_E,
        "D": RankUpTrialType.RANK_D,
        "C": RankUpTrialType.RANK_C,
        "B": RankUpTrialType.RANK_B,
        "A": RankUpTrialType.RANK_A,
    }

    @classmethod
    def get_trial_type(cls, rank: str) -> RankUpTrialType:
        """
        ランク文字列から RankUpTrialType を取得

        Args:
            rank: "G", "F", "E", "D", "C", "B", "A"

        Returns:
            RankUpTrialType の値
        """
        return cls.RANK_MAPPING.get(rank.upper(), cls.NONE)

    @classmethod
    def set_for_trial(cls, builder: 'DramaBuilder', rank: str) -> 'DramaBuilder':
        """
        ランクアップ試験開始前にフラグを設定

        Args:
            builder: DramaBuilder インスタンス
            rank: "G", "F", "E", "D", "C", "B", "A"

        Returns:
            builder（チェーン用）
        """
        trial_type = cls.get_trial_type(rank)
        return builder.set_flag(cls.FLAG_NAME, int(trial_type))

    @classmethod
    def clear(cls, builder: 'DramaBuilder') -> 'DramaBuilder':
        """
        結果処理後にフラグをクリア

        Args:
            builder: DramaBuilder インスタンス

        Returns:
            builder（チェーン用）
        """
        return builder.set_flag(cls.FLAG_NAME, int(cls.NONE))

    @classmethod
    def get_switch_cases(cls, labels: Dict[RankUpTrialType, str], fallback: str) -> List[str]:
        """
        switch_flag 用のケースリストを生成

        Args:
            labels: {RankUpTrialType: ラベル名} の辞書
            fallback: フォールバック時のラベル名

        Returns:
            switch_flag に渡すリスト
        """
        cases = [fallback]  # 0: NONE
        for trial_type in [cls.RANK_G, cls.RANK_F, cls.RANK_E, cls.RANK_D, cls.RANK_C, cls.RANK_B, cls.RANK_A]:
            cases.append(labels.get(trial_type, fallback))
        cases.append(fallback)  # 末尾フォールバック
        return cases
