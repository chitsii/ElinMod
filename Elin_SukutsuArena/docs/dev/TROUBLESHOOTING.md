# 開発でよく引っかかるポイント

## ビルド関連

### 全体ビルド
```bash
# プロジェクトルートで実行
build.bat
```
これにより以下が実行される：
- ドラマExcel生成
- クエストデータ生成
- その他必要なアセット生成

### Python実行環境
```bash
# tools ディレクトリ内で実行すること
cd tools
uv run python builder/create_drama_excel.py
uv run python builder/generate_quest_data.py
```

**注意**: システムのPythonではなく、`uv run python` を使用すること。依存関係が正しく解決される。

---

## フラグ関連

### フラグ名のプレフィックス
全てのプレイヤーフラグは `chitsii.arena.` プレフィックスを使用：
```python
# 正しい
Keys.RANK = "chitsii.arena.player.rank"

# 間違い（動作しない）
"player.rank"
```

### フラグ値の対応
| ランク | 値 |
|--------|-----|
| UNRANKED | 0 |
| G | 1 |
| F | 2 |
| E | 3 |
| D | 4 |
| C | 5 |
| B | 6 |
| A | 7 |
| S | 8 |

---

## ドラマビルダー関連

### バトル統合パターン
クエストバトルを統合する際の標準パターン：

```python
# 1. バトル開始時にフラグを設定
builder.step(battle_start) \
    .set_flag("sukutsu_is_quest_battle_result", 1) \
    .set_flag("sukutsu_quest_battle", 2)  # 1=upper, 2=vs_balgas, 3=last
    .start_battle_by_stage("stage_id", master_id="sukutsu_arena_master") \
    .finish()

# 2. 勝利後の継続は別フラグで制御
builder.step(main) \
    .branch_if("sukutsu_vs_balgas_victory", "==", 1, scene_after_victory) \
    ...
```

### 勝利/敗北結果の追加
`arena_master.py` に結果ステップを追加する際：
1. ラベルを定義
2. `switch_on_flag` に分岐を追加
3. `add_*_result_steps()` 関数を呼び出し

---

## よくあるエラー

### "モジュールが見つからない"
```
ModuleNotFoundError: No module named 'xxx'
```
→ `uv run python` を使っているか確認。`tools/` ディレクトリ内で実行しているか確認。

### ドラマが開始しない
- `say_and_start_drama()` の第3引数（master_id）が正しいか確認
- ドラマ名が `drama_constants.py` に登録されているか確認

### バトル後にドラマが再開しない
- `sukutsu_is_quest_battle_result` フラグが設定されているか
- `arena_master.py` の `quest_battle_result_check` に分岐が追加されているか

---

## ファイル生成順序

1. `create_chara_excel.py` - キャラクター定義 → `LangMod/*/Chara.tsv`
2. `create_drama_excel.py` - ドラマ生成 → `Dialog/*.xlsx`
3. `generate_quest_data.py` - クエストデータ → `quest_data.json`

変更後は必ず `build.bat` を実行して全体を再生成すること。
