"""
オープニングドラマ「虚無の呼び声」生成スクリプト
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
from drama_constants import DramaIds

# Import numbered scenario modules using importlib
define_opening_drama = importlib.import_module('scenarios.01_opening').define_opening_drama

PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'LangMod', 'JP', 'Dialog', 'Drama', f'drama_{DramaIds.SUKUTSU_OPENING}.xlsx')

def main():
    builder = DramaBuilder()
    define_opening_drama(builder)

    # シート名は任意だが、ユニークなものが安全
    builder.save(OUTPUT_PATH, sheet_name="opening")

if __name__ == "__main__":
    main()
