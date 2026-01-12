"""
19_epilogue.py - 最終決戦後のエピローグ

アスタロト撃破後のエンディング選択と帰還シーン。
勝利後にarena_masterドラマから呼び出される。
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, FlagValues, QuestIds


def define_epilogue(builder: DramaBuilder):
    """
    エピローグ：エンディング選択と帰還
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    astaroth = builder.register_actor(Actors.ASTAROTH, "アスタロト", "Astaroth")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    zek = builder.register_actor(Actors.ZEK, "ゼク", "Zek")

    # ラベル定義
    main = builder.label("main")
    act5 = builder.label("act5_victory")
    act6 = builder.label("act6_return")
    ending_choice = builder.label("ending_choice")
    ending_a_rescue = builder.label("ending_a_rescue")  # 連れ出し
    ending_b_inherit = builder.label("ending_b_inherit")  # 継承
    epilogue = builder.label("epilogue")
    finale = builder.label("finale")

    # バルガス死亡版ラベル
    act5_check_lily_dead = builder.label("act5_check_lily_dead")  # 分岐チェック用
    act5_dead = builder.label("act5_balgas_dead")
    act6_dead = builder.label("act6_balgas_dead")
    ending_choice_dead = builder.label("ending_choice_balgas_dead")
    ending_a_dead = builder.label("ending_a_balgas_dead")
    ending_b_dead = builder.label("ending_b_balgas_dead")
    finale_check_lily_dead = builder.label("finale_check_lily_dead")  # 分岐チェック用
    finale_dead = builder.label("finale_balgas_dead")

    # リリィ離反版ラベル（バルガス生存、リリィ離反）
    act5_lily_hostile = builder.label("act5_lily_hostile")
    act6_lily_hostile = builder.label("act6_lily_hostile")
    ending_choice_lily_hostile = builder.label("ending_choice_lily_hostile")
    ending_a_lily_hostile = builder.label("ending_a_lily_hostile")
    ending_b_lily_hostile = builder.label("ending_b_lily_hostile")
    finale_lily_hostile = builder.label("finale_lily_hostile")

    # 最悪版ラベル（バルガス死亡、リリィ離反）
    act5_worst = builder.label("act5_worst")
    act6_worst = builder.label("act6_worst")
    ending_choice_worst = builder.label("ending_choice_worst")
    ending_a_worst = builder.label("ending_a_worst")
    ending_b_worst = builder.label("ending_b_worst")
    finale_worst = builder.label("finale_worst")

    # ========================================
    # メイン（act5から開始）
    # ========================================
    builder.step(main) \
        .jump(act5)

    # ========================================
    # 第5幕: 終焉と、はじまり
    # ========================================
    builder.step(act5) \
        .branch_if(Keys.BALGAS_KILLED, "==", FlagValues.BalgasChoice.KILLED, act5_check_lily_dead) \
        .branch_if(Keys.LILY_HOSTILE, "==", FlagValues.TRUE, act5_lily_hostile) \
        .play_bgm("BGM/Victory_Epilogue") \
        .say("narr_14", "（激闘の末、アスタロトの身体が崩れ始める。王座は砕け、アリーナの外壁は剥がれ落ち、そこから美しい『本当の星空』が姿を現した。）", "", actor=pc) \
        .say("astaroth_6", "「……見事だ。私は……ただ、この閉じられた孵化器を守るだけの、古い部品に過ぎなかったのかもしれないな。」", "", actor=astaroth) \
        .say("astaroth_7", "「……リリィ、バルガス、ゼク。……そして新しき王よ。この世界の重さを、お前たちが分かち合うというのなら……私は、安心して土へ還ろう。」", "", actor=astaroth) \
        .say("narr_15", "（アスタロトが柔らかな光となって霧散していく。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_12", "……やれやれ。これほどの損失（コスト）を出して、得られた利益は『自由』だけですか。……悪くない取引でしたね。", "", actor=zek) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_5", "ケッ、重てえな。だが、一人で背負うよりはマシだ。", "", actor=balgas) \
        .jump(act6)

    # ========================================
    # 第6幕: 帰還の道
    # ========================================
    builder.step(act6) \
        .play_bgm("BGM/Hopeful_Theme") \
        .say("narr_16", "（アスタロトが完全に消えると、アリーナ全体を覆っていた次元の壁が、ガラスのように砕け散り始める。）", "", actor=pc) \
        .say("narr_17", "（紫紺の虚無が晴れ、その向こうに久しく忘れていた『青空』が広がっていた。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_6", "……おい、見ろ。あれは……", "", actor=balgas) \
        .say("narr_18", "（崩れゆく次元の境界線の中に、一筋の光の階段が浮かび上がる。それはイルヴァへと続く、帰還の道だ。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_7", "この道は、地上と、かつてのアリーナ跡を繋ぐ『自由な通路』になるでしょう。行きたい者は行き、留まりたい者は留まる。……それが、あなたが勝ち取った『解放』なのですね。", "", actor=lily) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_7", "……おい、鴉。いや、屠竜者。お前、この先どうする？ 地上に戻るか？ それとも……", "", actor=balgas) \
        .jump(ending_choice)

    # ========================================
    # エンディング選択
    # ========================================
    builder.step(ending_choice) \
        .choice(ending_a_rescue, "皆を連れて、イルヴァへ行こう", "", text_id="ending_a_rescue") \
        .choice(ending_b_inherit, "新しいアリーナを作り直したい", "", text_id="ending_b_inherit")

    # エンディングA: 連れ出し（皆を連れてイルヴァへ）
    builder.step(ending_a_rescue) \
        .focus_chara(Actors.LILY) \
        .say("lily_ea2", "あなたとの契約を通じて、私も……初めて『帰る場所』を持てるのね。", "", actor=lily) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_ea1", "……ケッ、35年ぶりの故郷か。カインのやつにも見せてやりたかった。", "", actor=balgas) \
        .focus_chara(Actors.ZEK) \
        .say("zek_ea1", "ふむ、私は……もう少しここに残りましょう。アルカディアの技術者として、この次元の安定化を見届ける義務がありますからね。", "", actor=zek) \
        .say("zek_ea2", "……また会いましょう。私の最高傑作が、どんな人生を歩むのか、記録させてもらいますよ。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.RESCUE) \
        .jump(epilogue)

    # エンディングB: 継承（アリーナを純粋な闘技場として再建）
    builder.step(ending_b_inherit) \
        .focus_chara(Actors.LILY) \
        .say("lily_eb1", "……ふふ、あなたらしいですね。この場所にも、居場所を必要とする者がいますから。", "", actor=lily) \
        .say("lily_eb2", "私も残ります。あなたが新しいグランドマスターなら、私は……受付嬢ではなく、『伴侶』として支えさせてください。", "", actor=lily) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_eb1", "ハッ、そうこなくちゃな。『神の孵化場』はもう終わりだ。これからは、自分の意志で戦いたい奴だけが来る場所にする。", "", actor=balgas) \
        .say("balgas_eb2", "俺は引退済みだが……まあ、若い奴らの相談役くらいはやってやるさ。", "", actor=balgas) \
        .focus_chara(Actors.ZEK) \
        .say("zek_eb1", "ふむ、それなら私が商店街を取り仕切りましょう。アルカディアの技術と、各次元の品物……ククッ、繁盛しそうですね。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.INHERIT) \
        .jump(epilogue)


    # ========================================
    # エピローグ
    # ========================================
    builder.step(epilogue) \
        .play_bgm("BGM/ProgressiveDance") \
        .wait(500) \
        .say("narr_21", "かつて、異次元の闘技場に迷い込んだ一人の冒険者がいた。そこで絶望の底で友を得て、魂を賭けて戦い、ついには、『うつろいし神』をも超える存在となった。そして今、解放された魂は、新たな物語を紡ぎ始めるーー", "", actor=pc) \
        .jump(finale)

    # ========================================
    # フィナーレ
    # ========================================
    builder.step(finale) \
        .branch_if(Keys.BALGAS_KILLED, "==", FlagValues.BalgasChoice.KILLED, finale_check_lily_dead) \
        .branch_if(Keys.LILY_HOSTILE, "==", FlagValues.TRUE, finale_lily_hostile) \
        .say("balgas_f1", "……おい、いつまで感傷に浸ってんだ。次は俺の奢りで、地上で一番うまい酒を飲みに行くぞ！", "", actor=balgas) \
        .say("lily_f1", "ふふ、楽しみです。……リリィとして、初めての『デート』ですから。", "", actor=lily) \
        .say("zek_f1", "おや、私も混ぜてくださいよ？", "", actor=zek) \
        .complete_quest(QuestIds.LAST_BATTLE) \
        .say("sys_complete", "【巣窟アリーナ】メインストーリークリア！", actor=pc) \
        .drama_end()

    # ========================================
    # バルガス死亡版: 第5幕
    # ========================================
    builder.step(act5_dead) \
        .play_bgm("BGM/Victory_Epilogue") \
        .say("narr_14", "（激闘の末、アスタロトの身体が崩れ始める。王座は砕け、アリーナの外壁は剥がれ落ち、そこから美しい『本当の星空』が姿を現した。）", "", actor=pc) \
        .say("astaroth_6d", "「……見事だ。私は……ただ、この閉じられた孵化器を守るだけの、古い部品に過ぎなかったのかもしれないな。」", "", actor=astaroth) \
        .say("astaroth_7d", "「……リリィ、ゼク。……そして新しき王よ。この世界の重さを、お前たちが分かち合うというのなら……私は、安心して土へ還ろう。」", "", actor=astaroth) \
        .say("narr_15", "（アスタロトが柔らかな光となって霧散していく。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_12", "……やれやれ。これほどの損失（コスト）を出して、得られた利益は『自由』だけですか。……悪くない取引でしたね。", "", actor=zek) \
        .focus_chara(Actors.LILY) \
        .say("lily_d5", "……バルガスさんも、きっと喜んでくれているわ。彼の分まで、私たちは生きていかなきゃね。", "", actor=lily) \
        .jump(act6_dead)

    # バルガス死亡版: 第6幕
    builder.step(act6_dead) \
        .play_bgm("BGM/Hopeful_Theme") \
        .say("narr_16", "（アスタロトが完全に消えると、アリーナ全体を覆っていた次元の壁が、ガラスのように砕け散り始める。）", "", actor=pc) \
        .say("narr_17", "（紫紺の虚無が晴れ、その向こうに久しく忘れていた『青空』が広がっていた。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_d6", "……見て。あれは……帰り道。", "", actor=lily) \
        .say("narr_18", "（崩れゆく次元の境界線の中に、一筋の光の階段が浮かび上がる。それはイルヴァへと続く、帰還の道だ。）", "", actor=pc) \
        .say("lily_7", "この道は、地上と、かつてのアリーナ跡を繋ぐ『自由な通路』になるでしょう。行きたい者は行き、留まりたい者は留まる。……それが、あなたが勝ち取った『解放』なのですね。", "", actor=lily) \
        .focus_chara(Actors.ZEK) \
        .say("zek_d7", "……おい、屠竜者。この先どうする？ 地上に戻るか？ それとも……", "", actor=zek) \
        .jump(ending_choice_dead)

    # バルガス死亡版: エンディング選択
    builder.step(ending_choice_dead) \
        .choice(ending_a_dead, "皆を連れて、イルヴァへ行こう", "", text_id="ending_a_rescue_dead") \
        .choice(ending_b_dead, "新しいアリーナを作り直したい", "", text_id="ending_b_inherit_dead")

    # バルガス死亡版: エンディングA
    builder.step(ending_a_dead) \
        .focus_chara(Actors.LILY) \
        .say("lily_ea2", "あなたとの契約を通じて、私も……初めて『帰る場所』を持てるのね。", "", actor=lily) \
        .say("lily_ead", "……バルガスさんの分まで、私たちは生きていくわ。", "", actor=lily) \
        .focus_chara(Actors.ZEK) \
        .say("zek_ea1", "ふむ、私は……もう少しここに残りましょう。アルカディアの技術者として、この次元の安定化を見届ける義務がありますからね。", "", actor=zek) \
        .say("zek_ea2", "……また会いましょう。私の最高傑作が、どんな人生を歩むのか、記録させてもらいますよ。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.RESCUE) \
        .jump(epilogue)

    # バルガス死亡版: エンディングB
    builder.step(ending_b_dead) \
        .focus_chara(Actors.LILY) \
        .say("lily_eb1", "……ふふ、あなたらしいですね。この場所にも、居場所を必要とする者がいますから。", "", actor=lily) \
        .say("lily_eb2", "私も残ります。あなたが新しいグランドマスターなら、私は……受付嬢ではなく、『伴侶』として支えさせてください。", "", actor=lily) \
        .say("lily_ebd", "バルガスさんの意志も、きっとこのアリーナに宿っているはず。私たちで受け継ぎましょう。", "", actor=lily) \
        .focus_chara(Actors.ZEK) \
        .say("zek_eb1", "ふむ、それなら私が商店街を取り仕切りましょう。アルカディアの技術と、各次元の品物……ククッ、繁盛しそうですね。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.INHERIT) \
        .jump(epilogue)

    # バルガス死亡版: フィナーレ
    builder.step(finale_dead) \
        .say("lily_f1d", "……さあ、行きましょう。私たちの新しい物語が、始まるのですから。", "", actor=lily) \
        .say("zek_f1", "おや、私も混ぜてくださいよ？", "", actor=zek) \
        .complete_quest(QuestIds.LAST_BATTLE) \
        .say("sys_complete", "【巣窟アリーナ】メインストーリークリア！", actor=pc) \
        .drama_end()

    # ========================================
    # 分岐チェック用ステップ
    # ========================================
    # act5分岐: バルガス死亡の場合、さらにリリィ離反をチェック
    builder.step(act5_check_lily_dead) \
        .branch_if(Keys.LILY_HOSTILE, "==", FlagValues.TRUE, act5_worst) \
        .jump(act5_dead)

    # finale分岐: バルガス死亡の場合、さらにリリィ離反をチェック
    builder.step(finale_check_lily_dead) \
        .branch_if(Keys.LILY_HOSTILE, "==", FlagValues.TRUE, finale_worst) \
        .jump(finale_dead)

    # ========================================
    # リリィ離反版: 第5幕（バルガス生存、リリィ離反）
    # ========================================
    builder.step(act5_lily_hostile) \
        .play_bgm("BGM/Victory_Epilogue") \
        .say("narr_14", "（激闘の末、アスタロトの身体が崩れ始める。王座は砕け、アリーナの外壁は剥がれ落ち、そこから美しい『本当の星空』が姿を現した。）", "", actor=pc) \
        .say("astaroth_6", "「……見事だ。私は……ただ、この閉じられた孵化器を守るだけの、古い部品に過ぎなかったのかもしれないな。」", "", actor=astaroth) \
        .say("astaroth_7_lh", "「……バルガス、ゼク。……そして新しき王よ。この世界の重さを、お前たちが分かち合うというのなら……私は、安心して土へ還ろう。」", "", actor=astaroth) \
        .say("narr_15", "（アスタロトが柔らかな光となって霧散していく。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_12", "……やれやれ。これほどの損失（コスト）を出して、得られた利益は『自由』だけですか。……悪くない取引でしたね。", "", actor=zek) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_5", "ケッ、重てえな。だが、一人で背負うよりはマシだ。", "", actor=balgas) \
        .say("balgas_lh5", "……リリィの奴も、いつか分かってくれるといいんだがな。", "", actor=balgas) \
        .jump(act6_lily_hostile)

    # リリィ離反版: 第6幕
    builder.step(act6_lily_hostile) \
        .play_bgm("BGM/Hopeful_Theme") \
        .say("narr_16", "（アスタロトが完全に消えると、アリーナ全体を覆っていた次元の壁が、ガラスのように砕け散り始める。）", "", actor=pc) \
        .say("narr_17", "（紫紺の虚無が晴れ、その向こうに久しく忘れていた『青空』が広がっていた。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_6", "……おい、見ろ。あれは……", "", actor=balgas) \
        .say("narr_18", "（崩れゆく次元の境界線の中に、一筋の光の階段が浮かび上がる。それはイルヴァへと続く、帰還の道だ。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_lh7", "この道は、地上と、かつてのアリーナ跡を繋ぐ『自由な通路』になるでしょう。行きたい者は行き、留まりたい者は留まる。……それが、あなたが勝ち取った『解放』です。", "", actor=zek) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_7", "……おい、鴉。いや、屠竜者。お前、この先どうする？ 地上に戻るか？ それとも……", "", actor=balgas) \
        .jump(ending_choice_lily_hostile)

    # リリィ離反版: エンディング選択
    builder.step(ending_choice_lily_hostile) \
        .choice(ending_a_lily_hostile, "皆を連れて、イルヴァへ行こう", "", text_id="ending_a_rescue_lh") \
        .choice(ending_b_lily_hostile, "新しいアリーナを作り直したい", "", text_id="ending_b_inherit_lh")

    # リリィ離反版: エンディングA
    builder.step(ending_a_lily_hostile) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_ea_lh", "……ケッ、35年ぶりの故郷か。カインのやつにも見せてやりたかった。", "", actor=balgas) \
        .focus_chara(Actors.ZEK) \
        .say("zek_ea1", "ふむ、私は……もう少しここに残りましょう。アルカディアの技術者として、この次元の安定化を見届ける義務がありますからね。", "", actor=zek) \
        .say("zek_ea2", "……また会いましょう。私の最高傑作が、どんな人生を歩むのか、記録させてもらいますよ。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.RESCUE) \
        .jump(epilogue)

    # リリィ離反版: エンディングB
    builder.step(ending_b_lily_hostile) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_eb_lh1", "ハッ、そうこなくちゃな。『神の孵化場』はもう終わりだ。これからは、自分の意志で戦いたい奴だけが来る場所にする。", "", actor=balgas) \
        .say("balgas_eb_lh2", "俺は引退済みだが……まあ、若い奴らの相談役くらいはやってやるさ。", "", actor=balgas) \
        .focus_chara(Actors.ZEK) \
        .say("zek_eb1", "ふむ、それなら私が商店街を取り仕切りましょう。アルカディアの技術と、各次元の品物……ククッ、繁盛しそうですね。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.INHERIT) \
        .jump(epilogue)

    # リリィ離反版: フィナーレ
    builder.step(finale_lily_hostile) \
        .say("balgas_f_lh", "……おい、いつまで感傷に浸ってんだ。次は俺の奢りで、地上で一番うまい酒を飲みに行くぞ！", "", actor=balgas) \
        .say("zek_f1", "おや、私も混ぜてくださいよ？", "", actor=zek) \
        .complete_quest(QuestIds.LAST_BATTLE) \
        .say("sys_complete", "【巣窟アリーナ】メインストーリークリア！", actor=pc) \
        .drama_end()

    # ========================================
    # 最悪版: 第5幕（バルガス死亡、リリィ離反）
    # ========================================
    builder.step(act5_worst) \
        .play_bgm("BGM/Victory_Epilogue") \
        .say("narr_14", "（激闘の末、アスタロトの身体が崩れ始める。王座は砕け、アリーナの外壁は剥がれ落ち、そこから美しい『本当の星空』が姿を現した。）", "", actor=pc) \
        .say("astaroth_6", "「……見事だ。私は……ただ、この閉じられた孵化器を守るだけの、古い部品に過ぎなかったのかもしれないな。」", "", actor=astaroth) \
        .say("astaroth_7_w", "「……ゼク。……そして新しき王よ。この世界の重さを、お前たちが分かち合うというのなら……私は、安心して土へ還ろう。」", "", actor=astaroth) \
        .say("narr_15", "（アスタロトが柔らかな光となって霧散していく。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_12", "……やれやれ。これほどの損失（コスト）を出して、得られた利益は『自由』だけですか。……悪くない取引でしたね。", "", actor=zek) \
        .say("zek_w5", "……バルガスもリリィも、もういない。残ったのは私たちだけですか。", "", actor=zek) \
        .jump(act6_worst)

    # 最悪版: 第6幕
    builder.step(act6_worst) \
        .play_bgm("BGM/Hopeful_Theme") \
        .say("narr_16", "（アスタロトが完全に消えると、アリーナ全体を覆っていた次元の壁が、ガラスのように砕け散り始める。）", "", actor=pc) \
        .say("narr_17", "（紫紺の虚無が晴れ、その向こうに久しく忘れていた『青空』が広がっていた。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_w6", "……見て。あれは……帰り道。", "", actor=zek) \
        .say("narr_18", "（崩れゆく次元の境界線の中に、一筋の光の階段が浮かび上がる。それはイルヴァへと続く、帰還の道だ。）", "", actor=pc) \
        .say("zek_w7", "この道は、地上と、かつてのアリーナ跡を繋ぐ『自由な通路』になるでしょう。行きたい者は行き、留まりたい者は留まる。……それが、あなたが勝ち取った『解放』です。", "", actor=zek) \
        .say("zek_w8", "……さて、孤独な英雄よ。この先どうする？ 地上に戻るか？ それとも……", "", actor=zek) \
        .jump(ending_choice_worst)

    # 最悪版: エンディング選択
    builder.step(ending_choice_worst) \
        .choice(ending_a_worst, "イルヴァへ行こう", "", text_id="ending_a_rescue_w") \
        .choice(ending_b_worst, "新しいアリーナを作り直したい", "", text_id="ending_b_inherit_w")

    # 最悪版: エンディングA
    builder.step(ending_a_worst) \
        .focus_chara(Actors.ZEK) \
        .say("zek_ea_w1", "ふむ、私は……もう少しここに残りましょう。アルカディアの技術者として、この次元の安定化を見届ける義務がありますからね。", "", actor=zek) \
        .say("zek_ea_w2", "……また会いましょう。孤独な英雄が、どんな人生を歩むのか、記録させてもらいますよ。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.RESCUE) \
        .jump(epilogue)

    # 最悪版: エンディングB
    builder.step(ending_b_worst) \
        .focus_chara(Actors.ZEK) \
        .say("zek_eb_w1", "……ふふ、あなたらしいですね。この場所にも、居場所を必要とする者がいますから。", "", actor=zek) \
        .say("zek_eb_w2", "それなら私が商店街を取り仕切りましょう。アルカディアの技術と、各次元の品物……ククッ、繁盛しそうですね。", "", actor=zek) \
        .say("zek_eb_w3", "私とあなた、二人でこの場所を作り上げていきましょう。……悪くない、取引ですよ。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.INHERIT) \
        .jump(epilogue)

    # 最悪版: フィナーレ
    builder.step(finale_worst) \
        .say("zek_fw1", "……さて、孤独な英雄よ。次はどこへ行きますか？", "", actor=zek) \
        .say("zek_fw2", "私は……見届けさせてもらいましょう。あなたの選択の結末を。", "", actor=zek) \
        .complete_quest(QuestIds.LAST_BATTLE) \
        .say("sys_complete", "【巣窟アリーナ】メインストーリークリア！", actor=pc) \
        .drama_end()
