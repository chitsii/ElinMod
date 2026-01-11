
from typing import Dict, List, Tuple, Union, TYPE_CHECKING
from drama_builder import DramaBuilder, DramaActor
from flag_definitions import Keys

if TYPE_CHECKING:
    from rewards import Reward, RankReward


class ArenaDramaBuilder(DramaBuilder):
    """
    アリーナMod専用の拡張DramaBuilder

    C#側のAPI呼び出しをラップし、eval文字列の直接記述によるミスを防ぐ。

    高レベルAPI（推奨）:
    - start_quest_drama(): クエスト開始 + ドラマ遷移 + 終了
    - start_battle_and_end(): バトル開始 + 終了
    - complete_quest_with_rewards(): クエスト完了 + 関係値更新

    低レベルAPI（内部用、_プレフィックス）:
    - _start_drama(): ドラマ遷移のみ（finish()が別途必要）
    - _start_battle_by_stage(): バトル開始のみ（finish()が別途必要）
    """

    def show_rank_info_log(self) -> 'ArenaDramaBuilder':
        """
        ランク情報をログウィンドウに表示する
        """
        script = "Elin_SukutsuArena.ArenaManager.ShowRankInfoLog();"
        return self.action("eval", param=script)

    # =========================================================================
    # 低レベルAPI（内部用）
    # =========================================================================

    def _start_drama(self, drama_name: str) -> 'ArenaDramaBuilder':
        """
        [内部用] 別のドラマを開始する

        注意: このメソッドの後にfinish()が必要です。
        通常は start_quest_drama() を使用してください。

        Args:
            drama_name: ドラマ名（シート名、例: "drama_rank_up_game_01"）
        """
        # 1. 開始ログ
        self.action("eval", param=f"UnityEngine.Debug.Log(\"[SukutsuArena] Pre-invoke StartDrama: {drama_name}\");")

        # 2. メソッド呼び出し
        script = f"Elin_SukutsuArena.ArenaManager.StartDrama(\"{drama_name}\");"
        self.action("eval", param=script)

        # 3. 完了ログ
        self.action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] Post-invoke StartDrama\");")

        return self

    def _start_battle_by_stage(self, stage_id: str, master_id: str = None) -> 'ArenaDramaBuilder':
        """
        [内部用] ステージIDを指定して戦闘を開始する

        注意: このメソッドの後にfinish()が必要です。
        通常は start_battle_and_end() を使用してください。

        Args:
            stage_id: ステージID（例: "rank_g_trial", "stage_1", "debug_weak"）
            master_id: アリーナマスターのキャラクターID（省略時は tg を使用）
        """
        if master_id:
            script = f"Elin_SukutsuArena.ArenaManager.StartBattleByStage(\"{stage_id}\", \"{master_id}\");"
        else:
            script = f"Elin_SukutsuArena.ArenaManager.StartBattleByStage(\"{stage_id}\", tg);"
        return self.action("eval", param=script)

    # =========================================================================
    # 高レベルAPI（推奨）
    # =========================================================================

    def start_quest_drama(self, quest_id: str, drama_name: str) -> 'ArenaDramaBuilder':
        """
        クエストを開始し、対応するドラマを再生して終了

        これは以下の操作を一括で行う安全なAPI:
        1. start_quest(quest_id)
        2. _start_drama(drama_name)
        3. finish()

        Args:
            quest_id: クエストID（例: QuestIds.ZEK_INTRO）
            drama_name: ドラマ名（例: DramaNames.ZEK_INTRO）

        Example:
            builder.step(start_zek_intro) \\
                .start_quest_drama(QuestIds.ZEK_INTRO, DramaNames.ZEK_INTRO)
        """
        self.start_quest(quest_id)
        self._start_drama(drama_name)
        self.finish()
        return self

    def start_battle_and_end(self, stage_id: str, master_id: str = None) -> 'ArenaDramaBuilder':
        """
        バトルを開始してドラマを終了

        これは以下の操作を一括で行う安全なAPI:
        1. _start_battle_by_stage(stage_id, master_id)
        2. finish()

        Args:
            stage_id: ステージID（例: "rank_g_trial"）
            master_id: アリーナマスターのキャラクターID（省略時は tg を使用）

        Example:
            builder.step(battle) \\
                .say("master1", "さあ、戦いだ！", actor=master) \\
                .start_battle_and_end("rank_g_trial")
        """
        self._start_battle_by_stage(stage_id, master_id)
        self.finish()
        return self

    def complete_quest_with_rewards(
        self,
        quest_id: str,
        flags: Dict[str, int] = None
    ) -> 'ArenaDramaBuilder':
        """
        クエスト完了、フラグ設定を一括処理

        Args:
            quest_id: 完了するクエストID
            flags: 設定するフラグ {フラグキー: 値}

        Example:
            builder.step(ending) \\
                .say("thanks", "ありがとう！", actor=lily) \\
                .complete_quest_with_rewards(QuestIds.LILY_EXP) \\
                .finish()
        """
        self.complete_quest(quest_id)

        if flags:
            for flag_key, value in flags.items():
                self.set_flag(flag_key, value)

        return self

    def dramatic_scene(
        self,
        actor: Union[str, DramaActor],
        lines: List[Tuple[str, str, str]],
        bgm: str = None,
        shake: bool = False,
        focus: bool = True
    ) -> 'ArenaDramaBuilder':
        """
        演出付きシーン（BGM + フォーカス + 連続台詞）を一括設定

        Args:
            actor: 発言者のアクター
            lines: 台詞リスト [(text_id, text_jp, text_en), ...]
            bgm: 再生するBGM ID（省略可）
            shake: 画面を揺らすか
            focus: アクターにフォーカスするか

        Example:
            builder.step(dramatic_moment) \\
                .dramatic_scene(
                    balgas,
                    [
                        ("b1", "来たか……", "So you came..."),
                        ("b2", "待っていたぞ。", "I've been waiting."),
                    ],
                    bgm="BGM/Tension_Rising",
                    shake=True
                )
        """
        if bgm:
            self.play_bgm(bgm)

        if shake:
            self.shake()

        if focus:
            actor_key = actor.key if isinstance(actor, DramaActor) else actor
            self.focus_chara(actor_key)

        for text_id, text_jp, text_en in lines:
            self.say(text_id, text_jp, text_en, actor=actor)

        return self

    # =========================================================================
    # 後方互換性のためのエイリアス（非推奨）
    # =========================================================================

    def start_drama(self, drama_name: str) -> 'ArenaDramaBuilder':
        """
        [非推奨] _start_drama のエイリアス

        警告: このメソッドの後にfinish()が必要です。
        代わりに start_quest_drama() を使用してください。
        """
        return self._start_drama(drama_name)

    def start_battle_by_stage(self, stage_id: str, master_id: str = None) -> 'ArenaDramaBuilder':
        """
        [非推奨] _start_battle_by_stage のエイリアス

        警告: このメソッドの後にfinish()が必要です。
        代わりに start_battle_and_end() を使用してください。
        """
        return self._start_battle_by_stage(stage_id, master_id)

    def say_and_start_drama(self, message: str, drama_name: str, actor_id: str = "sukutsu_arena_master") -> 'ArenaDramaBuilder':
        """
        メッセージを表示してからドラマを開始する

        重要: CWLのsayアクション後にevalを実行すると失敗することがあるため、
        C#側でメッセージ表示とドラマ開始を一括で行う。

        Args:
            message: 表示するメッセージ
            drama_name: 開始するドラマ名
            actor_id: 発言者のキャラクターID（デフォルト: アリーナマスター）
        """
        script = f"Elin_SukutsuArena.ArenaManager.SayAndStartDrama(\"{actor_id}\", \"{message}\", \"{drama_name}\");"
        return self.action("eval", param=script)

    # =========================================================================
    # 報酬システムAPI
    # =========================================================================

    def grant_reward(
        self,
        reward: 'Reward',
        actor: Union[str, DramaActor] = None,
        text_id_prefix: str = "reward"
    ) -> 'ArenaDramaBuilder':
        """
        汎用報酬付与API

        Args:
            reward: Reward定義
            actor: メッセージの発言者（省略時はメッセージなし）
            text_id_prefix: text_idのプレフィックス

        処理順序:
        1. NPCメッセージ（あれば）
        2. アイテム付与
        3. バフ付与
        4. フラグ設定
        5. システムメッセージ（あれば）
        """
        # 1. NPCメッセージ
        if reward.message_jp and actor:
            self.say(f"{text_id_prefix}_msg", reward.message_jp, reward.message_en, actor=actor)

        # 2. アイテム付与
        if reward.items:
            self._grant_items(reward.items)

        # 3. バフ付与
        if reward.buff_method:
            script = f"Elin_SukutsuArena.ArenaManager.{reward.buff_method}();"
            self.action("eval", param=script)

        # 4. フラグ設定
        self._apply_flags(reward.flags)

        # 5. システムメッセージ
        if reward.system_message_jp:
            self.say(f"{text_id_prefix}_sys", reward.system_message_jp, reward.system_message_en)

        return self

    def grant_rank_reward(
        self,
        rank: str,
        actor: Union[str, DramaActor] = None
    ) -> 'ArenaDramaBuilder':
        """
        ランク報酬を付与し、クエスト完了とランク設定も行う

        Args:
            rank: ランク（"G", "F", "E", "D", "C", "B", "A"）
            actor: メッセージの発言者

        処理順序:
        1. アイテム付与
        2. クエスト完了
        3. ランク設定
        4. システムメッセージ
        5. バフ付与
        """
        from rewards import RANK_REWARDS

        rank_upper = rank.upper()
        if rank_upper not in RANK_REWARDS:
            raise ValueError(f"Unknown rank: {rank}")

        reward = RANK_REWARDS[rank_upper]
        text_id_prefix = f"rup_{rank.lower()}"

        # 1. NPCメッセージ
        if reward.message_jp and actor:
            self.say(f"{text_id_prefix}_msg", reward.message_jp, reward.message_en, actor=actor)

        # 2. アイテム付与
        if reward.items:
            self._grant_items(reward.items)

        # 3. クエスト完了
        if reward.quest_id:
            self.complete_quest(reward.quest_id)

        # 4. ランク設定
        if reward.rank_value > 0:
            self.set_flag(Keys.RANK, reward.rank_value)

        # 5. システムメッセージ
        if reward.system_message_jp:
            self.say(f"{text_id_prefix}_sys", reward.system_message_jp, reward.system_message_en)

        # 6. バフ付与（システムメッセージの後）
        if reward.buff_method:
            script = f"Elin_SukutsuArena.ArenaManager.{reward.buff_method}();"
            self.action("eval", param=script)

        return self

    def grant_quest_reward(
        self,
        quest_key: str,
        actor: Union[str, DramaActor] = None
    ) -> 'ArenaDramaBuilder':
        """
        クエスト報酬を付与

        Args:
            quest_key: クエストキー（QUEST_REWARDSのキー）
            actor: メッセージの発言者
        """
        from rewards import QUEST_REWARDS

        if quest_key not in QUEST_REWARDS:
            raise ValueError(f"Unknown quest reward key: {quest_key}")

        reward = QUEST_REWARDS[quest_key]
        return self.grant_reward(reward, actor, f"qr_{quest_key}")

    # =========================================================================
    # 内部ヘルパーメソッド
    # =========================================================================

    def _grant_items(self, items: list) -> 'ArenaDramaBuilder':
        """
        アイテムリストを付与

        Args:
            items: RewardItemのリスト
        """
        # 効率的なアイテム生成コードを生成
        # 同じアイテムは1つのforループでまとめる
        item_counts = {}
        for item in items:
            if item.item_id not in item_counts:
                item_counts[item.item_id] = 0
            item_counts[item.item_id] += item.count

        # C#コード生成
        parts = []
        for item_id, count in item_counts.items():
            if count == 1:
                parts.append(f'EClass.pc.Pick(ThingGen.Create("{item_id}"));')
            else:
                parts.append(f'for(int i=0; i<{count}; i++) {{ EClass.pc.Pick(ThingGen.Create("{item_id}")); }}')

        script = " ".join(parts)
        return self.action("eval", param=script)

    def _apply_flags(self, flags: Dict[str, int]) -> 'ArenaDramaBuilder':
        """
        フラグを設定

        Args:
            flags: {フラグキー: 値}
        """
        if not flags:
            return self

        for flag_key, value in flags.items():
            self.set_flag(flag_key, value)

        return self
