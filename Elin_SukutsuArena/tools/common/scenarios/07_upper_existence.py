"""
07_upper_existence.md - Rank D 初戦『見えざる観客の供物』
観客の介入が始まる戦い
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors

def define_upper_existence(builder: DramaBuilder):
    """
    上位存在の観察 - Rank D初戦
    シナリオ: 07_upper_existence.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_warning")
    choice1 = builder.label("choice1")
    react1_how = builder.label("react1_how")
    react1_silence = builder.label("react1_silence")
    react1_ok = builder.label("react1_ok")
    scene2 = builder.label("scene2_announcement")
    scene3 = builder.label("scene3_battle")
    scene4 = builder.label("scene4_aftermath")
    reward_choice = builder.label("reward_choice")
    reward_cloth = builder.label("reward_cloth")
    reward_iron = builder.label("reward_iron")
    reward_bone = builder.label("reward_bone")
    reward_end = builder.label("reward_end")
    final_choice = builder.label("final_choice")
    final_next = builder.label("final_next")
    final_stop = builder.label("final_stop")
    final_tired = builder.label("final_tired")
    ending = builder.label("ending")

    # ========================================
    # シーン1: 鉄格子の前の警告
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Ominous_Suspense_01") \
        .say("narr_1", "（門扉の前に立つあなたに対し、バルガスはいつになく真剣な表情で、武器の調子を確認している。）", "", actor=pc) \
        .say("narr_2", "（上空からは、地鳴りのような低い笑い声が降ってきている。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_1", "……おい、耳を澄ませ。あの連中の笑い声が聞こえるか？", "", actor=balgas) \
        .say("balgas_2", "ランクDからは、連中はお前をただ観るだけじゃ満足しねえ。", "", actor=balgas) \
        .say("balgas_3", "お前の踊りが退屈だったり、逆に『もっと血が見たい』と思われりゃ……上から『プレゼント』が降ってくるぜ。", "", actor=balgas) \
        .say("narr_3", "（彼は武器を叩き、続ける。）", "", actor=pc) \
        .say("balgas_4", "ヤジ（物理的な嫌がらせ）だ。", "", actor=balgas) \
        .say("balgas_5", "空から降ってくるのは、ポーションかもしれねえし、鈍器かもしれねえ。あるいは地上の物理法則を無視した『異次元のゴミ』だ。", "", actor=balgas) \
        .say("balgas_6", "敵だけを見てりゃ、頭を割られて終わりだぞ。", "", actor=balgas) \
        .say("balgas_7", "空の機嫌も伺いながら戦え……クソッタレな商売だろう？", "", actor=balgas) \
        .jump(choice1)

    # プレイヤーの選択肢1
    builder.choice(react1_how, "対処法はあるのか？", "", text_id="c1_how") \
           .choice(react1_silence, "観客を黙らせることはできないのか？", "", text_id="c1_silence") \
           .choice(react1_ok, "……分かった", "", text_id="c1_ok")

    # 選択肢反応1
    builder.step(react1_how) \
        .say("balgas_r1", "動き続けることだ。止まれば標的になる。……あと、運を祈れ。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_silence) \
        .say("balgas_r2", "無理だ。奴らは高次元にいる。俺たちには手が届かねえ。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_ok) \
        .say("balgas_r3", "……気をつけろ。死ぬなよ。", "", actor=balgas) \
        .jump(scene2)

    # ========================================
    # シーン2: リリィの残酷なアナウンス
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Fanfare_Audience") \
        .say("narr_4", "（闘技場に足を踏み入れると、姿の見えない観客たちの熱気が、肌を焼くような不快な波動となって押し寄せる。）", "", actor=pc) \
        .say("narr_5", "（リリィの声が、魔術的な拡声によって会場全体に響き渡った。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_1", "……皆様、お待たせいたしました。", "", actor=lily) \
        .say("lily_2", "本日のメインディッシュは、新たな『銅貨稼ぎ』……期待の新人による、命の切り売りでございます！", "", actor=lily) \
        .say("obs_1", "（観客の歓声と拍手のような音が響く。）", "", actor=pc) \
        .say("lily_3", "さあ、皆様。もしこの闘士の戦いぶりがお気に召さない、あるいは『もっと刺激が欲しい』と感じられましたら……", "", actor=lily) \
        .say("lily_4", "どうぞ、お手元の『慈悲』を投げ込んであげてくださいな！", "", actor=lily) \
        .say("obs_2", "（観客の笑い声、何かが飛んでくる音。）", "", actor=pc) \
        .jump(scene3)

    # ========================================
    # シーン3: 戦闘中の「異次元のヤジ」
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Battle_Audience_Chaos") \
        .say("narr_6", "（対戦相手である「異次元の剣闘士」と刃を交えた瞬間、頭上の虚空が歪む。）", "", actor=pc) \
        .shake() \
        .say("narr_7", "（紫色の閃光と共に、戦場に「異質な物体」が次々と降り注ぎ始めた。）", "", actor=pc) \
        .shake() \
        .action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] TODO: 観客のヤジ戦闘 - 落下物ギミック\");") \
        .jump(scene4)

    # ========================================
    # シーン4: 嘲笑の中の幕引き
    # ========================================
    builder.step(scene4) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_8", "（満身創痍で敵を倒した瞬間、会場を包んだのは喝采ではなく、勝者を馬鹿にするような高い笑い声だった。）", "", actor=pc) \
        .say("narr_9", "（ロビーに戻ると、リリィがクスクスと笑いながら出迎える。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_5", "……ふふ、見事な逃げ回りっぷりでした。", "", actor=lily) \
        .say("lily_6", "上の方々は、あなたが重力石に足を取られた時の慌てた顔が、今日一番の傑作だったと仰っていますよ。", "", actor=lily) \
        .say("narr_10", "（バルガスが近づいてくる。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_8", "……ケッ、笑わせておけ。", "", actor=balgas) \
        .say("balgas_9", "生き残れば、そのヤジもいつかは『金』に変わる。", "", actor=balgas) \
        .say("balgas_10", "だがな、次はもっと酷いもんが降ってくるぜ。連中はすぐに飽きるからな。", "", actor=balgas) \
        .say("balgas_11", "常に奴らの想像を越える『絶望』を見せてやるか、さっさと全員を黙らせるほど強くなるか……", "", actor=balgas) \
        .say("balgas_12", "選ぶのはお前だ。", "", actor=balgas) \
        .say("narr_11", "（リリィは台帳を開き、報酬を記録する。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_7", "では、報酬の授与です。", "", actor=lily) \
        .say("lily_8", "観客からの投げ銭……小さなコイン10枚とプラチナコイン2枚。それと、戦闘記録として素材を一つ選んでいただけます。", "", actor=lily) \
        .jump(reward_choice)

    # 報酬選択肢
    builder.choice(reward_cloth, "布の切れ端を頼む", "", text_id="c_reward_cloth") \
           .choice(reward_iron, "鉄の欠片が欲しい", "", text_id="c_reward_iron") \
           .choice(reward_bone, "骨を選ぶ", "", text_id="c_reward_bone")

    builder.step(reward_cloth) \
        .say("lily_rew1", "『布の切れ端×1』、記録いたしました。地味ですが、実用的ですね。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"cloth\"));") \
        .jump(reward_end)

    builder.step(reward_iron) \
        .say("lily_rew2", "『鉄の欠片×1』、記録いたしました。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"fragment_iron\"));") \
        .jump(reward_end)

    builder.step(reward_bone) \
        .say("lily_rew3", "『骨×1』ですね。……安定の選択ですこと。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"bone\"));") \
        .jump(reward_end)

    builder.step(reward_end) \
        .action("eval", param="for(int i=0; i<10; i++) { EClass.pc.Pick(ThingGen.Create(\"coin\")); } for(int i=0; i<2; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .say("lily_9", "記録完了です。", "", actor=lily) \
        .say("lily_10", "……それと、今回の戦いで、あなたは観客の『ヤジ』を少し避けられるようになったようですね。称号も記録しておきました。", "", actor=lily) \
        .jump(final_choice)

    # 最終選択肢
    builder.choice(final_next, "次も……同じことが起きるのか？", "", text_id="c_final_next") \
           .choice(final_stop, "観客を黙らせる方法はないのか？", "", text_id="c_final_stop") \
           .choice(final_tired, "（疲れた様子で頷く）", "", text_id="c_final_tired")

    builder.step(final_next) \
        .say("lily_r4", "ええ。むしろ、もっと酷くなりますよ。……楽しみにしていてくださいね？", "", actor=lily) \
        .jump(ending)

    builder.step(final_stop) \
        .say("lily_r5", "ふふ、ありますよ。あなたが彼らの想像を絶する『絶望』を見せれば、彼らは熱狂し、ヤジは止まります。", "", actor=lily) \
        .jump(ending)

    builder.step(final_tired) \
        .say("lily_r6", "……お疲れのようですね。ゆっくりお休みください。", "", actor=lily) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .say("sys_title", "【システム】称号『笑われる者』を獲得しました。", "", actor=pc) \
        .action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] TODO: 称号付与 - 落下物回避率+5%\");") \
        .finish()
