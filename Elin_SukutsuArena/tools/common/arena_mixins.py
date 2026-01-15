"""
arena_mixins.py - Arena Drama Builder Mixins

Mixin classes for ArenaDramaBuilder providing domain-specific functionality.
Each mixin handles a specific subsystem:

- RankSystemMixin: Rank-up system (trials, results, confirmations)
- QuestSystemMixin: Quest dispatching and info display
- BattleSystemMixin: Battle stage progression
- MenuMixin: Menu construction

Usage:
    class ArenaDramaBuilder(
        RankSystemMixin,
        QuestSystemMixin,
        BattleSystemMixin,
        MenuMixin,
        DramaBuilder
    ):
        pass
"""

from typing import Dict, List, Union, Callable, TYPE_CHECKING

from arena_types import (
    RankDefinition, GreetingDefinition, QuestEntry,
    BattleStageDefinition, MenuItem, QuestInfoDefinition, QuestStartDefinition
)
from battle_flags import RankUpTrialFlags

if TYPE_CHECKING:
    from drama_builder import DramaLabel, DramaActor


class RankSystemMixin:
    """
    ランクアップシステム関連のビルダーメソッド

    Provides:
    - build_rank_system(): ランクアップシステム全体を自動生成
    - build_greetings(): ランク別挨拶ステップを生成
    - build_greeting_dispatcher(): 挨拶ディスパッチャーを生成
    """

    def build_rank_system(
        self,
        ranks: List[RankDefinition],
        actor: Union[str, 'DramaActor'],
        fallback_step: Union[str, 'DramaLabel'],
        cancel_step: Union[str, 'DramaLabel'],
        end_step: Union[str, 'DramaLabel'],
    ) -> Dict[str, 'DramaLabel']:
        """
        ランクアップシステム全体を自動生成

        Args:
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
        labels = {}

        # 各ランクのラベルを先に作成
        for rank_def in ranks:
            r = rank_def.rank.lower()
            labels[f'rank_up_result_{r}'] = self.label(f'rank_up_result_{r}')
            labels[f'rank_up_victory_{r}'] = self.label(f'rank_up_victory_{r}')
            labels[f'rank_up_defeat_{r}'] = self.label(f'rank_up_defeat_{r}')
            labels[f'start_rank_{r}'] = self.label(f'start_rank_{r}')
            labels[f'start_rank_{r}_confirmed'] = self.label(f'start_rank_{r}_confirmed')

        # 結果分岐ステップを生成
        for rank_def in ranks:
            r = rank_def.rank.lower()
            result_label = labels[f'rank_up_result_{r}']
            victory_label = labels[f'rank_up_victory_{r}']
            defeat_label = labels[f'rank_up_defeat_{r}']

            # sukutsu_arena_result: 0=未設定, 1=勝利, 2=敗北
            # sukutsu_rank_up_trialをクリア（switch_flag後に次回影響しないように）
            self.step(result_label) \
                .set_flag(RankUpTrialFlags.FLAG_NAME, RankUpTrialFlags.NONE) \
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
                    self,
                    labels[f'rank_up_victory_{r}'],
                    labels[f'rank_up_defeat_{r}'],
                    fallback_step
                )

        # 試験開始確認ステップ
        for rank_def in ranks:
            r = rank_def.rank.lower()
            start_label = labels[f'start_rank_{r}']
            confirmed_label = labels[f'start_rank_{r}_confirmed']

            self.step(start_label) \
                .say(f"rank_up_confirm_{r}", rank_def.confirm_msg, "", actor=actor) \
                .choice(confirmed_label, rank_def.confirm_button, "", text_id=f"c_confirm_rup_{r}") \
                .choice(cancel_step, "やめておく", "", text_id="c_cancel_rup") \
                .on_cancel(cancel_step)

        # 試験実行ステップ
        for rank_def in ranks:
            r = rank_def.rank.lower()
            confirmed_label = labels[f'start_rank_{r}_confirmed']

            self.step(confirmed_label) \
                .set_flag(RankUpTrialFlags.FLAG_NAME, rank_def.trial_flag_value) \
                .say_and_start_drama(rank_def.sendoff_msg, rank_def.drama_name, "sukutsu_arena_master") \
                .jump(end_step)

        return labels

    def build_greetings(
        self,
        greetings: List[GreetingDefinition],
        actor: Union[str, 'DramaActor'],
        add_choices_func: Callable,
        default_greeting: GreetingDefinition = None,
    ) -> Dict[int, 'DramaLabel']:
        """
        ランク別挨拶ステップを自動生成

        Args:
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
            label = self.label(label_name)
            labels[greet.rank_value] = label

            b = self.step(label).say(
                greet.text_id,
                greet.text_jp,
                greet.text_en or greet.text_jp,
                actor=actor
            )
            add_choices_func(b)

        # デフォルト挨拶
        if default_greeting:
            default_label = self.label("greet_default")
            labels['default'] = default_label
            b = self.step(default_label).say(
                default_greeting.text_id,
                default_greeting.text_jp,
                default_greeting.text_en or default_greeting.text_jp,
                actor=actor
            )
            add_choices_func(b)

        return labels

    def build_greeting_dispatcher(
        self,
        greeting_labels: Dict[int, 'DramaLabel'],
        entry_step: Union[str, 'DramaLabel'],
        flag_key: str = "player.rank",
        default_label: 'DramaLabel' = None,
    ) -> None:
        """
        ランク別挨拶へのディスパッチャーを生成

        Args:
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

        self.step(entry_step) \
            .switch_flag(flag_key, cases_list)


class QuestSystemMixin:
    """
    クエストシステム関連のビルダーメソッド

    Provides:
    - build_quest_dispatcher(): クエストディスパッチャーを構築
    - build_quest_info_steps(): クエスト情報表示ステップを生成
    - build_quest_start_steps(): クエスト開始ステップを生成
    """

    def build_quest_dispatcher(
        self,
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

        C#側のArenaQuestManager.GetAvailableQuests()を使用して
        前提条件を正しくチェックし、利用可能なクエストのみを選択する。

        フラグ値の意味:
        - 0: 利用可能なクエストなし（fallback）
        - 1: リストの1番目のクエストが利用可能
        - 2: リストの2番目のクエストが利用可能
        - ...

        Args:
            quests: QuestEntryのリスト（優先度順）
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
            labels[quest.step_name] = self.label(quest.step_name)

        # エントリーステップ
        step_builder = self.step(entry_step)

        if intro_message:
            step_builder.say(intro_id or "quest_check", intro_message, "", actor=actor)

        step_builder \
            .set_flag("sukutsu_quest_found", 0) \
            .set_flag(flag_name, 0) \
            .debug_log_quests()

        # C#側で利用可能なクエストをチェックし、最優先のクエストのインデックスを設定
        quest_ids = [quest.quest_id for quest in quests]
        step_builder.check_quests_for_dispatch(flag_name, quest_ids)

        # switch_flag用のケースリストを作成（インデックスベース）
        # index 0: fallback, index 1: 最初のクエスト, index 2: 2番目のクエスト, ...
        cases_list = [fallback_step]
        for quest in quests:
            cases_list.append(labels[quest.step_name])

        step_builder.switch_flag(flag_name, cases_list)

        return labels

    def build_quest_info_steps(
        self,
        infos: List[QuestInfoDefinition],
        actor: Union[str, 'DramaActor'],
        return_step: Union[str, 'DramaLabel'],
    ) -> Dict[str, 'DramaLabel']:
        """
        クエスト情報表示ステップを一括生成

        Args:
            infos: QuestInfoDefinitionのリスト
            actor: 発言者
            return_step: 戻り先ステップ

        Returns:
            {step_name: label} の辞書
        """
        labels = {}

        for info in infos:
            label = self.label(info.step_name)
            labels[info.step_name] = label

            step_builder = self.step(label)

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
        self,
        starts: List[QuestStartDefinition],
        actor: Union[str, 'DramaActor'],
        cancel_step: Union[str, 'DramaLabel'],
        end_step: Union[str, 'DramaLabel'],
    ) -> Dict[str, 'DramaLabel']:
        """
        直接開始可能なクエストのステップを一括生成

        Args:
            starts: QuestStartDefinitionのリスト
            actor: 発言者
            cancel_step: キャンセル時のジャンプ先
            end_step: 終了ステップ

        Returns:
            {step_name: label} の辞書
        """
        labels = {}

        for start in starts:
            info_label = self.label(start.info_step)
            start_label = self.label(start.start_step)
            labels[start.info_step] = info_label
            labels[start.start_step] = start_label

            # 情報表示ステップ
            step_builder = self.step(info_label)

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
            self.step(start_label) \
                .say_and_start_drama(start.start_message, start.drama_name, "sukutsu_arena_master") \
                .jump(end_step)

        return labels


class BattleSystemMixin:
    """
    バトルステージシステム関連のビルダーメソッド

    Provides:
    - build_battle_stages(): バトルステージシステムを構築
    """

    def build_battle_stages(
        self,
        stages: List[BattleStageDefinition],
        actor: Union[str, 'DramaActor'],
        entry_step: Union[str, 'DramaLabel'],
        cancel_step: Union[str, 'DramaLabel'],
        stage_flag: str = "sukutsu_arena_stage",
    ) -> Dict[int, 'DramaLabel']:
        """
        バトルステージシステムを自動生成

        Args:
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
                'prep': self.label(f"stage{stage.stage_num}_prep"),
                'start': self.label(f"battle_start_stage{stage.stage_num}"),
            }

        # エントリーステップ（最初のステージへの分岐チェーン）
        current_builder = self.step(entry_step)

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

            stage_builder = self.step(prep_label)

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
                self.step(start_label) \
                    .say(stage.sendoff_id or f"sendoff{stage.stage_num}",
                         stage.sendoff, "", actor=actor) \
                    .start_battle_and_end(stage.stage_id)
            else:
                self.step(start_label) \
                    .start_battle_and_end(stage.stage_id)

        return labels


class MenuMixin:
    """
    メニュー構築関連のビルダーメソッド

    Provides:
    - add_menu(): メニュー選択肢を追加
    """

    def add_menu(
        self,
        items: List[MenuItem],
        cancel: Union[str, 'DramaLabel'] = None,
    ) -> 'MenuMixin':
        """
        メニュー（選択肢リスト）を追加

        Args:
            items: MenuItemのリスト
            cancel: キャンセル時のジャンプ先

        Returns:
            self（チェーン用）
        """
        for item in items:
            if item.condition:
                self.choice_if(
                    item.jump_to,
                    item.text_jp,
                    item.condition,
                    item.text_en,
                    item.text_id
                )
            else:
                self.choice(
                    item.jump_to,
                    item.text_jp,
                    item.text_en,
                    item.text_id
                )

        if cancel:
            self.on_cancel(cancel)

        return self
