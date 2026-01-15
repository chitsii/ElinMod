# -*- coding: utf-8 -*-
"""
12_makuma.md - 銀翼を彩る背徳の衣、そして遺棄された真実
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, FlagValues, QuestIds


def define_makuma(builder: DramaBuilder):
    """
    ランクB達成報酬：リリィの礼装授与とゼクによるヌルの真実暴露
    シナリオ: 12_makuma.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    zek = builder.register_actor(Actors.ZEK, "ゼク", "Zek")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_lily_gift")
    choice1 = builder.label("choice1")
    react1_thanks = builder.label("react1_thanks")
    react1_property = builder.label("react1_property")
    react1_silent = builder.label("react1_silent")
    scene2 = builder.label("scene2_zek_appears")
    choice2 = builder.label("choice2")
    react2_failure = builder.label("react2_failure")
    react2_adventurer = builder.label("react2_adventurer")
    react2_silent = builder.label("react2_silent")
    scene3 = builder.label("scene3_null_truth")
    choice4 = builder.label("choice4")
    react4_bored = builder.label("react4_bored")
    react4_scared = builder.label("react4_scared")
    react4_defiant = builder.label("react4_defiant")
    scene3_continue = builder.label("scene3_continue")
    choice3 = builder.label("choice3")
    react3_wait = builder.label("react3_wait")
    react3_become = builder.label("react3_become")
    react3_stare = builder.label("react3_stare")
    scene4 = builder.label("scene4_balgas")
    ending = builder.label("ending")

    # ========================================
    # シーン1: リリィの作業室『次元固定装置のメンテナンス』
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Lily_Seductive") \
        .focus_chara(Actors.LILY) \
        .say("narr_1", "（リリィの作業室。普段の甘い香りはなく、代わりに金属とエーテルの匂いが漂っている。）", "", actor=pc) \
        .say("narr_2", "（彼女は机の上に分解された魔道具の部品を並べ、細かな調整を行っていた。）", "", actor=pc) \
        .say("narr_3", "（それは複雑な魔術回路が刻まれた球体状の装置ーーアリーナという異次元空間を維持するための『次元固定装置』の一部だった。）", "", actor=pc) \
        .say("lily_1", "……あら、いらっしゃい。少し待っていて。今、繊細な調整中なの。", "", actor=lily) \
        .say("narr_4", "（リリィは集中しながらも、あなたの存在を意識するように髪をかきあげた。）", "", actor=pc) \
        .say("lily_2", "これはね、アリーナという空間そのものを維持する装置よ。この次元は本来、不安定で存在できないはずの場所。それを『在る』ものとして固定しているの。……私の担当なの。", "", actor=lily) \
        .say("lily_2b", "……ねえ、もう少し近くに来て？ あなたの体温を感じていたいの。この部屋、少し冷えるから。", "", actor=lily) \
        .say("lily_3", "さて……あなたの戦績、確認しましたよ。最初に比べて、動きの質が変わったわね。以前は荒削りだったけれど、今は無駄がない。", "", actor=lily) \
        .say("narr_5", "（リリィの視線があなたの体をゆっくりと這うように観察する。）", "", actor=pc) \
        .say("lily_3b", "……体つきも変わったわ。筋肉の付き方、重心の取り方……ふふ、見ていて飽きないわね、あなたは。", "", actor=lily) \
        .say("lily_4", "正式に認定します。あなたは今日から『銀翼』。……ふふ、数字や記録以上に、あなたの戦いには『華』がある。私を魅了する何かがね。", "", actor=lily) \
        .jump(choice1)

    # プレイヤーの選択肢
    builder.choice(react1_thanks, "……ありがとう", "", text_id="c1_thanks") \
           .choice(react1_property, "技術者の仕事もするのか", "", text_id="c1_technical") \
           .choice(react1_silent, "（無言で頷く）", "", text_id="c1_silent")

    # 選択肢反応
    builder.step(react1_thanks) \
        .say("lily_r1", "どういたしまして。……あなたの成長を見守るのは、私の楽しみなの。……特別な意味で、ね。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_property) \
        .say("lily_r2", "ええ。受付嬢だけが私の仕事じゃないの。アリーナという空間全体、私が管理しているのよ。……それに、あなた専属の『観察係』もね。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_silent) \
        .say("lily_r3", "……相変わらず無口ね。でも、その沈黙も悪くないわ。言葉がなくても、あなたの鼓動は伝わってくるから。", "", actor=lily) \
        .jump(scene2)

    # ========================================
    # シーン2: ゼクの囁き『遺棄された記憶：ヌルの正体』
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_6", "（リリィの部屋を辞し、薄暗い廊下を歩くあなたの背後に不自然な影が伸びる。）", "", actor=pc) \
        .say("narr_7", "（ゼクが、まるで壁のシミから染み出すように姿を現した。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("narr_8", "（その手には、先ほど倒した暗殺者『ヌル』から抜き取られた、鈍く明滅するクリスタルの破片ーー『記録チップ』が握られていた。）", "", actor=pc) \
        .say("zek_2", "昇格おめでとうございます。ところで、あの人形……ヌル。あれが何であったか、知りたくはありませんか？", "", actor=zek) \
        .say("narr_9", "（彼はクリスタルの破片を掲げる。）", "", actor=pc) \
        .say("zek_3", "このチップに残されていたのは……かつてグランドマスター・アスタロトに挑み、敗れ、魂を『整理』された……ある冒険者の最期の記録です。", "", actor=zek) \
        .say("zek_4", "ヌルは、アスタロトが退屈しのぎに作った『失敗作』に過ぎない。", "", actor=zek) \
        .jump(choice2)

    # プレイヤーの選択肢
    builder.choice(react2_adventurer, "アスタロトが冒険者を……？", "", text_id="c2_adventurer") \
           .choice(react2_silent, "（無言で聞く）", "", text_id="c2_silent")

    # 選択肢反応
    builder.step(react2_adventurer) \
        .say("zek_r2", "ええ。彼にとって、闘士は『素材』に過ぎません。", "", actor=zek) \
        .jump(scene3)

    builder.step(react2_silent) \
        .say("zek_r3", "……ふふ、沈黙は賢明さの証。では、続けさせていただきましょう。", "", actor=zek) \
        .jump(scene3)

    # ========================================
    # シーン3: ヌルの真実とアリーナの目的
    # ========================================
    builder.step(scene3) \
        .say("narr_10", "（ゼクはクリスタルの破片を翳し、その中に浮かぶ記憶を語る。）", "", actor=pc) \
        .say("zek_5", 'チップにはこう記されています。……『アリーナは、"神の種"を育てるための孵化器だ』と。', "", actor=zek) \
        .say("zek_6b", "敗北した闘士がどうなるか……あなたはもうご覧になったはず。あの黒い霧に包まれ、『回収』された者たちは……アスタロトの計画の礎となるのです。", "", actor=zek) \
        .say("zek_6c", "あなたも、本来ならば彼女と同じ運命を辿るはずだった。……あなたは『特別な事情がある』ようですが。", "", actor=zek) \
        .say("zek_6d", "……不思議に思いませんか？ なぜあなたは、敗北しても『回収』されないのか。", "", actor=zek) \
        .say("zek_6e", "私の推測ですが……あなたはイルヴァと繋がりがあるでしょう？ あなただけが、外部のリソースを使って、効率よく強くなれる。", "", actor=zek) \
        .say("zek_6f", "それは、アスタロト様にとって、あなたが『投資価値のある商品』であることを意味します。今すぐ回収するより、もっと育ててからの方が得だと判断されたのでしょうね。", "", actor=zek) \
        .say("zek_6g", "……つまり、あなたは大事に育てられているのですよ。おめでとうございます。", "", actor=zek) \
        .jump(choice4)

    # プレイヤーのRP選択肢（回収されない理由への反応）
    builder.choice(react4_bored, "……与太話はうんざりだ", "", text_id="c4_bored") \
           .choice(react4_scared, "ゾッとする話だね", "", text_id="c4_scared") \
           .choice(react4_defiant, "私に手を出す奴は必ず後悔させてやる", "", text_id="c4_defiant")

    builder.step(react4_bored) \
        .say("zek_r4a", "与太話……ふふ、そう思いたい気持ちは分かりますよ。でも、真実は変わりません。", "", actor=zek) \
        .jump(scene3_continue)

    builder.step(react4_scared) \
        .say("zek_r4b", "ええ、そうでしょうとも。", "", actor=zek) \
        .jump(scene3_continue)

    builder.step(react4_defiant) \
        .say("zek_r4c", "クク……その気概、嫌いではありません。アスタロト様もきっと、そう言われたら喜ぶでしょうね。", "", actor=zek) \
        .jump(scene3_continue)

    # シーン3続き
    builder.step(scene3_continue) \
        .say("narr_11", "（遠くでバルガスの足音が聞こえる。）", "", actor=pc) \
        .say("zek_8", "おや、バルガスさんが来られましたね。あの方には嫌われているので、私はここでおいとましましょうか。", "", actor=zek) \
        .say("zek_9", "……いずれまた、この続きを話すとしましょう。", "", actor=zek) \
        .jump(choice3)

    # プレイヤーの選択肢
    builder.choice(react3_wait, "待て！", "", text_id="c3_wait") \
           .choice(react3_become, "私も……ヌルのようになるのか？", "", text_id="c3_become") \
           .choice(react3_stare, "（無言を貫く）", "", text_id="c3_stare")

    # 選択肢反応
    builder.step(react3_wait) \
        .say("zek_r4", "……ふふ、焦らないで。時が来れば、全てが明らかになるでしょう。", "", actor=zek) \
        .say("narr_12", "（ゼクが影の中へと消えていく。）", "", actor=pc) \
        .jump(scene4)

    builder.step(react3_become) \
        .say("zek_r5", "……それは、あなた次第です。", "", actor=zek) \
        .say("narr_13", "（ゼクが影の中へと消えていく。）", "", actor=pc) \
        .jump(scene4)

    builder.step(react3_stare) \
        .say("zek_r6", "……では、またお会いしましょう。", "", actor=zek) \
        .say("narr_14", "（ゼクが影の中へと消えていく。）", "", actor=pc) \
        .jump(scene4)

    # ========================================
    # シーン4: バルガスの警告
    # ========================================
    builder.step(scene4) \
        .play_bgm("BGM/Lobby_Normal") \
        .focus_chara(Actors.BALGAS) \
        .say("narr_15", "（バルガスが廊下に現れる。）", "", actor=pc) \
        .say("balgas_1", "……おい、ゼクの野郎、また何か吹き込んでいったんじゃねえだろうな？", "", actor=balgas) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .set_flag(Keys.NULL_CHIP, FlagValues.TRUE) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantMakumaReward();") \
        .complete_quest(QuestIds.MAKUMA) \
        .finish()
