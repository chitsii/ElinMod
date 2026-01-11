"""
16_lily_real_name.md - リリィの告白『真名の刻印、永遠の共犯』
リリィが真名を明かし、運命を共にすることを誓う
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, FlagValues

def define_lily_real_name(builder: DramaBuilder):
    """
    リリィの真名
    シナリオ: 16_lily_real_name.md

    条件:
    - Lily relationship ≥ 20
    - Saved Balgas (scenario 15)
    - Didn't betray Lily with bottle swap (scenario 13)
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_meeting")
    choice1 = builder.label("choice1")
    react1_what = builder.label("react1_what")
    react1_want = builder.label("react1_want")
    react1_silent = builder.label("react1_silent")
    scene2 = builder.label("scene2_observer_end")
    choice2 = builder.label("choice2")
    react2_enchanted = builder.label("react2_enchanted")
    react2_me_too = builder.label("react2_me_too")
    react2_touch = builder.label("react2_touch")
    scene2_5 = builder.label("scene2_5_no_home")
    choice2_5 = builder.label("choice2_5")
    react2_5_hard = builder.label("react2_5_hard")
    react2_5_place = builder.label("react2_5_place")
    react2_5_hand = builder.label("react2_5_hand")
    scene2_5_cont = builder.label("scene2_5_cont")
    scene3 = builder.label("scene3_true_name")
    choice3 = builder.label("choice3")
    react3_tell = builder.label("react3_tell")
    react3_carry = builder.label("react3_carry")
    react3_nod = builder.label("react3_nod")
    name_revelation = builder.label("name_revelation")
    scene4 = builder.label("scene4_contract")
    final_choice = builder.label("final_choice")
    final_thanks = builder.label("final_thanks")
    final_protect = builder.label("final_protect")
    final_embrace = builder.label("final_embrace")
    ending = builder.label("ending")

    # ========================================
    # シーン1: 月光のない密会
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Lily_Private_Room") \
        .say("narr_1", "（激闘が終わり、静まり返ったアリーナの私室。）", "", actor=pc) \
        .say("narr_2", "（いつも以上に濃い紫煙が揺らめき、その奥でリリィはバルガスから贈られた古い酒瓶を愛おしそうに眺めていた。）", "", actor=pc) \
        .say("narr_3", "（あなたが部屋に入ると、彼女はゆっくりと立ち上がり、普段の事務的な仮面を完全に脱ぎ捨てた「一人の女」の顔で微笑んだ。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .focus_chara(Actors.LILY) \
        .say("lily_1", "……おかえりなさい。バルガスさんは、今頃泥のように眠っています。", "", actor=lily) \
        .say("lily_2", "あんなに安らかな寝顔を見たのは、私も初めてかもしれません。……ふふ、本当に、あなたという人は。", "", actor=lily) \
        .say("narr_4", "（彼女は酒瓶を置き、あなたに近づく。）", "", actor=pc) \
        .say("lily_3", "バルガスさんを助けてくれたこと、お礼を言わせてください。……でも、それは単なる『感謝』ではありません。", "", actor=lily) \
        .say("lily_4", "あなたが今日、あの残酷な喝采を黙らせた時……私の中で、何かが音を立てて崩れたのです。", "", actor=lily) \
        .jump(choice1)

    # プレイヤーの選択肢1
    builder.choice(react1_what, "……何が崩れたんだ？", "", text_id="c1_what") \
           .choice(react1_want, "お前は、俺に何を求めている？", "", text_id="c1_want") \
           .choice(react1_silent, "（無言で聞く）", "", text_id="c1_silent")

    # 選択肢反応1
    builder.step(react1_what) \
        .say("lily_r1", "私の……『観察者』としての仮面です。もう、あなたを冷静に見ることができません。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_want) \
        .say("lily_r2", "……全てです。あなたの全てを、私に委ねてほしい。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_silent) \
        .say("lily_r3", "……無口ですが、その瞳は饒舌ですね。続けさせていただきます。", "", actor=lily) \
        .jump(scene2)

    # ========================================
    # シーン2: 観察者の終焉
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Lily_Seductive_Danger") \
        .say("narr_5", "（リリィはあなたの至近距離まで歩み寄り、その冷たいはずの指先であなたの胸元に触れた。）", "", actor=pc) \
        .say("narr_6", "（そこには「黄金の戦鬼」としての力強い鼓動が刻まれている。）", "", actor=pc) \
        .say("lily_5", "私は、このアリーナに囚われた魂が、絶望に染まり、最後の一滴まで絞り出されるのを見届けるのが役割でした。", "", actor=lily) \
        .say("lily_6", "……あなたも、その一人になるはずだった。", "", actor=lily) \
        .say("lily_7", "けれど、あなたは強くなるほどに優しく、孤独になるほどに誰かの手を握ろうとした。", "", actor=lily) \
        .say("lily_8", "……その姿を特等席で眺めているうちに、私の方が、あなたの魂に『魅了』されてしまったようです。", "", actor=lily) \
        .jump(choice2)

    # プレイヤーの選択肢2
    builder.choice(react2_enchanted, "サキュバスなのに……？", "", text_id="c2_enchanted") \
           .choice(react2_me_too, "俺も、お前に魅了されている", "", text_id="c2_me_too") \
           .choice(react2_touch, "（無言で頬に触れる）", "", text_id="c2_touch")

    # 選択肢反応2
    builder.step(react2_enchanted) \
        .say("lily_r4", "ええ。サキュバスが、人間に魅了される……滑稽でしょう？", "", actor=lily) \
        .jump(scene2_5)

    builder.step(react2_me_too) \
        .say("lily_r5", "……！ あなた、そんな……。", "", actor=lily) \
        .say("narr_7", "（リリィは頬を染め、目を逸らす。）", "", actor=pc) \
        .jump(scene2_5)

    builder.step(react2_touch) \
        .say("lily_r6", "……あぁ、温かい。あなたの手は、いつも温かいですね。", "", actor=lily) \
        .jump(scene2_5)

    # ========================================
    # シーン2.5: 帰る場所のない者
    # ========================================
    builder.step(scene2_5) \
        .play_bgm("BGM/Lily_Confession") \
        .say("narr_nh1", "（リリィは窓辺に歩み寄り、次元の狭間に浮かぶ歪んだ景色を眺める。）", "", actor=pc) \
        .say("lily_nh1", "……ねえ、あなたは知っていますか？ 私がどこから来たのか。", "", actor=lily) \
        .say("lily_nh2", "私には『故郷』がないのです。他のサキュバスのように、どこかの確定次元で生まれ、そこから落ちてきたわけではありません。", "", actor=lily) \
        .say("lily_nh3", "私は……この次元の狭間そのもので生まれました。崩壊した世界の残滓、漂流する感情の欠片、そして『誰かに愛されたい』という無数の魂の願い……。それらが凝縮して、私という存在が生まれた。", "", actor=lily) \
        .say("lily_nh4", "だから私には、家族も、帰る場所もない。どこの世界にも属さない。本当の意味で、誰とも繋がっていない、と。……500年もの間、ずっとそう思って生きてきました。", "", actor=lily) \
        .jump(choice2_5)

    # プレイヤーの選択肢2.5
    builder.choice(react2_5_hard, "……それは、辛かっただろう", "", text_id="c2_5_hard") \
           .choice(react2_5_hand, "（無言で手を握る）", "", text_id="c2_5_hand")

    # 選択肢反応2.5
    builder.step(react2_5_hard) \
        .say("lily_nh_r1", "……ふふ、それが当たり前でしたから。だからこそ、私は、この闘技場での義務に忠実であることができた。", "", actor=lily) \
        .jump(scene2_5_cont)

    builder.step(react2_5_hand) \
        .say("lily_nh_r3", "……温かい。あなたの手は、いつも温かいですね……。", "", actor=lily) \
        .jump(scene2_5_cont)

    # シーン2.5続き
    builder.step(scene2_5_cont) \
        .say("lily_nh5", "あなたは違う。あなたには、イルヴァという帰る場所がある。神々との繋がりがあって、いつでもここを去ることができる。", "", actor=lily) \
        .say("lily_nh6", "……最初、それが羨ましく苛立たしかった。『どうせこの人も、いつかは帰るべき場所へ去っていく。私を置いて』と。", "", actor=lily) \
        .say("lily_nh7", "でも、あなたは一度去っても、また帰ってきてくれる。バルガスさんのために戦い、私のために怒り……。『義務』ではなく『選択』として、ここにいてくれる。", "", actor=lily) \
        .say("lily_nh8", "それが、どれほど私を救ったか……あなたには分からないでしょう。帰る場所がある人に、『それでも傍にいる』と選ばれること。それは、居場所のない私にとって、初めて与えられた『居場所』でした。", "", actor=lily) \
        .shake() \
        .say("narr_nh3", "（リリィは涙を流しながら、微笑む。）", "", actor=pc) \
        .jump(scene3)

    # ========================================
    # シーン3: 禁忌の真名
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Lily_Confession") \
        .say("narr_8", "（部屋の照明が一段と暗くなり、リリィの背中にある翼が、意思を持つかのように微かに震える。）", "", actor=pc) \
        .say("narr_9", "（彼女は意を決したように、あなたの耳元に唇を寄せた。）", "", actor=pc) \
        .say("lily_9", "……これからお話しするのは、この世界のどこにも記録されていない、私の本当の名前。", "", actor=lily) \
        .say("lily_10", "アスタロト様すら知らない……私の魂の、一番奥にある『鍵』。", "", actor=lily) \
        .say("lily_11", "これを知る者は、私の全てを支配し、同時に私の運命を一生背負うことになります。……あなたに知っておいてもらいたいのです。", "", actor=lily) \
        .jump(choice3)

    # プレイヤーの選択肢3（重要）
    builder.choice(react3_tell, "……聞かせてくれ", "", text_id="c3_tell") \
           .choice(react3_carry, "お前の全てを、背負わせてくれ", "", text_id="c3_carry") \
           .choice(react3_nod, "（無言で頷く）", "", text_id="c3_nod")

    # 選択肢反応3
    builder.step(react3_tell) \
        .say("lily_r7", "……ふふ、やっぱり、あなたはそう言ってくれるのですね。", "", actor=lily) \
        .jump(name_revelation)

    builder.step(react3_carry) \
        .say("narr_11", "（リリィは涙を流し、微笑む。）", "", actor=pc) \
        .jump(name_revelation)

    builder.step(react3_nod) \
        .say("lily_r9", "……無口ですが、その瞳は真剣ですね。では、お伝えします。", "", actor=lily) \
        .jump(name_revelation)

    # 真名の啓示
    builder.step(name_revelation) \
        .say("lily_12", "……私の名は、『リリアリス・ヴォイド・テンプテイション』。", "", actor=lily) \
        .shake() \
        .say("lily_14", "これからは、単なるあなたのマネージャーとしてではなく……", "", actor=lily) \
        .say("lily_15", "あなたの行く末を地獄の果てまで共にする、『共犯者』として隣に置かせてちょうだい。", "", actor=lily) \
        .jump(scene4)

    # ========================================
    # シーン4: 契約の接吻
    # ========================================
    builder.step(scene4) \
        .say("narr_13", "（彼女の真名が告げられた瞬間、あなたの視界に未知のルーンが浮かび上がり、リリィの魔力があなたの体内に流れ込んでくる。）", "", actor=pc) \
        .shake() \
        .say("narr_14", "（それは契約であり、守護であり、深い愛情の証だった。）", "", actor=pc) \
        .say("lily_16", "……ふふ、これで逃げられなくなりましたね。", "", actor=lily) \
        .say("lily_17", "アスタロト様の待つ頂上で、何が起きようとも……あなたの背中は私が守ります。", "", actor=lily) \
        .say("narr_15", "（リリィはあなたの頬に手を添え、優しく口づけをする。）", "", actor=pc) \
        .shake() \
        .say("lily_18", "さあ、行きましょう。あなたの伝説に、私の名前を添えて。", "", actor=lily) \
        .jump(final_choice)

    # 最終選択肢
    builder.choice(final_thanks, "……ありがとう、リリアリス", "", text_id="c_final_thanks") \
           .choice(final_protect, "お前を、必ず守る", "", text_id="c_final_protect") \
           .choice(final_embrace, "（抱きしめる）", "", text_id="c_final_embrace")

    builder.step(final_thanks) \
        .say("lily_r10", "その名で呼ばれるのは、初めてです。……嬉しいわ。", "", actor=lily) \
        .jump(ending)

    builder.step(final_protect) \
        .say("lily_r11", "ふふ、守るのは私の役目ですよ。でも……ありがとう。", "", actor=lily) \
        .jump(ending)

    builder.step(final_embrace) \
        .say("lily_r12", "……あぁ、温かい。あなたの温もりが、私を満たしてくれる……。", "", actor=lily) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .set_flag(Keys.LILY_TRUE_NAME, FlagValues.LilyTrueName.KNOWN) \
        .say("sys_buff", "【システム】『真名の絆』を獲得しました。魔力+10、精神耐性+20、魅了耐性+20 の加護を得た！", "") \
        .say("sys_title", "【システム】称号『リリアリスの伴侶』を獲得しました。", "") \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantLilyRealNameBonus();") \
        .finish()
