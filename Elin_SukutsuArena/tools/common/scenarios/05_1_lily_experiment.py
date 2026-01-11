"""
05_1_lily_experiment.md - リリィの私的依頼『残響の器』
材料提供型クエスト: 骨を集めてリリィに渡す
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, QuestIds

def define_lily_experiment(builder: DramaBuilder):
    """
    リリィの私的依頼「残響の器」
    シナリオ: 05_1_lily_experiment.md

    変更: 製作クエスト → 材料提供クエスト
    必要材料: 骨 (bone) x1
    報酬: プラチナコイン20枚
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_request")
    choice1 = builder.label("choice1")
    react1_what = builder.label("react1_what")
    react1_reward = builder.label("react1_reward")
    react1_help = builder.label("react1_help")
    scene2 = builder.label("scene2_requirements")
    choice2 = builder.label("choice2")
    react2_accept = builder.label("react2_accept")
    react2_bone = builder.label("react2_bone")
    react2_silent = builder.label("react2_silent")
    check_materials = builder.label("check_materials")
    has_material = builder.label("has_material")
    no_material = builder.label("no_material")
    scene4 = builder.label("scene4_delivery")
    ending = builder.label("ending")

    # ========================================
    # シーン1: 受付嬢の不機嫌な午後
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Lobby_Normal") \
        .focus_chara(Actors.LILY) \
        .say("narr_1", "（ロビーは相変わらず、異次元の歪みが軋む不快な音に満ちている。）", "", actor=pc) \
        .say("narr_2", "（リリィは眉間に皺を寄せ、羽根ペンを乱暴に机に置いた。その前には、どこか禍々しい幾何学模様が描かれた、古ぼけた設計図が広げられている。）", "", actor=pc) \
        .say("lily_1", "……あぁ、忌々しい。", "", actor=lily) \
        .say("lily_2", "このロビーの『雑音』のせいで、私の大切な研究がちっとも進みません。戦士たちの絶望、観客の哄笑、次元の摩擦音……これらは本来、純粋な『魔力の残滓』として回収されるべきものなのに。", "", actor=lily) \
        .say("narr_3", "（彼女はあなたを見つけ、わずかに目を細める。）", "", actor=pc) \
        .say("lily_3", "ねえ、そこの『泥犬』さん。少しは私に牙以外の役に立つところを見せてくださる？", "", actor=lily) \
        .say("lily_4", "私の研究のために、特別な『実験用具』が必要なのです。……材料さえあれば、私が作れるのですが。", "", actor=lily)

    # プレイヤーの選択肢
    builder.choice(react1_what, "どんな材料が必要なんだ？", "", text_id="c1_what") \
           .choice(react1_reward, "報酬次第だな", "", text_id="c1_reward") \
           .choice(react1_help, "手伝おう", "", text_id="c1_help")

    # 選択肢反応
    builder.step(react1_what) \
        .say("lily_r1", "ふふ、興味を持っていただけましたか。では、詳しくご説明いたしましょう。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_reward) \
        .say("lily_r2", "まあ、現実的ですこと。ええ、もちろん報酬はお支払いいたしますよ。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_help) \
        .say("lily_r3", "あら、素直ですこと。では、お願いいたしますね。", "", actor=lily) \
        .jump(scene2)

    # ========================================
    # シーン2: 材料の説明
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Mystical_Ritual") \
        .say("narr_4", "（リリィは細長い指先で設計図の一点を鋭く指し示した。そこには、内部に複雑な空洞を持つ、特殊な瓶のような構造が描かれている。）", "", actor=pc) \
        .say("lily_5", "必要なのは**『虚空の共鳴瓶』**。この器があれば、アリーナに満ちる雑音を……純粋な魔力として回収できるのです。", "", actor=lily) \
        .say("lily_6", "器の製作は私が行います。あなたには、材料を集めてきてほしいのです。", "", actor=lily) \
        .say("lily_7", "必要なのは**『骨』**。生き物の残骸に宿る魔力の残滓……それが、器の核となるのです。", "", actor=lily) \
        .say("lily_8", "闘技場で倒した敵から手に入るでしょう。……一つで十分ですよ。", "", actor=lily)

    # プレイヤーの選択肢
    builder.choice(react2_accept, "任せてくれ", "", text_id="c2_accept") \
           .choice(react2_bone, "骨……どこで手に入る？", "", text_id="c2_bone") \
           .choice(react2_silent, "（無言で頷く）", "", text_id="c2_silent")

    # 選択肢反応
    builder.step(react2_accept) \
        .say("lily_r4", "ふふ、頼もしいこと。では、お待ちしておりますね。", "", actor=lily) \
        .jump(check_materials)

    builder.step(react2_bone) \
        .say("lily_r5", "闘技場の敵を倒せば手に入りますよ。骨を持った生き物ならどれでも構いません。", "", actor=lily) \
        .jump(check_materials)

    builder.step(react2_silent) \
        .say("lily_r6", "……無口ですが、仕事はきっちりこなしてくださるのでしょう？", "", actor=lily) \
        .jump(check_materials)

    # ========================================
    # シーン3: 材料チェック（選択肢ベース）
    # ========================================
    builder.step(check_materials) \
        .say("lily_check", "……さて、骨はお持ちですか？", "", actor=lily)

    # 条件付き選択肢: 骨を持っている場合のみ「渡す」が表示される
    builder.choice_if(has_material, "骨を渡す", "hasItem,bone", text_id="c_give_bone") \
           .choice(no_material, "まだ持っていない", "", text_id="c_no_bone")

    # 材料あり → 消費して納品へ
    builder.step(has_material) \
        .cs_eval("var mat = EClass.pc.things.Find(t => t.id == \"bone\"); if(mat != null) mat.Destroy();") \
        .say("lily_take", "……ありがとうございます。優秀ですこと。", "", actor=lily) \
        .jump(scene4)

    # 材料なし → 会話終了（再度話しかけで再試行可能）
    builder.step(no_material) \
        .say("lily_no_mat", "そうですか。骨がまだ揃っていないのですね。", "", actor=lily) \
        .say("lily_no_mat2", "闘技場で戦えば手に入りますよ。……探してきてくださいな。", "", actor=lily) \
        .finish()

    # ========================================
    # シーン4: 器の製作と報酬
    # ========================================
    builder.step(scene4) \
        .play_bgm("BGM/Lily_Tranquil") \
        .say("narr_5", "（リリィは骨を受け取ると、それを机の上に置いた。）", "", actor=pc) \
        .say("narr_6", "（彼女は骨に指先を当て、何やら呪文を唱え始める。骨が淡く光り、徐々にその形を変えていく。）", "", actor=pc) \
        .say("narr_7", "（数分後、そこには精緻な模様が刻まれた、小さな器が現れた。）", "", actor=pc) \
        .say("lily_11", "……完成です。", "", actor=lily) \
        .say("narr_8", "（不意に、彼女の尻尾が満足げに揺れた。）", "", actor=pc) \
        .say("lily_12", "ふふ、良い素材でした。これなら、このアリーナに満ちる『死の残響』を存分に吸い取ってくれるでしょう。", "", actor=lily) \
        .say("narr_9", "（彼女は器を丁寧に棚に置き、台帳を開く。）", "", actor=pc) \
        .say("lily_13", "これはお礼です。", "", actor=lily) \
        .cs_eval("for(int i=0; i<20; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .say("lily_14", "**プラチナコイン20枚**を台帳に記録いたしました。", "", actor=lily) \
        .say("lily_15", "それと……あなたの協力を評価して、称号も記録しておきました。『繊細な泥犬』。ふふ、あなたは暴力だけではないのですね。", "", actor=lily) \
        .say("lily_16", "これからも、何か特別な依頼があれば、あなたにお願いするかもしれません。……期待していますよ。", "", actor=lily) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .complete_quest(QuestIds.LILY_EXPERIMENT) \
        .finish()
