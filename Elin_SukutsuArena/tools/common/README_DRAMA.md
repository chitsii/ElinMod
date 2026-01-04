# ドラマシステム管理ガイド

## ドラマ名の一元管理

全てのドラマ名は `drama_constants.py` で一元管理されています。これにより、ドラマ名の誤記を防ぎ、一貫性を保つことができます。

## ドラマ名の構造

- **DramaIds**: 短縮形のID（例: `"rank_up_G"`）
  - Excelファイル生成時に使用: `f"drama_{ID}.xlsx"`
  - ファイル名: `drama_rank_up_G.xlsx`

- **DramaNames**: 完全なドラマ名（例: `"drama_rank_up_G"`）
  - C#から呼び出す際に使用
  - `say_and_start_drama()` 等で使用

## 新しいドラマの追加手順

### 1. `drama_constants.py` に定数を追加

```python
class DramaIds:
    # 新しいドラマIDを追加
    NEW_DRAMA = "new_drama"

class DramaNames:
    # 自動的に生成される完全名
    NEW_DRAMA = f"drama_{DramaIds.NEW_DRAMA}"

# リストにも追加
ALL_DRAMA_IDS = [
    # ... 既存のID
    DramaIds.NEW_DRAMA,
]
```

### 2. シナリオファイルを作成

`tools/common/scenarios/XX_new_drama.py`:

```python
from drama_builder import DramaBuilder
from drama_constants import DramaNames  # インポート

def define_new_drama(builder: DramaBuilder):
    pc = builder.register_actor("pc", "あなた", "You")
    npc = builder.register_actor("npc_id", "NPC名", "NPC Name")

    # ドラマ定義...

    # 他のドラマを呼び出す場合は定数を使用
    builder.step(some_label) \
        .say_and_start_drama("メッセージ", DramaNames.RANK_UP_G, "sukutsu_arena_master")
```

### 3. `create_drama_excel.py` にドラマを登録

```python
from drama_constants import DramaIds  # インポート済み
from scenarios.new_drama import define_new_drama  # インポート追加

def main():
    # ... 既存のコード

    # ドラマを追加
    process_scenario(output_dir_jp, DramaIds.NEW_DRAMA, define_new_drama)
```

### 4. ビルド実行

```bash
cd Elin_SukutsuArena
./build.bat
```

## よくある間違いと対策

### ❌ 間違い: 文字列を直接使用

```python
# NG: ドラマ名を直接文字列で指定
.say_and_start_drama("メッセージ", "rank_up_G", "sukutsu_arena_master")
# 問題: "rank_up_G" は不完全（正しくは "drama_rank_up_G"）
```

### ✅ 正しい: 定数を使用

```python
# OK: 定数を使用
from drama_constants import DramaNames
.say_and_start_drama("メッセージ", DramaNames.RANK_UP_G, "sukutsu_arena_master")
# DramaNames.RANK_UP_G = "drama_rank_up_G" が自動的に使用される
```

## ファイル構造

```
tools/
├── common/
│   ├── drama_constants.py          # ドラマ名定数（ここで一元管理）
│   ├── scenarios/
│   │   ├── 00_arena_master.py      # DramaNames を使用
│   │   ├── 01_opening.py
│   │   └── ...
│   └── README_DRAMA.md             # このファイル
└── builder/
    ├── create_drama_excel.py       # DramaIds を使用してExcel生成
    └── create_opening_drama.py     # DramaIds を使用
```

## チェックリスト

新しいドラマを追加する際は、以下を確認してください：

- [ ] `drama_constants.py` に `DramaIds` を追加
- [ ] `drama_constants.py` の `ALL_DRAMA_IDS` リストに追加
- [ ] シナリオファイルで `DramaNames` をインポート
- [ ] シナリオファイル内で定数を使用（文字列直接指定は禁止）
- [ ] `create_drama_excel.py` で `DramaIds` を使用して登録
- [ ] `build.bat` を実行してビルド成功を確認

## 既存コードの移行

全てのシナリオファイルは既に `DramaNames` 定数を使用するよう更新されています。新しいコードを追加する際も、必ずこの規約に従ってください。
