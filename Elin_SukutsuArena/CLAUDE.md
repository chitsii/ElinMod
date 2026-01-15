# Elin_SukutsuArena プロジェクト

Elin用のMod。闘技場を追加する。

## 重要な注意事項

### ドラマ開発時は必ず差分確認

ドラマ（シナリオ）を編集した後は、ビルド時に表示されるExcel差分を確認すること。

```
--- Excel Changes ---
[CHANGED] drama_sukutsu_arena_master.xlsx
  Row 45, Col D: '旧' -> '新'
```

- 意図しない変更がないか確認
- 問題があれば修正して再ビルド（バックアップは保持される）
- 完了後: `cd tools && uv run python builder/excel_diff_manager.py clean`

詳細は [DEVELOPMENT.md](./DEVELOPMENT.md) の「ドラマ開発サイクル」を参照。

## クイックリファレンス

### ビルド
```batch
build.bat debug    # 検証用（DEBUGビルド、推奨）
build.bat          # 公開用（Releaseビルド）
```

**検証時は必ず `debug` を使用すること。** デバッグキー（F9/F11/F12）が有効になる。

### 部分ビルド
```bash
cd tools
uv run python builder/create_drama_excel.py   # ドラマExcelのみ
```

### 主要ディレクトリ
- `src/` - C#ソース
- `tools/common/scenarios/` - シナリオ定義
- `LangMod/JP/Dialog/Drama/` - 生成されたドラマExcel

### 外部参照
- CWLドキュメント: `elin_modding/Elin.Docs/articles/100_Mod Documentation/Custom Whatever Loader/JP/`
- ゲームソース: `elin_modding/Elin-Decompiled/`

## 開発ドキュメント

詳細は [DEVELOPMENT.md](./DEVELOPMENT.md) を参照。
