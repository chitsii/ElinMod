"""
Sukutsu Arena シナリオ定義

フラグ管理システム（flag_definitions.py）を使用
"""
import os
from drama_builder import DramaBuilder
from flag_definitions import (
    Keys,
    Motivation, Rank,
    PlayerFlags, RelFlags
)


def define_opening_drama(builder: DramaBuilder):
    """
    オープニングドラマ「虚無の呼び声」を定義
    フラグ管理システムを使用したバージョン + 演出強化
    """
    # アクター登録
    pc = builder.register_actor("pc", "あなた", "You")
    lily = builder.register_actor("sukutsu_receptionist", "リリィ", "Lily")
    vargus = builder.register_actor("sukutsu_arena_master", "バルガス", "Vargus")

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

    # BGM開始
    builder.play_bgm(22001)

    # ナレーション (PCの独白)
    builder.say("narr1", "(色彩は混濁し、上下左右の感覚が溶けていく。次に足が触れたのは、石畳だ。)", actor=pc) \
           .say("narr2", "(それは、数多の敗者の絶望が凝固し、永遠に熱を失ったかのような黒曜石だった。頭上を見上げれば、そこには空も太陽もない。)", actor=pc)

    # 画面を揺らす - 異次元の不安定さを表現
    builder.shake()

    builder.say("narr3", "(ただ、紫紺の渦を巻く「虚無」が天を覆い、時折、空間の裂け目から巨大な鎖が垂れ下がっている。遠くから響くのは、雷鳴のような喝采。だが、その声には「熱」がない。\n高次元の観客たちが、ただ死を消費するために発する、冷ややかな振動だ。)", actor=pc)

    # リリィ登場（フォーカスにウェイト内蔵）
    builder.focus_chara("sukutsu_receptionist") \
           .say("lily1", "……あら。珍しいこともあるものですね。召喚の儀も、空間の歪みもなしに、この『ヴォイド・コロシアム』に迷い込む『生きた肉』がいるなんて。", actor=lily) \
           .say("lily2", "お客様、それとも……新たな『商品』かしら？ここは境界の終わり、そして絶望の始まり。", actor=lily) \
           .say("lily3", "あなたがどこから来たのかは問いません。入られた方は皆、あそこにいる「飲んだくれ」に話を通すのが、ここの作法ですから。", actor=lily)

    # バルガス登場（フォーカスにウェイト内蔵）
    builder.unfocus() \
           .focus_chara("sukutsu_arena_master") \
           .say("vargus1", "……ケッ、シケた面してやがる。おい、サキュバス。そんなひょろいガキ、鑑定するまでもねえ。", actor=vargus) \
           .say("vargus2", "どうせ地上でちょっとばかり魔物に追われて、運悪く次元の割れ目に滑り落ちただけの「迷い犬」だ。おい、小僧。ここは選ばれた狂人どもが、神々の暇つぶしのために殺し合う場所だ。", actor=vargus) \
           .say("vargus3", "そう、いわば闘技場だ。故郷が恋しいなら、隅で丸まって震えてな。運が良ければ、次の次元の潮流でお前の死体くらいは地上に打ち上げられるかもしれねえぜ。\n……あ？ なんだその目は。お前になにができるってんだ？", actor=vargus)

    # フォーカス解除（ウェイト内蔵）
    builder.unfocus()

    # プレイヤー決意 (選択肢)
    vargus_react = builder.label("vargus_react")

    builder.choice(vargus_react, "腕には自信があるし、闘技場に興味もある", "", text_id="c_resolve_fight") \
           .choice(vargus_react, "頼もしい仲間がいる", "", text_id="c_resolve_survive") \
           .choice(vargus_react, "得意なことはない", "", text_id="c_resolve_drift")

    # バルガス反応
    builder.step(vargus_react) \
           .shake() \
           .say("vargus_react1", "……ハッ、そうかよ！ ", actor=vargus) \
           .say("vargus_react2", "おまえのクソ度胸、安酒のツマミくらいにはなりそうだ。……だが、ただの駒で終わるか、名を刻むかはお前次第だ。\n聞かせろ、お前は何のために戦う？", actor=vargus)

    # 動機選択 (フラグ管理システムのキーを使用)
    builder.choice(greed, "【強欲】富と名声、そして力が欲しい", "", text_id="c1") \
           .choice(battle, "【求道】己の限界を知りたい。強い奴と戦わせろ", "", text_id="c2") \
           .choice(void, "【虚無】帰る場所などない。ここが終着点だ", "", text_id="c3") \
           .choice(pride, "【傲慢】この闘技場も、あのドラゴンも、いずれ配下に置いてやる", "", text_id="c4") \
           .choice(drift, "【狂人】理由はない", "", text_id="c5") \
           .on_cancel(drift)

    # --- Greed Route ---
    builder.step(greed) \
        .set_flag(Keys.MOTIVATION, 0) \
        .say("greed_v1", "ハッ！ わかりやすくていいぜ。金と権力……地上のクズどもが一生かけて追いまわすゴミ屑だ。だがいいか、ここでは金などただの石ころだ。", actor=vargus) \
        .say("greed_v2", "お前が手にするのは、神々すら平伏させる「圧倒的な階位」……。それが欲しけりゃ、他人の内臓を積み上げて階段を作るんだな。", actor=vargus) \
        .say("greed_l1", "ふふ、強欲な魂は好物ですよ。あなたが稼ぐ賞金……その何割を私が手数料としていただくことになるのか、楽しみです。精々、死なずに稼いでくださいね？", actor=lily) \
        .jump(ending)

    # --- Battle Route ---
    builder.step(battle) \
        .set_flag(Keys.MOTIVATION, 1) \
        .say("battle_v1", "……チッ、一番厄介な手合いだ。己の限界だと？ 深淵を前にそんなセリフが吐けるか。", actor=vargus) \
        .say("battle_v2", "いいぜ、お前のその真っ直ぐな瞳が、絶望で濁っていく様を見るのは……", actor=vargus) \
        .say("battle_v3", "……かつての俺を見るようで、反吐が出るがな。", actor=vargus) \
        .say("battle_l1", "……あら。戦うこと自体が目的、ですか。あなたの放つその濃密な「闘気」……少し当てられただけで、サキュバスとしての本能が疼いてしまいます。壊れてしまう前に、その輝きを存分に見せてくださいね。", actor=lily) \
        .jump(ending)

    # --- Void Route ---
    builder.step(void) \
        .set_flag(Keys.MOTIVATION, 2) \
        .say("void_v1", "……（沈黙）フン、訳ありか。だがな小僧、ここは逃げ込むための掃き溜めじゃねえ。生への執着を捨てた奴から死んでいく場所だ。", actor=vargus) \
        .say("void_v2", "……いいか、戦いの中でしか己の輪郭を保てねえってんなら、死に物狂いで剣を振れ。そうすりゃ、その虚無も少しは埋まるかもしれねえぜ。", actor=vargus) \
        .say("void_l1", "……居場所を求めて、わざわざ異次元まで。少し同情してしまいますね。ですが、事務手続きに私情は挟みませんよ？", actor=lily) \
        .jump(ending)

    # --- Pride Route ---
    builder.step(pride) \
        .set_flag(Keys.MOTIVATION, 3) \
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
        .say("end_v1", "リリィ！ こいつの名前を、最低ランクの「肉屑」の列に書き加えろ！", actor=vargus) \
        .say("end_v2", "お前がただの肉塊か、それとも多少は骨のある肉塊か……。このコロシアムが、一億の死をもって証明してやるよ。", actor=vargus) \
        .set_flag(Keys.RANK, 0) \
        .set_flag(Keys.REL_LILY, 30) \
        .set_flag(Keys.REL_BALGAS, 20) \
        .set_flag(Keys.REL_ZEK, 0) \
        .set_flag("sukutsu_gladiator", 1) \
        .set_flag("sukutsu_arena_stage", 1) \
        .set_flag("sukutsu_opening_seen", 1) \
        .finish()


def define_arena_master_drama(builder: DramaBuilder):
    """
    アリーナマスターのドラマを定義
    フラグ管理システムを使用（ランク/関係値チェック）
    """
    pc = builder.register_actor("pc", "あなた", "You")
    vargus = builder.register_actor("sukutsu_arena_master", "バルガス", "Vargus")
    lily = builder.register_actor("sukutsu_receptionist", "リリィ", "Lily")

    main = builder.label("main")
    victory_comment = builder.label("victory_comment")
    defeat_comment = builder.label("defeat_comment")
    defeat_stage2 = builder.label("defeat_stage2")
    defeat_stage3 = builder.label("defeat_stage3")
    defeat_champion = builder.label("defeat_champion")
    registered = builder.label("registered")
    join_yes = builder.label("join_yes")
    join_no = builder.label("join_no")
    battle_prep = builder.label("battle_prep")
    stage2_prep = builder.label("stage2_prep")
    stage3_prep = builder.label("stage3_prep")
    stage_champion = builder.label("stage_champion")
    battle_start_stage1 = builder.label("battle_start_stage1")
    battle_start_stage2 = builder.label("battle_start_stage2")
    battle_start_stage3 = builder.label("battle_start_stage3")
    battle_start_champion = builder.label("battle_start_champion")
    end = builder.label("end")

    # Main Step
    builder.step(main) \
        .branch_if("sukutsu_arena_result", "==", 1, victory_comment) \
        .branch_if("sukutsu_arena_result", "==", 2, defeat_comment) \
        .branch_if("sukutsu_gladiator", "==", 1, registered)

    # 未登録者挨拶
    builder.say("greet1", "何の用だ、ひよっこ。見たところ、戦いの「せ」の字も知らなそうだな。", "", actor=vargus) \
        .choice(join_yes, "闘士になりたい", "", text_id="c1") \
        .choice(join_no, "いや、やめておく", "", text_id="c2") \
        .on_cancel(end)

    # === Victory Comment ===
    # 勝利後、関係値を少し上げる
    builder.step(victory_comment) \
        .mod_flag("sukutsu_arena_result", "=", 0) \
        .mod_flag(Keys.REL_BALGAS, "+", 5) \
        .say("win1", "ふん、生きて戻ったか。まあ、最低限の働きはしたようだな。勘違いするなよ、雑魚が。", "", actor=vargus) \
        .jump(registered)

    # === Defeat Comment ===
    builder.step(defeat_comment) \
        .mod_flag("sukutsu_arena_result", "=", 0) \
        .branch_if("sukutsu_arena_failed_stage", ">=", 2, defeat_stage2) \
        .say("defeat1", "ハッ、獣にやられたか。情けない。まあ、初心者が負けるのは当然だな。次は足を使え。止まったら死ぬぞ。", "", actor=vargus) \
        .jump(registered)

    # Defeat Stage 2
    builder.step(defeat_stage2) \
        .branch_if("sukutsu_arena_failed_stage", ">=", 3, defeat_stage3) \
        .say("defeat2", "ケンタウロスに蹴り殺されたか？馬並みの速さについていけなかったな。逃げるのは悪くない。だが、いつまでも逃げてばかりじゃ勝てないぞ。", "", actor=vargus) \
        .jump(registered)

    # Defeat Stage 3
    builder.step(defeat_stage3) \
        .branch_if("sukutsu_arena_failed_stage", ">=", 4, defeat_champion) \
        .say("defeat3", "ミノタウロスか...あれは厄介だったろう。俺も初見では負けたさ。奴の攻撃を見切れるようになれば、勝機はある。鍛え直して来い。", "", actor=vargus) \
        .jump(registered)

    # Defeat Champion
    builder.step(defeat_champion) \
        .say("defeat4", "...グランドマスターに挑んだのか。お前、無謀だな。だが、その無謀さは嫌いじゃない。もっと強くなってから、また来い。", "", actor=vargus) \
        .jump(registered)


    # === Registered Greeting ===
    builder.step(registered) \
        .say("greet2", "おう、闘士よ。今日は何の用だ？", "", actor=vargus) \
        .choice(battle_prep, "戦いに挑む", "", text_id="c3") \
        .choice(end, "また今度", "", text_id="c4") \
        .on_cancel(end)

    # === Join Yes ===
    builder.step(join_yes) \
        .say("join1", "おまえが？ハーッハッハ...まあいい、死にたいなら止めはしない。これでお前も闘士だ。戦いの準備ができたら声をかけろ。", "", actor=vargus) \
        .set_flag("sukutsu_gladiator", 1) \
        .set_flag("sukutsu_arena_stage", 1) \
        .set_flag(Keys.RANK, 0) \
        .set_flag(Keys.REL_LILY, 30) \
        .set_flag(Keys.REL_BALGAS, 20) \
        .action("reload", jump=main)

    # === Join No ===
    builder.step(join_no) \
        .say("reject1", "話は終わりだ。ママのミルクでも飲んでな。", "", actor=vargus) \
        .jump(end)

    # === Battle Prep ===
    builder.step(battle_prep) \
        .branch_if("sukutsu_arena_stage", ">=", 2, stage2_prep) \
        .say("stage1_advice", "お前の最初の相手は「森の狼」だ。素早い攻撃には気をつけろ。武器と防具は整えたか？回復アイテムもあると安心だぞ。", "", actor=vargus) \
        .choice(battle_start_stage1, "準備できた、行く！", "", text_id="c_go1") \
        .choice(registered, "もう少し準備してくる", "", text_id="c_cancel1") \
        .on_cancel(registered)

    # Stage 2 Prep
    builder.step(stage2_prep) \
        .branch_if("sukutsu_arena_stage", ">=", 3, stage3_prep) \
        .say("stage2_advice", "次の相手は「ケンタウロス」だ。奴の突進は威力があるぞ。", "", actor=vargus) \
        .choice(battle_start_stage2, "準備できた！", "", text_id="c_go2") \
        .choice(registered, "待ってくれ", "", text_id="c_cancel2") \
        .on_cancel(registered)

    # Stage 3 Prep
    builder.step(stage3_prep) \
        .branch_if("sukutsu_arena_stage", ">=", 4, stage_champion) \
        .say("stage3_advice", "ここからが本番だ。「ミノタウロス」...奴は俺も手こずった相手だ。力任せに攻めるな。奴の隙を狙え。", "", actor=vargus) \
        .choice(battle_start_stage3, "挑む！", "", text_id="c_go3") \
        .choice(registered, "...もう少し鍛えてくる", "", text_id="c_cancel3") \
        .on_cancel(registered)

    # Champion Prep
    builder.step(stage_champion) \
        .say("champion_advice", "よくぞここまで来た。最後の相手は...グランドマスターだ。覚悟はいいか？あれは...俺でも勝てるかわからん相手だ。", "", actor=vargus) \
        .choice(battle_start_champion, "俺は負けない", "", text_id="c_go_champ") \
        .choice(registered, "...考え直す", "", text_id="c_cancel_champ") \
        .on_cancel(registered)

    # === Battle Starts ===
    builder.step(battle_start_stage1) \
        .say("sendoff1", "よし、行け！生きて戻ってこい...できればな。", "", actor=vargus) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.StartBattle(tg, 1);") \
        .finish()

    builder.step(battle_start_stage2) \
        .say("sendoff2", "いい度胸だ。お前ならやれる！", "", actor=vargus) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.StartBattle(tg, 2);") \
        .finish()

    builder.step(battle_start_stage3) \
        .say("sendoff3", "...無茶するなよ。お前はもうただの新人じゃない。", "", actor=vargus) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.StartBattle(tg, 3);") \
        .finish()

    builder.step(battle_start_champion) \
        .say("sendoff_champ", "...見届けてやる。行って来い、闘士よ。", "", actor=vargus) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.StartBattle(tg, 4);") \
        .finish()

    builder.step(end).finish()
