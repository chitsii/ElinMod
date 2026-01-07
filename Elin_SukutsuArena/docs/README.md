# Sukutsu Arena ドキュメント

地下闘技場（ヴォイド・コロシアム）Modの開発ドキュメント集。

---

## 設計ドキュメント (design/)

| ファイル | 内容 |
|----------|------|
| [quest_system.md](design/quest_system.md) | クエストシステム全体設計 |
| [battle_system_design.md](design/battle_system_design.md) | バトルシステム設計 |
| [arena_ranks.md](design/arena_ranks.md) | アリーナランク定義（G〜虚空の王） |
| [flags.md](design/flags.md) | フラグ仕様・状態管理 |

---

## 開発者向け (dev/)

| ファイル | 内容 |
|----------|------|
| [troubleshooting.md](dev/troubleshooting.md) | **よく引っかかるポイント** |
| [scenario_coding.md](dev/scenario_coding.md) | シナリオ実装ガイド（DramaBuilder API等） |
| [cwl_drama_format.md](dev/cwl_drama_format.md) | CWLドラマ形式リファレンス |
| [quest_implementation.md](dev/quest_implementation.md) | クエストシステム実装詳細 |
| [production_facilities_technical.md](dev/production_facilities_technical.md) | **生産施設 技術検証レポート** |

---

## 世界観・設定 (lore/)

| ファイル | 内容 |
|----------|------|
| [world_setting.md](lore/world_setting.md) | 世界設定書（次元構造、キャラクター詳細、年表） |

---

## AIプロンプト (prompts/)

| ファイル | 内容 |
|----------|------|
| [scenario_prompt.md](prompts/scenario_prompt.md) | シナリオレビュー用プロンプト |
| [bgm_prompt.md](prompts/bgm_prompt.md) | BGM生成用プロンプト |
| [bgm_list.md](prompts/bgm_list.md) | BGMリスト・仕様 |

---

## シナリオファイル (scenario/)

シナリオ本体は `docs/scenario/formatted/` に配置：

```
scenario/formatted/
├── 01_opening.md          オープニング
├── 02_rank_up_01.md       ランクG昇格試験
├── 03_zek.md              ゼクとの出会い
├── ...
└── 18_last_battle.md      最終決戦
```

---

## ツールドキュメント

各ツールの説明書はツールと同じ場所に配置：

- `tools/common/README_DRAMA.md` - ドラマビルダー説明
- `tools/graphics/README.md` - グラフィックツール説明
- `tools/graphics/CHARACTER_PROMPTS.md` - キャラクター画像生成プロンプト
