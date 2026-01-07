"""
17_vs_grandmaster_1.md - 虚空の王、静寂の断罪：影の介入
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, FlagValues

def define_vs_grandmaster_1(builder: DramaBuilder):
    """
    最終試練：アスタロトとの初遭遇、ゼクによる救出
    シナリオ: 17_vs_grandmaster_1.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    astaroth = builder.register_actor(Actors.ASTAROTH, "アスタロト", "Astaroth")
    zek = builder.register_actor(Actors.ZEK, "ゼク", "Zek")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_descent")
    scene2 = builder.label("scene2_killing_intent")
    scene3 = builder.label("scene3_intervention")
    scene4 = builder.label("scene4_escape")
    scene5 = builder.label("scene5_hideout")
    choice1 = builder.label("choice1")
    react1_proceed = builder.label("react1_proceed")
    react1_unforgivable = builder.label("react1_unforgivable")
    react1_kain = builder.label("react1_kain")
    ending = builder.label("ending")

    # ========================================
    # シーン1: 王の降臨
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Astaroth_Theme") \
        .say("narr_1", "（闘技場の空が、墨を流したように真っ黒に染まる。）", "", actor=pc) \
        .say("narr_2", "（観客の声は一瞬で消え失せ、代わりにこの世のものとは思えない巨大な『心音』が次元全体を揺さぶり始めた。）", "", actor=pc) \
        .shake() \
        .say("narr_3", "（王座の間に続く大扉が粉々に砕け散り、そこから、背中に巨大な紅蓮の翼を湛えた男——グランドマスター・アスタロトが、重力を無視してゆっくりと降り立つ。）", "", actor=pc) \
        .say("narr_4", "（彼が地を踏んだ瞬間、床の石畳が恐怖に震えるように粉砕された。）", "", actor=pc) \
        .shake() \
        .say("astaroth_1", "……なるほど。これが私の庭を騒がせている『特異点』か。", "", actor=astaroth) \
        .say("astaroth_2", "バルガスの命を救い、サキュバスに真名を吐かせ……あまつさえ、このアリーナの『理』を塗り替えようとするとは。", "", actor=astaroth) \
        .say("astaroth_3", "面白い。実に面白いぞ、人間よ。", "", actor=astaroth) \
        .jump(scene2)

    # ========================================
    # シーン2: 静かなる殺意
    # ========================================
    builder.step(scene2) \
        .say("narr_5", "（アスタロトは、絶望に震えるリリィと、彼女を庇って前に出るバルガスを一瞥し、嘲笑するように鼻を鳴らした。）", "", actor=pc) \
        .say("astaroth_4", "リリィ……お前が愛したその人間は、もはやお前の手には負えぬバケモノだ。", "", actor=astaroth) \
        .say("astaroth_5", "そしてバルガス、老いさらばえた敗残兵の分際で、運命の書き換えを許したか。", "", actor=astaroth) \
        .say("astaroth_6", "……よかろう。システムの不備は、私の手で『焼却』し、無に帰すのが王の責務だ。", "", actor=astaroth) \
        .say("narr_6", "（アスタロトが右手を掲げると、その周囲に凝縮された虚空の炎が渦巻く。）", "", actor=pc) \
        .say("astaroth_7", "さらばだ。輝かしいバグ（英雄）よ。お前の物語は、ここで『なかったこと』になる。", "", actor=astaroth) \
        .jump(scene3)

    # ========================================
    # シーン3: 断罪の炎と、影の道具
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_7", "（アスタロトの放った『虚空のブレス』が、次元そのものを焼き尽くさんばかりの勢いであなたに迫る。）", "", actor=pc) \
        .shake() \
        .say("narr_8", "（回避も防御も不可能な、概念的な死。）", "", actor=pc) \
        .say("narr_9", "（リリィが叫び、バルガスが叫ぶ。その直前——。）", "", actor=pc) \
        .say("narr_10", "（空間がガラスのようにパリンと音を立てて割れ、あなたの目の前に、ゼクがひょっこりと現れた。）", "", actor=pc) \
        .say("narr_11", "（その手には、不気味に明滅し、バグったように色彩が反転し続ける立方体——**『因果の断片（パラドックス・キューブ）』**が握られていた。）", "", actor=pc) \
        .say("zek_1", "おっと……！ 王様、あまり急いではいけません。", "", actor=zek) \
        .say("zek_2", "私の最高級のコレクションが灰になっては、商売あがったりですからね！", "", actor=zek) \
        .say("narr_12", "（ゼクがキューブを起動させると、アスタロトの炎があなたを通り抜け、まるで『そこには誰もいない』かのように虚空へ消えていく。）", "", actor=pc) \
        .jump(scene4)

    # ========================================
    # シーン4: 影の救済と撤退
    # ========================================
    builder.step(scene4) \
        .say("narr_13", "（ゼクは冷や汗を流しながらも、不敵な笑みを浮かべてアスタロトを見上げる。）", "", actor=pc) \
        .say("narr_14", "（キューブの周りでは、数式やノイズが乱舞し、あなたたちの存在を一時的に『世界の演算』から切り離していた。）", "", actor=pc) \
        .say("astaroth_8", "……ゼクか。ゴミ拾いの分際で、この私の『確定した死』を歪めたか。", "", actor=astaroth) \
        .say("zek_3", "クク……歪めたのではありません。少しだけ『ページを飛ばした』のですよ。", "", actor=zek) \
        .say("zek_4", "さあ、闘士殿！ リリィもバルガスも連れて、私の影に飛び込みなさい！", "", actor=zek) \
        .say("zek_5", "この道具が保つのはあと数秒だ。アスタロトを倒すための『本当の力』、それを手に入れる猶予を……私が無理やり作ってあげましょう！", "", actor=zek) \
        .say("narr_15", "（あなたはバルガスとリリィを連れて、ゼクの影の中へ飛び込む。）", "", actor=pc) \
        .say("narr_16", "（背後からアスタロトの怒号に近い咆哮が聞こえるが、視界は瞬時に暗転した。）", "", actor=pc) \
        .jump(scene5)

    # ========================================
    # シーン5: 次元のゴミ捨て場
    # ========================================
    builder.step(scene5) \
        .play_bgm("BGM/Zek_Hideout") \
        .say("narr_17", "（辿り着いたのは、アリーナのロビーでも私室でもない、無数のガラクタと遺品が積み上がった不気味な異空間——ゼクの本拠地だった。）", "", actor=pc) \
        .say("narr_18", "（バルガスが激しく咳き込み、リリィが膝をついて震えている。）", "", actor=pc) \
        .say("narr_19", "（薄暗い空間の奥に、無数の『展示台』が並んでいる。そこに置かれているのは、ガラスケースに封じられた『瞬間』の数々。）", "", actor=pc) \
        .say("narr_20", "（ある戦士は、剣を掲げたまま絶望の表情で凍りついている。その顔には、『なぜ俺が……』という最期の疑問が刻まれたまま。）", "", actor=pc) \
        .say("narr_21", "（ある魔術師は、魔導書を抱きしめ、涙を流したまま時が止まっている。その指先には、唱えきれなかった最後の呪文の残滓が漂う。）", "", actor=pc) \
        .say("narr_22", "（ある盗賊は、仲間の死体にすがりつき、狂ったように笑い続けている。その笑顔は、正気を失った瞬間を永遠に閉じ込められた地獄。）", "", actor=pc) \
        .say("narr_23", "（ガラスケースの一つに、見覚えのある鎧が展示されている。——それは、あなたがRank Eで倒した『錆びついた英雄・カイン』の残骸だ。）", "", actor=pc) \
        .say("narr_24", "（彼の表情は、最期の安堵と、それでも消えない後悔が混じり合っていた。）", "", actor=pc) \
        .say("balgas_1", "……クソが。あいつら全員、ゼクの『作品』かよ。", "", actor=balgas) \
        .say("balgas_2", "こいつは博物館なんかじゃねえ。……英雄の墓場を、趣味で飾り立ててやがる。", "", actor=balgas) \
        .say("lily_1", "……酷い。これは、魂の冒涜よ。", "", actor=lily) \
        .say("lily_2", "彼らは死後も、こんな場所で……永遠に『最悪の瞬間』を演じ続けさせられている……。", "", actor=lily) \
        .say("zek_6", "……ふぅ。命拾いしましたね。", "", actor=zek) \
        .say("zek_7", "今のあなたは、アスタロトにとっては『目障りな不具合』に過ぎない。彼を殺すには……システムの外側にある力、**『レベル1億の深淵』**の力を引き出すしかありません。", "", actor=zek) \
        .say("zek_8", "さあ、ここからが本当の『取引』の始まりです。王を殺すための武器。そして、この呪われたアリーナの真実。", "", actor=zek) \
        .say("zek_9", "……それらを手に入れる覚悟があるなら、このゴミの山をさらに奥へ進んでいただきましょうか。", "", actor=zek) \
        .jump(choice1)

    # プレイヤーの選択肢
    builder.choice(react1_proceed, "……分かった。進もう", "", text_id="c1_proceed") \
           .choice(react1_unforgivable, "お前のコレクション……許せない", "", text_id="c1_unforgivable") \
           .choice(react1_kain, "カインを……解放しろ", "", text_id="c1_kain")

    # 選択肢反応
    builder.step(react1_proceed) \
        .say("zek_r1", "ふふ、素直ですこと。では、こちらへどうぞ。", "", actor=zek) \
        .jump(ending)

    builder.step(react1_unforgivable) \
        .say("zek_r2", "許さなくて結構。ですが、今はアスタロトを倒すことが先決でしょう？", "", actor=zek) \
        .jump(ending)

    builder.step(react1_kain) \
        .say("zek_r3", "……ふむ。それは、アスタロトを倒した後で考えましょう。今は無理です。", "", actor=zek) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .set_flag(Keys.FUGITIVE, FlagValues.TRUE) \
        .finish()
