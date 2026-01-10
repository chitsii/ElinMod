"""
アリーナマスター（バルガス）のメインダイアログ

高レベルAPIを使用した宣言的定義
"""

from drama_builder import DramaBuilder, ChoiceReaction
from drama_constants import DramaNames
from flag_definitions import (
    Keys, Actors, QuestIds,
    Motivation, Rank,
    PlayerFlags, RelFlags
)
from arena_high_level_api import (
    RankDefinition, GreetingDefinition, QuestEntry,
    BattleStageDefinition, MenuItem, QuestInfoDefinition, QuestStartDefinition,
    build_rank_system, build_greetings, build_greeting_dispatcher,
    build_battle_stages, build_quest_dispatcher, add_menu,
    build_quest_info_steps, build_quest_start_steps,
)
import importlib

# ランクアップ結果ステップ関数のインポート
from scenarios.rank_up.rank_g import add_rank_up_G_result_steps
from scenarios.rank_up.rank_f import add_rank_up_F_result_steps
from scenarios.rank_up.rank_e import add_rank_up_E_result_steps
from scenarios.rank_up.rank_d import add_rank_up_D_result_steps
from scenarios.rank_up.rank_c import add_rank_up_C_result_steps
from scenarios.rank_up.rank_b import add_rank_up_B_result_steps
from scenarios.rank_up.rank_a import add_rank_up_A_result_steps

# モジュール名が数字で始まるためimportlibを使用
_upper_existence_module = importlib.import_module('scenarios.07_upper_existence')
add_upper_existence_result_steps = _upper_existence_module.add_upper_existence_result_steps

_last_battle_module = importlib.import_module('scenarios.18_last_battle')
add_last_battle_result_steps = _last_battle_module.add_last_battle_result_steps


# ============================================================================
# データ定義
# ============================================================================

# ランクアップ試験定義
RANK_DEFINITIONS = [
    RankDefinition(
        rank="g",
        quest_id=QuestIds.RANK_UP_G,
        drama_name=DramaNames.RANK_UP_G,
        confirm_msg="ほう…『屑肉の洗礼』を受けるつもりか？死んでも文句は言えんぞ。",
        confirm_button="問題ない",
        sendoff_msg="いい度胸だ！",
        trial_flag_value=1,
        quest_flag_value=11,
        result_steps_func=add_rank_up_G_result_steps,
    ),
    RankDefinition(
        rank="f",
        quest_id=QuestIds.RANK_UP_F,
        drama_name=DramaNames.RANK_UP_F,
        confirm_msg="『凍土の魔犬』との戦いだな。覚悟はいいか？",
        confirm_button="いくぞ",
        sendoff_msg="行ってこい！",
        trial_flag_value=2,
        quest_flag_value=12,
        result_steps_func=add_rank_up_F_result_steps,
    ),
    RankDefinition(
        rank="e",
        quest_id=QuestIds.RANK_UP_E,
        drama_name=DramaNames.RANK_UP_E,
        confirm_msg="『カイン亡霊戦』だな。あいつは……俺が知る中でも最強の剣闘士だった。覚悟はいいか？",
        confirm_button="挑む",
        sendoff_msg="……あいつの魂を、解放してやれ。",
        trial_flag_value=3,
        quest_flag_value=13,
        result_steps_func=add_rank_up_E_result_steps,
    ),
    RankDefinition(
        rank="d",
        quest_id=QuestIds.RANK_UP_D,
        drama_name=DramaNames.RANK_UP_D,
        confirm_msg="『銅貨稼ぎの洗礼』だな。観客のヤジが降ってくる。避けながら戦えるか？",
        confirm_button="やってみる",
        sendoff_msg="観客を楽しませてやれ！",
        trial_flag_value=4,
        quest_flag_value=14,
        result_steps_func=add_rank_up_D_result_steps,
    ),
    RankDefinition(
        rank="c",
        quest_id=QuestIds.RANK_UP_C,
        drama_name=DramaNames.RANK_UP_C,
        confirm_msg="『闘技場の鴉』への試練だな……俺のかつての仲間たちと戦ってもらう。",
        confirm_button="分かった",
        sendoff_msg="……頼んだぞ。あいつらを、この地獄から解放してやってくれ。",
        trial_flag_value=5,
        quest_flag_value=15,
        result_steps_func=add_rank_up_C_result_steps,
    ),
    RankDefinition(
        rank="b",
        quest_id=QuestIds.RANK_UP_B,
        drama_name=DramaNames.RANK_UP_B,
        confirm_msg="『虚無の処刑人』……ヌルとの戦いだ。あいつは、虚空そのものだ。覚悟はいいか？",
        confirm_button="挑む",
        sendoff_msg="……虚空を見つめるな。飲み込まれるぞ。",
        trial_flag_value=6,
        quest_flag_value=16,
        result_steps_func=add_rank_up_B_result_steps,
    ),
    RankDefinition(
        rank="a",
        quest_id=QuestIds.RANK_UP_A,
        drama_name=DramaNames.RANK_UP_A,
        confirm_msg="『影との戦い』だ。お前自身の影と戦うことになる。覚悟はいいか？",
        confirm_button="挑む",
        sendoff_msg="……行ってこい。お前の内なる敵を、打ち倒せ。",
        trial_flag_value=7,
        quest_flag_value=17,
        result_steps_func=add_rank_up_A_result_steps,
    ),
]

# 挨拶定義
GREETINGS = [
    GreetingDefinition(0, "greet_u", "おう、ひよっこ。今日は何の用だ？"),
    GreetingDefinition(1, "greet_G", "おう、『屑肉』よ。今日は何の用だ？"),
    GreetingDefinition(2, "greet_F", "おう、『泥犬』よ。今日は何の用だ？"),
    GreetingDefinition(3, "greet_E", "おう、『鉄屑』よ。今日は何の用だ？"),
    GreetingDefinition(4, "greet_D", "おう、『銅貨稼ぎ』よ。今日は何の用だ？"),
    GreetingDefinition(5, "greet_C", "おう、『鴉』よ。今日は何の用だ？"),
    GreetingDefinition(6, "greet_B", "おう、『銀翼』よ。今日は何の用だ？"),
    GreetingDefinition(7, "greet_A", "おう、『戦鬼』よ。今日は何の用だ？"),
    GreetingDefinition(8, "greet_S", "……待っていたぞ、『屠竜者』！何の用だ？"),
    GreetingDefinition(9, "greet_SS", "……『覇者』か。相変わらず凄まじい覇気だ。今日は何用だ？"),
    GreetingDefinition(10, "greet_SSS", "……よお、『因果を断つ者』よ。酒でも飲みに来たか？"),
    GreetingDefinition(11, "greet_U", "……ははっ、『星砕き』よ。今日はどの星を落とすつもりだ？"),
    GreetingDefinition(12, "greet_Z", "……『終末の観測者』よ。お前の瞳には、この世界の最期が見えているのか？"),
    GreetingDefinition(13, "greet_gs", "……『神殺し』よ。その翼、どこまで広げるつもりだ？"),
    GreetingDefinition(14, "greet_sg", "……『特異点』よ。お前の存在だけで空間が歪む音がするぜ。用件を聞こうか。"),
    GreetingDefinition(15, "greet_vk", "……『虚空の王』よ。この俺に命令があるのか？それとも、ただの気まぐれか？"),
]

DEFAULT_GREETING = GreetingDefinition(0, "greet_def", "おう、闘士よ。今日は何の用だ？")

# バトルステージ定義
BATTLE_STAGES = [
    BattleStageDefinition(
        stage_num=1,
        stage_id="stage_1",
        advice="お前の最初の相手は「森の狼」だ。素早い攻撃には気をつけろ。武器と防具は整えたか？回復アイテムもあると安心だぞ。",
        advice_id="stage1_advice",
        sendoff="よし、行け！生きて戻ってこい...できればな。",
        sendoff_id="sendoff1",
        go_button="準備できた、行く！",
        cancel_button="もう少し準備してくる",
        next_stage_flag=2,
    ),
    BattleStageDefinition(
        stage_num=2,
        stage_id="stage_2",
        advice="次の相手は「ケンタウロス」だ。奴の突進は威力があるぞ。",
        advice_id="stage2_advice",
        sendoff="いい度胸だ。お前ならやれる！",
        sendoff_id="sendoff2",
        go_button="準備できた！",
        cancel_button="待ってくれ",
        next_stage_flag=3,
    ),
    BattleStageDefinition(
        stage_num=3,
        stage_id="stage_3",
        advice="ここからが本番だ。「ミノタウロス」...奴は俺も手こずった相手だ。力任せに攻めるな。奴の隙を狙え。",
        advice_id="stage3_advice",
        sendoff="...無茶するなよ。お前はもうただの新人じゃない。",
        sendoff_id="sendoff3",
        go_button="挑む！",
        cancel_button="...もう少し鍛えてくる",
        next_stage_flag=4,
    ),
    BattleStageDefinition(
        stage_num=4,
        stage_id="stage_4",
        advice="よくぞここまで来た。最後の相手は...グランドマスターだ。覚悟はいいか？あれは...俺でも勝てるかわからん相手だ。",
        advice_id="champion_advice",
        sendoff="...見届けてやる。行って来い、闘士よ。",
        sendoff_id="sendoff_champ",
        go_button="俺は負けない",
        cancel_button="...考え直す",
        next_stage_flag=None,  # 最後のステージ
    ),
]

# クエスト情報定義（ゼク・リリィ関連 - 情報提供のみ）
QUEST_INFOS = [
    # ゼク関連
    QuestInfoDefinition(
        "quest_zek_intro",
        "quest_zek_info",
        ["おい、見慣れねえ商人が来てるぞ。『ゼク』って名乗る怪しい野郎だ。", "ロビーの隅にいるはずだ。興味があるなら話しかけてみろ。"],
    ),
    QuestInfoDefinition(
        "quest_zek_steal_bottle",
        "quest_zek_bottle_info",
        ["ゼクの野郎が何やら企んでやがる。あいつに話しかけてみろ。", "……俺は関わらねえが、お前の判断だ。"],
    ),
    QuestInfoDefinition(
        "quest_zek_steal_soulgem",
        "quest_zek_soulgem_info",
        ["ゼクがカインの『魂宝石』について何か言いたいことがあるらしい。", "あいつのところへ行け。……慎重に選べよ。"],
    ),
    # リリィ関連
    QuestInfoDefinition(
        "quest_lily_exp",
        "quest_lily_info",
        ["リリィが何やら困ってるらしいぜ。『虚空の共鳴瓶』とかいう怪しげなアイテムを作りたいとか。", "あいつのところへ行って話を聞いてやれ。"],
    ),
    QuestInfoDefinition(
        "quest_lily_private",
        "quest_lily_priv_info",
        ["リリィが『自分の過去』について話したいらしい。……珍しいな。", "興味があるならあいつに話しかけてやれ。"],
    ),
    QuestInfoDefinition(
        "quest_makuma",
        "quest_makuma_info",
        ["怪しい連中が闘技場をうろついてる。『マクマ』とかいう組織らしい。", "リリィが詳しく知ってるかもしれねえ。あいつに聞いてみろ。"],
    ),
    QuestInfoDefinition(
        "quest_lily_real_name",
        "quest_lily_name_info",
        ["リリィが『真の名』を教えてくれるらしい。", "……あいつを本気で信用するのか？　あいつに話しかけろ。"],
    ),
    # 自動発動系
    QuestInfoDefinition(
        "quest_makuma2",
        "quest_makuma2_info",
        ["マクマの連中が何か企んでやがる。リリィも巻き込まれてるかもしれねえ。", "……気をつけろ。"],
    ),
    QuestInfoDefinition(
        "quest_vs_grandmaster_1",
        "quest_gm_info",
        ["……いよいよだな。グランドマスターとの戦いが近い。", "覚悟しておけ。"],
    ),
    QuestInfoDefinition(
        "quest_last_battle",
        "quest_last_info",
        ["……これが最後の戦いだ。", "お前は何のために戦う？　答えを見つけておけ。"],
    ),
    # ランクアップ情報
    QuestInfoDefinition(
        "quest_rank_up_g",
        "quest_rank_g_info",
        ["【昇格試験】ランクG『屑肉の洗礼』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。"],
    ),
    QuestInfoDefinition(
        "quest_rank_up_f",
        "quest_rank_f_info",
        ["【昇格試験】ランクF『凍土の魔犬』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。"],
    ),
    QuestInfoDefinition(
        "quest_rank_up_e",
        "quest_rank_e_info",
        ["【昇格試験】ランクE『カイン亡霊戦』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。"],
    ),
    QuestInfoDefinition(
        "quest_rank_up_d",
        "quest_rank_d_info",
        ["【昇格試験】ランクD『銅貨稼ぎの洗礼』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。"],
    ),
    QuestInfoDefinition(
        "quest_rank_up_c",
        "quest_rank_c_info",
        ["【昇格試験】ランクC『闘技場の鴉』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。"],
    ),
    QuestInfoDefinition(
        "quest_rank_up_b",
        "quest_rank_b_info",
        ["【昇格試験】ランクB『虚無の処刑人』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。"],
    ),
    QuestInfoDefinition(
        "quest_rank_up_a",
        "quest_rank_a_info",
        ["【昇格試験】ランクA『影との戦い』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。"],
    ),
]

# バルガスから直接開始可能なクエスト
QUEST_STARTS = [
    QuestStartDefinition(
        info_step="quest_upper_existence",
        start_step="start_upper_existence",
        info_messages=["……お前には『観客』の正体を教えておく必要がある。", "聞く覚悟はあるか？　真実は重いぞ。"],
        info_id_prefix="quest_upper_info",
        accept_button="聞く",
        accept_id="c_accept_upper",
        decline_button="今はいい",
        decline_id="c_decline_upper",
        start_message="……いいだろう。座れ。",
        drama_name=DramaNames.UPPER_EXISTENCE,
    ),
    QuestStartDefinition(
        info_step="quest_balgas_training",
        start_step="start_balgas_training",
        info_messages=["……おい。俺が直接、お前を鍛えてやろうと思ってる。", "死にたくなければ付いてこい。どうだ？"],
        info_id_prefix="quest_balgas_info",
        accept_button="ついていく",
        accept_id="c_accept_balgas",
        decline_button="今はやめておく",
        decline_id="c_decline_balgas",
        start_message="よし、来い！",
        drama_name=DramaNames.BALGAS_TRAINING,
    ),
    QuestStartDefinition(
        info_step="quest_vs_balgas",
        start_step="start_vs_balgas",
        info_messages=["……おい。俺と本気で戦う気はあるか？", "これは試験じゃねえ。俺の『決着』だ。"],
        info_id_prefix="quest_vs_balgas_info",
        accept_button="受けて立つ",
        accept_id="c_accept_vs_balgas",
        decline_button="今は遠慮する",
        decline_id="c_decline_vs_balgas",
        start_message="……覚悟はいいな。",
        drama_name=DramaNames.VS_BALGAS,
    ),
]

# クエストディスパッチャー用エントリ
AVAILABLE_QUESTS = [
    # ストーリー系（優先）
    QuestEntry(QuestIds.ZEK_INTRO, 21, "quest_zek_intro"),
    QuestEntry(QuestIds.LILY_EXPERIMENT, 22, "quest_lily_exp"),
    QuestEntry(QuestIds.ZEK_STEAL_BOTTLE, 23, "quest_zek_steal_bottle"),
    QuestEntry(QuestIds.ZEK_STEAL_SOULGEM, 24, "quest_zek_steal_soulgem"),
    QuestEntry(QuestIds.UPPER_EXISTENCE, 25, "quest_upper_existence"),
    QuestEntry(QuestIds.LILY_PRIVATE, 26, "quest_lily_private"),
    QuestEntry(QuestIds.BALGAS_TRAINING, 27, "quest_balgas_training"),
    QuestEntry(QuestIds.MAKUMA, 28, "quest_makuma"),
    QuestEntry(QuestIds.MAKUMA2, 29, "quest_makuma2"),
    QuestEntry(QuestIds.RANK_UP_S, 30, "quest_vs_balgas"),
    QuestEntry(QuestIds.LILY_REAL_NAME, 31, "quest_lily_real_name"),
    QuestEntry(QuestIds.VS_GRANDMASTER_1, 32, "quest_vs_grandmaster_1"),
    QuestEntry(QuestIds.LAST_BATTLE, 33, "quest_last_battle"),
    # ランクアップ系
    QuestEntry(QuestIds.RANK_UP_G, 11, "quest_rank_up_g"),
    QuestEntry(QuestIds.RANK_UP_F, 12, "quest_rank_up_f"),
    QuestEntry(QuestIds.RANK_UP_E, 13, "quest_rank_up_e"),
    QuestEntry(QuestIds.RANK_UP_D, 14, "quest_rank_up_d"),
    QuestEntry(QuestIds.RANK_UP_C, 15, "quest_rank_up_c"),
    QuestEntry(QuestIds.RANK_UP_B, 16, "quest_rank_up_b"),
    QuestEntry(QuestIds.RANK_UP_A, 17, "quest_rank_up_a"),
]

# 昇格試験用クエストエントリ（rank_up_checkで使用）
RANK_UP_QUESTS = [
    QuestEntry(QuestIds.RANK_UP_G, 11, "start_rank_g"),
    QuestEntry(QuestIds.RANK_UP_F, 12, "start_rank_f"),
    QuestEntry(QuestIds.RANK_UP_E, 13, "start_rank_e"),
    QuestEntry(QuestIds.RANK_UP_D, 14, "start_rank_d"),
    QuestEntry(QuestIds.RANK_UP_C, 15, "start_rank_c"),
    QuestEntry(QuestIds.RANK_UP_B, 16, "start_rank_b"),
    QuestEntry(QuestIds.RANK_UP_A, 17, "start_rank_a"),
]


# ============================================================================
# ドラマ定義
# ============================================================================

def define_arena_master_drama(builder: DramaBuilder):
    """
    アリーナマスターのドラマを定義
    高レベルAPIを使用した宣言的記述
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    vargus = builder.register_actor(Actors.BALGAS, "バルガス", "Vargus")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")

    # 基本ラベル定義
    main = builder.label("main")
    victory_comment = builder.label("victory_comment")
    defeat_comment = builder.label("defeat_comment")
    registered = builder.label("registered")
    pre_registered = builder.label("pre_registered")
    registered_choices = builder.label("registered_choices")
    end = builder.label("end")

    # 機能ラベル
    battle_prep = builder.label("battle_prep")
    rank_check = builder.label("rank_check")
    rank_up_check = builder.label("rank_up_check")
    rank_up_not_ready = builder.label("rank_up_not_ready")
    check_available_quests = builder.label("check_available_quests")
    quest_none = builder.label("quest_none")

    # ========================================
    # 共通選択肢ヘルパー
    # ========================================
    def add_choices(b):
        """共通の選択肢を追加"""
        add_menu(b, [
            MenuItem("戦いに挑む", battle_prep, text_id="c3"),
            MenuItem("ランクを確認したい", rank_check, text_id="c_rank_check"),
            MenuItem("昇格試験を受けたい", rank_up_check, text_id="c_rank_up"),
            MenuItem("利用可能なクエストを確認", check_available_quests, text_id="c_check_quests"),
            MenuItem("また今度", end, text_id="c4"),
        ], cancel=end)


    # ========================================
    # メインエントリーポイント
    # ========================================
    # 未登録プレイヤー用のオープニング開始
    opening_start = builder.label("opening_start")

    builder.step(main) \
        .branch_if("sukutsu_is_rank_up_result", "==", 1, "rank_up_result_check") \
        .branch_if("sukutsu_is_quest_battle_result", "==", 1, "quest_battle_result_check") \
        .branch_if("sukutsu_arena_result", "==", 1, victory_comment) \
        .branch_if("sukutsu_arena_result", "==", 2, defeat_comment) \
        .branch_if("sukutsu_gladiator", "==", 1, pre_registered) \
        .jump(opening_start)

    # 未登録プレイヤー: オープニングドラマを開始
    builder.step(opening_start) \
        ._start_drama(DramaNames.OPENING) \
        .finish()

    # ========================================
    # ランクアップ結果チェック
    # ========================================
    rank_up_result_check = builder.label("rank_up_result_check")
    # sukutsu_rank_up_trial: 1=G, 2=F, 3=E, 4=D, 5=C, 6=B, 7=A
    trial_cases = [registered]  # 0: フォールバック
    for rank_def in RANK_DEFINITIONS:
        # trial_flag_value順に追加
        trial_cases.append(builder.label(f"rank_up_result_{rank_def.rank}"))
    trial_cases.append(registered)  # 末尾フォールバック

    builder.step(rank_up_result_check) \
        .set_flag("sukutsu_is_rank_up_result", 0) \
        .switch_flag("sukutsu_rank_up_trial", trial_cases)

    # ランクアップシステムを自動生成
    rank_labels = build_rank_system(
        builder,
        RANK_DEFINITIONS,
        actor=vargus,
        fallback_step=registered,
        cancel_step=registered_choices,
        end_step=end,
    )

    # ========================================
    # クエストバトル結果チェック
    # ========================================
    quest_battle_result_check = builder.label("quest_battle_result_check")
    upper_existence_victory = builder.label("upper_existence_victory")
    upper_existence_defeat = builder.label("upper_existence_defeat")
    last_battle_victory = builder.label("last_battle_victory")
    last_battle_defeat = builder.label("last_battle_defeat")

    quest_battle_result_upper = builder.label("quest_battle_result_upper_existence")
    quest_battle_result_last = builder.label("quest_battle_result_last_battle")

    # sukutsu_quest_battle: 0=なし, 1=upper_existence, 2=未使用, 3=last_battle
    builder.step(quest_battle_result_check) \
        .set_flag("sukutsu_is_quest_battle_result", 0) \
        .switch_flag("sukutsu_quest_battle", [
            registered,                  # 0: なし
            quest_battle_result_upper,   # 1: upper_existence
            registered,                  # 2: 未使用
            quest_battle_result_last,    # 3: last_battle
        ])

    # sukutsu_arena_result: 0=未設定, 1=勝利, 2=敗北
    builder.step(quest_battle_result_upper) \
        .switch_flag("sukutsu_arena_result", [
            registered,               # 0: 未設定
            upper_existence_victory,  # 1: 勝利
            upper_existence_defeat,   # 2: 敗北
        ])

    builder.step(quest_battle_result_last) \
        .switch_flag("sukutsu_arena_result", [
            registered,           # 0: 未設定
            last_battle_victory,  # 1: 勝利
            last_battle_defeat,   # 2: 敗北
        ])

    # クエストバトル勝利/敗北ステップ
    add_upper_existence_result_steps(builder, upper_existence_victory, upper_existence_defeat, registered_choices)
    add_last_battle_result_steps(builder, last_battle_victory, last_battle_defeat, registered_choices)

    # ========================================
    # 通常戦闘結果
    # ========================================
    b = builder.step(victory_comment) \
        .set_flag("sukutsu_arena_result", 0) \
        .say("vic_msg", "やるじゃねえか。だが調子に乗るなよ。", "", actor=vargus)
    add_choices(b)

    b = builder.step(defeat_comment) \
        .set_flag("sukutsu_arena_result", 0) \
        .say("def_msg", "無様だな。出直してこい。", "", actor=vargus)
    add_choices(b)

    # ========================================
    # ランク確認
    # ========================================
    b = builder.step(rank_check) \
        .show_rank_info_log() \
        .say("rank_info", "現在のステータスをログに表示したぜ。確認しな。", "", actor=vargus)
    add_choices(b)

    # ========================================
    # 昇格試験チェック
    # ========================================
    # シンプル化: ランク値のみで判定
    # switch_flag を使用 - drama.sequence.Play() を直接呼び出す
    # rank=0(unranked)→G, rank=1(G)→F, rank=2(F)→E, ...
    builder.step(rank_up_check) \
        .switch_flag("chitsii.arena.player.rank", [
            rank_labels["start_rank_g"],  # rank=0 (unranked) → Gランクアップ
            rank_labels["start_rank_f"],  # rank=1 (G) → Fランクアップ
            rank_labels["start_rank_e"],  # rank=2 (F) → Eランクアップ
            rank_labels["start_rank_d"],  # rank=3 (E) → Dランクアップ
            rank_labels["start_rank_c"],  # rank=4 (D) → Cランクアップ
            rank_labels["start_rank_b"],  # rank=5 (C) → Bランクアップ
            rank_labels["start_rank_a"],  # rank=6 (B) → Aランクアップ
        ], fallback=rank_up_not_ready)

    b = builder.step(rank_up_not_ready) \
        .say("rank_up_error", "まだお前には早い。条件を満たしていないか、すでに昇格済みだ。", "", actor=vargus)
    add_choices(b)

    # ========================================
    # 登録済みプレイヤーフロー
    # ========================================
    # 直接挨拶へ遷移（挨拶後すぐに選択肢を表示）
    builder.step(pre_registered) \
        .jump(registered)

    # ========================================
    # 挨拶システム
    # ========================================
    greeting_labels = build_greetings(
        builder,
        GREETINGS,
        actor=vargus,
        add_choices_func=add_choices,
        default_greeting=DEFAULT_GREETING,
    )

    build_greeting_dispatcher(
        builder,
        greeting_labels,
        entry_step=registered,
        flag_key="player.rank",
        default_label=greeting_labels.get('default'),
    )

    # 選択肢のみのステップ
    b = builder.step(registered_choices)
    add_choices(b)

    # ========================================
    # バトルステージシステム
    # ========================================
    build_battle_stages(
        builder,
        BATTLE_STAGES,
        actor=vargus,
        entry_step=battle_prep,
        cancel_step=registered_choices,
        stage_flag="sukutsu_arena_stage",
    )

    # ========================================
    # クエストディスパッチャー
    # ========================================
    quest_labels = build_quest_dispatcher(
        builder,
        AVAILABLE_QUESTS,
        entry_step=check_available_quests,
        fallback_step=quest_none,
        actor=vargus,
        intro_message="利用可能なクエストがあるか確認するぜ...",
        intro_id="quest_check",
    )

    # クエスト情報ステップ（情報提供のみ）
    build_quest_info_steps(
        builder,
        QUEST_INFOS,
        actor=vargus,
        return_step=registered_choices,
    )

    # 直接開始可能なクエスト
    build_quest_start_steps(
        builder,
        QUEST_STARTS,
        actor=vargus,
        cancel_step=registered_choices,
        end_step=end,
    )

    # クエストなし
    builder.step(quest_none) \
        .say("no_quest", "今は特に依頼はねえな。まずは実力をつけることだ。", "", actor=vargus) \
        .jump(registered_choices)

    # ========================================
    # 終了
    # ========================================
    builder.step(end).finish()
