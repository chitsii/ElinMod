"""
09_balgas_training.md - 戦士の哲学：鉄を打つ鉄
バルガスの特別訓練とRank C昇格への道
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, QuestIds

def define_balgas_training(builder: DramaBuilder):
    """
    バルガスの訓練
    シナリオ: 09_balgas_training.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_question")
    choice1 = builder.label("choice1")
    react1_philosophy = builder.label("react1_philosophy")
    react1_survive = builder.label("react1_survive")
    react1_silent = builder.label("react1_silent")
    scene2 = builder.label("scene2_invitation")
    choice2 = builder.label("choice2")
    react2_accept = builder.label("react2_accept")
    react2_death = builder.label("react2_death")
    react2_nod = builder.label("react2_nod")
    scene3 = builder.label("scene3_combat")
    scene4 = builder.label("scene4_transmission")
    reward_choice = builder.label("reward_choice")
    reward_stone = builder.label("reward_stone")
    reward_steel = builder.label("reward_steel")
    reward_bone = builder.label("reward_bone")
    reward_end = builder.label("reward_end")
    final_choice = builder.label("final_choice")
    final_thanks = builder.label("final_thanks")
    final_again = builder.label("final_again")
    final_nod = builder.label("final_nod")
    ending = builder.label("ending")

    # ========================================
    # シーン1: 酒場に響く「問い」
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_1", "（ロビーの隅、いつもの酒瓶を横に置き、バルガスが自慢の大剣を丁寧に研いでいる。）", "", actor=pc) \
        .say("narr_2", "（研石が剣を研ぐ規則的な音が、静まり返ったロビーに響く。）", "", actor=pc) \
        .say("narr_3", "（あなたが近づくと、彼は研石を止め、濁った、しかし鋭い眼光を向けた。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_1", "……おい、銅貨稼ぎ。最近の戦いぶり、悪かねえ。", "", actor=balgas) \
        .say("balgas_2", "だがな、今のままじゃランクCの壁……あそこに巣食う『本当のバケモノ』どもに、鼻歌交じりで解体されるのがオチだ。", "", actor=balgas) \
        .say("narr_4", "（彼は研石を置き、腕を組む。）", "", actor=pc) \
        .say("balgas_3", "お前には『技術』がある。だが、『哲学』がねえ。", "", actor=balgas) \
        .say("balgas_4", "……剣を振る時、お前は何を考えてる？ 敵のHPか？ 次に飲むポーションの種類か？", "", actor=balgas) \
        .say("balgas_5", "そんなもんじゃねえ。戦士が最後に頼るのは、己の魂に刻んだ一文字の『理（ことわり）』だ。", "", actor=balgas)

    # プレイヤーの選択肢1
    builder.choice(react1_philosophy, "哲学……？", "", text_id="c1_philosophy") \
           .choice(react1_survive, "俺の哲学は、生き残ることだ", "", text_id="c1_survive") \
           .choice(react1_silent, "（無言で聞く）", "", text_id="c1_silent")

    # 選択肢反応1
    builder.step(react1_philosophy) \
        .say("balgas_r1", "ああ、哲学だ。お前が何のために剣を振るのか、その答えだ。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_survive) \
        .say("balgas_r2", "……ハッ、悪くねえ。だが、それだけじゃまだ足りねえ。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_silent) \
        .say("balgas_r3", "……まあ、黙って聞いててくれ。続きがある。", "", actor=balgas) \
        .jump(scene2)

    # ========================================
    # シーン2: 特設訓練場への誘い
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Ominous_Suspense_01") \
        .say("narr_5", "（バルガスは重い腰を上げ、闘技場の中心ではなく、さらに地下深くへと続く「封印された練習場」を指差した。）", "", actor=pc) \
        .say("balgas_6", "来い。今日はリリィの事務仕事じゃねえ。俺が直接、そのなまくらな魂を叩き直してやる。", "", actor=balgas) \
        .say("balgas_7", "……死んでも文句は言うなよ。地獄に落ちてから、俺の愚痴を肴に飲め。", "", actor=balgas) \
        .say("narr_6", "（リリィが受付から顔を上げ、クスクスと笑う。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_1", "……ふふ、バルガスさんがここまでやるなんて珍しい。", "", actor=lily) \
        .say("lily_2", "お客様、これは特別な『授業料』が必要かもしれませんね？", "", actor=lily) \
        .say("lily_3", "あ、ご心配なく。お代は、あなたがそこで流す『美しい血の雫』で十分ですから。", "", actor=lily)

    # プレイヤーの選択肢2
    builder.choice(react2_accept, "……分かった。行こう", "", text_id="c2_accept") \
           .choice(react2_death, "本当に死なないよな？", "", text_id="c2_death") \
           .choice(react2_nod, "（無言で頷く）", "", text_id="c2_nod")

    # 選択肢反応2
    builder.step(react2_accept) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_r4", "ハッ、良い返事だ。ついてこい。", "", actor=balgas) \
        .jump(scene3)

    builder.step(react2_death) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_r5", "……知らねえ。だが、死ぬ気で来い。", "", actor=balgas) \
        .jump(scene3)

    builder.step(react2_nod) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_r6", "……よし。じゃあ行くぞ。", "", actor=balgas) \
        .jump(scene3)

    # ========================================
    # シーン3: 実戦講義『魂の重量』
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Battle_Balgas_Training") \
        .say("narr_7", "（地下の練習場は、虚空から漏れる微かな光に照らされている。）", "", actor=pc) \
        .say("narr_8", "（バルガスは武器を持たず、無造作に構えた。）", "", actor=pc) \
        .say("narr_9", "（その背後からは、歴戦の猛者だけが放つ、物理的な「圧」が空間を歪ませている。）", "", actor=pc) \
        .shake() \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_8", "さあ、構えろ。ルールは一つ……俺の足を一歩でも動かしてみせろ。", "", actor=balgas) \
        .say("balgas_9", "魔法でも、薬でも、卑怯な手でも何でも使え。", "", actor=balgas) \
        .say("balgas_10", "戦士の哲学とは、『手段』を尽くした先にある『目的』の純粋さだ！", "", actor=balgas) \
        .say("narr_10", "（バルガスとの特別な手合わせが始まる……！）", "", actor=pc) \
        .action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] TODO: バルガス訓練戦闘 - 満足度システム\");") \
        .jump(scene4)

    # ========================================
    # シーン4: 哲学の伝承
    # ========================================
    builder.step(scene4) \
        .play_bgm("BGM/Emotional_Sacred_Triumph_Special") \
        .say("narr_11", "（息を切らし、膝をつくあなた。）", "", actor=pc) \
        .say("narr_12", "（バルガスは一歩も動いていないが、その口元には満足げな笑みが浮かんでいた。）", "", actor=pc) \
        .say("narr_13", "（彼はあなたの肩を、岩のような拳で一つ叩いた。）", "", actor=pc) \
        .shake() \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_11", "……ハッ！ 少しは『意志』が剣に乗るようになったじゃねえか。", "", actor=balgas) \
        .say("balgas_12", "いいか、戦いってのはな、ただの殺し合いじゃねえ。", "", actor=balgas) \
        .say("balgas_13", "自分の命を、何のために『消費』するかを決める聖域だ。", "", actor=balgas) \
        .say("balgas_14", "その哲学を忘れるな。そうすれば、どんな異次元の闇もお前を呑み込むことはできねえ。", "", actor=balgas) \
        .say("narr_14", "（ロビーに戻ると、リリィが台帳を開いて待っている。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_4", "……素晴らしい。バルガスさんの説教を聞いて生き残るなんて、あなたは本当の意味で『闘技場の鴉』になる資格を得たようです。", "", actor=lily) \
        .say("lily_5", "カラスは死肉を喰らい、戦場を飛び回る。……今のあなたに、相応しい二つ名ですね。", "", actor=lily) \
        .say("narr_15", "（彼女は台帳に何かを書き込む。）", "", actor=pc) \
        .say("lily_6", "観客からの報酬として、小さなコイン12枚とプラチナコイン5枚。それと、戦闘記録として素材を一つ選んでいただけます。", "", actor=lily) \
        .jump(reward_choice)

    # 報酬選択肢
    builder.choice(reward_stone, "研磨石を頼む", "", text_id="c_reward_stone") \
           .choice(reward_steel, "鋼鉄の欠片が欲しい", "", text_id="c_reward_steel") \
           .choice(reward_bone, "骨を選ぶ", "", text_id="c_reward_bone")

    builder.step(reward_stone) \
        .say("lily_rew1", "『研磨石×1』、記録いたしました。バルガスさんの哲学を継ぐ、良い選択ですね。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"whetstone\"));") \
        .jump(reward_end)

    builder.step(reward_steel) \
        .say("lily_rew2", "『鋼鉄の欠片×1』、記録いたしました。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"steel\"));") \
        .jump(reward_end)

    builder.step(reward_bone) \
        .say("lily_rew3", "『骨×1』ですね。……地味ですが、実用的です。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"bone\"));") \
        .jump(reward_end)

    builder.step(reward_end) \
        .action("eval", param="for(int i=0; i<12; i++) { EClass.pc.Pick(ThingGen.Create(\"coin\")); } for(int i=0; i<5; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .say("lily_7", "記録完了です。", "", actor=lily) \
        .say("lily_8", "……それと、今回の戦いで、あなたは『闘技場の鴉』としての称号を獲得しました。", "", actor=lily) \
        .say("lily_9", "死肉を喰らい、戦場を飛び回る……ふふ、あなたらしいですね。", "", actor=lily) \
        .say("narr_16", "（バルガスが酒瓶を傾けながら、あなたに背を向けたまま言う。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_15", "……お前は、カインが持っていた以上の、本物の『鋼の心』を持った戦士だ。", "", actor=balgas) \
        .say("balgas_16", "俺がかつて率いていた『英雄の軍団』にも、お前みたいな奴がいた。", "", actor=balgas) \
        .say("balgas_17", "……あいつも、最後まで哲学を曲げなかった。", "", actor=balgas) \
        .say("narr_17", "（彼は深く息を吐き、酒を飲み干す。）", "", actor=pc) \
        .say("balgas_18", "……行け。次はもっと厳しい戦いが待ってる。", "", actor=balgas) \
        .say("balgas_19", "だが、お前なら……大丈夫だ。", "", actor=balgas) \
        .jump(final_choice)

    # 最終選択肢
    builder.choice(final_thanks, "……ありがとう", "", text_id="c_final_thanks") \
           .choice(final_again, "次も教えてくれるか？", "", text_id="c_final_again") \
           .choice(final_nod, "（無言で頷く）", "", text_id="c_final_nod")

    builder.step(final_thanks) \
        .say("balgas_r7", "ハッ、礼はいらねえ。生き残って、俺を超えてみせろ。", "", actor=balgas) \
        .jump(ending)

    builder.step(final_again) \
        .say("balgas_r8", "……ああ。必要なら、いつでも来い。", "", actor=balgas) \
        .jump(ending)

    builder.step(final_nod) \
        .say("balgas_r9", "……よし。じゃあ行け。", "", actor=balgas) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .complete_quest(QuestIds.BALGAS_TRAINING) \
        .mod_flag(Keys.REL_BALGAS, "+", 20) \
        .say("sys_title", "【システム】バルガスの哲学を学びました。", "", actor=pc) \
        .action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] TODO: バフ付与処理 - 永続的な戦闘力向上\");") \
        .finish()
