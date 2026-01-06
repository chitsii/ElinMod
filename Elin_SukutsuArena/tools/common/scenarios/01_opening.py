
from drama_builder import DramaBuilder
from flag_definitions import (
    Keys, Actors, FlagValues, QuestIds,
    Motivation, Rank,
    PlayerFlags, RelFlags
)

def define_opening_drama(builder: DramaBuilder):
    """
    オープニングドラマ「虚無の呼び声」を定義
    フラグ管理システムを使用したバージョン + 演出強化
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    vargus = builder.register_actor(Actors.BALGAS, "バルガス", "Vargus")

    # ラベル定義
    main = builder.label("main")
    greed = builder.label("greed")
    battle = builder.label("battle")
    void = builder.label("void")
    pride = builder.label("pride")
    drift = builder.label("drift")
    ending = builder.label("ending")

    # ==== メインステップ: 異次元への転落 ====
    builder.step(main)

    # BGM開始 (CWL仕様: Sound/BGM/ファイル名 → "BGM/sukutsu_arena_opening")
    builder.play_bgm("BGM/sukutsu_arena_opening")

    # ナレーション (PCの独白)
    builder.say("narr1", "(奇妙な場所に足を踏み入れると、あなたの上下左右の感覚が溶けていく。次に足が触れたのは、石畳だ。)", actor=pc) \
           .say("narr2", "(それは、数多の敗者の絶望が凝固し、永遠に熱を失ったかのような黒曜石だった。頭上を見上げれば、そこには空も太陽もない。)", actor=pc)

    # 画面を揺らす - 異次元の不安定さを表現
    builder.shake()

    builder.say("narr3", "(ただ、紫紺の渦を巻く「虚無」が天を覆い、時折、空間の裂け目から巨大な触手が垂れ下がっている。)", actor=pc) \
           .say("narr3b", "(ここは**次元の狭間**——世界と世界の隙間に浮かぶ領域。確定した因果律を持たず、時間の流れすら曖昧な「無法地帯」だ。)", actor=pc) \
           .say("narr3c", "(遠くから響くのは、雷鳴のような喝采。だが、観客の姿は見えない。姿の見えない「何か」が、この闘技場を見下ろしている——それだけは感じられる。)", actor=pc)

    # リリィ登場（フォーカスにウェイト内蔵）
    builder.focus_chara(Actors.LILY) \
           .say("lily1", "……あら。召喚の儀も、空間の歪みもなしに、この『ヴォイド・コロシアム』に迷い込む『生きた肉』がいるなんて。", actor=lily) \
           .say("lily1b", "……おかしいですね。普通、この狭間に落ちた者は、イルヴァとの繋がりを失うはずなのに。あなた、まだ『帰り道』を持っている……？ イルヴァの神々の加護でもあるのかしら。", actor=lily) \
           .say("lily2", "まあ、いいでしょう。お客様、それとも……新たな『商品』かしら？ここは次元の狭間、そして絶望の始まり。", actor=lily) \
           .say("lily3", "……あなたは自由に出入りできるようですけれど、ここの『仕組み』はあそこにいる「飲んだくれ」に聞くのが作法ですから。", actor=lily)

    # バルガス登場（フォーカスにウェイト内蔵）
    builder.focus_chara(Actors.BALGAS) \
           .say("vargus1", "これはこれは。ちょっとばかり魔物に追われて、運悪く次元の割れ目に滑り落ちた『迷い犬』か？", actor=vargus) \
           .say("vargus1b", "……お前、まだイルヴァの神々との繋がりが切れてねえな。こいつは珍しい。普通、この狭間に落ちりゃ、どんな加護も消し飛ぶんだが。", actor=vargus) \
           .say("vargus2", "ここは、選ばれた狂人どもが、『観客』の暇つぶしのために、殺し合うための場所だ。お前は『帰れる』んだろう？ なら、さっさと帰んな。ここに留まる理由なんざ、正気の奴にはねえはずだ。", actor=vargus) \
           .say("vargus3", "……あ？ なんだその目は？ 言いたいことでもあるのか？", actor=vargus)

    # プレイヤー決意 (選択肢)
    vargus_react = builder.label("vargus_react")

    builder.choice(vargus_react, "腕っぷしには自信がある。闘技場に参加したい", "", text_id="c_resolve_fight") \
           .choice(vargus_react, "ここで魔法の腕試しをしたい", "", text_id="c_resolve_magic") \
           .choice(vargus_react, "心強い仲間と一緒なら怖くはない", "", text_id="c_resolve_survive") \
           .choice(vargus_react, "観光がてら、試合に参加したい", "", text_id="c_resolve_drift")

    # バルガス反応
    builder.step(vargus_react) \
           .shake() \
           .say("vargus_react1", "……ハッ、正気か？ 帰れるのに、自分の意志でこの地獄の底に留まりてえと言いやがったか。", actor=vargus) \
           .say("vargus_react2", "いいぜ。囚われた奴らが生き残るために戦うのとは訳が違う。『選んで』来る奴は、最高に面白いか、最高に馬鹿か、どっちかだ。\n聞かせろ、お前は何のために戦う？", actor=vargus)

    # 動機選択 (フラグ管理システムのキーを使用)
    builder.choice(greed, "【強欲】富と名声、そして力が欲しい", "", text_id="c1") \
           .choice(battle, "【求道】己の限界を知りたい。強い奴と戦わせろ", "", text_id="c2") \
           .choice(void, "【虚無】帰る場所などない。ここが終着点だ", "", text_id="c3") \
           .choice(pride, "【傲慢】この闘技場も、あのドラゴンも、いずれ配下に置いてやる", "", text_id="c4") \
           .choice(drift, "【狂人】理由はない", "", text_id="c5") \
           .on_cancel(drift)

    # --- Greed Route ---
    builder.step(greed) \
        .set_flag(Keys.MOTIVATION, FlagValues.Motivation.GREED) \
        .say("greed_v1", "ハッ！ わかりやすくていいぜ。金と権力……地上のクズどもが一生かけて追いまわすゴミ屑だ。だがいいか、ここでは金などただの石ころだ。", actor=vargus) \
        .say("greed_v2", "お前が手にするのは、神々すら平伏させる「圧倒的な階位」……。それが欲しけりゃ、他人の内臓を積み上げて階段を作るんだな。", actor=vargus) \
        .say("greed_l1", "ふふ、強欲な魂は好物ですよ。あなたが稼ぐ賞金……その何割を私が手数料としていただくことになるのか、楽しみです。精々、死なずに稼いでくださいね？", actor=lily) \
        .jump(ending)

    # --- Battle Route ---
    builder.step(battle) \
        .set_flag(Keys.MOTIVATION, FlagValues.Motivation.BATTLE_LUST) \
        .say("battle_v1", "……チッ、一番厄介な手合いだ。己の限界だと？ 深淵を前にそんなセリフが吐けるか。", actor=vargus) \
        .say("battle_v2", "いいぜ、お前のその真っ直ぐな瞳が、絶望で濁っていく様を見るのは……", actor=vargus) \
        .say("battle_v3", "……かつての俺を見るようで、反吐が出るがな。", actor=vargus) \
        .say("battle_l1", "……あら。戦うこと自体が目的、ですか。あなたの放つその濃密な「闘気」……少し当てられただけで、サキュバスとしての本能が疼いてしまいます。壊れてしまう前に、その輝きを存分に見せてくださいね。", actor=lily) \
        .jump(ending)

    # --- Void Route ---
    builder.step(void) \
        .set_flag(Keys.MOTIVATION, FlagValues.Motivation.NIHILISM) \
        .say("void_v1", "……（沈黙）フン、訳ありか。だがな小僧、ここは逃げ込むための掃き溜めじゃねえ。生への執着を捨てた奴から死んでいく場所だ。", actor=vargus) \
        .say("void_v2", "……いいか、戦いの中でしか己の輪郭を保てねえってんなら、死に物狂いで剣を振れ。そうすりゃ、その虚無も少しは埋まるかもしれねえぜ。", actor=vargus) \
        .say("void_l1", "……居場所を求めて、わざわざ異次元まで。少し同情してしまいますね。ですが、事務手続きに私情は挟みませんよ？", actor=lily) \
        .jump(ending)

    # --- Pride Route ---
    builder.step(pride) \
        .set_flag(Keys.MOTIVATION, FlagValues.Motivation.ARROGANCE) \
        .shake() \
        .say("pride_v1", "……ハハハ！傑作だ！聞こえたかリリィ？ この新入り、初日から『王』を気取ってやがる！", actor=vargus) \
        .say("pride_v2", "だがな、その傲慢さが武器になることもある。神を殺すのはいつだって、己の身の程を知らぬ大馬鹿野郎だ。", actor=vargus) \
        .say("pride_l1", "……まぁ。グランドマスターの座を狙うなんて。ふふ、夢物語でも期待しておきましょう。", actor=lily) \
        .jump(ending)

    # --- Drift (Madman) Route ---
    builder.step(drift) \
        .say("drift_v1", "……チッ。ヤク中か、それとも脳みそまで混沌に冒されたか。会話もできねえ壊れた玩具に用はねえんだがな。", actor=vargus) \
        .say("drift_l1", "あら、私は嫌いではありませんよ？ 理由なき衝動ほど、純粋で美しいものはありません。あなたのその濁った瞳……何を見るのか楽しみです。", actor=lily) \
        .jump(ending)


    # --- Ending ---
    builder.step(ending) \
        .shake() \
        .say("end_v1", "リリィ！ こいつの名前を、剣闘士の列に書き加えろ！", actor=vargus) \
        .say("end_v2", "お前がただの肉塊か、それとも多少は骨のある肉塊か……。このコロシアムで証明してみせな。", actor=vargus) \
        .set_flag(Keys.RANK, 0) \
        .set_flag(Keys.REL_LILY, 30) \
        .set_flag(Keys.REL_BALGAS, 20) \
        .set_flag(Keys.REL_ZEK, 0) \
        .set_flag("sukutsu_gladiator", 1) \
        .set_flag("sukutsu_arena_stage", 1) \
        .set_flag("sukutsu_opening_seen", 1) \
        .complete_quest(QuestIds.OPENING) \
        .finish()
