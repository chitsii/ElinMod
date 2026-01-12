"""
07_upper_existence.md - Rank D 初戦『見えざる観客の供物』
観客の介入が始まる戦い
"""

from drama_builder import DramaBuilder
from arena_drama_builder import ArenaDramaBuilder
from flag_definitions import Keys, Actors, QuestIds

def define_upper_existence(builder: ArenaDramaBuilder):
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

    # ========================================
    # シーン1: 鉄格子の前の警告
    # ========================================
    builder.step(main) \
        .drama_start(
            bg_id="Drama/arena_battle_normal",
            bgm_id="BGM/Ominous_Suspense_01"
        ) \
        .say("narr_1", "（門扉の前に立つあなたに対し、バルガスはいつになく真剣な表情で、武器の調子を確認している。）", "", actor=pc) \
        .say("narr_2", "（上空からは、地鳴りのような低い笑い声が降ってきている。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_1", "……おい、耳を澄ませ。あの連中の笑い声が聞こえるか？", "", actor=balgas) \
        .say("balgas_2", "ランクDからは、連中はお前をただ観るだけじゃ満足しねえ。", "", actor=balgas) \
        .say("balgas_3", "お前の踊りが退屈だったり、逆に『もっと血が見たい』と思われりゃ……次元の向こうから『プレゼント』が投げ込まれるぜ。", "", actor=balgas) \
        .say("narr_3", "（彼は武器を叩き、続ける。）", "", actor=pc) \
        .say("balgas_4", "ヤジ（物理的な嫌がらせ）だ。", "", actor=balgas) \
        .say("balgas_5", "爆風とともに飛んでくるのは、ポーションかもしれねえし、鈍器かもしれねえ。あるいは地上の物理法則を無視した『異次元のゴミ』だ。", "", actor=balgas) \
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
        .say("lily_4", "どうぞ、お手元の『慈悲』を……次元を超えて投げ込んであげてくださいな！", "", actor=lily) \
        .say("obs_2", "（観客の笑い声、何かが飛んでくる音。）", "", actor=pc) \
        .jump(scene3)

    # ========================================
    # シーン3: 戦闘開始
    # ========================================
    builder.step(scene3) \
        .say("narr_6", "（対戦相手である「異次元の剣闘士」と刃を交えた瞬間、頭上の虚空が歪む。）", "", actor=pc) \
        .shake() \
        .say("narr_7", "（紫色の閃光と共に、戦場に「異質な物体」が次々と降り注ぎ始めた……！）", "", actor=pc) \
        .shake() \
        .set_flag("sukutsu_is_quest_battle_result", 1) \
        .set_flag("sukutsu_quest_battle", 1) \
        .start_battle_by_stage("upper_existence_battle", master_id="sukutsu_arena_master") \
        .finish()


def add_upper_existence_result_steps(builder: ArenaDramaBuilder, victory_label: str, defeat_label: str, return_label: str):
    """
    上位存在クエストの勝利/敗北ステップを arena_master ビルダーに追加する

    Args:
        builder: arena_master の ArenaDramaBuilder インスタンス
        victory_label: 勝利ステップのラベル名
        defeat_label: 敗北ステップのラベル名
        return_label: 結果表示後にジャンプするラベル名
    """
    pc = Actors.PC
    lily = Actors.LILY
    balgas = Actors.BALGAS

    # 報酬授与用ラベル
    reward_end_ue = builder.label("reward_end_ue")

    # ========================================
    # 上位存在クエスト 勝利
    # ========================================
    builder.step(victory_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_v1", "（満身創痍で敵を倒した瞬間、会場を包んだのは喝采ではなく、勝者を馬鹿にするような高い笑い声だった。）", "", actor=pc) \
        .say("narr_v2", "（ロビーに戻ると、リリィがクスクスと笑いながら出迎える。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_v1", "……ふふ、見事な逃げ回りっぷりでした。", "", actor=lily) \
        .say("lily_v2", "上の方々は、あなたが重力石に足を取られた時の慌てた顔が、今日一番の傑作だったと仰っていますよ。", "", actor=lily) \
        .say("narr_process1", "（ふと闘技場の方を振り返ると、黒い霧が敗北した闘士の体を包んでいくのが見えた。）", "", actor=pc) \
        .say("narr_process2", "（霧が晴れた後、そこには何も残っていなかったーー衣服も、武器も、血痕すらも。）", "", actor=pc) \
        .say("lily_process", "……ああ、気になさらないでください。『回収』されただけですから。", "", actor=lily) \
        .say("narr_process3", "（リリィの声には、どこか悲しげな響きがあった。）", "", actor=pc) \
        .say("narr_v3", "（バルガスが近づいてくる。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_v1", "……ケッ、笑わせておけ。", "", actor=balgas) \
        .say("balgas_v2", "生き残れば、そのヤジもいつかは『金』に変わる。", "", actor=balgas) \
        .say("balgas_v3", "だがな、次はもっと酷いもんが降ってくるぜ。連中はすぐに飽きるからな。", "", actor=balgas) \
        .focus_chara(Actors.LILY) \
        .say("lily_v3", "では、報酬の授与です。", "", actor=lily) \
        .say("lily_v4", "観客からの投げ銭……小さなコイン10枚とプラチナコイン2枚です。", "", actor=lily) \
        .jump(reward_end_ue)

    builder.step(reward_end_ue) \
        .action("eval", param="for(int i=0; i<10; i++) { EClass.pc.Pick(ThingGen.Create(\"medal\")); } for(int i=0; i<2; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .complete_quest(QuestIds.UPPER_EXISTENCE) \
        .say("sys_title", "【システム】称号『笑われる者』を獲得しました。回避+3、運+3 の加護を得た！", "") \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantUpperExistenceBonus();") \
        .finish()

    # ========================================
    # 上位存在クエスト 敗北
    # ========================================
    builder.step(defeat_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Lobby_Normal") \
        .focus_chara(Actors.LILY) \
        .say("lily_d1", "……あらあら、落下物に潰されてしまいましたね。", "", actor=lily) \
        .say("lily_d2", "観客の皆様も、少し期待外れだったようです。また挑戦してくださいね。", "", actor=lily) \
        .finish()
