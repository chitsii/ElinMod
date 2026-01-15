"""
arena_types.py - Arena Drama System Data Types

This module defines the data classes used throughout the arena drama system.
These are shared between arena_mixins.py and arena_drama_builder.py.

Data Classes:
- RankDefinition: Rank-up trial definition
- GreetingDefinition: Rank-based greeting definition
- QuestEntry: Quest dispatcher entry
- BattleStageDefinition: Battle stage definition
- MenuItem: Menu item definition
- QuestInfoDefinition: Quest info display definition
- QuestStartDefinition: Quest start definition
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from drama_builder import DramaLabel


@dataclass
class RankDefinition:
    """
    ランクアップ試験の定義

    これ1つで以下のステップを自動生成:
    - rank_up_result_{rank}: 結果チェック（勝利/敗北分岐）
    - rank_up_victory_{rank}: 勝利処理
    - rank_up_defeat_{rank}: 敗北処理
    - start_rank_{rank}: 試験開始確認
    - start_rank_{rank}_confirmed: 試験実行
    """
    rank: str  # "g", "f", "e" など（小文字）
    quest_id: str  # QuestIds.RANK_UP_G
    drama_name: str  # DramaNames.RANK_UP_G
    confirm_msg: str  # 確認メッセージ
    confirm_button: str = "挑む"  # 確認ボタンテキスト
    sendoff_msg: str = "行ってこい！"  # 送り出しメッセージ
    trial_flag_value: int = 0  # sukutsu_rank_up_trial の値
    quest_flag_value: int = 0  # sukutsu_quest_target_name の値
    # 外部で定義された勝利/敗北ステップ追加関数
    result_steps_func: Optional[Callable] = None


@dataclass
class GreetingDefinition:
    """
    ランク別挨拶の定義

    Example:
        GreetingDefinition(0, "greet_u", "おう、ひよっこ。今日は何の用だ？")
    """
    rank_value: int  # player.rank の値
    text_id: str  # テキストID
    text_jp: str  # 日本語テキスト
    text_en: str = ""  # 英語テキスト（省略時は日本語と同じ）


@dataclass
class QuestEntry:
    """
    クエストディスパッチャーのエントリ

    Example:
        QuestEntry(QuestIds.ZEK_INTRO, 21, "quest_zek_intro")
    """
    quest_id: str  # クエストID
    flag_value: int  # sukutsu_quest_target_name の値
    step_name: str  # ジャンプ先ステップ名


@dataclass
class BattleStageDefinition:
    """
    バトルステージの定義

    Example:
        BattleStageDefinition(
            stage_num=1,
            stage_id="stage_1",
            advice="お前の最初の相手は...",
            sendoff="よし、行け！",
            go_button="準備できた、行く！",
            cancel_button="もう少し準備してくる",
            next_stage_flag=2,  # この値以上なら次ステージへ
        )
    """
    stage_num: int  # ステージ番号 (1, 2, 3, 4)
    stage_id: str  # ステージID ("stage_1", "stage_2", etc.)
    advice: str  # 戦闘前アドバイス
    advice_id: str = ""  # アドバイスのtext_id
    sendoff: str = ""  # 送り出しメッセージ
    sendoff_id: str = ""  # 送り出しのtext_id
    go_button: str = "準備できた！"  # 開始ボタン
    cancel_button: str = "待ってくれ"  # キャンセルボタン
    next_stage_flag: Optional[int] = None  # この値以上なら次ステージにスキップ


@dataclass
class MenuItem:
    """
    メニュー項目の定義

    Example:
        MenuItem("戦いに挑む", battle_prep, text_id="c3")
    """
    text_jp: str  # 選択肢テキスト
    jump_to: Union[str, 'DramaLabel']  # ジャンプ先
    text_en: str = ""  # 英語テキスト
    text_id: str = ""  # テキストID
    condition: str = ""  # 表示条件


@dataclass
class QuestInfoDefinition:
    """
    クエスト情報表示の定義（バルガスが情報だけ伝える系）

    Example:
        QuestInfoDefinition(
            "quest_zek_intro",
            "quest_zek_info",
            ["おい、見慣れねえ商人が来てるぞ。", "ロビーの隅にいるはずだ。"]
        )
    """
    step_name: str  # ステップ名
    text_id_prefix: str  # text_idのプレフィックス
    messages: List[str]  # メッセージリスト
    messages_en: List[str] = field(default_factory=list)


@dataclass
class QuestStartDefinition:
    """
    バルガスから直接開始できるクエストの定義

    Example:
        QuestStartDefinition(
            info_step="quest_upper_existence",
            start_step="start_upper_existence",
            info_messages=["お前には『観客』の正体を教えておく必要がある。", "聞く覚悟はあるか？"],
            accept_button="聞く",
            decline_button="今はいい",
            start_message="いいだろう。座れ。",
            drama_name=DramaNames.UPPER_EXISTENCE,
        )
    """
    info_step: str  # 情報表示ステップ名
    start_step: str  # 開始ステップ名
    info_messages: List[str]  # 情報メッセージ
    info_id_prefix: str = ""  # 情報のtext_idプレフィックス
    accept_button: str = "受ける"  # 受諾ボタン
    accept_id: str = ""  # 受諾ボタンのtext_id
    decline_button: str = "今はいい"  # 辞退ボタン
    decline_id: str = ""  # 辞退ボタンのtext_id
    start_message: str = ""  # 開始時メッセージ
    drama_name: str = ""  # 開始するドラマ名
