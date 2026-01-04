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

from drama_builder import DramaBuilder
from scenarios import define_arena_master_drama, define_rank_up_game_01

PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
MASTER_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'LangMod', 'JP', 'Dialog', 'Drama', 'drama_sukutsu_arena_master.xlsx')
RANK_UP_01_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'LangMod', 'JP', 'Dialog', 'Drama', 'drama_rank_up_game_01.xlsx')

def main():
    # --- Arena Master ---
    builder_master = DramaBuilder()
    define_arena_master_drama(builder_master)
    builder_master.save(MASTER_OUTPUT_PATH, sheet_name="sukutsu_arena_master")
    print(f"Generated: {MASTER_OUTPUT_PATH}")

    # --- Rank Up G ---
    builder_rankG = DramaBuilder()
    define_rank_up_game_01(builder_rankG)
    builder_rankG.save(RANK_UP_01_OUTPUT_PATH, sheet_name="drama_rank_up_game_01")
    print(f"Generated: {RANK_UP_01_OUTPUT_PATH}")

if __name__ == "__main__":
    main()
