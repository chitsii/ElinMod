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
from arena_drama_builder import ArenaDramaBuilder
from scenarios.arena_master import define_arena_master_drama
from scenarios.rank_up import define_rank_up_G

PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
MASTER_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'LangMod', 'JP', 'Dialog', 'Drama', 'drama_sukutsu_arena_master.xlsx')

def main():
    output_dir_jp = os.path.join(PROJECT_ROOT, "LangMod", "JP", "Dialog", "Drama")
    os.makedirs(output_dir_jp, exist_ok=True)

    # Sukutsu Arena Master
    builder_master = ArenaDramaBuilder()
    define_arena_master_drama(builder_master)
    builder_master.save(MASTER_OUTPUT_PATH, sheet_name="sukutsu_arena_master")
    print(f"Generated: {MASTER_OUTPUT_PATH}")

    # --- Rank Up G ---
    RANK_G_OUTPUT_PATH = os.path.join(output_dir_jp, 'drama_rank_up_G.xlsx')
    builder_rankG = ArenaDramaBuilder()
    define_rank_up_G(builder_rankG)
    builder_rankG.save(RANK_G_OUTPUT_PATH, sheet_name="drama_rank_up_G")
    print(f"Generated: {RANK_G_OUTPUT_PATH}")

if __name__ == "__main__":
    main()
