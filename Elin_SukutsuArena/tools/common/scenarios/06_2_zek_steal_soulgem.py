"""
06_2_zek_steal_soulgem.md - 英雄の残響、商人の天秤
ゼクがカインの魂の欠片を狙う重要な道徳的選択イベント
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, FlagValues, QuestIds


def define_zek_steal_soulgem(builder: DramaBuilder):
    """
    ゼクがカインの魂の欠片を狙う
    シナリオ: 06_2_zek_steal_soulgem.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")
    zek = builder.register_actor(Actors.ZEK, "ゼク", "Zek")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_whisper")
    choice1 = builder.label("choice1")
    react1_what = builder.label("react1_what")
    react1_friend = builder.label("react1_friend")
    react1_silent = builder.label("react1_silent")
    scene2 = builder.label("scene2_cruel_choice")
    choice2 = builder.label("choice2")
    react2_price = builder.label("react2_price")
    react2_balgas = builder.label("react2_balgas")
    react2_stare = builder.label("react2_stare")
    scene3 = builder.label("scene3_decision")
    final_choice = builder.label("final_choice")
    refuse = builder.label("refuse")
    refuse_balgas = builder.label("refuse_balgas")
    sell = builder.label("sell")
    sell_balgas = builder.label("sell_balgas")
    scene4_lily = builder.label("scene4_lily")
    ending = builder.label("ending")

    # ========================================
    # シーン1: 砂上の囁き
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Ominous_Suspense_01") \
        .say("narr_1", "（闘技場の熱気が冷めやらぬ、薄暗い廊下。）", "", actor=pc) \
        .say("narr_2", "（勝利の余韻に浸るあなたの前に、鎖の音と共にゼクが現れる。）", "", actor=pc) \
        .shake() \
        .say("narr_3", "（彼は、あなたの掌にある『カインの魂の欠片』を、まるで極上の宝石を見るような飢えた目で見つめていた。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .focus_chara(Actors.ZEK) \
        .say("zek_1", "……あぁ、なんと美しい。", "", actor=zek) \
        .say("zek_2", "数千回の敗北と、最期の瞬間の安らぎが凝固した、混じり気なしの『純粋な魂』だ。", "", actor=zek) \
        .say("narr_4", "（彼は細長い指を伸ばし、魂の欠片を指し示す。）", "", actor=pc) \
        .say("zek_3", "バルガスがそれを望んでいるのは分かっています。……ですが、闘士殿。あのおっさんにこれを返して、一体何になるのですか？", "", actor=zek) \
        .say("zek_4", "死者に安らぎを、生者に感傷を。……そんなもの、一文の得にもなりゃしない。", "", actor=zek)

    # プレイヤーの選択肢1
    builder.choice(react1_what, "……何が言いたい", "", text_id="c1_what") \
           .choice(react1_friend, "友情に価値がないと？", "", text_id="c1_friend") \
           .choice(react1_silent, "（無言で聞く）", "", text_id="c1_silent")

    # 選択肢反応1
    builder.step(react1_what) \
        .say("zek_r1", "おや、警戒心がおありで。では、単刀直入に申し上げましょう。", "", actor=zek) \
        .jump(scene2)

    builder.step(react1_friend) \
        .say("zek_r2", "価値がない、とは言いません。ただ、『足りない』と言っているのです。", "", actor=zek) \
        .jump(scene2)

    builder.step(react1_silent) \
        .say("zek_r3", "……ふふ、沈黙は賢明さの証。では、続けさせていただきましょう。", "", actor=zek) \
        .jump(scene2)

    # ========================================
    # シーン2: 残酷な二択
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_5", "（ゼクはさらに一歩踏み込み、フードの下から歪んだ笑みを覗かせる。）", "", actor=pc) \
        .say("zek_5", "それよりも、私にその欠片を預けてはいただけませんか？これほどの素材があれば、私はあなたの武具に『神話』の一片を刻むことができる。", "", actor=zek) \
        .say("zek_6", "選ぶのはあなただ。バルガスに返し、友情と名誉という名の、腹の足しにもならない温もりを噛み締めるか。", "", actor=zek) \
        .say("zek_7", "それとも、私に売り払い、この先の地獄を生き抜くための『絶対的な暴力』を手に入れるか。", "", actor=zek) \
        .say("zek_8", "バルガスに返せば、彼は救われるでしょう。ですが、あなたは弱いままだ。私に売れば、あなたは英雄の力を食らって強くなる。", "", actor=zek) \
        .say("zek_9", "……どちらがこのアリーナの『正解』か、賢明なあなたならお分かりでしょう？", "", actor=zek)

    # プレイヤーの選択肢2
    builder.choice(react2_price, "代償は何だ？", "", text_id="c2_price") \
           .choice(react2_balgas, "バルガスが知ったら……", "", text_id="c2_balgas") \
           .choice(react2_stare, "（無言で魂の欠片を見つめる）", "", text_id="c2_stare")

    # 選択肢反応2
    builder.step(react2_price) \
        .say("zek_r4", "代償は……あなたの『良心』を、少しばかりいただくだけです。ああ、それと友情も。", "", actor=zek) \
        .jump(scene3)

    builder.step(react2_balgas) \
        .say("zek_r5", "ふふ、知られなければいいのですよ。それとも、正直に告白なさいますか？", "", actor=zek) \
        .jump(scene3)

    builder.step(react2_stare) \
        .say("zek_r6", "……悩んでおられる。それが正常です。人間らしいですね。", "", actor=zek) \
        .jump(scene3)

    # ========================================
    # シーン3: 決断の瞬間
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Ominous_Heartbeat") \
        .say("narr_6", "（ゼクはあなたの返答を待つ。その目は、あなたの決断を愉しむように細められた。）", "", actor=pc) \
        .jump(final_choice)

    # ========================================
    # 最終選択
    # ========================================
    builder.step(final_choice) \
        .choice(refuse, "バルガスとの絆を選ぶ", "", text_id="c_refuse") \
        .choice(sell, "力を手に入れる。売る", "", text_id="c_sell")

    # ========================================
    # 分岐A: 断る（バルガスに返す）
    # ========================================
    builder.step(refuse) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("zek_ref1", "……残念です。ですが、無理強いはいたしません。あなたが『感傷』を選ばれるというのなら、それもまた一興。", "", actor=zek) \
        .say("zek_ref2", "……いつか、その選択を後悔する日が来るかもしれませんが。その時はまた、お声掛けください。私は常に、影の中におりますから。", "", actor=zek) \
        .say("narr_ref", "（ゼクは影の中へと消えていく。）", "", actor=pc) \
        .jump(refuse_balgas)

    builder.step(refuse_balgas) \
        .play_bgm("BGM/Emotional_Sorrow") \
        .say("narr_ref2", "（あなたはロビーに戻り、バルガスにカインの魂の欠片を渡す。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_ref1", "……あぁ。これでようやく、あいつもこの錆びた檻から出られる。", "", actor=balgas) \
        .say("narr_ref3", "（彼は震える手で魂の欠片を受け取る。その目には涙。）", "", actor=pc) \
        .say("narr_ref4", "（彼は魂の欠片を兜の中にそっと収める。）", "", actor=pc) \
        .say("balgas_ref2", "……ありがよ。お前をただの『鉄屑』呼ばわりしたのは取り消してやる。", "", actor=balgas) \
        .say("balgas_ref3", "お前は……カインが持っていた以上の、本物の『鋼の心』を持った戦士だ。", "", actor=balgas) \
        .set_flag(Keys.KAIN_SOUL_CHOICE, FlagValues.KainSoulChoice.RETURNED) \
        .complete_quest(QuestIds.ZEK_STEAL_SOULGEM) \
        .complete_quest(QuestIds.ZEK_STEAL_SOULGEM_RETURN) \
        .finish()

    # ========================================
    # 分岐B: 売る
    # ========================================
    builder.step(sell) \
        .say("zek_sell1", "ふふ、素晴らしい！ これです、これこそが私が求めていた『合理的かつ冷酷な決断』だ！", "", actor=zek) \
        .say("zek_sell2", "友情を燃料にして、さらなる高みへ昇る……。あなたは、本物の怪物の素質がある。", "", actor=zek) \
        .say("narr_sell1", "（彼は懐から禍々しい注射器を取り出す。）", "", actor=pc) \
        .say("zek_sell3", "さあ、約束の報酬です。私の店の秘蔵品……『禁断の覚醒剤』を差し上げましょう。", "", actor=zek) \
        .shake() \
        .say("zek_sell4", "これで、あなたは『魂を喰らう者』となりました。……では、良い演技を。彼に気づかれないよう、お気をつけて。", "", actor=zek) \
        .say("narr_sell2", "（ゼクは影の中へと消えていく。）", "", actor=pc) \
        .cs_eval("EClass.pc.Pick(ThingGen.Create(\"sukutsu_stimulant\"));") \
        .jump(sell_balgas)

    builder.step(sell_balgas) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_sell3", "（あなたはロビーに戻る。バルガスがあなたを待っている。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_sell1", "……おい。カインの魂の欠片は見つかったか？", "", actor=balgas) \
        .say("narr_sell4", "（あなたは首を横に振る。）", "", actor=pc) \
        .say("balgas_sell2", "……そうか。見つからなかったか。", "", actor=balgas) \
        .say("narr_sell5", "（彼は深く息を吐き、酒瓶を手に取る。）", "", actor=pc) \
        .say("balgas_sell3", "……まあ、仕方ねえ。お前は十分頑張った。……ありがよ。", "", actor=balgas) \
        .set_flag(Keys.KAIN_SOUL_CHOICE, FlagValues.KainSoulChoice.SOLD) \
        .complete_quest(QuestIds.ZEK_STEAL_SOULGEM) \
        .complete_quest(QuestIds.ZEK_STEAL_SOULGEM_SELL) \
        .finish()
