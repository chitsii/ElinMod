"""
12_rank_up_A.md - Rank A 昇格試験『黄金の戦鬼』
影の自己との戦い - 自分自身を超える
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Rank, Actors, QuestIds
from reward_system import add_reward_choice, get_reward_tier_for_rank


def define_rank_up_A(builder: DramaBuilder):
    """
    Rank A 昇格試験「黄金の戦鬼」
    シナリオ: 12_rank_up_A.md

    観客の「注目」が生み出した影の自己と戦う
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")
    zek = builder.register_actor(Actors.ZEK, "ゼク", "Zek")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_shadow_warning")
    choice1 = builder.label("choice1")
    react1_shadow = builder.label("react1_shadow")
    react1_ready = builder.label("react1_ready")
    react1_silent = builder.label("react1_silent")
    scene2 = builder.label("scene2_zek_revelation")
    choice2 = builder.label("choice2")
    react2_understand = builder.label("react2_understand")
    react2_fear = builder.label("react2_fear")
    react2_nod = builder.label("react2_nod")
    scene3 = builder.label("scene3_lily_blessing")
    choice3 = builder.label("choice3")
    react3_promise = builder.label("react3_promise")
    react3_confident = builder.label("react3_confident")
    react3_hold = builder.label("react3_hold")
    battle_start = builder.label("battle_start")

    # ========================================
    # シーン1: 影の予兆
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_1", "（ロビーに足を踏み入れた瞬間、あなたは自分の影が妙に濃いことに気づく。）", "", actor=pc) \
        .say("narr_2", "（それは、松明の光に関係なく、まるで意志を持つかのように蠢いている。）", "", actor=pc) \
        .say("narr_3", "（バルガスが厳しい表情で近づいてくる。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .say("balgas_1", "……おい、銀翼。お前、自分の影をよく見てみろ。", "", actor=balgas) \
        .say("balgas_2", "観客どもの『注目』が、お前に集まりすぎたんだ。その結果、お前の影から……『もう一人のお前』が生まれようとしている。", "", actor=balgas) \
        .say("balgas_3", "『黄金の戦鬼』——それが、次の試練の名前だ。", "", actor=balgas) \
        .say("balgas_4", "お前が積み上げてきた全ての技術、全ての経験、全ての殺意……それを完璧にコピーした存在と戦うことになる。", "", actor=balgas) \
        .say("narr_4", "（バルガスは苦々しげに首を振る。）", "", actor=pc) \
        .say("balgas_5", "こいつは、ヌルとは違う意味で厄介だ。虚無には『意味』で対抗できた。だが、影はお前自身だ。", "", actor=balgas) \
        .say("balgas_6", "お前の強さも、弱さも、全て知っている。お前が次に何をするか、完璧に読んでくる。", "", actor=balgas)

    # プレイヤーの選択肢1
    builder.choice(react1_shadow, "自分自身と戦う……どうすれば勝てる？", "", text_id="c1_shadow") \
           .choice(react1_ready, "覚悟はできている", "", text_id="c1_ready") \
           .choice(react1_silent, "（無言で影を見つめる）", "", text_id="c1_silent")

    # 選択肢反応1
    builder.step(react1_shadow) \
        .say("balgas_r1", "……それは、俺にも分からねえ。だが、お前は今まで、いつも予想を裏切ってきた。それが、答えかもしれねえな。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_ready) \
        .say("balgas_r2", "……ハッ、その顔だ。その目を忘れるなよ。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_silent) \
        .say("balgas_r3", "……そうだ。よく見ておけ。あれが、お前の『可能性』の一つだ。", "", actor=balgas) \
        .jump(scene2)

    # ========================================
    # シーン2: ゼクの洞察
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Zek_Theme") \
        .say("narr_5", "（影の中から、ゼクが姿を現す。）", "", actor=pc) \
        .say("zek_1", "クク……影の自己との対決ですか。実に興味深い試練ですね。", "", actor=zek) \
        .say("zek_2", "あの『黄金の戦鬼』は、あなたの『現在』を完璧に写し取った鏡。技術、反射、経験……全てが同じです。", "", actor=zek) \
        .say("zek_3", "ですが、一つだけ違うものがある。", "", actor=zek) \
        .say("narr_6", "（ゼクは意味深に微笑む。）", "", actor=pc) \
        .say("zek_4", "影には『未来』がない。あなたが次の瞬間に何を選ぶか……その『可能性』だけは、影にはコピーできない。", "", actor=zek) \
        .say("zek_5", "あなたが今まで誰かを助け、誰かに助けられ、その度に『変化』してきたこと……それが、影との唯一の違いです。", "", actor=zek) \
        .say("zek_6", "……まあ、私としては、どちらが勝っても『最高の瞬間』を記録できるので、気楽に見物させてもらいますよ。", "", actor=zek)

    # プレイヤーの選択肢2
    builder.choice(react2_understand, "……変化し続けることが、答えか", "", text_id="c2_understand") \
           .choice(react2_fear, "自分自身を超えられるか……", "", text_id="c2_fear") \
           .choice(react2_nod, "（無言で頷く）", "", text_id="c2_nod")

    # 選択肢反応2
    builder.step(react2_understand) \
        .say("zek_r1", "ふふ、その通りです。過去の自分を超え続けること……それが、真の成長というものですから。", "", actor=zek) \
        .jump(scene3)

    builder.step(react2_fear) \
        .say("zek_r2", "クク、恐れるのは当然です。自分が自分の最大の敵になるのですから。……でも、それを乗り越えた時、あなたは本物になる。", "", actor=zek) \
        .jump(scene3)

    builder.step(react2_nod) \
        .say("zek_r3", "……無口ですが、覚悟は決まったようですね。期待していますよ。", "", actor=zek) \
        .jump(scene3)

    # ========================================
    # シーン3: リリィの祝福
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Lily_Tranquil") \
        .say("narr_7", "（リリィが静かに近づき、あなたの手を取る。）", "", actor=pc) \
        .say("lily_1", "……あなたの影は、確かに強い。あなたと同じだけの力を持っている。", "", actor=lily) \
        .say("lily_2", "でも、影には一つ、決定的に欠けているものがあります。", "", actor=lily) \
        .say("lily_3", "……それは、『繋がり』です。", "", actor=lily) \
        .say("lily_4", "あなたがバルガスさんから学んだ哲学、私と交わした言葉、ゼクとの駆け引き……それらは全て、あなたの『今』を形作っている。", "", actor=lily) \
        .say("lily_5", "影はあなたの『力』をコピーできても、あなたの『絆』まではコピーできません。", "", actor=lily) \
        .say("narr_8", "（リリィは、あなたの胸に手を当てる。）", "", actor=pc) \
        .say("lily_6", "ここに、私たちの想いがあります。……それを、忘れないでくださいね。", "", actor=lily)

    # プレイヤーの選択肢3
    builder.choice(react3_promise, "……必ず、勝って戻る", "", text_id="c3_promise") \
           .choice(react3_confident, "俺は、俺を超えてみせる", "", text_id="c3_confident") \
           .choice(react3_hold, "（リリィの手を握り返す）", "", text_id="c3_hold")

    # 選択肢反応3
    builder.step(react3_promise) \
        .say("lily_r4", "……その言葉、信じています。", "", actor=lily) \
        .jump(battle_start)

    builder.step(react3_confident) \
        .say("lily_r5", "ええ、あなたなら……きっと。", "", actor=lily) \
        .jump(battle_start)

    builder.step(react3_hold) \
        .say("lily_r6", "……あぁ、温かい。この温もりを、忘れないで。", "", actor=lily) \
        .jump(battle_start)

    # ========================================
    # シーン4: 戦闘開始
    # ========================================
    builder.step(battle_start) \
        .play_bgm("BGM/Battle_Shadow_Self") \
        .say("narr_9", "（闘技場の中央に足を踏み入れた瞬間、空気が凍りつく。）", "", actor=pc) \
        .say("narr_10", "（そこに立っていたのは、まさに鏡像。あなたと寸分違わぬ姿をした、黄金色に輝く戦士。）", "", actor=pc) \
        .shake() \
        .say("narr_11", "（その瞳は、あなたと同じ光を湛えながらも、どこか虚ろだ。）", "", actor=pc) \
        .say("narr_12", "（影が剣を構える。その動作は、あなたがこれから行おうとした動作と、寸分違わず一致していた。）", "", actor=pc) \
        .shake() \
        .say("narr_13", "（観客席から、異様な熱狂が渦巻く——自分自身との決闘。これほど『面白い』見世物は、アリーナの歴史にも稀だろう。）", "", actor=pc) \
        .start_battle_by_stage("rank_a_trial", master_id="sukutsu_arena_master") \
        .finish()


def add_rank_up_A_result_steps(builder: DramaBuilder, victory_label: str, defeat_label: str, return_label: str):
    """
    Rank A 昇格試験の勝利/敗北ステップを arena_master ビルダーに追加する

    Args:
        builder: arena_master の DramaBuilder インスタンス
        victory_label: 勝利ステップのラベル名
        defeat_label: 敗北ステップのラベル名
        return_label: 結果表示後にジャンプするラベル名
    """
    pc = Actors.PC
    lily = Actors.LILY
    balgas = Actors.BALGAS
    zek = Actors.ZEK

    # ========================================
    # Rank A 昇格試験 勝利
    # ========================================
    after_reward_label_a = f"{victory_label}_after_reward"

    builder.step(victory_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Emotional_Sacred_Triumph_Special") \
        .say("narr_v1", "（影が砕け散る瞬間、その破片はあなたの体に吸い込まれていった。）", "", actor=pc) \
        .say("narr_v2", "（それは、あなたが自分自身を超えた証。）", "", actor=pc) \
        .say("narr_v3", "（ロビーに戻ると、三人があなたを待っていた。）", "", actor=pc) \
        .say("balgas_v1", "……ケッ、やりやがったな。自分自身を超えるってのは、口で言うほど簡単じゃねえ。", "", actor=balgas) \
        .say("lily_v1", "……おかえりなさい。今日からあなたは『黄金の戦鬼（Golden War Demon）』です。", "", actor=lily) \
        .say("lily_v2", "報酬を選んでください。", "", actor=lily) \
        .complete_quest(QuestIds.RANK_UP_A) \
        .mod_flag(Keys.REL_BALGAS, "+", 15) \
        .mod_flag(Keys.REL_LILY, "+", 15) \
        .mod_flag(Keys.REL_ZEK, "+", 10)

    # 3択報酬選択
    add_reward_choice(
        builder,
        tier=get_reward_tier_for_rank("A"),
        choice_label_prefix="rup_a_reward",
        after_reward_label=after_reward_label_a,
        lily_actor=lily,
        pc_actor=pc
    )

    builder.step(after_reward_label_a) \
        .say("sys_title", "【システム】称号『黄金の戦鬼（Golden War Demon）』を獲得しました。筋力+5、魔力+5、回避+5、PV+5 の加護を得た！", "") \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantRankABonus();") \
        .set_flag(Keys.RANK, 7)

    # 最終選択肢
    final_next_a = builder.label("final_next_a")
    final_rest_a = builder.label("final_rest_a")
    final_silent_a = builder.label("final_silent_a")

    builder.choice(final_next_a, "次は……アスタロトか", "", text_id="c_final_next_a") \
           .choice(final_rest_a, "少し、休ませてくれ", "", text_id="c_final_rest_a") \
           .choice(final_silent_a, "（無言で頷く）", "", text_id="c_final_silent_a")

    builder.step(final_next_a) \
        .say("lily_f1_a", "ええ。……その前に、バルガスさんとの『最後の試練』があります。準備ができたら、声をかけてくださいね。", "", actor=lily) \
        .jump(return_label)

    builder.step(final_rest_a) \
        .say("lily_f2_a", "もちろんです。十分に休んでください。……次の戦いは、今までで最も過酷なものになりますから。", "", actor=lily) \
        .jump(return_label)

    builder.step(final_silent_a) \
        .say("lily_f3_a", "……お疲れ様でした。ゆっくりなさってください。", "", actor=lily) \
        .jump(return_label)

    # ========================================
    # Rank A 昇格試験 敗北
    # ========================================
    builder.step(defeat_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("lily_d1", "……影に、飲み込まれてしまいましたね。", "", actor=lily) \
        .say("lily_d2", "でも、大丈夫です。影はあなた自身……いつか必ず、超えられます。", "", actor=lily) \
        .say("lily_d3", "準備が整ったら、また挑戦してください。私たちは、いつでもここにいます。", "", actor=lily) \
        .jump(return_label)
