
from typing import Dict, List, Tuple, Union
from drama_builder import DramaBuilder, DramaActor


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
        relations: Dict[str, int] = None,
        flags: Dict[str, int] = None
    ) -> 'ArenaDramaBuilder':
        """
        クエスト完了、関係値更新、フラグ設定を一括処理

        Args:
            quest_id: 完了するクエストID
            relations: 関係値の変更 {フラグキー: 変更量}
                       例: {Keys.REL_LILY: 10, Keys.REL_ZEK: -5}
            flags: 設定するフラグ {フラグキー: 値}

        Example:
            builder.step(ending) \\
                .say("thanks", "ありがとう！", actor=lily) \\
                .complete_quest_with_rewards(
                    QuestIds.LILY_EXP,
                    relations={Keys.REL_LILY: 10}
                ) \\
                .finish()
        """
        self.complete_quest(quest_id)

        if relations:
            for flag_key, value in relations.items():
                if value >= 0:
                    self.mod_flag(flag_key, "+", value)
                else:
                    self.mod_flag(flag_key, "-", abs(value))

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
