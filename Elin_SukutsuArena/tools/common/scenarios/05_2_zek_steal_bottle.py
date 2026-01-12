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
        .say("narr_1", "（リリィが作った『死の共鳴瓶』。彼女は満足げに、その器を受付の棚に飾っていた。）", "", actor=pc) \
        .say("narr_2", "（ーー廊下を歩いていると、灯火が不自然に揺らぎ、あなたの足元の影が、まるで意思を持った沼のように長く伸びる。）", "", actor=pc) \
        .shake() \
        .say("narr_3", "（そこから、鎖の擦れる音と共に、ゼクが音もなく這い出してきた。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_1", "……素晴らしい。実に、溜息が出るほどに。", "", actor=zek) \
        .say("zek_2", "あのサキュバスが作った『共鳴瓶』……実に惜しい傑作ですね、闘士殿。", "", actor=zek) \
        .say("narr_4", "（彼は細長い指で、受付の方角を指し示す。）", "", actor=pc) \
        .say("zek_3", "彼女が何と言ったかは知りませんが……あの女がその器で集めようとしているのは、単なる魔力ではありません。", "", actor=zek) \
        .say("zek_4", "そこに溜まるのは、あなたがた闘士の戦いが生み出した、魂の残滓……。彼女はそれを啜り、あなたをより効率的に『管理』しようとしているのですよ。……ふふ、お気づきでしたか？", "", actor=zek)

    # プレイヤーの選択肢
    builder.choice(react1_what, "……何が言いたい", "", text_id="c1_what") \
           .choice(react1_manage, "リリィに管理されているって？", "", text_id="c1_manage") \
           .choice(react1_silent, "（無言で聞く）", "", text_id="c1_silent")

    # 選択肢反応
    builder.step(react1_what) \
        .say("zek_r1", "おや、警戒心がおありで。では、単刀直入に申し上げましょう。", "", actor=zek) \
        .jump(scene2)

    builder.step(react1_manage) \
        .say("zek_r2", "ええ、そうです。彼女はサキュバス。獲物を支配し、魂をすすり喰らう存在なのですよ。", "", actor=zek) \
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
        .say("narr_6", "（見た目はリリィが作った共鳴瓶と瓜二つだが、そのガラスの奥には、澱んだどす黒い霧が渦巻いている。）", "", actor=pc) \
        .say("zek_5", "どうでしょう、一つ提案があります。", "", actor=zek) \
        .say("zek_6", "あの本物の器を盗み出し、私に譲ってはいただけませんか？代わりに、この『模造品』を棚に戻しておくのです。", "", actor=zek) \
        .say("narr_7", "（彼は偽物の器をあなたの前に差し出す。）", "", actor=pc) \
        .say("zek_7", "彼女は気づかないでしょう……。いえ、気づいた時には、彼女の『研究』はあなたの支配ではなく、私への捧げ物へとすり替わっている。", "", actor=zek) \
        .say("zek_8", "そしてあなたには、その誠実な裏切りの対価として、私が異次元のゴミ捨て場で拾い上げた珍品を差し上げましょう。……それと、特別な報酬も、ね。", "", actor=zek)

    # プレイヤーの選択肢
    builder.choice(react2_forbidden, "その珍品とは何だ？", "", text_id="c2_forbidden") \
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
        .say("narr_8", "（ゼクは「偽物の器」と報酬となる「禍々しい品」を並べ、あなたの返答を待つ。）", "", actor=pc) \
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
        .complete_quest(QuestIds.ZEK_STEAL_BOTTLE_REFUSE) \
        .finish()

    # 選択肢: 受諾
    builder.step(accept) \
        .say("zek_acc1", "ふふ、賢明な判断です。", "", actor=zek) \
        .say("narr_acc1", "（ゼクは満足げに偽物の器をあなたの手に握らせる。）", "", actor=pc) \
        .say("zek_acc2", "これがあなたへの報酬……**小さなコイン10枚**と**プラチナコイン3枚**を、台帳に記録する手はずを整えておきましょう。それと、この『影の印』を。", "", actor=zek) \
        .shake() \
        .say("zek_acc3", "これで、私の店での取引が、より『有利』になりますよ。……では、良い仕事を。彼女が寝静まった頃に、すり替えてきてくださいな。", "", actor=zek) \
        .say("narr_acc2", "（ゼクは影の中へと消えていく。）", "", actor=pc) \
        .cs_eval("for(int i=0; i<10; i++) { EClass.pc.Pick(ThingGen.Create(\"medal\")); } for(int i=0; i<3; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .jump(scene4_aftermath)

    # ========================================
    # シーン4: 事後の静寂（受諾した場合のみ）
    # ========================================
    builder.step(scene4_aftermath) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_aft1", "（深夜ーーリリィが休んでいる隙に、あなたは受付に忍び込み、棚の『共鳴瓶』を偽物とすり替えた。）", "", actor=pc) \
        .say("narr_aft2", "（本物の器はゼクの元へ。あなたの手には、澱んだ霧を宿す模造品だけが残った。）", "", actor=pc) \
        .say("narr_aft3", "（翌朝ーー）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_a1", "……あら、なんだか少し、器の感触が変わったかしら？", "", actor=lily) \
        .say("narr_aft4", "（彼女は棚の器を手に取り、軽く傾ける。一瞬、その瞳があなたを鋭く見つめるが、すぐに笑顔に戻る。）", "", actor=pc) \
        .say("lily_a2", "……まぁいいわ。これで私の研究は飛躍的に進みます。ふふ、感謝してくださいね。あなたが『使い物』にならなくなった後も、その響きだけは私の手元に残るのですから。", "", actor=lily) \
        .say("narr_aft5", "（彼女は気づいていないのか、それともーー）", "", actor=pc) \
        .jump(ending)

    # ========================================
    # 終了処理（受諾した場合のみここに到達）
    # ========================================
    builder.step(ending) \
        .complete_quest(QuestIds.ZEK_STEAL_BOTTLE_ACCEPT) \
        .finish()
