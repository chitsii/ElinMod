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

### デバッグキー（DEBUGビルドのみ）
- F9: 状態表示
- F11: クエスト完了
- F12: ランク変更

※ 公開版(Releaseビルド)ではデバッグキーは無効

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

## 公開ロードマップ

### Phase 1: 実装 (完了)
- [x] バルガス戦 → **バトル統合** (rank_s_trial使用)
- [x] デバッグ機能 → **削除** (公開版から除外)
- [x] 15_vs_balgas.py バトル追加
- [x] 00_arena_master.py 結果処理追加
- [x] Plugin.cs デバッグキー削除 (#if DEBUG)
- [x] デバッグメニュー自動化 (99_debug_menu.py)
  - 命名規則でカテゴリ自動判定
  - 新ドラマ/バトル追加時に自動反映

### Phase 2: QA
- [ ] フルプレイテスト (全分岐 + 3エンディング)
- [ ] バトルバランス確認

### Phase 3: 公開準備
- [ ] preview.jpg 作成 (512x512, 1MB未満)
- [ ] package.xml バージョン更新 (0.24.0)

### Phase 4: リリース
- [ ] 最終ビルド (build.bat)
- [ ] Steam Workshop 公開

### 依存Mod
- Custom Whatever Loader (CWL)

