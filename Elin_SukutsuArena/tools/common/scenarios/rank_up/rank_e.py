"""
06_1_rank_up_03.md - Rank E 昇格試験『鉄屑の慟哭』
カインとの戦い
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Rank, Actors, QuestIds

def define_rank_up_E(builder: DramaBuilder):
    """
    Rank E 昇格試験「鉄屑の慟哭」
    シナリオ: 06_1_rank_up_03.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_night")
    choice1 = builder.label("choice1")
    react1_hard = builder.label("react1_hard")
    react1_kain = builder.label("react1_kain")
    react1_silent = builder.label("react1_silent")
    scene2 = builder.label("scene2_declaration")
    choice2 = builder.label("choice2")
    react2_accept = builder.label("react2_accept")
    react2_saved = builder.label("react2_saved")
    react2_nod = builder.label("react2_nod")
    battle_start = builder.label("battle_start")

    # ========================================
    # シーン1: 酒の切れた夜に
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_1", "（ロビーの喧騒が嘘のように静まり返った深夜。）", "", actor=pc) \
        .say("narr_2", "（バルガスはいつもの酒瓶を持たず、代わりに血錆にまみれた「古い戦士の兜」を無造作に眺めていた。）", "", actor=pc) \
        .say("narr_3", "（彼がこれほどまでに静かなのは、あなたがここへ来てから初めてのことだった。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_1", "……来たか。", "", actor=balgas) \
        .say("narr_4", "（彼は兜を撫でながら、低く掠れた声で話し始める。）", "", actor=pc) \
        .say("balgas_2", "おい、新入り。お前は『鉄』がなぜ錆びるか知ってるか？手入れを怠るからじゃねえ。……持ち主の心が折れた時、鉄も一緒に死ぬんだよ。", "", actor=balgas) \
        .say("balgas_3", "かつて俺と一緒に地獄を這いずり回った相棒がいた。名はカイン。俺たちは『鉄の意志』を掲げてこのアリーナに挑んだが……あいつは、グランドマスターの影に触れ、魂をこの異次元の『錆』に食い尽くされた。", "", actor=balgas) \
        .say("narr_5", "（彼は兜を床に置き、深く息を吐く。）", "", actor=pc) \
        .say("balgas_4", "あいつは……強かった。だが、守るべきものを失って、壊れちまった。……俺は、あいつを救えなかった。", "", actor=balgas)

    # プレイヤーの選択肢
    builder.choice(react1_hard, "……辛い話だな", "", text_id="c1_hard") \
           .choice(react1_kain, "カインは今どうなっている？", "", text_id="c1_kain") \
           .choice(react1_silent, "（無言で聞く）", "", text_id="c1_silent")

    # 選択肢反応
    builder.step(react1_hard) \
        .say("balgas_r1", "辛い？ ……ああ、そうだな。だが、それがこのアリーナの現実だ。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_kain) \
        .say("balgas_r2", "……あいつは、この場所の『記憶』になっちまった。お前の次の相手だ。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_silent) \
        .say("balgas_r3", "……まあ、黙って聞いててくれ。続きがある。", "", actor=balgas) \
        .jump(scene2)

    # ========================================
    # シーン2: 因縁の宣告
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Emotional_Sorrow") \
        .say("narr_6", "（バルガスは兜を床に転がすと、あなたを射抜くような鋭い視線で立ち上がった。）", "", actor=pc) \
        .say("balgas_5", "次のRank E……『鉄屑』への試験。相手は、そのカインの成れの果てだ。", "", actor=balgas) \
        .say("balgas_6", "アリーナの記憶が具現化した、心も言葉も持たねえ『錆びついた英雄（ラスティ・ヒーロー）』。", "", actor=balgas) \
        .say("narr_7", "（彼は拳を握りしめ、わずかに震える声で続ける。）", "", actor=pc) \
        .say("balgas_7", "あいつを倒せば、お前は晴れて『鉄屑』だ。だが、もし負ければ……お前もあいつの一部として、永遠にこの床を磨き続けることになる。", "", actor=balgas) \
        .say("balgas_8", "……いいか、これは俺の我儘だ。あいつを……あの錆びついた悪夢を、終わらせてやってくれ。", "", actor=balgas)

    # プレイヤーの選択肢
    builder.choice(react2_accept, "分かった。任せてくれ", "", text_id="c2_accept") \
           .choice(react2_saved, "カインを倒せば、彼は救われるのか？", "", text_id="c2_saved") \
           .choice(react2_nod, "（無言で頷く）", "", text_id="c2_nod")

    # 選択肢反応
    builder.step(react2_accept) \
        .say("balgas_r4", "……ありがよ。お前なら、やってくれると思ってた。", "", actor=balgas) \
        .jump(battle_start)

    builder.step(react2_saved) \
        .say("balgas_r5", "……ああ。この地獄から解放される。それが俺にできる、最後の友情だ。", "", actor=balgas) \
        .jump(battle_start)

    builder.step(react2_nod) \
        .say("balgas_r6", "……頼んだぜ。", "", actor=balgas) \
        .jump(battle_start)

    # ========================================
    # シーン3: 戦闘開始
    # ========================================
    builder.step(battle_start) \
        .play_bgm("BGM/Battle_Kain_Requiem") \
        .say("narr_8", "（闘技場の門を潜ると、そこはいつもの砂地ではなく、無数の折れた剣と壊れた鎧が積み上がった「武具の墓場」へと変貌していた。）", "", actor=pc) \
        .shake() \
        .say("narr_9", "（中央に立つのは、全身から赤黒い錆を滴らせ、顔のない兜から青い炎を揺らめかせる一人の騎士。）", "", actor=pc) \
        .say("narr_10", "（騎士は巨大な錆びた剣を地に突き立て、ゆっくりと頭を上げる。）", "", actor=pc) \
        .shake() \
        .start_battle_by_stage("rank_e_trial", master_id="sukutsu_arena_master") \
        .finish()


def add_rank_up_E_result_steps(builder: DramaBuilder, victory_label: str, defeat_label: str, return_label: str):
    """
    Rank E 昇格試験の勝利/敗北ステップを arena_master ビルダーに追加する

    Args:
        builder: arena_master の DramaBuilder インスタンス
        victory_label: 勝利ステップのラベル名
        defeat_label: 敗北ステップのラベル名
        return_label: 結果表示後にジャンプするラベル名
    """
    pc = Actors.PC
    lily = Actors.LILY
    balgas = Actors.BALGAS

    # ========================================
    # Rank E 昇格試験 勝利
    # ========================================
    builder.step(victory_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Emotional_Sorrow_2") \
        .say("narr_v1", "（カインの体が粒子となって崩れ去る瞬間、騎士は一瞬だけバルガスの方向を見つめ、静かに首を振ったように見えた。）", "", actor=pc) \
        .say("narr_v2", "（静寂の中、ロビーに戻ると、バルガスが背を向けたまま待っている。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_v1", "……終わったか。", "", actor=balgas) \
        .say("narr_v3", "（彼はゆっくりと振り返る。その目には、涙の跡。）", "", actor=pc) \
        .say("balgas_v2", "あの野郎、最期まで意地っ張りな面をしてやがったな。", "", actor=balgas) \
        .say("narr_v4", "（彼は拳でこっそりと目を拭う。）", "", actor=pc) \
        .say("balgas_v3", "……ありがよ。今日からお前は、ただの『泥犬』じゃねえ。何度叩かれても折れねえ、鈍く輝く『鉄屑（Iron Scrap）』だ。", "", actor=balgas) \
        .say("balgas_v4", "……お前は、カインが持っていた以上の、本物の『鋼の心』を持った戦士だ。", "", actor=balgas) \
        .focus_chara(Actors.LILY) \
        .say("lily_v1", "お疲れ様でした。カインさんの魂の一部……回収いたしました。", "", actor=lily) \
        .say("lily_v2", "バルガスさんが珍しく涙ぐんでいたのは見なかったことにしてあげますから、報酬の授与をさせていただきます。", "", actor=lily) \
        .say("lily_v3", "報酬として、小さなメダル2枚、エーテル抗体1本、媚薬1本をお渡しします。", "", actor=lily) \
        .action("eval", param="for(int i=0; i<2; i++) { EClass.pc.Pick(ThingGen.Create(\"medal\")); } EClass.pc.Pick(ThingGen.Create(\"1165\")); EClass.pc.Pick(ThingGen.Create(\"lovepotion\"));") \
        .complete_quest(QuestIds.RANK_UP_E) \
        .set_flag(Keys.RANK, 3) \
        .mod_flag(Keys.REL_BALGAS, "+", 15) \
        .say("sys_title", "【システム】称号『鉄屑（Iron Scrap）』を獲得しました。筋力+3、PV+5 の加護を得た！", "") \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantRankEBonus();") \
        .finish()

    # ========================================
    # Rank E 昇格試験 敗北
    # ========================================
    builder.step(defeat_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_d1", "……チッ。終わったか。", "", actor=balgas) \
        .say("balgas_d2", "お前も、あいつと同じ錆の一部になっちまったか。", "", actor=balgas) \
        .finish()
