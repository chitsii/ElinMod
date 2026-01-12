"""
BGM JSON生成スクリプト

Sound/BGM/*.mp3 からJSONメタデータを生成する。
"""

import json
import os
import sys
from pathlib import Path

# パス設定
BUILDER_DIR = Path(__file__).parent
TOOLS_DIR = BUILDER_DIR.parent
PROJECT_ROOT = TOOLS_DIR.parent
COMMON_DIR = TOOLS_DIR / "common"

# common ディレクトリをパスに追加
sys.path.insert(0, str(COMMON_DIR))

from bgm_definitions import BGM_BASE_ID, create_bgm_json_data

# BGMフォルダ
BGM_DIR = PROJECT_ROOT / "Sound" / "BGM"


def get_bgm_files() -> list[str]:
    """Sound/BGM/*.mp3 のファイル名リスト（拡張子なし、ソート済み）を取得"""
    if not BGM_DIR.exists():
        return []

    mp3_files = sorted(
        [f.stem for f in BGM_DIR.glob("*.mp3")],
        key=str.lower,  # 大文字小文字を区別しないソート
    )
    return mp3_files


def generate_bgm_json():
    """BGM JSONファイルを生成"""
    bgm_files = get_bgm_files()

    if not bgm_files:
        print("No BGM files found in Sound/BGM/")
        return

    print(f"Generating BGM JSON files...")
    print(f"  Base ID: {BGM_BASE_ID}")
    print(f"  Found {len(bgm_files)} BGM files")

    for offset, filename in enumerate(bgm_files):
        bgm_id = BGM_BASE_ID + offset
        json_data = create_bgm_json_data(bgm_id)

        json_path = BGM_DIR / f"{filename}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"  Generated {len(bgm_files)} JSON files")


if __name__ == "__main__":
    generate_bgm_json()
