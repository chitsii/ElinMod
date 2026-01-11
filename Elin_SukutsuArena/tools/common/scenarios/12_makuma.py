# -*- coding: utf-8 -*-
"""
12_makuma.md - 銀翼を彩る背徳の衣、そして遺棄された真実
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, FlagValues


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
    choice3 = builder.label("choice3")
    react3_wait = builder.label("react3_wait")
    react3_become = builder.label("react3_become")
    react3_stare = builder.label("react3_stare")
    scene4 = builder.label("scene4_balgas")
    ending = builder.label("ending")

    # ========================================
    # シーン1: リリィの報奨『銀翼を彩る背徳の衣』
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Lily_Seductive") \
        .focus_chara(Actors.LILY) \
        .say("narr_1", "（リリィの私室。以前よりも紫煙は濃く、甘い香りが理性を揺さぶる。）", "", actor=pc) \
        .say("narr_2", "（彼女は机の上に、銀色に輝く未知の布地と、空間を切り裂くほどに鋭い針を並べていた。）", "", actor=pc) \
        .say("narr_3", "（それは地上のどんな名工も手にしたことのない、『次元の境界線』そのものを織り込んだ素材だった。）", "", actor=pc) \
        .say("lily_1", "……あら、待っていましたよ。私の大切な『銀翼』さん。", "", actor=lily) \
        .say("lily_2", "ヌルという無機質な虚無を打ち破ったあなたには、相応の装いが必要だわ。これはね、あなたが戦いの中で流した汗と、次元の揺らぎを固定して作り上げた特別な布地……**『ヴォイド・シルク』**よ。", "", actor=lily) \
        .say("lily_3", "さあ、こちらへ。寸法の測定（メジャー）が必要です。", "", actor=lily) \
        .say("lily_4", "……ふふ、動かないで。あなたの筋肉の動き、魔力の拍動……その全てをこの衣に覚え込ませるのですから。", "", actor=lily) \
        .say("narr_4", "（彼女の指があなたの体を這うように寸法を測る。）", "", actor=pc) \
        .say("lily_5", "……あぁ、いい感触。ランクGの頃の無骨なだけの肉体とは、まるで別人のようね。", "", actor=lily) \
        .say("narr_5", "（しばらくして、リリィは完成した礼装をあなたに差し出す。）", "", actor=pc) \
        .say("lily_6", "完成しました。これを身に纏いなさい。", "", actor=lily) \
        .say("lily_7", "それはあなたの体を守る鎧であると同時に、私の『所有物』であることを示す刻印でもあるの。……その翼を広げて戦う時、あなたは誰よりも美しく、そして残酷に見えるはずよ。", "", actor=lily) \
        .jump(choice1)

    # プレイヤーの選択肢
    builder.choice(react1_thanks, "……ありがとう", "", text_id="c1_thanks") \
           .choice(react1_property, "所有物……か", "", text_id="c1_property") \
           .choice(react1_silent, "（無言で礼装を受け取る）", "", text_id="c1_silent")

    # 選択肢反応
    builder.step(react1_thanks) \
        .say("lily_r1", "ふふ、どういたしまして。……あなたが戦う姿を見るのが楽しみですわ。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_property) \
        .say("lily_r2", "ええ。あなたは私の大切な『観察対象』ですもの。当然でしょう？", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_silent) \
        .say("lily_r3", "……無口ですが、気持ちは伝わりましたよ。", "", actor=lily) \
        .jump(scene2)

    # ========================================
    # シーン2: ゼクの囁き『遺棄された記憶：ヌルの正体』
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_6", "（リリィの部屋を辞し、薄暗い廊下を歩くあなたの背後に、不自然な影が伸びる。）", "", actor=pc) \
        .say("narr_7", "（ゼクが、まるで壁のシミから染み出すように姿を現した。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("narr_8", "（その手には、先ほど倒した暗殺者『ヌル』の頭部から抜き取られた、鈍く明滅するクリスタルの破片——**『記録チップ』**が握られていた。）", "", actor=pc) \
        .say("zek_1", "……ククッ、美しい衣装ですな。", "", actor=zek) \
        .say("zek_2", "ですが、その華やかな衣の下に隠された『真実』に、あなたは耐えられますかな？ あなたが壊したあの人形……ヌル。あれが何であったか、知りたくはありませんか？", "", actor=zek) \
        .say("narr_9", "（彼はクリスタルの破片を掲げる。）", "", actor=pc) \
        .say("zek_3", "このチップに残されていたのは、命令（プログラム）ではありません。……それは、かつてグランドマスター・アスタロトに挑み、敗れ、魂を『整理』された……ある冒険者の最期の記憶です。", "", actor=zek) \
        .say("zek_4", "ヌルは、アスタロトが退屈しのぎに作った『失敗作の剥製』に過ぎない。", "", actor=zek) \
        .jump(choice2)

    # プレイヤーの選択肢
    builder.choice(react2_failure, "……失敗作だと？", "", text_id="c2_failure") \
           .choice(react2_adventurer, "アスタロトが冒険者を……？", "", text_id="c2_adventurer") \
           .choice(react2_silent, "（無言で聞く）", "", text_id="c2_silent")

    # 選択肢反応
    builder.step(react2_failure) \
        .say("zek_r1", "ええ。成功作は、もっと恐ろしいものになっているでしょうね。", "", actor=zek) \
        .jump(scene3)

    builder.step(react2_adventurer) \
        .say("zek_r2", "ええ。彼にとって、冒険者は『素材』に過ぎません。", "", actor=zek) \
        .jump(scene3)

    builder.step(react2_silent) \
        .say("zek_r3", "……ふふ、沈黙は賢明さの証。では、続けさせていただきましょう。", "", actor=zek) \
        .jump(scene3)

    # ========================================
    # シーン3: ヌルの真実とアリーナの目的
    # ========================================
    builder.step(scene3) \
        .say("narr_10", "（ゼクはクリスタルの破片を翳し、その中に浮かぶ記憶を語る。）", "", actor=pc) \
        .say("zek_5", 'チップにはこう記されています。……『アリーナは牢獄ではない。ここは、観客たちが"神の種"を育てるための孵化器だ』と。', "", actor=zek) \
        .say("zek_6", "あなたが強くなるほど、彼らは喜び、そして……あなたは『人間』から遠ざかる。ヌルが感情を失ったのは、強くなりすぎた末の成れの果て。", "", actor=zek) \
        .say("zek_7", "……次は、あなたの番かもしれませんよ？", "", actor=zek) \
        .say("narr_11", "（遠くでバルガスの足音が聞こえる。）", "", actor=pc) \
        .say("zek_8", "……おや、バルガスの足音が聞こえる。このチップは私が預かっておきましょう。", "", actor=zek) \
        .say("zek_9", "真実を知るには、まだあなたの『深度』が足りない。……いずれまた、この続きを話すとしましょう。", "", actor=zek) \
        .jump(choice3)

    # プレイヤーの選択肢
    builder.choice(react3_wait, "待て、もっと教えろ！", "", text_id="c3_wait") \
           .choice(react3_become, "俺も……ヌルのようになるのか？", "", text_id="c3_become") \
           .choice(react3_stare, "（無言で記録チップが消えた場所を見つめる）", "", text_id="c3_stare")

    # 選択肢反応
    builder.step(react3_wait) \
        .say("zek_r4", "……ふふ、焦らないで。時が来れば、全てを明かしましょう。", "", actor=zek) \
        .say("narr_12", "（ゼクが影の中へと消えていく。）", "", actor=pc) \
        .jump(scene4)

    builder.step(react3_become) \
        .say("zek_r5", "……それは、あなた次第です。", "", actor=zek) \
        .say("narr_13", "（ゼクが影の中へと消えていく。）", "", actor=pc) \
        .jump(scene4)

    builder.step(react3_stare) \
        .say("zek_r6", "……賢明ですね。では、またお会いしましょう。", "", actor=zek) \
        .say("narr_14", "（ゼクが影の中へと消えていく。）", "", actor=pc) \
        .jump(scene4)

    # ========================================
    # シーン4: バルガスの警告
    # ========================================
    builder.step(scene4) \
        .play_bgm("BGM/Lobby_Normal") \
        .focus_chara(Actors.BALGAS) \
        .say("narr_15", "（バルガスが廊下に現れる。）", "", actor=pc) \
        .say("balgas_1", "……おい、何をボーッとしてる？ ゼクの野郎、また何か吹き込んでいったんじゃねえだろうな？", "", actor=balgas) \
        .say("balgas_2", "あいつの言うことは半分嘘、半分本当だ。全部を信じるなよ。……ただ、こいつだけは覚えておけ。お前が人間でいられるかどうかは、お前自身の選択次第だ。", "", actor=balgas) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .set_flag(Keys.NULL_CHIP, FlagValues.TRUE) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantMakumaReward();") \
        .finish()
