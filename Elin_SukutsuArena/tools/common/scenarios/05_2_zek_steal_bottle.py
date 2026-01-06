"""
05_2_zek_steal_lily.md - ゼクの囁き『偽りの器、真実の対価』
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, FlagValues, QuestIds


def define_zek_steal_bottle(builder: DramaBuilder):
    """
    ゼクの囁き「偽りの器、真実の対価」
    シナリオ: 05_2_zek_steal_lily.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    zek = builder.register_actor(Actors.ZEK, "ゼク", "Zek")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_shadow_call")
    choice1 = builder.label("choice1")
    react1_what = builder.label("react1_what")
    react1_manage = builder.label("react1_manage")
    react1_silent = builder.label("react1_silent")
    scene2 = builder.label("scene2_betrayal_offer")
    choice2 = builder.label("choice2")
    react2_forbidden = builder.label("react2_forbidden")
    react2_betray = builder.label("react2_betray")
    react2_price = builder.label("react2_price")
    scene3 = builder.label("scene3_choice")
    refuse = builder.label("refuse")
    accept = builder.label("accept")
    scene4_aftermath = builder.label("scene4_aftermath")
    ending = builder.label("ending")

    # ========================================
    # シーン1: 影からの招き
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Ominous_Suspense_01") \
        .say("narr_1", "（器が完成した。あなたはリリィに渡すため、受付へと向かう廊下を歩いていた。）", "", actor=pc) \
        .say("narr_2", "（その途中——灯火が不自然に揺らぎ、あなたの足元の影が、まるで意思を持った沼のように長く伸びる。）", "", actor=pc) \
        .shake() \
        .say("narr_3", "（そこから、鎖の擦れる音と共に、ゼクが音もなく這い出してきた。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_1", "……素晴らしい。実に、溜息が出るほどに。", "", actor=zek) \
        .say("zek_2", "あのサキュバスに渡すには、あまりに惜しい『傑作』を作られましたね、闘士殿。", "", actor=zek) \
        .say("narr_4", "（彼は細長い指で、あなたが持つ器を指し示す。）", "", actor=pc) \
        .say("zek_3", "彼女が何と言ったかは知りませんが……あの女がその器で集めようとしているのは、単なる『音』ではありません。", "", actor=zek) \
        .say("zek_4", "そこに溜まるのは、あなたの戦いが生み出した、あなたの自身の魂の残滓……。彼女はそれを啜り、あなたをより効率的に『管理』しようとしているのですよ。……ふふ、お気づきでしたか？", "", actor=zek)

    # プレイヤーの選択肢
    builder.choice(react1_what, "……何が言いたい", "", text_id="c1_what") \
           .choice(react1_manage, "リリィが俺を管理しているだと？", "", text_id="c1_manage") \
           .choice(react1_silent, "（無言で聞く）", "", text_id="c1_silent")

    # 選択肢反応
    builder.step(react1_what) \
        .say("zek_r1", "おや、警戒心がおありで。では、単刀直入に申し上げましょう。", "", actor=zek) \
        .jump(scene2)

    builder.step(react1_manage) \
        .say("zek_r2", "ええ、そうです。彼女はサキュバス。魂を喰らう存在です。あなたは気づいていなかったのですか？", "", actor=zek) \
        .jump(scene2)

    builder.step(react1_silent) \
        .say("zek_r3", "……ふふ、沈黙は賢明さの証。では、続けさせていただきましょう。", "", actor=zek) \
        .jump(scene2)

    # ========================================
    # シーン2: 裏切りの提案
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_5", "（ゼクは長い指で、懐から一つの『偽物』を取り出した。）", "", actor=pc) \
        .say("narr_6", "（見た目はあなたが作った共鳴瓶と瓜二つだが、そのガラスの奥には、澱んだどす黒い霧が渦巻いている。）", "", actor=pc) \
        .say("zek_5", "どうでしょう、一つ提案があります。", "", actor=zek) \
        .say("zek_6", "その本物の器を、私に譲ってはいただけませんか？代わりに、この**『呪われた模造品（ミミック・ボトル）』**を彼女に渡すのです。", "", actor=zek) \
        .say("narr_7", "（彼は偽物の器をあなたの前に差し出す。）", "", actor=pc) \
        .say("zek_7", "彼女は気づかないでしょう……。いえ、気づいた時には、彼女の『研究』はあなたの支配ではなく、私への捧げ物へとすり替わっている。", "", actor=zek) \
        .say("zek_8", "そしてあなたには、その誠実な裏切りの対価として、私が異次元のゴミ捨て場で拾い上げた『本物の禁忌』を差し上げましょう。……それと、特別な報酬も、ね。", "", actor=zek)

    # プレイヤーの選択肢
    builder.choice(react2_forbidden, "その『禁忌』とは何だ？", "", text_id="c2_forbidden") \
           .choice(react2_betray, "リリィを裏切れと？", "", text_id="c2_betray") \
           .choice(react2_price, "……代償は何だ", "", text_id="c2_price")

    # 選択肢反応
    builder.step(react2_forbidden) \
        .say("zek_r4", "ふふ、興味を持たれましたか。では、お見せいたしましょう。", "", actor=zek) \
        .jump(scene3)

    builder.step(react2_betray) \
        .say("zek_r5", "裏切りとは聞こえが悪い。……『戦略的な選択』と呼びましょう。", "", actor=zek) \
        .jump(scene3)

    builder.step(react2_price) \
        .say("zek_r6", "おや、慎重ですね。代償は……あなたの『良心』を、少しばかりいただくだけです。", "", actor=zek) \
        .jump(scene3)

    # ========================================
    # シーン3: 天秤にかけられる魂
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Ominous_Heartbeat") \
        .say("narr_8", "（ゼクは「本物の器」と「偽物の器」、そして報酬となる「禍々しい品」を並べ、あなたの返答を待つ。）", "", actor=pc) \
        .say("narr_9", "（彼のフードの奥にある瞳が、あなたの決断を愉しむように細められた。）", "", actor=pc) \
        .say("zek_9", "リリィに従い、大人しく彼女の飼い犬となるか。それとも、私と手を組み、彼女を欺いて『真なる力』を手にするか。", "", actor=zek) \
        .say("zek_10", "……ふふ、どちらを選んでも、このアリーナに刻まれるあなたの物語は、より残酷で美しいものになるでしょう。さあ、お選びください。", "", actor=zek)

    # 重要な選択
    builder.choice(refuse, "断る。リリィを裏切るつもりはない", "", text_id="c_refuse") \
           .choice(accept, "……分かった。取引に応じる", "", text_id="c_accept")

    # 選択肢: 断る
    builder.step(refuse) \
        .say("zek_ref1", "……残念です。ですが、無理強いはいたしません。", "", actor=zek) \
        .say("zek_ref2", "あなたが『忠犬』の道を選ばれるというのなら、それもまた一興。……いつか、その選択を後悔する日が来るかもしれませんが。", "", actor=zek) \
        .say("narr_ref", "（ゼクは影の中へと消えていく。）", "", actor=pc) \
        .set_flag(Keys.BOTTLE_CHOICE, FlagValues.BottleChoice.REFUSED) \
        .mod_flag(Keys.REL_LILY, "+", 10) \
        .jump(ending)

    # 選択肢: 受諾
    builder.step(accept) \
        .say("zek_acc1", "ふふ、賢明な判断です。", "", actor=zek) \
        .say("narr_acc1", "（ゼクは満足げに本物の器を影の中へと消し、偽物をあなたの手に握らせる。）", "", actor=pc) \
        .say("zek_acc2", "これがあなたへの報酬……**小さなコイン10枚**と**プラチナコイン3枚**を、台帳に記録する手はずを整えておきましょう。それと、この『影の印』を。", "", actor=zek) \
        .shake() \
        .say("zek_acc3", "これで、私の店での取引が、より『有利』になりますよ。……では、良い演技を。彼女に気づかれないよう、お気をつけて。", "", actor=zek) \
        .say("narr_acc2", "（ゼクは影の中へと消えていく。）", "", actor=pc) \
        .set_flag(Keys.BOTTLE_CHOICE, FlagValues.BottleChoice.SWAPPED) \
        .mod_flag(Keys.REL_LILY, "+", 10) \
        .mod_flag(Keys.REL_ZEK, "+", 15) \
        .action("eval", param="for(int i=0; i<10; i++) { EClass.pc.Pick(ThingGen.Create(\"coin\")); } for(int i=0; i<3; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .jump(scene4_aftermath)

    # ========================================
    # シーン4: 事後の静寂（受諾した場合のみ）
    # ========================================
    builder.step(scene4_aftermath) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_aft1", "（ゼクが消えた後、あなたは何食わぬ顔で受付へと向かい、その「偽物」をリリィに手渡す。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_a1", "お疲れ様でした。見せていただけますか？", "", actor=lily) \
        .say("narr_aft2", "（彼女は器を手に取り、軽く傾ける。）", "", actor=pc) \
        .say("lily_a2", "……あら、なんだか少し、器の感触が変わったかしら？", "", actor=lily) \
        .say("narr_aft3", "（一瞬、彼女の瞳があなたを鋭く見つめるが、すぐに笑顔に戻る。）", "", actor=pc) \
        .say("lily_a3", "……まぁいいわ。これで私の研究は飛躍的に進みます。ふふ、感謝してくださいね。あなたが『使い物』にならなくなった後も、その響きだけは私の手元に残るのですから。", "", actor=lily) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .complete_quest(QuestIds.ZEK_STEAL_BOTTLE) \
        .finish()
