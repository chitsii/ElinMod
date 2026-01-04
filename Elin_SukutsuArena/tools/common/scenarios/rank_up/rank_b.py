"""
11_rank_up_B.md - Rank B 昇格試験『虚無の処刑人』
ヌルとの戦い - 感情と虚無の対決
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Rank

def define_rank_up_B(builder: DramaBuilder):
    """
    Rank B 昇格試験「虚無の処刑人」
    シナリオ: 11_rank_up_B.md
    """
    # アクター登録
    pc = builder.register_actor("pc", "あなた", "You")
    lily = builder.register_actor("sukutsu_receptionist", "リリィ", "Lily")
    balgas = builder.register_actor("sukutsu_arena_master", "バルガス", "Balgas")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_warning")
    choice1 = builder.label("choice1")
    react1_null = builder.label("react1_null")
    react1_fear = builder.label("react1_fear")
    react1_silent = builder.label("react1_silent")
    scene2 = builder.label("scene2_lily_advice")
    choice2 = builder.label("choice2")
    react2_survive = builder.label("react2_survive")
    react2_meaning = builder.label("react2_meaning")
    react2_nod = builder.label("react2_nod")
    battle_start = builder.label("battle_start")

    # ========================================
    # シーン1: 虚無の予兆
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_1", "（ロビーの空気が異様に重い。）", "", actor=pc) \
        .say("narr_2", "（バルガスは珍しく、酒瓶を手にせず、険しい表情で闘技場の門を見つめている。）", "", actor=pc) \
        .say("narr_3", "（リリィも、いつもの事務的な仮面の下に、微かな緊張を滲ませていた。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .focus_chara("sukutsu_arena_master") \
        .say("balgas_1", "……おい、闘技場の鴉。", "", actor=balgas) \
        .say("balgas_2", "お前はここまで、よく戦ってきた。だが、次の相手は……今までの敵とは次元が違う。", "", actor=balgas) \
        .say("balgas_3", "『虚無の処刑人ヌル』。", "", actor=balgas) \
        .say("balgas_4", "あいつは、このアリーナの『概念』そのものだ。感情も、意志も、魂すらも持たねえ。", "", actor=balgas) \
        .say("balgas_5", "ただひたすらに、『存在を無に還す』ことだけを目的に動く、生ける虚無だ。", "", actor=balgas) \
        .say("narr_4", "（彼は深く息を吐く。）", "", actor=pc) \
        .say("balgas_6", "……かつての英雄たち、カインを含めた俺の仲間たちも、あいつに飲み込まれて消えた。", "", actor=balgas) \
        .say("balgas_7", "俺たちが持っていた『意志』も、『哲学』も、全てあいつの『無』の前では意味を成さなかった。", "", actor=balgas)

    # プレイヤーの選択肢1
    builder.choice(react1_null, "どうすれば倒せる？", "", text_id="c1_null") \
           .choice(react1_fear, "……お前も恐れているのか", "", text_id="c1_fear") \
           .choice(react1_silent, "（無言で聞く）", "", text_id="c1_silent")

    # 選択肢反応1
    builder.step(react1_null) \
        .say("balgas_r1", "分からねえ。だが、お前なら……。お前が積み上げてきた『絆』が、鍵になるかもしれねえ。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_fear) \
        .say("balgas_r2", "……ああ。恐れてる。あいつは、俺が今まで信じてきた全てを否定する存在だ。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_silent) \
        .say("balgas_r3", "……まあ、黙って聞いててくれ。リリィからも話がある。", "", actor=balgas) \
        .jump(scene2)

    # ========================================
    # シーン2: リリィの忠告
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Lily_Seductive_Danger") \
        .focus_chara("sukutsu_receptionist") \
        .say("narr_5", "（リリィが近づいてくる。その目には、珍しく真剣な光が宿っている。）", "", actor=pc) \
        .say("lily_1", "……お客様。ヌルは、このアリーナが生み出した『究極の絶望』の結晶です。", "", actor=lily) \
        .say("lily_2", "あなたがどれほど強くなっても、どれほど技術を磨いても、『虚無』の前では全てが等しく無意味。", "", actor=lily) \
        .say("narr_6", "（彼女は、あなたの手を取る。）", "", actor=pc) \
        .say("lily_3", "でも……あなたには、私たちがいます。", "", actor=lily) \
        .say("lily_4", "バルガスさんの哲学、あなたが救った魂たち、そして……私の真名を知るあなた。", "", actor=lily) \
        .say("lily_5", "虚無に抗う唯一の方法は、『意味』を信じ続けることです。", "", actor=lily) \
        .say("lily_6", "あなたが今まで積み上げてきた全ての選択、全ての戦い……それが、あなたを虚無から守る盾になります。", "", actor=lily) \
        .say("narr_7", "（リリィは、あなたの額に軽く口づけをする。）", "", actor=pc) \
        .say("lily_7", "……行ってらっしゃい。そして、必ず戻ってきてください。", "", actor=lily)

    # プレイヤーの選択肢2
    builder.choice(react2_survive, "……生き残る。必ず", "", text_id="c2_survive") \
           .choice(react2_meaning, "意味を、信じる", "", text_id="c2_meaning") \
           .choice(react2_nod, "（無言で頷く）", "", text_id="c2_nod")

    # 選択肢反応2
    builder.step(react2_survive) \
        .say("lily_r4", "ええ。その言葉を信じていますよ。", "", actor=lily) \
        .jump(battle_start)

    builder.step(react2_meaning) \
        .say("lily_r5", "……ええ。それがあなたの、最強の武器です。", "", actor=lily) \
        .jump(battle_start)

    builder.step(react2_nod) \
        .say("lily_r6", "……無口ですが、その目は答えを語っていますね。", "", actor=lily) \
        .jump(battle_start)

    # ========================================
    # シーン3: 戦闘開始
    # ========================================
    builder.step(battle_start) \
        .play_bgm("BGM/Battle_Null_Assassin") \
        .say("narr_8", "（闘技場の門を潜ると、そこは無音の世界だった。）", "", actor=pc) \
        .say("narr_9", "（観客の声も、風の音も、自分の心臓の鼓動さえも、全てが消え去っている。）", "", actor=pc) \
        .shake() \
        .say("narr_10", "（中央に立つのは、輪郭すら曖昧な、黒い霧のような人型の影。）", "", actor=pc) \
        .say("narr_11", "（それは、こちらを見ているのか、見ていないのかすら分からない。ただ、その存在が放つ『虚無』の圧力が、魂を押し潰そうとしている。）", "", actor=pc) \
        .shake() \
        .say("obs_1", "（観客の声：「……始まるぞ。虚無の舞が」）", "", actor=pc) \
        .say("obs_2", "（観客の声：「賭けは『3ターン以内に精神崩壊』で」）", "", actor=pc) \
        .say("obs_3", "（観客の声：「いや、この新人は……少しは抗うだろう」）", "", actor=pc) \
        .start_battle(6, is_rank_up=True, master_id="sukutsu_arena_master") \
        .finish()


def add_rank_up_B_result_steps(builder: DramaBuilder, victory_label: str, defeat_label: str, return_label: str):
    """
    Rank B 昇格試験の勝利/敗北ステップを arena_master ビルダーに追加する

    Args:
        builder: arena_master の DramaBuilder インスタンス
        victory_label: 勝利ステップのラベル名
        defeat_label: 敗北ステップのラベル名
        return_label: 結果表示後にジャンプするラベル名
    """
    pc = "pc"
    lily = "sukutsu_receptionist"
    balgas = "sukutsu_arena_master"

    # ========================================
    # Rank B 昇格試験 勝利
    # ========================================
    builder.step(victory_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Emotional_Sacred_Triumph_Special") \
        .say("narr_v1", "（ヌルの体が霧のように消え去る瞬間、あなたの耳に、かすかに音が戻ってきた。）", "", actor=pc) \
        .say("narr_v2", "（それは、観客の歓声でも、嘲笑でもない。ただ、静かな沈黙の中に響く、あなた自身の心臓の鼓動。）", "", actor=pc) \
        .say("narr_v3", "（ロビーに戻ると、リリィが駆け寄ってきた。）", "", actor=pc) \
        .focus_chara("sukutsu_receptionist") \
        .say("lily_v1", "……おかえりなさい。", "", actor=lily) \
        .say("narr_v4", "（彼女の目には涙。サキュバスが、二度目の涙を流している。）", "", actor=pc) \
        .say("lily_v2", "あなたは……本当に、虚無を打ち破ったのですね。", "", actor=lily) \
        .say("lily_v3", "信じられません。このアリーナの歴史で、ヌルを倒した闘士は……あなたが初めてです。", "", actor=lily) \
        .focus_chara("sukutsu_arena_master") \
        .say("narr_v5", "（バルガスが、珍しく笑顔で近づいてくる。）", "", actor=pc) \
        .say("balgas_v1", "……ケッ、やりやがったな。", "", actor=balgas) \
        .say("balgas_v2", "お前は、カインが持っていた以上の……いや、俺たち全員が持っていなかった『何か』を持っている。", "", actor=balgas) \
        .say("balgas_v3", "今日からお前は、ただの『闘技場の鴉』じゃねえ。", "", actor=balgas) \
        .say("balgas_v4", "絶望の空を飛び越え、希望を掴み取る……『銀翼（Silver Wing）』だ。", "", actor=balgas) \
        .focus_chara("sukutsu_receptionist") \
        .say("lily_v4", "では、報酬の授与です。", "", actor=lily) \
        .say("lily_v5", "観客からの祝福……小さなコイン20枚とプラチナコイン10枚。それと、戦闘記録として特別な素材を一つ選んでいただけます。", "", actor=lily)

    # 報酬選択肢 (ラベル名に _b サフィックスを付けて衝突を回避)
    reward_ether_b = builder.label("reward_ether_b")
    reward_void_b = builder.label("reward_void_b")
    reward_mana_b = builder.label("reward_mana_b")
    reward_end_b = builder.label("reward_end_b")

    builder.choice(reward_ether_b, "エーテルの欠片を頼む", "", text_id="c_reward_ether_b") \
           .choice(reward_void_b, "虚無の結晶が欲しい", "", text_id="c_reward_void_b") \
           .choice(reward_mana_b, "魔力の結晶を選ぶ", "", text_id="c_reward_mana_b")

    builder.step(reward_ether_b) \
        .say("lily_rew1_b", "『エーテルの欠片×1』、記録いたしました。虚無を超えた証ですね。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"ether\"));") \
        .jump(reward_end_b)

    builder.step(reward_void_b) \
        .say("lily_rew2_b", "『虚無の結晶×1』、記録いたしました。……危険ですが、強力な素材です。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"void_crystal\"));") \
        .jump(reward_end_b)

    builder.step(reward_mana_b) \
        .say("lily_rew3_b", "『魔力の結晶×1』ですね。……安定の選択ですこと。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"gem_mana\"));") \
        .jump(reward_end_b)

    builder.step(reward_end_b) \
        .action("eval", param="for(int i=0; i<20; i++) { EClass.pc.Pick(ThingGen.Create(\"coin\")); } for(int i=0; i<10; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .say("lily_v6", "記録完了です。", "", actor=lily) \
        .say("lily_v7", "……あなたは今、このアリーナの頂点まであと僅かです。", "", actor=lily) \
        .say("lily_v8", "次は、グランドマスター・アスタロトとの決戦。……準備が整ったら、また声をかけてくださいね？", "", actor=lily) \
        .complete_quest("11_rank_up_B") \
        .set_flag(Keys.RANK, 6) \
        .mod_flag(Keys.REL_BALGAS, "+", 20) \
        .mod_flag(Keys.REL_LILY, "+", 20) \
        .say("sys_title", "【システム】称号『銀翼（Silver Wing）』を獲得しました。", "", actor=pc) \
        .action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] TODO: 称号付与処理 - 全ステータス+10%, 虚無耐性+50%\");") \
        .jump(return_label)

    # ========================================
    # Rank B 昇格試験 敗北
    # ========================================
    builder.step(defeat_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Lobby_Normal") \
        .focus_chara("sukutsu_receptionist") \
        .say("lily_d1", "……虚無に、飲み込まれてしまいましたね。", "", actor=lily) \
        .say("lily_d2", "でも、あなたはまだ生きています。それだけで、十分に奇跡です。", "", actor=lily) \
        .say("lily_d3", "準備が整ったら、また挑戦してください。私たちは、ここで待っていますから。", "", actor=lily) \
        .jump(return_label)
