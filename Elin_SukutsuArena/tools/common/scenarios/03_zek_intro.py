"""
03_zek.md - 影歩きの邂逅
ゼクとの初遭遇イベント
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, QuestIds

def define_zek_intro(builder: DramaBuilder):
    """
    ゼクとの初遭遇イベント
    シナリオ: 03_zek.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")
    zek = builder.register_actor(Actors.ZEK, "ゼク", "Zek")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_lobby_anomaly")
    scene2 = builder.label("scene2_introduction")
    react_who = builder.label("react_who")
    react_merchant = builder.label("react_merchant")
    react_silent = builder.label("react_silent")
    scene3 = builder.label("scene3_forbidden_offer")
    price_ask = builder.label("price_ask")
    price_refuse = builder.label("price_refuse")
    price_consider = builder.label("price_consider")
    scene4 = builder.label("scene4_return_shadow")
    balgas_reaction = builder.label("balgas_reaction")
    lily_reaction = builder.label("lily_reaction")
    ending = builder.label("ending")

    # ========================================
    # シーン1: ロビーの異変
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Ominous_Suspense_01") \
        .say("narr_1", "（ロビーの喧騒が、突如として膜を隔てたかのように遠のく。バルガスの怒声も、リリィのペンが紙を削る音も、水の底に沈んだように遠い。）", "", actor=pc) \
        .say("narr_2", "（ロビーの北西の隅、瓦礫が積み上がった影が、生き物のように蠢き始めた。）", "", actor=pc) \
        .shake() \
        .say("narr_3", "（空間がガラスのように鋭くひび割れ、その亀裂から、煤けたぼろ布を幾重にも纏った長身の影が滑り出す。）", "", actor=pc) \
        .say("narr_4", "（男が踏み出す足跡からは、黒い霧のような魔力の残滓が立ち上り、一瞬で消えていく。周囲の温度が数度下がり、肌を刺すような違和感がその場の空気を支配した。）", "", actor=pc) \
        .jump(scene1)

    # ========================================
    # シーン1: ゼク登場
    # ========================================
    builder.step(scene1) \
        .focus_chara(Actors.ZEK) \
        .say("zek_1", "……おや。失礼、驚かせるつもりはなかったのですよ。", "", actor=zek) \
        .say("zek_2", "ただ、あまりに芳しい『敗北の予感』が漂ってきたもので……。つい、こちらへ顔を出してしまいました。", "", actor=zek) \
        .say("narr_5", "（彼は優雅に、しかしどこか爬虫類を思わせる動作で一礼する。）", "", actor=pc) \
        .jump(scene2)

    # ========================================
    # シーン2: 商人の自己紹介
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Zek_Merchant") \
        .say("narr_6", "（ゼクは懐から、何か金属的な物体を取り出し、軽く弄ぶ。それは、錆びついた懐中時計のようにも、歪んだ魔導具のようにも見える。）", "", actor=pc) \
        .say("zek_3", "お初にお目に掛かります、若き闘士殿。私はゼク……この虚無の狭間で、行き場を失った『価値ある遺物』を拾い集める、しがない商人に過ぎません。", "", actor=zek) \
        .say("zek_4", "バルガスのように、あなたの肉体を試すような無作法はいたしません。私はただ、あなたの行く先に待つ『絶望』を、少しだけ華やかなものに変えるお手伝いをしたいだけなのです……ふふ。", "", actor=zek)

    # プレイヤーの選択肢
    builder.choice(react_who, "……お前は何者だ？", "", text_id="c_who") \
           .choice(react_merchant, "商人だと？ ここで何を売っているんだ", "", text_id="c_merchant") \
           .choice(react_silent, "（無言で警戒する）", "", text_id="c_silent")

    # 選択肢反応: お前は何者だ？
    builder.step(react_who) \
        .say("zek_r1", "ふふ、警戒心がおありで結構。ですが、私はただの商人。あなたに害を加える気など、毛頭ございませんよ。……少なくとも、今は。", "", actor=zek) \
        .jump(scene3)

    # 選択肢反応: 商人だと？
    builder.step(react_merchant) \
        .say("zek_r2", "おや、興味をお持ちで？ では、ご覧に入れましょう。この世界の果てで、命を繋ぐための『道具』を。", "", actor=zek) \
        .jump(scene3)

    # 選択肢反応: 無言で警戒
    builder.step(react_silent) \
        .say("zek_r3", "……ほう。言葉少なに、しかし鋭い視線。あなたの本能が、私を『危険』だと囁いているのでしょうね。賢明です。", "", actor=zek) \
        .jump(scene3)

    # ========================================
    # シーン3: 禁忌の誘い
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_7", "（ゼクが長い指先を虚空で躍らせると、空間の裂け目から禍々しいオーラを放つ品々が浮かび上がる。）", "", actor=pc) \
        .say("narr_8", "（焼けただれた魔導書、ページが勝手にめくれ、奇妙な文字が光る。不規則に脈打つ肉塊、まるで心臓のように拍動している。毒々しく発光する薬瓶、中の液体が泡立っている。）", "", actor=pc) \
        .say("zek_5", "次なるランクF……『泥犬』への試練。そこには、あなたの体温を根こそぎ奪い去る『凍てつく魔物』が待ち構えている。", "", actor=zek) \
        .say("zek_6", "地上の安っぽい防具では、魂まで凍り付いてしまうでしょう。……ああ、想像できますよ。あなたが氷漬けになり、そのまま観客たちの冷笑の中で砕け散る様が。", "", actor=zek) \
        .say("zek_7", "どうでしょう、この薬……名は『業火の接吻』。飲めば血潮が沸き立ち、氷をも溶かす力を得られます。", "", actor=zek) \
        .say("zek_8", "……もっとも、引き換えに、あなたの『運命（カルマ）』を少しばかりこのアリーナの糧としていただくことになりますが。命を落とす不条理に比べれば、安い対価だと思いませんか？", "", actor=zek)

    # プレイヤーの選択肢
    builder.choice(price_ask, "代償とは、具体的には？", "", text_id="c_price_ask") \
           .choice(price_refuse, "怪しすぎる。断る", "", text_id="c_price_refuse") \
           .choice(price_consider, "……考えておく", "", text_id="c_price_consider")

    # 選択肢反応: 代償とは？
    builder.step(price_ask) \
        .say("zek_p1", "ふふ、慎重なこと。ええ、あなたの運が少し悪くなる程度です。……まあ、『少し』がどの程度かは、使ってみてのお楽しみということで。", "", actor=zek) \
        .jump(scene4)

    # 選択肢反応: 断る
    builder.step(price_refuse) \
        .say("zek_p2", "おや、残念。ですが、無理強いはいたしません。……いつでもお声掛けくださいませ。あなたが『絶望』を前にした時、私の品が恋しくなるでしょうから。", "", actor=zek) \
        .jump(scene4)

    # 選択肢反応: 考えておく
    builder.step(price_consider) \
        .say("zek_p3", "賢明な判断です。焦る必要はございません。私は常に、影の中で待っておりますから。", "", actor=zek) \
        .jump(scene4)

    # ========================================
    # シーン4: 影への帰還
    # ========================================
    builder.step(scene4) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("zek_9", "さあ、賢明な選択を。私は常に、この歪んだ影の中に潜んでおりますよ。", "", actor=zek) \
        .say("zek_10", "あなたが『力』を、あるいは『救い』を求めたくなったら……いつでもお声掛けください。あなたの魂が、完熟した果実のように弾けるその時まで、ね。", "", actor=zek) \
        .say("narr_9", "（ゼクの姿が薄れ、影に溶けるように消えていく。空間の裂け目が閉じ、ロビーの喧騒が一気に戻る。まるで、先ほどの出来事が幻だったかのように。）", "", actor=pc) \
        .jump(balgas_reaction)

    # ========================================
    # バルガスの反応
    # ========================================
    builder.step(balgas_reaction) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_1", "……ゼクの野郎と話しやがったか。", "", actor=balgas) \
        .say("balgas_2", "あいつから物を買うのは、悪魔に魂の切り売りをしてるのと同じだ。……まぁ、勝てば官軍だがな。せいぜい、干からびる前に使い倒してやれ。", "", actor=balgas) \
        .say("balgas_3", "ただな……あいつは『力』を売ってるんじゃねえ。『絶望の瞬間』を集めてやがるんだ。お前が最期に何を感じるか、それを観察してやがる。……気をつけろよ。", "", actor=balgas) \
        .jump(lily_reaction)

    # ========================================
    # リリィの反応
    # ========================================
    builder.step(lily_reaction) \
        .focus_chara(Actors.LILY) \
        .say("lily_1", "ゼクと話をされたのですね。", "", actor=lily) \
        .say("lily_2", "……彼は、このアリーナでも特別な存在です。グランドマスターですら、彼を完全には制御できていません。", "", actor=lily) \
        .say("lily_3", "ただ、彼の品が闘士の生存率を上げているのも事実。……使うか使わないかは、あなた次第ですが。", "", actor=lily) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .complete_quest(QuestIds.ZEK_INTRO) \
        .set_flag(Keys.REL_ZEK, 10) \
        .finish()
