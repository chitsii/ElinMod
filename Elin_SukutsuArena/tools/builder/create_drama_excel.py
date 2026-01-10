"""
アリーナマスター用ドラマスクリプト生成 (Refactored)
scenarios.py の定義を使用してExcelを生成する。
"""

import os
import sys

# toolsディレクトリをパスに追加してモジュールをインポート可能にする
# toolsディレクトリをパスに追加してモジュールをインポート可能にする
BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.dirname(BUILDER_DIR)
COMMON_DIR = os.path.join(TOOLS_DIR, 'common')
sys.path.append(TOOLS_DIR)
sys.path.append(COMMON_DIR)

import importlib

from drama_builder import DramaBuilder
from arena_drama_builder import ArenaDramaBuilder
from drama_constants import DramaIds
from scenarios.rank_up import define_rank_up_G
from scenarios.rank_up.rank_f import define_rank_up_F
from scenarios.rank_up.rank_e import define_rank_up_E
from scenarios.rank_up.rank_d import define_rank_up_D
from scenarios.rank_up.rank_c import define_rank_up_C
from scenarios.rank_up.rank_b import define_rank_up_B
from scenarios.rank_up.rank_a import define_rank_up_A

# Import numbered scenario modules using importlib
define_arena_master_drama = importlib.import_module('scenarios.00_arena_master').define_arena_master_drama
define_zek_main_drama = importlib.import_module('scenarios.00_zek').define_zek_main_drama
define_lily_main_drama = importlib.import_module('scenarios.00_lily').define_lily_main_drama
define_zek_intro = importlib.import_module('scenarios.03_zek_intro').define_zek_intro
define_lily_experiment = importlib.import_module('scenarios.05_1_lily_experiment').define_lily_experiment
define_zek_steal_bottle = importlib.import_module('scenarios.05_2_zek_steal_bottle').define_zek_steal_bottle
define_zek_steal_soulgem = importlib.import_module('scenarios.06_2_zek_steal_soulgem').define_zek_steal_soulgem
define_upper_existence = importlib.import_module('scenarios.07_upper_existence').define_upper_existence
define_lily_private = importlib.import_module('scenarios.08_lily_private').define_lily_private
define_balgas_training = importlib.import_module('scenarios.09_balgas_training').define_balgas_training
define_makuma = importlib.import_module('scenarios.12_makuma').define_makuma
define_makuma2 = importlib.import_module('scenarios.13_makuma2').define_makuma2
define_vs_balgas = importlib.import_module('scenarios.15_vs_balgas').define_vs_balgas
define_lily_real_name = importlib.import_module('scenarios.16_lily_real_name').define_lily_real_name
define_vs_grandmaster_1 = importlib.import_module('scenarios.17_vs_grandmaster_1').define_vs_grandmaster_1
define_last_battle = importlib.import_module('scenarios.18_last_battle').define_last_battle
define_debug_battle = importlib.import_module('scenarios.debug_battle').define_debug_battle_drama

PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
MASTER_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'LangMod', 'JP', 'Dialog', 'Drama', 'drama_sukutsu_arena_master.xlsx')

def process_scenario(output_dir, drama_id, define_func, sheet_name=None):
    """シナリオを処理してExcelを生成"""
    if sheet_name is None:
        sheet_name = drama_id
    output_path = os.path.join(output_dir, f'drama_{drama_id}.xlsx')
    builder = ArenaDramaBuilder()
    define_func(builder)
    builder.save(output_path, sheet_name=sheet_name)
    print(f"Generated: {output_path}")

def main():
    output_dir_jp = os.path.join(PROJECT_ROOT, "LangMod", "JP", "Dialog", "Drama")
    os.makedirs(output_dir_jp, exist_ok=True)

    # Sukutsu Arena Master
    builder_master = ArenaDramaBuilder()
    define_arena_master_drama(builder_master)
    builder_master.save(MASTER_OUTPUT_PATH, sheet_name="sukutsu_arena_master")
    print(f"Generated: {MASTER_OUTPUT_PATH}")

    # Sukutsu Shady Merchant (Zek)
    zek_output_path = os.path.join(output_dir_jp, 'drama_sukutsu_shady_merchant.xlsx')
    builder_zek = ArenaDramaBuilder()
    define_zek_main_drama(builder_zek)
    builder_zek.save(zek_output_path, sheet_name="sukutsu_shady_merchant")
    print(f"Generated: {zek_output_path}")

    # Sukutsu Receptionist (Lily)
    lily_output_path = os.path.join(output_dir_jp, 'drama_sukutsu_receptionist.xlsx')
    builder_lily = ArenaDramaBuilder()
    define_lily_main_drama(builder_lily)
    builder_lily.save(lily_output_path, sheet_name="sukutsu_receptionist")
    print(f"Generated: {lily_output_path}")

    # --- Rank Up Trials ---
    process_scenario(output_dir_jp, DramaIds.RANK_UP_G, define_rank_up_G)
    process_scenario(output_dir_jp, DramaIds.RANK_UP_F, define_rank_up_F)
    process_scenario(output_dir_jp, DramaIds.RANK_UP_E, define_rank_up_E)
    process_scenario(output_dir_jp, DramaIds.RANK_UP_D, define_rank_up_D)
    process_scenario(output_dir_jp, DramaIds.RANK_UP_C, define_rank_up_C)
    process_scenario(output_dir_jp, DramaIds.RANK_UP_B, define_rank_up_B)
    process_scenario(output_dir_jp, DramaIds.RANK_UP_A, define_rank_up_A)

    # --- Story Events ---
    process_scenario(output_dir_jp, DramaIds.ZEK_INTRO, define_zek_intro)
    process_scenario(output_dir_jp, DramaIds.LILY_EXPERIMENT, define_lily_experiment)
    process_scenario(output_dir_jp, DramaIds.ZEK_STEAL_BOTTLE, define_zek_steal_bottle)
    process_scenario(output_dir_jp, DramaIds.ZEK_STEAL_SOULGEM, define_zek_steal_soulgem)
    process_scenario(output_dir_jp, DramaIds.UPPER_EXISTENCE, define_upper_existence)
    process_scenario(output_dir_jp, DramaIds.LILY_PRIVATE, define_lily_private)
    process_scenario(output_dir_jp, DramaIds.BALGAS_TRAINING, define_balgas_training)
    process_scenario(output_dir_jp, DramaIds.MAKUMA, define_makuma)
    process_scenario(output_dir_jp, DramaIds.MAKUMA2, define_makuma2)
    process_scenario(output_dir_jp, DramaIds.VS_BALGAS, define_vs_balgas)
    process_scenario(output_dir_jp, DramaIds.LILY_REAL_NAME, define_lily_real_name)
    process_scenario(output_dir_jp, DramaIds.VS_GRANDMASTER_1, define_vs_grandmaster_1)
    process_scenario(output_dir_jp, DramaIds.LAST_BATTLE, define_last_battle)

    # --- Debug ---
    process_scenario(output_dir_jp, DramaIds.DEBUG_BATTLE, define_debug_battle)

    print("\n[INFO] Drama Excel generation successful.")

if __name__ == "__main__":
    main()
