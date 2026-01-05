
from drama_builder import DramaBuilder
from flag_definitions import (
    Keys, Actors, QuestIds,
    Motivation, Rank,
    PlayerFlags, RelFlags
)

def define_rank_up_G(builder: DramaBuilder):
    """
    Rank G 昇格試験「屑肉の洗礼」

    シナリオ: 02_rank_up_01.md
    """
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    vargus = builder.register_actor(Actors.BALGAS, "バルガス", "Vargus")

    main = builder.label("main")

    # シーン1: 受付での宣告
    reception = builder.label("reception")
    # シーン2: バルガスの餞別
    vargus_advice = builder.label("vargus_advice")
    # シーン3: 戦闘開始
    battle_start = builder.label("battle_start")

    # 勝利時・敗北時コメント
    victory = builder.label("victory")
    defeat = builder.label("defeat")

    # --- Reception ---
    # BGM: 不穏な静寂、遠くで鎖の擦れる音
    # (既存の sukutsu_arena_opening が近い雰囲気)
    # 注意: 結果チェックは arena_master.py 側で行い、
    # このドラマは戦闘開始前の会話のみを担当する
    builder.step(main) \
        .play_bgm("BGM/sukutsu_arena_opening") \
        .focus_chara(Actors.LILY) \
        .say("narr_1", "（薄暗いロビーに、異次元の嵐が石壁を叩く音が不気味に響いている。空気は重く、血と錆の臭いが鼻腔を突く。）", "", actor=pc) \
        .say("lily_r1", "……準備はよろしいですか？", "", actor=lily) \
        .wait(1.0) \
        .say("narr_2", "（彼女は細長い爪で、血塗られた羊皮紙を軽く叩いた。パチン、パチンと、まるで死刑執行の秒読みのように。）", "", actor=pc) \
        .say("lily_r2", "これは単なる試合ではありません。あなたがこの『ヴォイド・コロシアム』の胃袋に放り込まれる、最初の『餌』になるための儀式です。", "", actor=lily) \
        .say("lily_r3", "対戦相手は『飢えたヴォイド・プチ』の群れ。……ああ、地上にいる愛らしい彼らだと思わないことね。敗者の絶望を啜って肥大化した、純然たる殺意の塊ですから。", "", actor=lily) \
        .say("lily_r4", "もし、五体満足で戻られたら……その時は、正式に『闘士』として登録して差し上げます。死体袋の用意は、あちらの隅に。……ご武運を。", "", actor=lily)

    # プレイヤー選択肢 - 各選択肢が直接反応ラベルにジャンプ
    # CWLでは選択肢の jump 先が直接反応ステップになるべき
    lily_confident = builder.label("lily_confident")
    lily_amused = builder.label("lily_amused")
    lily_silent = builder.label("lily_silent")

    builder.choice(lily_confident, "……死体袋は不要だ。俺は生きて帰る", "", text_id="c_r_1") \
           .choice(lily_amused, "プチごときに負けるか。すぐに終わらせてやる", "", text_id="c_r_2") \
           .choice(lily_silent, "（無言で羊皮紙を受け取る）", "", text_id="c_r_3")

    # 選択肢後の反応 - 各ラベルが直接独自のステップを持つ
    builder.step(lily_confident) \
        .say("lily_r5_a", "ふふ、自信はおありのようで。……では、存分に。", "", actor=lily) \
        .jump(vargus_advice)

    builder.step(lily_amused) \
        .say("lily_r5_b", "まあ。勇ましいこと。……その自信が、どこまで保つか楽しみですね。", "", actor=lily) \
        .jump(vargus_advice)

    builder.step(lily_silent) \
        .say("lily_r5_c", "……沈黙は恐怖の裏返しか、それとも覚悟の証か。まあ、どちらでもいいのですが。", "", actor=lily) \
        .jump(vargus_advice)

    # --- Vargus Advice ---
    builder.step(vargus_advice) \
        .focus_chara(Actors.BALGAS) \
        .say("narr_3", "（闘技場へ繋がる鉄格子の前で、バルガスが研ぎ澄まされた剣を無造作に弄んでいる。）", "", actor=pc) \
        .say("vargus_r1", "おい、足が震えてんぞ。", "", actor=vargus) \
        .say("vargus_r2", "……いいか、一度だけ教えてやる。プチ共は『数』で来る。一匹一匹はゴミだが、囲まれればお前の肉は一瞬で削げ落ち、綺麗な骨の標本ができあがりだ。", "", actor=vargus) \
        .say("vargus_r3", "壁を背にしろ。そして、スタミナを切らすな。呼吸を乱した瞬間に、奴らは喉笛に吸い付いてくる。……ほら、行け。観客どもが、お前の悲鳴を心待ちにしてやがるぜ。", "", actor=vargus) \
        .jump(battle_start)

    # --- Battle Start ---
    builder.step(battle_start) \
        .start_battle(1, is_rank_up=True, master_id="sukutsu_arena_master") \
        .finish()


def add_rank_up_G_result_steps(builder: DramaBuilder, victory_label: str, defeat_label: str, return_label: str):
    """
    Rank G 昇格試験の勝利/敗北ステップを arena_master ビルダーに追加する

    Args:
        builder: arena_master の DramaBuilder インスタンス
        victory_label: 勝利ステップのラベル名
        defeat_label: 敗北ステップのラベル名
        return_label: 結果表示後にジャンプするラベル名
    """
    # アクターは arena_master 側で既に登録済みのはず
    pc = Actors.PC
    lily = Actors.LILY
    vargus = Actors.BALGAS

    # === Rank G 昇格試験 勝利 ===
    builder.step(victory_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .focus_chara(Actors.BALGAS) \
        .say("rup_vic_v1", "……ケッ、しぶとい奴だ。", "", actor=vargus) \
        .say("rup_vic_v2", "まぁ、合格だ。", "", actor=vargus) \
        .focus_chara(Actors.LILY) \
        .say("rup_vic_l1", "お疲れ様でした。約束通り、ギルドの台帳にあなたの名を刻んでおきました。", "", actor=lily) \
        .say("rup_vic_l2", "ランクG『屑肉』。ふふ、あなたにぴったりの、美味しそうな二つ名だと思いませんか？", "", actor=lily) \
        .say("rup_vic_l3", "あぁ、それと……。あなたが暴れたおかげで、あちこちの備品が壊れました。次は戦うついでに、修理用の『石材』でも拾ってきていただけますか？", "", actor=lily) \
        .complete_quest(QuestIds.RANK_UP_G) \
        .set_flag("chitsii.arena.player.rank", 1) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"wine\")); EClass.pc.Pick(ThingGen.Create(\"ration\"));") \
        .say("rup_vic_sys", "報酬として『バルガスの安酒』と『リリィの配給食』を受け取った。", "", actor=pc) \
        .jump(return_label)

    # === Rank G 昇格試験 敗北 ===
    builder.step(defeat_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .focus_chara(Actors.LILY) \
        .say("rup_def_l1", "あらあら……。期待外れでしたね。", "", actor=lily) \
        .say("rup_def_l2", "死体袋の用意が無駄にならなくて何よりです。……次の方、どうぞ。", "", actor=lily) \
        .jump(return_label)
