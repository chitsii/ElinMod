"""
Drama Name Constants
=====================
全てのドラマ名を一元管理するための定数ファイル

ドラマ名の構造:
- ID: 短縮形 (例: "rank_up_G") - ファイル生成やキーとして使用
- Full Name: 完全なドラマ名 (例: "drama_rank_up_G") - C#から呼び出す際に使用

使い方:
    from drama_constants import DramaNames, DramaIds

    # シナリオファイルで使用 (say_and_start_drama等)
    builder.step(some_label) \
        .say_and_start_drama("メッセージ", DramaNames.RANK_UP_G, "sukutsu_arena_master")

    # Excel生成で使用 (create_drama_excel.py)
    process_scenario(output_dir, DramaIds.RANK_UP_G, define_rank_up_G)
"""


class DramaIds:
    """
    ドラマID定数クラス (短縮形)
    Excel生成時のファイル名生成に使用: f"drama_{ID}.xlsx"
    """
    # メインシナリオ
    SUKUTSU_OPENING = "sukutsu_opening"
    SUKUTSU_ARENA_MASTER = "sukutsu_arena_master"

    # ランクアップドラマ
    RANK_UP_G = "rank_up_G"
    RANK_UP_F = "rank_up_F"
    RANK_UP_E = "rank_up_E"
    RANK_UP_D = "rank_up_D"
    RANK_UP_C = "rank_up_C"
    RANK_UP_B = "rank_up_B"
    RANK_UP_A = "rank_up_A"

    # キャラクター関連
    ZEK_INTRO = "zek_intro"
    ZEK_STEAL_BOTTLE = "zek_steal_bottle"
    ZEK_STEAL_SOULGEM = "zek_steal_soulgem"

    LILY_EXPERIMENT = "lily_experiment"
    LILY_PRIVATE = "lily_private"
    LILY_REAL_NAME = "lily_real_name"

    BALGAS_TRAINING = "balgas_training"
    VS_BALGAS = "vs_balgas"

    # ストーリー進行
    UPPER_EXISTENCE = "upper_existence"
    MAKUMA = "makuma"
    MAKUMA2 = "makuma2"
    VS_ASTAROTH = "vs_astaroth"
    LAST_BATTLE = "last_battle"
    EPILOGUE = "epilogue"

    # デバッグ用
    DEBUG_BATTLE = "debug_battle"
    DEBUG_MENU = "debug_menu"


class DramaNames:
    """
    ドラマ名定数クラス (完全名)
    C#からdramaを呼び出す際に使用する完全なドラマ名
    """
    # メインシナリオ
    OPENING = f"drama_{DramaIds.SUKUTSU_OPENING}"
    ARENA_MASTER = f"drama_{DramaIds.SUKUTSU_ARENA_MASTER}"

    # ランクアップドラマ
    RANK_UP_G = f"drama_{DramaIds.RANK_UP_G}"
    RANK_UP_F = f"drama_{DramaIds.RANK_UP_F}"
    RANK_UP_E = f"drama_{DramaIds.RANK_UP_E}"
    RANK_UP_D = f"drama_{DramaIds.RANK_UP_D}"
    RANK_UP_C = f"drama_{DramaIds.RANK_UP_C}"
    RANK_UP_B = f"drama_{DramaIds.RANK_UP_B}"
    RANK_UP_A = f"drama_{DramaIds.RANK_UP_A}"

    # キャラクター関連
    ZEK_INTRO = f"drama_{DramaIds.ZEK_INTRO}"
    ZEK_STEAL_BOTTLE = f"drama_{DramaIds.ZEK_STEAL_BOTTLE}"
    ZEK_STEAL_SOULGEM = f"drama_{DramaIds.ZEK_STEAL_SOULGEM}"

    LILY_EXPERIMENT = f"drama_{DramaIds.LILY_EXPERIMENT}"
    LILY_PRIVATE = f"drama_{DramaIds.LILY_PRIVATE}"
    LILY_REAL_NAME = f"drama_{DramaIds.LILY_REAL_NAME}"

    BALGAS_TRAINING = f"drama_{DramaIds.BALGAS_TRAINING}"
    VS_BALGAS = f"drama_{DramaIds.VS_BALGAS}"

    # ストーリー進行
    UPPER_EXISTENCE = f"drama_{DramaIds.UPPER_EXISTENCE}"
    MAKUMA = f"drama_{DramaIds.MAKUMA}"
    MAKUMA2 = f"drama_{DramaIds.MAKUMA2}"
    VS_ASTAROTH = f"drama_{DramaIds.VS_ASTAROTH}"
    LAST_BATTLE = f"drama_{DramaIds.LAST_BATTLE}"
    EPILOGUE = f"drama_{DramaIds.EPILOGUE}"

    # デバッグ用
    DEBUG_MENU = f"drama_{DramaIds.DEBUG_MENU}"


def get_drama_category(drama_id: str) -> str:
    """
    ドラマIDからカテゴリを自動判定

    Returns:
        'rank': ランクアップ試練関連
        'character': キャラクター個別イベント
        'story': ストーリー進行
    """
    # ランクアップ・対戦系
    if drama_id.startswith(('rank_up_', 'vs_')):
        return 'rank'
    # キャラクター個別
    if any(drama_id.startswith(p) for p in ('lily_', 'zek_', 'balgas_')):
        return 'character'
    # それ以外はストーリー
    return 'story'


# ドラマ表示名マッピング（デバッグメニュー用）
DRAMA_DISPLAY_NAMES = {
    DramaIds.SUKUTSU_OPENING: ("オープニング", "Opening"),
    DramaIds.SUKUTSU_ARENA_MASTER: ("アリーナマスター", "Arena Master"),
    DramaIds.RANK_UP_G: ("ランクG昇格", "Rank G Trial"),
    DramaIds.RANK_UP_F: ("ランクF昇格", "Rank F Trial"),
    DramaIds.RANK_UP_E: ("ランクE昇格", "Rank E Trial"),
    DramaIds.RANK_UP_D: ("ランクD昇格", "Rank D Trial"),
    DramaIds.RANK_UP_C: ("ランクC昇格", "Rank C Trial"),
    DramaIds.RANK_UP_B: ("ランクB昇格", "Rank B Trial"),
    DramaIds.RANK_UP_A: ("ランクA昇格", "Rank A Trial"),
    DramaIds.VS_BALGAS: ("vsバルガス", "vs Balgas"),
    DramaIds.ZEK_INTRO: ("ゼク登場", "Zek Intro"),
    DramaIds.ZEK_STEAL_BOTTLE: ("ボトル交換", "Bottle Swap"),
    DramaIds.ZEK_STEAL_SOULGEM: ("魂宝石選択", "Soul Gem Choice"),
    DramaIds.LILY_EXPERIMENT: ("リリィ実験", "Lily Experiment"),
    DramaIds.LILY_PRIVATE: ("リリィ私室", "Lily Private"),
    DramaIds.LILY_REAL_NAME: ("リリィ真名", "Lily Real Name"),
    DramaIds.BALGAS_TRAINING: ("バルガス訓練", "Balgas Training"),
    DramaIds.UPPER_EXISTENCE: ("上位存在", "Upper Existence"),
    DramaIds.MAKUMA: ("マクマ", "Makuma"),
    DramaIds.MAKUMA2: ("マクマ2", "Makuma 2"),
    DramaIds.VS_ASTAROTH: ("vsアスタロト", "vs Astaroth"),
    DramaIds.LAST_BATTLE: ("最終決戦", "Last Battle"),
    DramaIds.EPILOGUE: ("エピローグ", "Epilogue"),
}


# 全ドラマIDのリスト（バリデーション用）
ALL_DRAMA_IDS = [
    DramaIds.SUKUTSU_OPENING,
    DramaIds.SUKUTSU_ARENA_MASTER,
    DramaIds.RANK_UP_G,
    DramaIds.RANK_UP_F,
    DramaIds.RANK_UP_E,
    DramaIds.RANK_UP_D,
    DramaIds.RANK_UP_C,
    DramaIds.RANK_UP_B,
    DramaIds.RANK_UP_A,
    DramaIds.ZEK_INTRO,
    DramaIds.ZEK_STEAL_BOTTLE,
    DramaIds.ZEK_STEAL_SOULGEM,
    DramaIds.LILY_EXPERIMENT,
    DramaIds.LILY_PRIVATE,
    DramaIds.LILY_REAL_NAME,
    DramaIds.BALGAS_TRAINING,
    DramaIds.VS_BALGAS,
    DramaIds.UPPER_EXISTENCE,
    DramaIds.MAKUMA,
    DramaIds.MAKUMA2,
    DramaIds.VS_ASTAROTH,
    DramaIds.LAST_BATTLE,
    DramaIds.EPILOGUE,
    DramaIds.DEBUG_MENU,
]
