"""
BGM定義

BGM IDとデフォルト設定値を管理する。
他のModとID衝突を避けるため、1000000〜1000099の範囲を使用。
"""

# ベースID（Sukutsu Arena用）
BGM_BASE_ID = 1000000

# デフォルト設定値
DEFAULT_BGM_CONFIG = {
    "allowMultiple": True,
    "bgmDataOptional": {
        "fadeIn": 0.1,
        "fadeOut": 0.5,
        "failDuration": 0.7,
        "failPitch": 0.12,
        "parts": [{"start": 0.5, "duration": 1.0}],
        "pitchDuration": 0.01,
    },
    "chance": 1.0,
    "pitch": 1.0,
    "reverbMix": 1.0,
    "type": "BGM",
    "volume": 0.5,
}


def get_bgm_id(filename: str, sorted_filenames: list[str]) -> int:
    """
    ファイル名からBGM IDを取得する。

    Args:
        filename: BGMファイル名（拡張子なし）
        sorted_filenames: ソート済みファイル名リスト

    Returns:
        BGM ID (1000000 + オフセット)
    """
    try:
        offset = sorted_filenames.index(filename)
        return BGM_BASE_ID + offset
    except ValueError:
        raise ValueError(f"Unknown BGM file: {filename}")


def create_bgm_json_data(bgm_id: int) -> dict:
    """
    BGM IDからJSON用のデータを作成する。

    Args:
        bgm_id: BGM ID

    Returns:
        JSON用の辞書
    """
    return {"id": bgm_id, **DEFAULT_BGM_CONFIG}
