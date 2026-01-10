# Elin_SukutsuArena プロジェクト

Elin用のMod。闘技場を追加する。

## 開発ドキュメント

詳細は [DEVELOPMENT.md](./DEVELOPMENT.md) を参照。

## クイックリファレンス

### ビルド
```batch
build.bat          # 全体ビルド（Excel生成→C#→デプロイ）
```

### 部分ビルド
```bash
cd tools
uv run python build_all.py                    # Excel/JSON生成のみ
uv run python builder/create_drama_excel.py   # ドラマExcelのみ
```

### デバッグキー（ゲーム内）
- F9: 状態表示
- F11: クエスト完了
- F12: ランク変更

### 主要ディレクトリ
- `src/` - C#ソース
- `tools/` - Python生成ツール
- `tools/common/scenarios/` - シナリオ定義
- `LangMod/JP/` - 日本語Excel/ドラマ
- `elin_link/` - ゲームリンク（ビルド用）

### CWLドキュメント
`elin_modding/Elin.Docs/articles/100_Mod Documentation/Custom Whatever Loader/JP/`

### CWLのソースコード
`Elin.Plugins/CustomWhateverLoader/`

### ゲームソースコード
`elin_modding/Elin-Decompiled/`

