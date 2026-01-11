"""
08_lily_private.md - 紫煙と観察者の深淵
リリィの私室での親密なイベント
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, QuestIds

def define_lily_private(builder: DramaBuilder):
    """
    リリィの私室
    シナリオ: 08_lily_private.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_invitation")
    choice1 = builder.label("choice1")
    react1_accept = builder.label("react1_accept")
    react1_scheme = builder.label("react1_scheme")
    react1_nod = builder.label("react1_nod")
    scene2 = builder.label("scene2_private_room")
    choice2 = builder.label("choice2")
    react2_no = builder.label("react2_no")
    react2_tasty = builder.label("react2_tasty")
    react2_silent = builder.label("react2_silent")
    scene3 = builder.label("scene3_observation")
    choice3 = builder.label("choice3")
    react3_ok = builder.label("react3_ok")
    react3_rest = builder.label("react3_rest")
    react3_watch = builder.label("react3_watch")
    scene4 = builder.label("scene4_farewell")
    choice4 = builder.label("choice4")
    react4_thanks = builder.label("react4_thanks")
    react4_again = builder.label("react4_again")
    react4_nod = builder.label("react4_nod")
    ending = builder.label("ending")

    # ========================================
    # シーン1: カウンター越しの視線
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_1", "（戦いの傷を癒し、戦果を報告しに受付へ向かったあなた。）", "", actor=pc) \
        .say("narr_2", "（リリィはいつものように書類を整理しているが、その動きはどこか緩慢だ。）", "", actor=pc) \
        .say("narr_3", "（彼女の細長い瞳が、あなたの全身を這うように舐め回す。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .focus_chara(Actors.LILY) \
        .say("lily_1", "……おかえりなさい。", "", actor=lily) \
        .say("lily_2", "観客席からの『供物』で、少しばかり身だしなみが乱れているようですね。ふふ、でも……今のあなたからは、とても複雑で、芳醇な香りがします。", "", actor=lily) \
        .say("narr_4", "（彼女は羽根ペンを置き、あなたに近づく。）", "", actor=pc) \
        .say("lily_3", "絶望と、不屈。そして、ほんの少しの『殺意』が混じり合った、熟成した魂の匂い。", "", actor=lily) \
        .say("lily_4", "……バルガスの酒臭い怒声が響くこの場所では、その香りを十分に楽しめません。少し、私の『私室』へいらっしゃいませんか？", "", actor=lily) \
        .say("lily_5", "仕事の話ではありません。ただ、観察者として……あなたのその魂を、もう少し近くで愛でたいのです。", "", actor=lily)

    # プレイヤーの選択肢1
    builder.choice(react1_accept, "……分かった。行こう", "", text_id="c1_accept") \
           .choice(react1_scheme, "何か企んでいるのか？", "", text_id="c1_scheme") \
           .choice(react1_nod, "（無言で頷く）", "", text_id="c1_nod")

    # 選択肢反応1
    builder.step(react1_accept) \
        .say("lily_r1", "ふふ、素直ですこと。では、こちらへどうぞ。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_scheme) \
        .say("lily_r2", "まあ、警戒心がおありで。ご心配なく、ただの社交ですよ。……多分。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_nod) \
        .say("lily_r3", "……無口ですが、了承はしていただけたようですね。どうぞ、ついてきてください。", "", actor=lily) \
        .jump(scene2)

    # ========================================
    # シーン2: サキュバスの私室
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Lily_Private_Room") \
        .say("narr_5", "（ロビーの裏手にある重厚な黒檀の扉。そこを潜った瞬間、大気の重さが変わる。）", "", actor=pc) \
        .say("narr_6", "（部屋全体を支配するのは、甘美でありながら肺の奥を痺れさせるような「紫煙」の香。）", "", actor=pc) \
        .say("narr_7", "（床には柔らかな魔獣の毛皮が敷き詰められ、壁には異次元の珍奇な書物や、何かの魂が閉じ込められたと思わしき脈打つ宝石が飾られている。）", "", actor=pc) \
        .say("narr_8", "（リリィは、毒々しいほど鮮やかなソファに深く腰掛け、事務服の襟元をわずかに緩めた。）", "", actor=pc) \
        .say("lily_6", "さあ、遠慮なさらず。", "", actor=lily) \
        .say("lily_7", "ここはアリーナの法則からも、神々の視線からも隔絶された場所。", "", actor=lily) \
        .say("lily_8", "……今のあなたの戦い、実に滑稽で、そして美しかったわ。落下物に翻弄されながらも、その瞳から光が消えなかった。", "", actor=lily) \
        .say("lily_9", "……あの瞬間、あなたの魂がどれほど甘く弾けたか、自覚はありますか？", "", actor=lily)

    # プレイヤーの選択肢2
    builder.choice(react2_no, "……自覚はない", "", text_id="c2_no") \
           .choice(react2_tasty, "俺の魂がそんなに美味しそうか？", "", text_id="c2_tasty") \
           .choice(react2_silent, "（無言で聞く）", "", text_id="c2_silent")

    # 選択肢反応2
    builder.step(react2_no) \
        .say("lily_r4", "ふふ、そうでしょうね。当事者は気づかないものです。", "", actor=lily) \
        .jump(scene3)

    builder.step(react2_tasty) \
        .say("lily_r5", "ええ。……とても。食べてしまいたいくらいに。", "", actor=lily) \
        .jump(scene3)

    builder.step(react2_silent) \
        .say("lily_r6", "……無口ですが、その瞳は饒舌ですね。", "", actor=lily) \
        .jump(scene3)

    # ========================================
    # シーン3: 観察と誘惑（捕食者の本能）
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Lily_Seductive_Danger") \
        .say("narr_9", "（リリィは指先を唇に当て、クスクスと喉を鳴らす。）", "", actor=pc) \
        .say("narr_10", "（彼女の尻尾が、まるで生き物のようにあなたの足首に絡みついた。）", "", actor=pc) \
        .say("lily_10", "……あなたは不思議な人。", "", actor=lily) \
        .say("lily_11", "多くの闘士は、ランクDに上がる頃には心が擦り切れて、ただの戦う機械になる。けれど、あなたからは『意志』の拍動が聞こえるの。", "", actor=lily) \
        .say("narr_11", "（サキュバスの本能が、抑えきれずに漏れ出す。）", "", actor=pc) \
        .say("lily_12", "……ねえ、一つ教えて。あなたは、どこまで登るつもり？その魂が完全に磨き上げられ、最高級の宝石になった時……", "", actor=lily) \
        .say("lily_13", "それを最初に手にするのは、私であってもいいかしら？", "", actor=lily) \
        .say("narr_12", "（あなたは彼女の吐息に、甘美でありながら危険な「何か」を感じ取る。——それは、捕食者の本能。）", "", actor=pc) \
        .shake() \
        .say("lily_14", "……ふふ、冗談よ。怖がらないで。", "", actor=lily) \
        .say("narr_13", "（彼女は一歩下がるが、その手は微かに震えている。）", "", actor=pc) \
        .say("lily_mono1", "（……だめ。この人は、『商品』じゃない。『観察対象』じゃない。）", "", actor=lily) \
        .say("lily_mono2", "（でも……この香り。この、熟した魂の甘い香り。……ああ、食べたい。喰らいたい。あなたの全てを、この牙で噛み砕いて、永遠に私の中に……）", "", actor=lily) \
        .say("narr_14", "（リリィは自分の唇を噛み、その衝動を必死に抑え込む。彼女の尻尾が、苦しげに床を叩いた。）", "", actor=pc) \
        .say("lily_15", "……ごめんなさい。少し、気分が……。", "", actor=lily) \
        .say("lily_16", "サキュバスにとって、『美味しそうな魂』を前にして我慢するのは……拷問に近いの。でも、あなたを傷つけたくない。……これは、初めての感覚。", "", actor=lily)

    # プレイヤーの選択肢3
    builder.choice(react3_ok, "大丈夫か？", "", text_id="c3_ok") \
           .choice(react3_rest, "無理をするな", "", text_id="c3_rest") \
           .choice(react3_watch, "（静かに見守る）", "", text_id="c3_watch")

    # 選択肢反応3
    builder.step(react3_ok) \
        .say("lily_r7", "……ええ、大丈夫です。少し、驚いただけ。", "", actor=lily) \
        .jump(scene4)

    builder.step(react3_rest) \
        .say("lily_r8", "……ありがとう。でも、私は大丈夫。……多分。", "", actor=lily) \
        .jump(scene4)

    builder.step(react3_watch) \
        .say("lily_r9", "……あなた、本当に優しいのですね。", "", actor=lily) \
        .jump(scene4)

    # ========================================
    # シーン4: 別れの接吻（バフ付与）
    # ========================================
    builder.step(scene4) \
        .play_bgm("BGM/Lily_Tranquil") \
        .say("narr_15", "（彼女は立ち上がり、至近距離まで顔を近づける。）", "", actor=pc) \
        .say("narr_16", "（サキュバス特有の、抗いがたい魔力の波動があなたを包み込んだ。）", "", actor=pc) \
        .say("lily_17", "……ふふ、今の質問の答えは、もっと先で聞かせてもらうことにしましょう。", "", actor=lily) \
        .say("lily_18", "これは、私のお気に入りの『観察対象』への投資です。次からも、もっと美味しい絶望と勝利を私に見せてくださいね。", "", actor=lily) \
        .say("narr_17", "（リリィがあなたの額に指先を触れる。瞬間、全身の疲労が霧散し、魔力が底から溢れ出すような感覚に陥る。）", "", actor=pc) \
        .shake() \
        .say("lily_19", "……これは、私からのささやかな贈り物。少しの間、あなたの力を高めてあげますよ。", "", actor=lily)

    # プレイヤーの選択肢4
    builder.choice(react4_thanks, "……ありがとう", "", text_id="c4_thanks") \
           .choice(react4_again, "次も来てもいいか？", "", text_id="c4_again") \
           .choice(react4_nod, "（無言で頷く）", "", text_id="c4_nod")

    # 選択肢反応4
    builder.step(react4_thanks) \
        .say("lily_r10", "ふふ、どういたしまして。……またいらしてくださいね。", "", actor=lily) \
        .jump(ending)

    builder.step(react4_again) \
        .say("lily_r11", "……ええ。もちろん。あなたなら、いつでも歓迎いたします。", "", actor=lily) \
        .jump(ending)

    builder.step(react4_nod) \
        .say("lily_r12", "……無口ですが、気持ちは伝わりましたよ。", "", actor=lily) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .complete_quest(QuestIds.LILY_PRIVATE) \
        .say("sys_buff", "【システム】『リリィの寵愛』を獲得しました。魔力+5、回避+5、魅了耐性+10 の加護を得た！", "") \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantLilyPrivateBonus();") \
        .finish()
