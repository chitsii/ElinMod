
from drama_builder import DramaBuilder

class ArenaDramaBuilder(DramaBuilder):
    """
    アリーナMod専用の拡張DramaBuilder

    C#側のAPI呼び出しをラップし、eval文字列の直接記述によるミスを防ぐ。
    """

    def show_rank_info_log(self) -> 'ArenaDramaBuilder':
        """
        ランク情報をログウィンドウに表示する
        """
        script = "Elin_SukutsuArena.ArenaManager.ShowRankInfoLog();"
        return self.action("eval", param=script)

    def start_drama(self, drama_name: str) -> 'ArenaDramaBuilder':
        """
        別のドラマを開始する

        Args:
            drama_name: ドラマ名（シート名、例: "drama_rank_up_game_01"）
        """
        # 複雑なeval文字列を避けるため、アクションを分割する

        # 1. 開始ログ
        self.action("eval", param=f"UnityEngine.Debug.Log(\"[SukutsuArena] Pre-invoke StartDrama: {drama_name}\");")

        # 2. メソッド呼び出し (直接呼び出しに戻す)
        # StartBattleが機能していたため、名前空間の問題ではない可能性が高い。
        # 引用符のエスケープに注意: "drama_name"
        script = f"Elin_SukutsuArena.ArenaManager.StartDrama(\"{drama_name}\");"
        self.action("eval", param=script)

        # 3. 完了ログ - これが表示されれば呼び出し自体は成功している
        self.action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] Post-invoke StartDrama\");")

        return self

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
        # C#側で一括処理
        script = f"Elin_SukutsuArena.ArenaManager.SayAndStartDrama(\"{actor_id}\", \"{message}\", \"{drama_name}\");"
        return self.action("eval", param=script)

    def start_battle_by_stage(self, stage_id: str, master_id: str = None) -> 'ArenaDramaBuilder':
        """
        ステージIDを指定して戦闘を開始する

        Args:
            stage_id: ステージID（例: "rank_g_trial", "stage_1", "debug_weak"）
            master_id: アリーナマスターのキャラクターID（省略時は tg を使用）

        Note:
            ステージ定義は battle_stages.json から読み込まれます。
            JSON内の敵設定、BGM、報酬が自動適用されます。
        """
        if master_id:
            script = f"Elin_SukutsuArena.ArenaManager.StartBattleByStage(\"{stage_id}\", \"{master_id}\");"
        else:
            script = f"Elin_SukutsuArena.ArenaManager.StartBattleByStage(\"{stage_id}\", tg);"
        return self.action("eval", param=script)
