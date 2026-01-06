using System.IO;
using UnityEngine;
using DG.Tweening;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// アリーナのステージ設定を保持するクラス（旧互換用）
    /// </summary>
    public class ArenaStageConfig
    {
        public string[] MonsterIds { get; set; }
        public int[] MonsterLevels { get; set; }
        public string[] MonsterRarities { get; set; }
        public int RewardPlat { get; set; }
        public string ZoneType { get; set; }
        public string BgmBattle { get; set; }
        public string BgmVictory { get; set; }
        public string StageId { get; set; }
    }

    /// <summary>
    /// アリーナ管理クラス
    /// CWL eval から呼び出すためにstatic メソッドを提供
    /// </summary>
    public static class ArenaManager
    {
        /// <summary>
        /// ステージごとの敵設定を取得
        /// </summary>
        public static ArenaStageConfig GetStageConfig(int stage, bool isRankUp = false)
        {
            // ランクアップ用の敵設定
            if (isRankUp)
            {
                return new ArenaStageConfig
                {
                    MonsterIds = new[] { "putty", "putty", "putty", "putty", "putty" },
                    MonsterLevels = new[] { 1, 1, 1, 1, 1 },
                    RewardPlat = 5,
                    ZoneType = "field"
                };
            }

            // 通常ステージ設定
            switch (stage)
            {
                case 1:
                    return new ArenaStageConfig
                    {
                        MonsterIds = new[] { "wolf" },
                        MonsterLevels = new[] { 1 },
                        RewardPlat = 10,
                        ZoneType = "field"
                    };
                case 2:
                    return new ArenaStageConfig
                    {
                        MonsterIds = new[] { "centaur" },
                        MonsterLevels = new[] { 1 },
                        RewardPlat = 20,
                        ZoneType = "field"
                    };
                case 3:
                    return new ArenaStageConfig
                    {
                        MonsterIds = new[] { "minotaur" },
                        MonsterLevels = new[] { 1 },
                        RewardPlat = 30,
                        ZoneType = "field"
                    };
                case 4:
                    return new ArenaStageConfig
                    {
                        MonsterIds = new[] { "dragon" },
                        MonsterLevels = new[] { 1 },
                        RewardPlat = 50,
                        ZoneType = "field"
                    };
                default:
                    return new ArenaStageConfig
                    {
                        MonsterIds = new[] { "wolf" },
                        MonsterLevels = new[] { 1 },
                        RewardPlat = 10,
                        ZoneType = "field"
                    };
            }
        }

        /// <summary>
        /// 戦闘開始（CWL evalから呼び出し）
        /// </summary>
        /// <param name="master">アリーナマスター</param>
        /// <param name="stage">ステージ番号</param>
        /// <param name="isRankUp">ランク検定かどうか</param>
        public static void StartBattle(Chara master, int stage, bool isRankUp = false)
        {
            Debug.Log($"[SukutsuArena] StartBattle called: master={master?.Name}, stage={stage}, isRankUp={isRankUp}");

            if (master == null)
            {
                Debug.LogError("[SukutsuArena] Arena Master is null!");
                return;
            }

            var config = GetStageConfig(stage, isRankUp);

            // 一時戦闘マップを作成
            Zone battleZone = SpatialGen.CreateInstance(config.ZoneType, new ZoneInstanceArenaBattle
            {
                uidMaster = master.uid,
                returnX = master.pos.x,
                returnZ = master.pos.z,
                uidZone = EClass._zone.uid,
                bossCount = config.MonsterIds.Length,
                stage = stage,
                rewardPlat = config.RewardPlat,
                isRankUp = isRankUp
            });

            // 敵配置イベントを追加
            battleZone.events.AddPreEnter(new ZonePreEnterArenaBattle
            {
                bossLevel = config.MonsterLevels[0],
                bossCount = config.MonsterIds.Length,
                bossIds = config.MonsterIds,
                stage = stage,
                isRankUp = isRankUp
            });

            // 戦闘監視イベントを追加
            battleZone.events.Add(new ZoneEventArenaBattle());

            Debug.Log($"[SukutsuArena] Created battle zone, moving player...");

            // ダイアログ終了後にゾーン移動
            LayerDrama.Instance?.SetOnKill(() =>
            {
                Debug.Log($"[SukutsuArena] Drama closed, moving to battle zone");
                EClass.pc.MoveZone(battleZone, ZoneTransition.EnterState.Center);
            });
        }

        /// <summary>
        /// 戦闘開始（キャラクターIDからマスターを検索）
        /// 別のドラマから呼び出す場合に使用
        /// </summary>
        /// <param name="masterId">アリーナマスターのキャラクターID</param>
        /// <param name="stage">ステージ番号</param>
        /// <param name="isRankUp">ランク検定かどうか</param>
        public static void StartBattleById(string masterId, int stage, bool isRankUp = false)
        {
            Debug.Log($"[SukutsuArena] StartBattleById called: masterId={masterId}, stage={stage}, isRankUp={isRankUp}");

            // ゾーン内からマスターを検索
            var master = EClass._zone.FindChara(masterId);
            if (master == null)
            {
                Debug.LogError($"[SukutsuArena] Arena Master not found by ID: {masterId}");
                return;
            }

            // 既存のStartBattleに委譲
            StartBattle(master, stage, isRankUp);
        }

        /// <summary>
        /// ランク情報をログに表示（CWL evalから呼び出し）
        /// </summary>
        public static void ShowRankInfoLog()
        {
            int rank = (int)ArenaFlagManager.Player.GetRank();
            int contribution = ArenaFlagManager.Player.GetContribution();

            string rankName = rank switch
            {
                0 => "Unranked (ランクなし)",
                1 => "G - 屑肉",
                2 => "F - 泥犬",
                3 => "E - 鉄屑",
                4 => "D - 銅貨稼ぎ",
                5 => "C - 鴉",
                6 => "B - 銀翼",
                7 => "A - 戦鬼",
                8 => "S - 屠竜者",
                _ => $"Rank {rank} (Unknown)"
            };

            Msg.Say($"現在のランク: {rankName}");
            Msg.Say($"貢献度: {contribution}");
        }

        /// <summary>
        /// 指定したドラマを開始する（CWL evalから呼び出し）
        /// </summary>
        public static void StartDrama(string dramaName)
        {
            Debug.Log($"[SukutsuArena] StartDrama called with: {dramaName}");

            if (LayerDrama.Instance == null)
            {
                Debug.LogError($"[SukutsuArena] LayerDrama.Instance is null! Cannot schedule next drama.");
                return;
            }

            // 現在のドラマが終了した後に、次のドラマを開始する
            LayerDrama.Instance.SetOnKill(() =>
            {
                Debug.Log($"[SukutsuArena] SetOnKill callback triggered for drama: {dramaName}. Scheduling delayed activation.");

                // 即座ではなく少し待つ（UIの破棄タイミング回避）
                DOVirtual.DelayedCall(0.05f, () =>
                {
                    Debug.Log($"[SukutsuArena] DelayedCall executed. Attempting to activate drama: {dramaName}");
                    try
                    {
                        LayerDrama.Activate(dramaName, null, null, null, null, null);
                        Debug.Log($"[SukutsuArena] LayerDrama.Activate returned successfully.");
                    }
                    catch (System.Exception ex)
                    {
                        Debug.LogError($"[SukutsuArena] Failed to activate drama '{dramaName}': {ex}");
                    }
                });
            });
            Debug.Log($"[SukutsuArena] SetOnKill registered successfully.");
        }

        /// <summary>
        /// メッセージをログに表示してからドラマを開始する
        /// CWLのsayアクション後にevalが実行されない問題を回避するための一括処理
        /// Msg.Sayでログに表示し、ドラマを開始する
        /// </summary>
        /// <param name="actorId">発言者のキャラクターID</param>
        /// <param name="message">表示するメッセージ</param>
        /// <param name="dramaName">開始するドラマ名</param>
        public static void SayAndStartDrama(string actorId, string message, string dramaName)
        {
            Debug.Log($"[SukutsuArena] SayAndStartDrama called: actor={actorId}, drama={dramaName}");

            // アクター名を取得してログに表示
            var actor = EClass._zone.FindChara(actorId);
            if (actor != null)
            {
                Msg.Say($"{actor.Name}: {message}");
            }
            else
            {
                Msg.Say(message);
            }

            // ドラマを開始
            StartDrama(dramaName);
        }

        /// <summary>
        /// ステージIDを指定して戦闘を開始（新API）
        /// JSONファイルからステージ設定を読み込んで戦闘を開始する
        /// </summary>
        /// <param name="stageId">ステージID</param>
        /// <param name="master">アリーナマスター（戻り先）</param>
        public static void StartBattleByStage(string stageId, Chara master)
        {
            Debug.Log($"[SukutsuArena] StartBattleByStage called: stageId={stageId}");

            if (master == null)
            {
                Debug.LogError("[SukutsuArena] Master is null!");
                return;
            }

            // パッケージパスを取得
            string packagePath = GetPackagePath();
            if (string.IsNullOrEmpty(packagePath))
            {
                Debug.LogError("[SukutsuArena] Could not determine package path!");
                return;
            }

            // ステージ設定を取得
            var stageData = BattleStageLoader.GetStage(stageId, packagePath);
            if (stageData == null)
            {
                Debug.LogError($"[SukutsuArena] Stage not found: {stageId}");
                Msg.Say($"Error: Stage '{stageId}' not found!");
                return;
            }

            // ArenaStageConfigに変換
            var config = ConvertToArenaStageConfig(stageData);

            // 一時戦闘マップを作成
            Zone battleZone = SpatialGen.CreateInstance(config.ZoneType, new ZoneInstanceArenaBattle
            {
                uidMaster = master.uid,
                returnX = master.pos.x,
                returnZ = master.pos.z,
                uidZone = EClass._zone.uid,
                bossCount = stageData.TotalEnemyCount,
                stage = 0, // ステージID方式では使用しない
                rewardPlat = config.RewardPlat,
                isRankUp = stageId.StartsWith("rank_"),
                stageId = stageId,
                bgmBattle = config.BgmBattle,
                bgmVictory = config.BgmVictory
            });

            // 敵配置イベントを追加
            battleZone.events.AddPreEnter(new ZonePreEnterArenaBattle
            {
                stageId = stageId,
                stageData = stageData
            });

            // 戦闘監視イベントを追加
            battleZone.events.Add(new ZoneEventArenaBattle());

            Debug.Log($"[SukutsuArena] Created battle zone for stage: {stageId}");

            // ダイアログ終了後にゾーン移動
            LayerDrama.Instance?.SetOnKill(() =>
            {
                Debug.Log($"[SukutsuArena] Moving to battle zone: {stageId}");
                EClass.pc.MoveZone(battleZone, ZoneTransition.EnterState.Center);
            });
        }

        /// <summary>
        /// ステージIDを指定して戦闘を開始（マスターIDで検索）
        /// </summary>
        public static void StartBattleByStage(string stageId, string masterId)
        {
            var master = EClass._zone.FindChara(masterId);
            if (master == null)
            {
                Debug.LogError($"[SukutsuArena] Master not found: {masterId}");
                return;
            }
            StartBattleByStage(stageId, master);
        }

        /// <summary>
        /// パッケージパスを取得
        /// </summary>
        private static string GetPackagePath()
        {
            // Pluginアセンブリの場所からパスを取得
            var modPath = Path.GetDirectoryName(typeof(Plugin).Assembly.Location);
            if (!string.IsNullOrEmpty(modPath))
            {
                var packagePath = Path.Combine(modPath, "Package");
                if (Directory.Exists(packagePath))
                {
                    return packagePath;
                }
            }

            // フォールバック: 既知のパスを試す
            string[] possiblePaths = new[]
            {
                Path.Combine(Application.dataPath, "..", "Package", "Elin_SukutsuArena", "Package"),
                Path.Combine(Application.dataPath, "..", "Mods", "Elin_SukutsuArena", "Package"),
            };

            foreach (var path in possiblePaths)
            {
                if (Directory.Exists(path))
                {
                    return path;
                }
            }

            return null;
        }

        /// <summary>
        /// BattleStageDataをArenaStageConfigに変換
        /// </summary>
        private static ArenaStageConfig ConvertToArenaStageConfig(BattleStageData stageData)
        {
            var monsterIds = new System.Collections.Generic.List<string>();
            var monsterLevels = new System.Collections.Generic.List<int>();
            var monsterRarities = new System.Collections.Generic.List<string>();

            foreach (var enemy in stageData.Enemies)
            {
                for (int i = 0; i < enemy.Count; i++)
                {
                    monsterIds.Add(enemy.CharaId);
                    monsterLevels.Add(enemy.Level);
                    monsterRarities.Add(enemy.Rarity);
                }
            }

            return new ArenaStageConfig
            {
                MonsterIds = monsterIds.ToArray(),
                MonsterLevels = monsterLevels.ToArray(),
                MonsterRarities = monsterRarities.ToArray(),
                RewardPlat = stageData.RewardPlat,
                ZoneType = stageData.ZoneType,
                BgmBattle = stageData.BgmBattle,
                BgmVictory = stageData.BgmVictory,
                StageId = stageData.StageId
            };
        }
    }
}
