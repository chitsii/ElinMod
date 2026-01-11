# Elin_SukutsuArena 開発ガイド

## CWLドキュメント

CWL（Custom Whatever Loader）の公式ドキュメント：

```
elin_modding/Elin.Docs/articles/100_Mod Documentation/Custom Whatever Loader/JP/
├── 0_README.md              # CWL概要・基本設定
├── API/                     # API拡張
├── Character/               # キャラクター定義
│   └── 1_talks.md           # addDrama_タグ、会話システム
├── Element/                 # 要素定義
├── Other/                   # その他
│   └── 4_drama.md           # ドラマアクション（invoke*, if_flag等）
└── Thing/                   # アイテム定義
```

主要な参照：
- `1_talks.md`: NPCにカスタムダイアログを紐付ける`addDrama_`タグ
- `4_drama.md`: `invoke*`, `if_flag`, `mod_flag`等の拡張アクション

## CWLキャラクタータグ

キャラクター定義（`create_chara_excel.py`）で使用するCWLタグ：

| タグ | 説明 |
|-----|------|
| `addZone_ゾーンID` | 指定ゾーンにキャラクターを生成 |
| `addFlag_StayHomeZone` | ランダム移動を無効化（初期ゾーンに留まる） |
| `addDrama_ドラマファイル名` | **ドラマシートをキャラクターにリンク** |
| `addStock` | 商人の在庫を追加 |
| `humanSpeak` | 人間らしい会話表示（括弧なし） |

### addDrama_ タグの重要性

**このタグがないと、NPCクリック時にゲームのデフォルト会話（`_chara.xlsx`）が表示される。**

```python
# 正しい例（ドラマが読み込まれる）
'tag': f'neutral,addZone_{ZONE_ID},addDrama_drama_sukutsu_receptionist,humanSpeak',

# 誤った例（デフォルト会話になる）
'tag': f'neutral,addZone_{ZONE_ID},humanSpeak',  # addDrama_がない！
```

ドラマファイル名は `drama_` プレフィックスを含める（例: `addDrama_drama_sukutsu_receptionist`）。

## ゲーム本体コード

Elin本体のソースコードは`Elin-Decompiled`以下に配置
```
Elin-Decompiled
```

## Mod構成

```
ElinMod/Elin_SukutsuArena/
├── src/                     # C#ソースコード
│   ├── Plugin.cs            # エントリーポイント（BepInExプラグイン）
│   ├── Commands/            # IArenaCommandの実装
│   ├── Core/                # ArenaContext, DialogFlagsStorage
│   ├── State/               # PlayerState, QuestState等
│   └── Generated/           # 自動生成（ArenaFlags.cs, ArenaQuestData.cs）
│
├── tools/                   # Python生成ツール
│   ├── build_all.py         # Python側フルビルド
│   ├── builder/             # 各種ジェネレーター
│   │   ├── create_chara_excel.py   # SourceChara.xlsx生成
│   │   ├── create_drama_excel.py   # ドラマExcel生成
│   │   ├── create_zone_excel.py    # SourceSukutsu.xlsx生成
│   │   ├── generate_flags.py       # ArenaFlags.cs生成
│   │   └── generate_quest_data.py  # ArenaQuestData.cs生成
│   └── common/              # 共通モジュール
│       ├── drama_builder.py        # ドラマDSL
│       ├── quest_dependencies.py   # クエスト定義
│       ├── battle_stages.py        # バトルステージ定義
│       └── scenarios/              # シナリオ定義（00_*.py）
│
├── LangMod/                 # 言語別データ（JP/EN）
│   └── */
│       ├── SourceChara.xlsx        # キャラクター定義
│       ├── SourceSukutsu.xlsx      # ゾーン定義
│       └── Dialog/Drama/*.xlsx     # ドラマファイル
│
├── Package/                 # 生成されるJSON設定
│   ├── quest_definitions.json
│   └── battle_stages.json
│
├── Texture/                 # テクスチャ
├── Portrait/                # キャラクターポートレート
├── Sound/                   # サウンド/BGM
│
├── elin_link/               # ゲームリンク（ビルド用）
│   └── Package/Elin_SukutsuArena/
│
├── build.bat                # 全体ビルドスクリプト
└── Elin_SukutsuArena.csproj # C#プロジェクト
```

## ビルド方法

### 全体ビルド（推奨）

```batch
cd ElinMod/Elin_SukutsuArena
build.bat
```

- build.bat → Releaseビルド（公開用）
- build.bat debug → DEBUGビルド（テスト用）


### Excel/Python単体ビルド

```bash
cd tools
uv run python build_all.py
```
※Elinゲームへのデプロイは行われない

### C#単体ビルド

```bash
cd ElinMod/Elin_SukutsuArena
dotnet build -c Release
```
※Elinゲームへのデプロイは行われない

### 個別スクリプト実行

```bash
cd tools

# ドラマExcelのみ再生成
uv run python builder/create_drama_excel.py

# キャラクターExcelのみ再生成
uv run python builder/create_chara_excel.py

# フラグコードのみ再生成
uv run python builder/generate_flags.py
```

## テスト・デバッグ

### バリデーション

```bash
cd tools/common
uv run python validation.py
```

シナリオ定義の整合性をチェック。

### フラグ検証

```bash
cd tools
uv run python builder/validate_scenario_flags.py
```

ドラマファイルで使用されるフラグがC#側で定義されているか検証。

## 既知の問題・バックログ

### キャラクターチップ移動問題
**報告日**: 2026-01-11
**状態**: 調査中

**症状**:
アスタロトやバルガスとの戦闘時、キャラクターの実体がキャラクターチップの表示についてきていない。
- キャラチップは最初の位置から動かない
- 実体は透明になって移動している

**影響キャラクター**:
- sukutsu_astaroth（アスタロト）
- sukutsu_balgas_prime（全盛期バルガス）

**調査メモ**:
- `_idRenderData: '@chara'` 設定は正しい（空にするとチップ自体が表示されなくなる）
- 現在の一時的なチップ画像の規格に起因する可能性あり
- ゲームエンジン側またはCWLの描画処理の問題かもしれない

**次のステップ**:
- カスタムチップ画像を正式な規格で作成後に再テスト
