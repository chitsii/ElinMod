"""
13_makuma2.md - 虚空を繋ぎ止める心臓、そして清算の時
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, FlagValues, QuestIds

def define_makuma2(builder: DramaBuilder):
    """
    ランクA前夜：虚空の心臓製作と過去の清算
    シナリオ: 13_makuma2.md

    Note: This scenario has complex conditional branches based on previous choices:
    - If bottle_choice == SWAPPED: bottle malfunction event occurs
    - If kain_soul_choice == SOLD: Balgas confrontation occurs
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")
    zek = builder.register_actor(Actors.ZEK, "ゼク", "Zek")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_void_core_request")
    choice1 = builder.label("choice1")
    react1_accept = builder.label("react1_accept")
    react1_soul = builder.label("react1_soul")
    react1_silent = builder.label("react1_silent")

    # 条件分岐: 瓶の暴走イベント
    check_bottle = builder.label("check_bottle")
    bottle_event = builder.label("bottle_event")
    bottle_battle = builder.label("bottle_battle")
    bottle_choice = builder.label("bottle_choice")
    bottle_confess = builder.label("bottle_confess")
    bottle_blame = builder.label("bottle_blame")
    bottle_deny = builder.label("bottle_deny")
    after_bottle = builder.label("after_bottle")

    # シーン2: 製作
    scene2 = builder.label("scene2_crafting")
    check_materials = builder.label("check_materials")
    has_materials = builder.label("has_materials")
    no_materials = builder.label("no_materials")
    crafting_complete = builder.label("crafting_complete")
    scene3 = builder.label("scene3_balgas_warning")

    # 条件分岐: カインの魂
    check_kain = builder.label("check_kain")
    kain_event = builder.label("kain_event")
    kain_choice = builder.label("kain_choice")
    kain_confess = builder.label("kain_confess")
    kain_lie = builder.label("kain_lie")
    after_kain = builder.label("after_kain")

    final_choice = builder.label("final_choice")
    final_thanks = builder.label("final_thanks")
    final_trust = builder.label("final_trust")
    final_knowledge = builder.label("final_knowledge")
    scene4 = builder.label("scene4_completion")
    ending = builder.label("ending")

    # ========================================
    # シーン1: リリィの虚空の心臓依頼
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Ominous_Tension") \
        .focus_chara(Actors.LILY) \
        .say("narr_1", "（最近、アリーナ全体を断続的な震動が襲っている。）", "", actor=pc) \
        .shake() \
        .say("narr_2", "（それは観客の喝采によるものではなく、あなたの強大すぎる存在感に、異次元の構造自体が悲鳴を上げているのだ。）", "", actor=pc) \
        .say("narr_3", "（リリィはカウンターの奥で、幾重にも重なった複雑な魔法幾何学の設計図と格闘していた。）", "", actor=pc) \
        .say("narr_4", "（彼女の瞳には、これまでにない焦燥と、それ以上の『愉悦』が宿っている。）", "", actor=pc) \
        .say("lily_1", "……あぁ、困りました。あなたの魂が放つ『重力』が、このアリーナの許容量を超え始めています。", "", actor=lily) \
        .say("lily_2", "このままでは、次の昇格試験を迎える前に、この空間ごと虚無の彼方へ霧散してしまうわ。", "", actor=lily) \
        .say("narr_5", "（彼女は設計図をあなたの前に広げる。）", "", actor=pc) \
        .say("lily_3", "そこで、あなたの手でこれを作りなさい。アリーナの動力源を安定させるための楔……**『虚空の心臓（ヴォイド・コア）』**を。", "", actor=lily) \
        .say("lily_4", "これは単なる機械でも石細工でもありません。あなたの『魔力』と『技術』、そしてこのアリーナに満ちる『死者の嘆き』を一つに鋳造する、究極の工芸品です。", "", actor=lily) \
        .say("lily_5", "『高品質な宝石』、『エーテルの結晶』、そしてゼクの店に並ぶ**『星の断片』**……。これらを『宝石細工』または『機械製作』の極致で練り上げ、一つの心臓として拍動させなさい。", "", actor=lily) \
        .say("lily_6", "……ふふ、これが完成した時、あなたはこの場所と文字通り『一心同体』になる。ランクAへの道は、そこからしか開かれません。", "", actor=lily) \
        .jump(choice1)

    # プレイヤーの選択肢
    builder.choice(react1_accept, "分かった。作ろう", "", text_id="c1_accept") \
           .choice(react1_soul, "俺の魂がアリーナを壊すのか……？", "", text_id="c1_soul") \
           .choice(react1_silent, "（無言で設計図を見つめる）", "", text_id="c1_silent")

    # 選択肢反応
    builder.step(react1_accept) \
        .say("lily_r1", "ふふ、素直ですこと。では、材料を集めてきてくださいね。", "", actor=lily) \
        .jump(check_bottle)

    builder.step(react1_soul) \
        .say("lily_r2", "ええ。あなたは既に、この異次元の限界を超え始めています。", "", actor=lily) \
        .jump(check_bottle)

    builder.step(react1_silent) \
        .say("lily_r3", "……難しそうに見えますが、あなたなら作れます。信じていますよ。", "", actor=lily) \
        .jump(check_bottle)

    # ========================================
    # 条件分岐: 瓶の暴走イベント (bottle_choice == SWAPPED)
    # ========================================
    # BottleChoice: 0=REFUSED, 1=SWAPPED
    builder.step(check_bottle) \
        .switch_flag(Keys.BOTTLE_CHOICE, [
            scene2,        # 0: 拒否した場合
            bottle_event,  # 1: すり替えた場合
            scene2,        # fallback
        ])

    builder.step(bottle_event) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_6", "（リリィが設計図を広げる中、彼女は棚の奥から、以前あなたが製作した『死の共鳴瓶』を取り出した。）", "", actor=pc) \
        .say("lily_7", "……虚空の心臓を起動させる前に、この共鳴瓶で次元の『周波数』を測定する必要があります。", "", actor=lily) \
        .say("lily_8", "あなたが作ってくれたこの器……今まで完璧に機能していたのだけれど。", "", actor=lily) \
        .say("narr_7", "（リリィが瓶に魔力を流し込むと、瓶の表面に不吉な亀裂が走る。）", "", actor=pc) \
        .shake() \
        .say("lily_9", "……！？ なに、これ……内部構造が崩壊している……！？", "", actor=lily) \
        .say("narr_8", "（瓶から黒い霧が噴き出し、ロビー全体を覆い始める。）", "", actor=pc) \
        .say("narr_9", "（霧の中から、これまでアリーナで死んでいった闘士たちの怨念が、おぞましい人型の影となって実体化していく。）", "", actor=pc) \
        .say("lily_10", "くっ……この瓶、まさか……！ 誰かが構造を改竄（かいざん）している……！", "", actor=lily) \
        .say("lily_11", "このままでは、溜め込んだ死者の残響が暴走して、アリーナごと呑み込まれるわ！", "", actor=lily) \
        .jump(bottle_battle)

    # 戦闘イベント
    builder.step(bottle_battle) \
        .shake() \
        .say("narr_10", "（黒い霧から形成された怨念の影が、悲鳴のような咆哮を上げてあなたに襲いかかる！）", "", actor=pc) \
        .say("narr_10_1", "（リリィが叫ぶ。「私が抑え込む！ 今のうちに核を砕いて！」）", "", actor=pc) \
        .shake() \
        .say("narr_10_2", "（あなたは怨念の中心、脈動する黒い結晶を砕き、影を霧散させた。）", "", actor=pc) \
        .say("narr_11", "（リリィは息を切らしながら、砕け散った偽物の瓶の破片を拾い上げる。）", "", actor=pc) \
        .say("narr_12", "（その断面には、ゼク特有の『影の刻印』が刻まれていた。）", "", actor=pc) \
        .say("lily_12", "……これは、ゼクの細工ね。間違いないわ。", "", actor=lily) \
        .say("narr_13", "（リリィはゆっくりとあなたを振り返る。その瞳には、怒りと悲しみ、そして『裏切られたかもしれない』という疑念が混じり合っていた。）", "", actor=pc) \
        .say("lily_13", "……答えて。あなたは、あの時私に渡した瓶が『偽物』だと知っていたの？ それとも、ゼクに騙されていたの？", "", actor=lily) \
        .jump(bottle_choice)

    # 瓶の真実についての選択肢
    builder.choice(bottle_confess, "……すまない。ゼクに唆されて、本物と偽物をすり替えた。君を裏切ってしまった", "", text_id="c_bottle_confess") \
           .choice(bottle_blame, "ゼクが勝手に細工したのだろう……", "", text_id="c_bottle_blame") \
           .choice(bottle_deny, "何も知らない。君の管理ミスじゃないか？", "", text_id="c_bottle_deny")

    # 瓶の選択肢反応
    builder.step(bottle_confess) \
        .say("lily_r4", "……そう。", "", actor=lily) \
        .say("narr_14", "（リリィの肩が小刻みに震えている。）", "", actor=pc) \
        .say("lily_15", "……ふふ、サキュバスが人間に裏切られるなんて、滑稽な話だわ。", "", actor=lily) \
        .say("narr_15", "（彼女は深く息を吐き、再びあなたを見つめる。）", "", actor=pc) \
        .say("lily_16", "でも……でもね。あなたが今、正直に話してくれたこと……それだけは、評価します。", "", actor=lily) \
        .say("lily_17", "『嘘つき』よりは、まだ救いがある。", "", actor=lily) \
        .say("lily_18", "……私は、あなたを許すわ。ただし、二度目はない。次にあなたが私を欺いたら……その時は、この爪であなたの喉を裂きます。約束よ。", "", actor=lily) \
        .set_flag(Keys.LILY_BOTTLE_CONFESSION, FlagValues.LilyBottleConfession.CONFESSED) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.Makuma2ConfessToLily();") \
        .jump(after_bottle)

    builder.step(bottle_blame) \
        .say("lily_r5", "……そう、ですか。", "", actor=lily) \
        .say("narr_16", "（リリィが破片を丁寧に片付け、いつもの事務的な表情に戻る。）", "", actor=pc) \
        .say("lily_19", "それなら仕方ありませんね。ゼクという男は、そういう生き物ですから。", "", actor=lily) \
        .say("lily_20", "……さあ、虚空の心臓の製作に取り掛かりましょう。時間がありません。", "", actor=lily) \
        .say("narr_17", "（リリィの尻尾だけが、不機嫌そうに床を叩いている。）", "", actor=pc) \
        .set_flag(Keys.LILY_BOTTLE_CONFESSION, FlagValues.LilyBottleConfession.BLAMED_ZEK) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.Makuma2BlameZek();") \
        .jump(after_bottle)

    builder.step(bottle_deny) \
        .say("narr_18", "（リリィの表情が凍りつく。）", "", actor=pc) \
        .say("narr_19", "（リリィの周囲に氷のような魔力の波動が広がる。）", "", actor=pc) \
        .say("lily_21", "……そうですか。私の、管理ミス。", "", actor=lily) \
        .say("lily_22", "ふふふ……ええ、私が、あなたという『獣』を『人間』だと勘違いしていた。それが最大のミスでした。", "", actor=lily) \
        .say("lily_23", "結構です。どうぞ、虚空の心臓でも何でも作って、アスタロト様に挑んでください。……私は、もうあなたに期待しません。", "", actor=lily) \
        .set_flag(Keys.LILY_BOTTLE_CONFESSION, FlagValues.LilyBottleConfession.DENIED) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.Makuma2DenyInvolvement();") \
        .jump(after_bottle)

    builder.step(after_bottle) \
        .jump(scene2)

    # ========================================
    # シーン2: 虚空の心臓の製作
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Mystical_Ritual") \
        .say("lily_24", "必要な素材は以下の通りです。", "", actor=lily) \
        .say("lily_25", "**心臓×1**と**ルーンモールド×1**。これらを私に渡してください。", "", actor=lily) \
        .say("lily_26", "……素材が揃ったら、私が『虚空の心臓』を組み上げます。", "", actor=lily) \
        .jump(check_materials)

    # 素材チェック
    builder.step(check_materials) \
        .say("lily_check", "……さて、素材はお持ちですか？", "", actor=lily)

    # 条件付き選択肢: 両方の素材を持っている場合のみ「渡す」が表示される
    builder.choice_if(has_materials, "素材を渡す（心臓×1、ルーンモールド×1）", "hasItem,heart&hasItem,rune_mold", text_id="c_give_materials") \
           .choice(no_materials, "まだ揃っていない", "", text_id="c_no_materials")

    # 素材あり → 消費して製作へ
    builder.step(has_materials) \
        .cs_eval("var heart = EClass.pc.things.Find(t => t.id == \"heart\"); if(heart != null) heart.Destroy();") \
        .cs_eval("var mold = EClass.pc.things.Find(t => t.id == \"rune_mold\"); if(mold != null) mold.Destroy();") \
        .say("lily_take", "……ありがとうございます。優秀ですこと。", "", actor=lily) \
        .jump(crafting_complete)

    # 素材なし → 会話終了（再度話しかけで再試行可能）
    builder.step(no_materials) \
        .say("lily_no_mat", "そうですか。素材がまだ揃っていないのですね。", "", actor=lily) \
        .say("lily_no_mat2", "心臓は簡単でしょう。ルーンモールドは、ご自身で魔法石から磨き上げる必要があります。", "", actor=lily) \
        .say("lily_no_mat3", "……揃ったらまた声をかけてくださいな。", "", actor=lily) \
        .finish()

    # 製作完了
    builder.step(crafting_complete) \
        .play_bgm("BGM/Lily_Tranquil") \
        .say("narr_20", "（リリィは素材を受け取ると、それらを机の上に並べた。）", "", actor=pc) \
        .say("narr_20_1", "（彼女は素材に指先を当て、何やら呪文を唱え始める。）", "", actor=pc) \
        .say("narr_20_2", "（心臓とルーンの鋳型が淡く光り、徐々に融合していく。）", "", actor=pc) \
        .say("narr_20_3", "（数分後、淡い青白い光を放つ、拳大の結晶が完成した。）", "", actor=pc) \
        .say("lily_craft", "……完成です。『虚空の心臓』。これがあれば、アスタロトの領域にも踏み込めるでしょう。", "", actor=lily) \
        .jump(scene3)

    # ========================================
    # シーン3: バルガスの忠告
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Ominous_Suspense_01") \
        .focus_chara(Actors.BALGAS) \
        .say("narr_21", "（リリィとの打ち合わせを終え、素材を探しに出ようとするあなたの腕を、酒臭い、しかし岩のように力強い手が掴んだ。）", "", actor=pc) \
        .say("narr_22", "（バルガスだ。彼はあなたを人気の無い柱の影へと引きずり込み、周囲を警戒しながら低く、掠れた声で話し始めた。）", "", actor=pc) \
        .say("balgas_1", "……おい、待て。リリィに言われるがまま、ゼクの店へ行くつもりか？", "", actor=balgas) \
        .say("balgas_2", "最近のお前は、あいつの吐く『毒』を飲みすぎだ。ヌルの記憶チップだの、世界のバグだの……ゼクが語る『真実』ってのはな、お前の足を止めるための泥濘（ぬかるみ）なんだよ。", "", actor=balgas) \
        .say("balgas_3", "あいつはな、ただの商人じゃねえ。……『剥製師（はくせいし）』なんだ。", "", actor=balgas) \
        .say("balgas_4", "英雄が絶望し、魂が折れる瞬間を待っている。そして、その『最も美しい瞬間』を切り取って、永遠にコレクションしやがる。", "", actor=balgas) \
        .say("balgas_5", "カインの時もそうだ……あいつはただ、お前が友を裏切るかどうかをニヤニヤしながら見てたんだよ。", "", actor=balgas) \
        .jump(check_kain)

    # ========================================
    # 条件分岐: カインの魂について (kain_soul_choice == SOLD)
    # ========================================
    # KainSoulChoice: 0=RETURNED, 1=SOLD
    builder.step(check_kain) \
        .switch_flag(Keys.KAIN_SOUL_CHOICE, [
            after_kain,  # 0: バルガスに返した場合
            kain_event,  # 1: ゼクに売った場合
            after_kain,  # fallback
        ])

    builder.step(kain_event) \
        .say("narr_23", "（バルガスは一瞬、言葉を止め、あなたを鋭く見つめる。）", "", actor=pc) \
        .say("balgas_6", "……おい。一つ、聞いていいか。", "", actor=balgas) \
        .say("balgas_7", "あの時……カインの魂の欠片。本当に、見つからなかったのか？", "", actor=balgas) \
        .say("narr_24", "（バルガスの手が微かに震えている。）", "", actor=pc) \
        .say("balgas_8", "いや……俺の勘違いかもしれねえ。だが、ゼクの野郎がやたらと上機嫌だった時期があってな。……まるで、『最高の獲物』を手に入れたような顔をしてやがった。", "", actor=balgas) \
        .say("balgas_9", "……お前が、あいつに何か『売った』なんてことは……ないよな？", "", actor=balgas) \
        .jump(kain_choice)

    # カインの魂についての選択肢
    builder.choice(kain_confess, "……すまない。カインの魂を、ゼクに売った", "", text_id="c_kain_confess") \
           .choice(kain_lie, "見つからなかった。ゼクとは関係ない", "", text_id="c_kain_lie")

    # カインの選択肢反応
    builder.step(kain_confess) \
        .say("narr_25", "（バルガスは深く息を吐き、拳を握りしめる。）", "", actor=pc) \
        .say("narr_26", "（バルガスの目に、怒りと失望、そして深い悲しみが宿る。）", "", actor=pc) \
        .say("balgas_10", "……そうか。お前は、俺の相棒を……カインを、二度殺したんだな。", "", actor=balgas) \
        .say("balgas_11", "一度目は、異次元の錆に魂を食われて。二度目は、お前に売り飛ばされて。", "", actor=balgas) \
        .say("balgas_12", "……ハッ、俺はなんてマヌケだ。お前を『カイン以上の戦士』だと思っちまってた。", "", actor=balgas) \
        .say("balgas_13", "……いいか、鴉。いや、もうお前を鴉とは呼ばねえ。俺はこれでも、裏切られ慣れてる。だから、お前を殺したりはしない。", "", actor=balgas) \
        .say("balgas_14", "だが……もう二度と、俺に『友』として話しかけるな。お前は今日から、ただの『契約闘士』だ。それ以上でも、それ以下でもねえ。", "", actor=balgas) \
        .set_flag(Keys.KAIN_SOUL_CONFESSION, FlagValues.KainSoulConfession.CONFESSED) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.Makuma2ConfessAboutKain();") \
        .jump(after_kain)

    builder.step(kain_lie) \
        .say("narr_27", "（バルガスは視線を逸らし、深く息を吐く。）", "", actor=pc) \
        .say("narr_28", "（バルガスが信じたいが、心の奥では真実を察している。）", "", actor=pc) \
        .say("balgas_15", "……そうか。", "", actor=balgas) \
        .say("balgas_16", "……なら、いい。……いや、よかねえな。俺の勘が外れてることを祈るよ。", "", actor=balgas) \
        .say("narr_29", "（バルガスがあなたの肩を叩くが、その手には以前のような力強さがない。）", "", actor=pc) \
        .set_flag(Keys.KAIN_SOUL_CONFESSION, FlagValues.KainSoulConfession.LIED) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.Makuma2LieAboutKain();") \
        .jump(after_kain)

    # ========================================
    # 共通後続
    # ========================================
    builder.step(after_kain) \
        .say("balgas_17", "いいか、鴉……いや、戦鬼。あいつの言葉に耳を貸すな。真実なんてのは、アスタロトの首を獲った後に、自分の目で見りゃいい。", "", actor=balgas) \
        .say("balgas_18", "影に潜む奴に背中を見せるなよ。……お前まで『物言わぬコレクション』にされるのは、俺の酒が不味くなるからな。", "", actor=balgas) \
        .jump(final_choice)

    # プレイヤーの選択肢
    builder.choice(final_thanks, "……ありがとう", "", text_id="c_final_thanks") \
           .choice(final_trust, "バルガスの言葉を信じる", "", text_id="c_final_trust") \
           .choice(final_knowledge, "ゼクの知識をさらに求める", "", text_id="c_final_knowledge")

    # 選択肢反応
    builder.step(final_thanks) \
        .say("balgas_r1", "……気をつけろ。生きて戻ってこい。", "", actor=balgas) \
        .jump(scene4)

    builder.step(final_trust) \
        .say("balgas_r2", "……よし。それでいい。", "", actor=balgas) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.Makuma2ChooseTrust();") \
        .jump(scene4)

    builder.step(final_knowledge) \
        .say("balgas_r3", "……ケッ、お前の好きにしろ。だが、後悔するなよ。", "", actor=balgas) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.Makuma2ChooseKnowledge();") \
        .jump(scene4)

    # ========================================
    # シーン4: 虚空の心臓の完成
    # ========================================
    builder.step(scene4) \
        .play_bgm("BGM/Lily_Tranquil") \
        .focus_chara(Actors.LILY) \
        .say("narr_30", "（素材を集め、虚空の心臓を完成させたあなた。それを手にしたあなたは、リリィのもとへ向かう。）", "", actor=pc) \
        .say("lily_27", "……完成したのですね。見せてください。", "", actor=lily) \
        .say("narr_31", "（リリィが虚空の心臓を手に取り、魔力を流し込む。）", "", actor=pc) \
        .say("lily_28", "……完璧です。あなたの魔力と技術が、この異次元の構造を支える楔となりました。", "", actor=lily) \
        .say("lily_29", "これで、ランクAへの挑戦権を授与いたします。……ふふ、あなたは既に、この異次元の一部となりました。誇っていいですよ。", "", actor=lily) \
        .say("narr_32", "（彼女は台帳に何かを書き込む。）", "", actor=pc) \
        .say("lily_30", "報酬として、**小さなコイン30枚**と**プラチナコイン15枚**を記録いたします。……それと、あなたは『虚空と共鳴する者』としての称号を獲得しました。", "", actor=lily) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantMakuma2Reward();") \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .complete_quest(QuestIds.MAKUMA2) \
        .finish()
