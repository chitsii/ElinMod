"""
Arena High-Level API - データ構造とビルダー拡張

arena_master.py を宣言的に書くためのデータ構造と高レベルAPI
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Callable, Any, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from arena_drama_builder import ArenaDramaBuilder
    from drama_builder import DramaLabel, DramaActor


# ============================================================================
# データ構造定義
# ============================================================================

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


# ============================================================================
# ビルダー拡張メソッド（ArenaDramaBuilderに追加）
# ============================================================================

def build_rank_system(
    builder: 'ArenaDramaBuilder',
    ranks: List[RankDefinition],
    actor: Union[str, 'DramaActor'],
    fallback_step: Union[str, 'DramaLabel'],
    cancel_step: Union[str, 'DramaLabel'],
    end_step: Union[str, 'DramaLabel'],
) -> Dict[str, 'DramaLabel']:
    """
    ランクアップシステム全体を自動生成

    Args:
        builder: ArenaDramaBuilder
        ranks: RankDefinitionのリスト
        actor: 発言者（通常はバルガス）
        fallback_step: フォールバック先（通常はregistered）
        cancel_step: キャンセル時のジャンプ先
        end_step: 終了ステップ

    Returns:
        生成されたラベルの辞書

    生成されるステップ:
    - rank_up_result_{rank}: 結果チェック（勝利/敗北分岐）
    - rank_up_victory_{rank}: 勝利処理
    - rank_up_defeat_{rank}: 敗北処理
    - start_rank_{rank}: 試験開始確認
    - start_rank_{rank}_confirmed: 試験実行
    """
    from drama_builder import DramaLabel

    labels = {}

    # 各ランクのラベルを先に作成
    for rank_def in ranks:
        r = rank_def.rank.lower()
        labels[f'rank_up_result_{r}'] = builder.label(f'rank_up_result_{r}')
        labels[f'rank_up_victory_{r}'] = builder.label(f'rank_up_victory_{r}')
        labels[f'rank_up_defeat_{r}'] = builder.label(f'rank_up_defeat_{r}')
        labels[f'start_rank_{r}'] = builder.label(f'start_rank_{r}')
        labels[f'start_rank_{r}_confirmed'] = builder.label(f'start_rank_{r}_confirmed')

    # 結果分岐ステップを生成
    for rank_def in ranks:
        r = rank_def.rank.lower()
        result_label = labels[f'rank_up_result_{r}']
        victory_label = labels[f'rank_up_victory_{r}']
        defeat_label = labels[f'rank_up_defeat_{r}']

        # sukutsu_arena_result: 0=未設定, 1=勝利, 2=敗北
        builder.step(result_label) \
            .switch_flag("sukutsu_arena_result", [
                fallback_step,   # 0: 未設定時
                victory_label,   # 1: 勝利
                defeat_label,    # 2: 敗北
            ])

    # 勝利/敗北ステップを追加（外部関数経由）
    for rank_def in ranks:
        r = rank_def.rank.lower()
        if rank_def.result_steps_func:
            rank_def.result_steps_func(
                builder,
                labels[f'rank_up_victory_{r}'],
                labels[f'rank_up_defeat_{r}'],
                fallback_step
            )

    # 試験開始確認ステップ
    for rank_def in ranks:
        r = rank_def.rank.lower()
        start_label = labels[f'start_rank_{r}']
        confirmed_label = labels[f'start_rank_{r}_confirmed']

        builder.step(start_label) \
            .say(f"rank_up_confirm_{r}", rank_def.confirm_msg, "", actor=actor) \
            .choice(confirmed_label, rank_def.confirm_button, "", text_id=f"c_confirm_rup_{r}") \
            .choice(cancel_step, "やめておく", "", text_id="c_cancel_rup") \
            .on_cancel(cancel_step)

    # 試験実行ステップ
    for rank_def in ranks:
        r = rank_def.rank.lower()
        confirmed_label = labels[f'start_rank_{r}_confirmed']

        builder.step(confirmed_label) \
            .set_flag("sukutsu_rank_up_trial", rank_def.trial_flag_value) \
            .say_and_start_drama(rank_def.sendoff_msg, rank_def.drama_name, "sukutsu_arena_master") \
            .jump(end_step)

    return labels


def build_greetings(
    builder: 'ArenaDramaBuilder',
    greetings: List[GreetingDefinition],
    actor: Union[str, 'DramaActor'],
    add_choices_func: Callable,
    default_greeting: GreetingDefinition = None,
) -> Dict[int, 'DramaLabel']:
    """
    ランク別挨拶ステップを自動生成

    Args:
        builder: ArenaDramaBuilder
        greetings: GreetingDefinitionのリスト
        actor: 発言者
        add_choices_func: 選択肢を追加する関数 (builder) -> None
        default_greeting: デフォルト挨拶

    Returns:
        {rank_value: label} の辞書
    """
    labels = {}

    for greet in greetings:
        label_name = f"greet_{greet.rank_value}"
        label = builder.label(label_name)
        labels[greet.rank_value] = label

        b = builder.step(label).say(
            greet.text_id,
            greet.text_jp,
            greet.text_en or greet.text_jp,
            actor=actor
        )
        add_choices_func(b)

    # デフォルト挨拶
    if default_greeting:
        default_label = builder.label("greet_default")
        labels['default'] = default_label
        b = builder.step(default_label).say(
            default_greeting.text_id,
            default_greeting.text_jp,
            default_greeting.text_en or default_greeting.text_jp,
            actor=actor
        )
        add_choices_func(b)

    return labels


def build_greeting_dispatcher(
    builder: 'ArenaDramaBuilder',
    greeting_labels: Dict[int, 'DramaLabel'],
    entry_step: Union[str, 'DramaLabel'],
    flag_key: str = "player.rank",
    default_label: 'DramaLabel' = None,
) -> None:
    """
    ランク別挨拶へのディスパッチャーを生成

    Args:
        builder: ArenaDramaBuilder
        greeting_labels: build_greetings() の戻り値
        entry_step: エントリーステップ
        flag_key: 分岐に使用するフラグキー
        default_label: デフォルトラベル
    """
    fallback = default_label or greeting_labels.get('default')

    # Dict形式からList形式に変換
    # greeting_labelsのキーはrank値（0, 1, 2, ...）
    int_cases = {v: label for v, label in greeting_labels.items() if isinstance(v, int)}
    if int_cases:
        max_rank = max(int_cases.keys())
        cases_list = [int_cases.get(i, fallback) for i in range(max_rank + 1)]
        cases_list.append(fallback)  # fallback追加
    else:
        cases_list = [fallback]

    builder.step(entry_step) \
        .switch_flag(flag_key, cases_list)


def build_battle_stages(
    builder: 'ArenaDramaBuilder',
    stages: List[BattleStageDefinition],
    actor: Union[str, 'DramaActor'],
    entry_step: Union[str, 'DramaLabel'],
    cancel_step: Union[str, 'DramaLabel'],
    stage_flag: str = "sukutsu_arena_stage",
) -> Dict[int, 'DramaLabel']:
    """
    バトルステージシステムを自動生成

    Args:
        builder: ArenaDramaBuilder
        stages: BattleStageDefinitionのリスト
        actor: 発言者
        entry_step: エントリーステップ
        cancel_step: キャンセル時のジャンプ先
        stage_flag: ステージ判定フラグ

    Returns:
        {stage_num: prep_label} の辞書
    """
    labels = {}

    # ラベル作成
    for stage in stages:
        labels[stage.stage_num] = {
            'prep': builder.label(f"stage{stage.stage_num}_prep"),
            'start': builder.label(f"battle_start_stage{stage.stage_num}"),
        }

    # エントリーステップ（最初のステージへの分岐チェーン）
    current_builder = builder.step(entry_step)

    for i, stage in enumerate(stages):
        if stage.next_stage_flag is not None and i < len(stages) - 1:
            next_stage = stages[i + 1]
            current_builder = current_builder.branch_if(
                stage_flag, ">=", stage.next_stage_flag,
                labels[next_stage.stage_num]['prep']
            )

    # 最初のステージのアドバイス（エントリーポイントに含める）
    first_stage = stages[0]
    current_builder \
        .say(first_stage.advice_id or f"stage{first_stage.stage_num}_advice",
             first_stage.advice, "", actor=actor) \
        .choice(labels[first_stage.stage_num]['start'],
                first_stage.go_button, "", text_id=f"c_go{first_stage.stage_num}") \
        .choice(cancel_step, first_stage.cancel_button, "", text_id=f"c_cancel{first_stage.stage_num}") \
        .on_cancel(cancel_step)

    # 各ステージのprepステップ（2番目以降）
    for i, stage in enumerate(stages[1:], start=1):
        prep_label = labels[stage.stage_num]['prep']
        start_label = labels[stage.stage_num]['start']

        stage_builder = builder.step(prep_label)

        # 次のステージへの分岐
        if stage.next_stage_flag is not None and i < len(stages) - 1:
            next_stage = stages[i + 1]
            stage_builder = stage_builder.branch_if(
                stage_flag, ">=", stage.next_stage_flag,
                labels[next_stage.stage_num]['prep']
            )

        stage_builder \
            .say(stage.advice_id or f"stage{stage.stage_num}_advice",
                 stage.advice, "", actor=actor) \
            .choice(start_label, stage.go_button, "", text_id=f"c_go{stage.stage_num}") \
            .choice(cancel_step, stage.cancel_button, "", text_id=f"c_cancel{stage.stage_num}") \
            .on_cancel(cancel_step)

    # 各ステージのstartステップ
    for stage in stages:
        start_label = labels[stage.stage_num]['start']

        if stage.sendoff:
            builder.step(start_label) \
                .say(stage.sendoff_id or f"sendoff{stage.stage_num}",
                     stage.sendoff, "", actor=actor) \
                .start_battle_and_end(stage.stage_id)
        else:
            builder.step(start_label) \
                .start_battle_and_end(stage.stage_id)

    return labels


def build_quest_dispatcher(
    builder: 'ArenaDramaBuilder',
    quests: List[QuestEntry],
    entry_step: Union[str, 'DramaLabel'],
    fallback_step: Union[str, 'DramaLabel'],
    actor: Union[str, 'DramaActor'],
    intro_message: str = "",
    intro_id: str = "",
    flag_name: str = "sukutsu_quest_target_name",
) -> Dict[str, 'DramaLabel']:
    """
    クエストディスパッチャーを自動生成

    Args:
        builder: ArenaDramaBuilder
        quests: QuestEntryのリスト
        entry_step: エントリーステップ
        fallback_step: フォールバックステップ
        actor: 発言者
        intro_message: イントロメッセージ
        intro_id: イントロのtext_id
        flag_name: クエストフラグ名

    Returns:
        {step_name: label} の辞書
    """
    labels = {}

    # ラベル作成
    for quest in quests:
        labels[quest.step_name] = builder.label(quest.step_name)

    # エントリーステップ
    step_builder = builder.step(entry_step)

    if intro_message:
        step_builder.say(intro_id or "quest_check", intro_message, "", actor=actor)

    step_builder \
        .set_flag("sukutsu_quest_found", 0) \
        .set_flag(flag_name, 0) \
        .debug_log_quests()

    # check_quests 呼び出し
    checks = [(quest.quest_id, labels[quest.step_name]) for quest in quests]
    step_builder.check_quests(checks)

    # Dict形式からList形式に変換（スパースな値に対応）
    cases = {quest.flag_value: labels[quest.step_name] for quest in quests}
    if cases:
        max_value = max(cases.keys())
        cases_list = [cases.get(i, fallback_step) for i in range(max_value + 1)]
        cases_list.append(fallback_step)  # fallback追加
    else:
        cases_list = [fallback_step]

    step_builder.switch_flag(flag_name, cases_list)

    return labels


def add_menu(
    builder: 'ArenaDramaBuilder',
    items: List[MenuItem],
    cancel: Union[str, 'DramaLabel'] = None,
) -> 'ArenaDramaBuilder':
    """
    メニュー（選択肢リスト）を追加

    Args:
        builder: ArenaDramaBuilder
        items: MenuItemのリスト
        cancel: キャンセル時のジャンプ先

    Returns:
        builder（チェーン用）
    """
    for item in items:
        if item.condition:
            builder.choice_if(
                item.jump_to,
                item.text_jp,
                item.condition,
                item.text_en,
                item.text_id
            )
        else:
            builder.choice(
                item.jump_to,
                item.text_jp,
                item.text_en,
                item.text_id
            )

    if cancel:
        builder.on_cancel(cancel)

    return builder


def build_quest_info_steps(
    builder: 'ArenaDramaBuilder',
    infos: List[QuestInfoDefinition],
    actor: Union[str, 'DramaActor'],
    return_step: Union[str, 'DramaLabel'],
) -> Dict[str, 'DramaLabel']:
    """
    クエスト情報表示ステップを一括生成

    Args:
        builder: ArenaDramaBuilder
        infos: QuestInfoDefinitionのリスト
        actor: 発言者
        return_step: 戻り先ステップ

    Returns:
        {step_name: label} の辞書
    """
    labels = {}

    for info in infos:
        label = builder.label(info.step_name)
        labels[info.step_name] = label

        step_builder = builder.step(label)

        for i, msg in enumerate(info.messages):
            msg_en = info.messages_en[i] if i < len(info.messages_en) else msg
            step_builder.say(
                f"{info.text_id_prefix}{i+1}" if i > 0 else info.text_id_prefix,
                msg,
                msg_en,
                actor=actor
            )

        step_builder.jump(return_step)

    return labels


def build_quest_start_steps(
    builder: 'ArenaDramaBuilder',
    starts: List[QuestStartDefinition],
    actor: Union[str, 'DramaActor'],
    cancel_step: Union[str, 'DramaLabel'],
    end_step: Union[str, 'DramaLabel'],
) -> Dict[str, 'DramaLabel']:
    """
    直接開始可能なクエストのステップを一括生成

    Args:
        builder: ArenaDramaBuilder
        starts: QuestStartDefinitionのリスト
        actor: 発言者
        cancel_step: キャンセル時のジャンプ先
        end_step: 終了ステップ

    Returns:
        {step_name: label} の辞書
    """
    labels = {}

    for start in starts:
        info_label = builder.label(start.info_step)
        start_label = builder.label(start.start_step)
        labels[start.info_step] = info_label
        labels[start.start_step] = start_label

        # 情報表示ステップ
        step_builder = builder.step(info_label)

        for i, msg in enumerate(start.info_messages):
            step_builder.say(
                f"{start.info_id_prefix}{i+1}" if start.info_id_prefix else f"{start.info_step}_{i+1}",
                msg,
                "",
                actor=actor
            )

        step_builder \
            .choice(start_label, start.accept_button, "", text_id=start.accept_id) \
            .choice(cancel_step, start.decline_button, "", text_id=start.decline_id) \
            .on_cancel(cancel_step)

        # 開始ステップ
        builder.step(start_label) \
            .say_and_start_drama(start.start_message, start.drama_name, "sukutsu_arena_master") \
            .jump(end_step)

    return labels
