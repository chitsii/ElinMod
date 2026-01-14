using System;
using System.IO;
using UnityEngine;
using DG.Tweening;
using Elin_SukutsuArena.Core;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// アリーナ管理クラス
    /// CWL eval から呼び出すためにstatic メソッドを提供
    /// </summary>
    public static class ArenaManager
    {
        /// <summary>
        /// ランク情報をログに表示（CWL evalから呼び出し）
        /// </summary>
        public static void ShowRankInfoLog()
        {
            int rank = (int)ArenaContext.I.Player.Rank;

            string rankName = rank switch
            {
                0 => "ランク外",
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

            Msg.Say($"現在のランク: 『{rankName}』 ");
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
                        // targetにPCを指定することで、CWLのif_flag等がEClass.player.dialogFlagsを参照できるようにする
                        LayerDrama.Activate(dramaName, null, null, EClass.pc, null, null);
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

            // 一時戦闘マップを作成
            Zone battleZone = SpatialGen.CreateInstance(stageData.ZoneType, new ZoneInstanceArenaBattle
            {
                uidMaster = master.uid,
                returnX = master.pos.x,
                returnZ = master.pos.z,
                uidZone = EClass._zone.uid,
                rewardPlat = stageData.RewardPlat,
                isRankUp = stageId.StartsWith("rank_"),
                stageId = stageId,
                bgmBattle = stageData.BgmBattle,
                bgmVictory = stageData.BgmVictory
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

        // ============================================================
        // 永久バフ付与システム（ランク昇格報酬）
        // ============================================================

        /// <summary>
        /// 闘志フィート付与/レベルアップ
        /// ランク昇格時にフィート「闘志（Arena Spirit）」を付与またはレベルアップする。
        /// </summary>
        /// <param name="level">フィートレベル (1-7)</param>
        public static void GrantArenaFeat(int level)
        {
            var pc = EClass.pc;
            if (pc == null || pc.elements == null)
            {
                Debug.LogWarning("[SukutsuArena] GrantArenaFeat: pc or elements is null, skipping");
                return;
            }

            try
            {
                const int featId = 10001; // featArenaSpirit

                // フィートを設定（既存の場合はレベルアップ）
                // SetFeatを使用することでfeat.Apply()が呼ばれ、活力ボーナスが適用される
                pc.SetFeat(featId, level, msg: false);

                // 活力ボーナスを計算
                int vigorBonus = level <= 5 ? level * 5 : (level == 6 ? 30 : 40);

                Msg.Say($"【闘志】Lv{level}を獲得！（活力+{vigorBonus}）");
                Debug.Log($"[SukutsuArena] Granted Arena Spirit feat Lv{level} (vigor+{vigorBonus})");
            }
            catch (Exception ex)
            {
                Debug.LogError($"[SukutsuArena] GrantArenaFeat failed: {ex.Message}");
            }
        }

        // ============================================================
        // サブクエスト報酬バフ
        // ============================================================

        /// <summary>
        /// リリィの私室クリア報酬: リリィの寵愛
        /// - 魔力+5
        /// - 回避+5
        /// - 魅了耐性+10
        /// </summary>
        public static void GrantLilyPrivateBonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 魔力+5 (Element ID: 76 = MAG)
            pc.elements.ModBase(76, 5);
            // 回避+5 (Element ID: 64 = DV)
            pc.elements.ModBase(64, 5);
            // 魅了耐性+10 (Element ID: 961 = resCharm)
            pc.elements.ModBase(961, 10);

            Msg.Say("【リリィの寵愛】魔力+5、回避+5、魅了耐性+10 を獲得！");
            Debug.Log("[SukutsuArena] Granted Lily Private bonus: MAG+5, DV+5, resCharm+10");
        }

        /// <summary>
        /// 上位存在クリア報酬: 観客の加護
        /// - 回避+3
        /// - 運+3
        /// </summary>
        public static void GrantUpperExistenceBonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 回避+3 (Element ID: 64 = DV)
            pc.elements.ModBase(64, 3);
            // 運+3 (Element ID: 78 = LUC)
            pc.elements.ModBase(78, 3);

            Msg.Say("【観客の加護】回避+3、運+3 を獲得！");
            Debug.Log("[SukutsuArena] Granted Upper Existence bonus: DV+3, LUC+3");
        }

        /// <summary>
        /// バルガス訓練クリア報酬: 戦士の心得
        /// - 筋力+3
        /// - 器用+3
        /// - PV+3
        /// </summary>
        public static void GrantBalgasTrainingBonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 筋力+3 (Element ID: 70 = STR)
            pc.elements.ModBase(70, 3);
            // 器用+3 (Element ID: 72 = DEX)
            pc.elements.ModBase(72, 3);
            // PV+3 (Element ID: 65 = PV)
            pc.elements.ModBase(65, 3);

            Msg.Say("【戦士の心得】筋力+3、器用+3、PV+3 を獲得！");
            Debug.Log("[SukutsuArena] Granted Balgas Training bonus: STR+3, DEX+3, PV+3");
        }

        /// <summary>
        /// バルガス戦クリア報酬: 戦鬼の証
        /// - 全耐性+5
        /// - 筋力+5
        /// - 耐久+5
        /// </summary>
        public static void GrantVsBalgasBonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 筋力+5 (Element ID: 70 = STR)
            pc.elements.ModBase(70, 5);
            // 耐久+5 (Element ID: 71 = END)
            pc.elements.ModBase(71, 5);
            // 火炎耐性+5 (Element ID: 950)
            pc.elements.ModBase(950, 5);
            // 冷気耐性+5 (Element ID: 951)
            pc.elements.ModBase(951, 5);
            // 電撃耐性+5 (Element ID: 952)
            pc.elements.ModBase(952, 5);
            // 毒耐性+5 (Element ID: 953)
            pc.elements.ModBase(953, 5);

            Msg.Say("【戦鬼の証】筋力+5、耐久+5、各種耐性+5 を獲得！");
            Debug.Log("[SukutsuArena] Granted VS Balgas bonus: STR+5, END+5, various resistances+5");
        }

        /// <summary>
        /// リリィ真名クリア報酬: 真名の絆
        /// - 魔力+10
        /// - 精神耐性+20
        /// - 魅了耐性+20
        /// </summary>
        public static void GrantLilyRealNameBonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 魔力+10 (Element ID: 77 = MAG)
            pc.elements.ModBase(77, 10);
            // 精神耐性+20 (Element ID: 954 = resMind)
            pc.elements.ModBase(954, 20);
            // 魅了耐性+20 (Element ID: 961 = resCharm)
            pc.elements.ModBase(961, 20);

            Msg.Say("【真名の絆】魔力+10、精神耐性+20、魅了耐性+20 を獲得！");
            Debug.Log("[SukutsuArena] Granted Lily Real Name bonus: MAG+10, resMind+20, resCharm+20");
        }

        /// <summary>
        /// 最終決戦クリア報酬: 虚空の王の力
        /// - 全主要ステータス+10
        /// - 全耐性+10
        /// </summary>
        public static void GrantLastBattleBonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 主要ステータス全て+10
            // STR=70, END=71, DEX=73, PER=74, LER=75, WIL=76, MAG=77, CHA=79
            int[] mainStats = { 70, 71, 73, 74, 75, 76, 77, 79 };
            foreach (int statId in mainStats)
            {
                pc.elements.ModBase(statId, 10);
            }

            // 全耐性+10
            // 火炎=950, 冷気=951, 電撃=952, 毒=953, 精神=954, 魔法=955
            int[] resistances = { 950, 951, 952, 953, 954, 955 };
            foreach (int resId in resistances)
            {
                pc.elements.ModBase(resId, 10);
            }

            Msg.Say("【虚空の王の力】全ステータス+10、全耐性+10 を獲得！");
            Debug.Log("[SukutsuArena] Granted Last Battle bonus: All stats+10, All resistances+10");
        }

        /// <summary>
        /// マクマ（ランクB後イベント）報酬
        /// </summary>
        public static void GrantMakumaReward()
        {
            Debug.Log("[SukutsuArena] Granted Makuma reward");
        }

        /// <summary>
        /// マクマ2（ランクA前イベント）報酬: コインとプラチナ
        /// </summary>
        public static void GrantMakuma2Reward()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 小さなコイン30枚
            for (int i = 0; i < 30; i++)
            {
                pc.Pick(ThingGen.Create("coin"));
            }

            // プラチナコイン15枚
            for (int i = 0; i < 15; i++)
            {
                pc.Pick(ThingGen.Create("plat"));
            }

            Msg.Say("【虚空の心臓】小さなコイン30枚、プラチナコイン15枚 を獲得！");
            Debug.Log("[SukutsuArena] Granted Makuma2 reward: 30 coins, 15 plat");
        }

        /// <summary>
        /// ゼクの共鳴瓶すり替えイベント完了処理
        /// </summary>
        public static void CompleteZekStealBottleQuest()
        {
            try
            {
                ArenaQuestManager.Instance.CompleteQuest("05_2_zek_steal_bottle");
                Debug.Log("[SukutsuArena] Completed Zek Steal Bottle quest");
            }
            catch (System.Exception ex)
            {
                Debug.LogError($"[SukutsuArena] Error completing Zek Steal Bottle quest: {ex.Message}");
            }
        }

        /// <summary>
        /// バルガス訓練クエスト完了処理
        /// </summary>
        public static void CompleteBalgasTrainingQuest()
        {
            try
            {
                ArenaQuestManager.Instance.CompleteQuest("09_balgas_training");

                // ステータスボーナス付与
                GrantBalgasTrainingBonus();

                Debug.Log("[SukutsuArena] Completed Balgas Training quest");
            }
            catch (System.Exception ex)
            {
                Debug.LogError($"[SukutsuArena] Error completing Balgas Training quest: {ex.Message}");
            }
        }

        /// <summary>
        /// マクマ2: 共鳴瓶告白 - リリィに正直に話した
        /// </summary>
        public static void Makuma2ConfessToLily()
        {
            var storage = Core.ArenaContext.I?.Storage;
            if (storage != null)
            {
                storage.SetInt("chitsii.arena.lily_trust_rebuild", 1);
            }
            // カルマ+5
            EClass.player.ModKarma(5);
            Debug.Log("[SukutsuArena] Makuma2: Confessed to Lily (Karma+5)");
        }

        /// <summary>
        /// マクマ2: 共鳴瓶告白 - ゼクのせいにした
        /// </summary>
        public static void Makuma2BlameZek()
        {
            // 関係値変更なし
            Debug.Log("[SukutsuArena] Makuma2: Blamed Zek");
        }

        /// <summary>
        /// マクマ2: 共鳴瓶告白 - 関与を否定した
        /// </summary>
        public static void Makuma2DenyInvolvement()
        {
            var storage = Core.ArenaContext.I?.Storage;
            if (storage != null)
            {
                storage.SetInt("chitsii.arena.lily_hostile", 1);
            }
            // カルマ-30
            EClass.player.ModKarma(-30);
            Debug.Log("[SukutsuArena] Makuma2: Denied involvement (Karma-30, hostile)");
        }

        /// <summary>
        /// マクマ2: カインの魂告白 - 正直に話した
        /// </summary>
        public static void Makuma2ConfessAboutKain()
        {
            var storage = Core.ArenaContext.I?.Storage;
            if (storage != null)
            {
                storage.SetInt("chitsii.arena.balgas_trust_broken", 1);
            }
            // カルマ-20
            EClass.player.ModKarma(-20);
            Debug.Log("[SukutsuArena] Makuma2: Confessed about Kain (Karma-20)");
        }

        /// <summary>
        /// マクマ2: カインの魂告白 - 嘘をついた
        /// </summary>
        public static void Makuma2LieAboutKain()
        {
            Debug.Log("[SukutsuArena] Makuma2: Lied about Kain");
        }

        /// <summary>
        /// マクマ2: 最終選択 - 信頼を選んだ
        /// </summary>
        public static void Makuma2ChooseTrust()
        {
            Debug.Log("[SukutsuArena] Makuma2: Chose trust");
        }

        /// <summary>
        /// マクマ2: 最終選択 - 知識を選んだ
        /// </summary>
        public static void Makuma2ChooseKnowledge()
        {
            Debug.Log("[SukutsuArena] Makuma2: Chose knowledge");
        }

        /// <summary>
        /// エンディングクレジットを表示
        /// Dialog.Confettiを使用した華やかなダイアログ
        /// </summary>
        public static void ShowEndingCredit()
        {
            var storage = Core.ArenaContext.I?.Storage;
            if (storage == null)
            {
                Debug.LogError("[SukutsuArena] ShowEndingCredit: Storage is null");
                return;
            }

            // エンディングタイプを取得
            int endingType = storage.GetInt("chitsii.arena.ending", -1);
            bool balgasKilled = storage.GetInt("chitsii.arena.balgas_killed", 0) == 1;
            bool lilyHostile = storage.GetInt("chitsii.arena.lily_hostile", 0) == 1;

            // エンド名を決定
            string endingName;
            if (balgasKilled && lilyHostile)
            {
                endingName = "孤独エンド";
            }
            else if (endingType == 0) // RESCUE
            {
                endingName = "解放エンド";
            }
            else if (endingType == 1) // INHERIT
            {
                endingName = "継承エンド";
            }
            else
            {
                endingName = "エンディング";
            }

            string title = $"～{endingName}～";
            string detail = "巣窟アリーナ\nメインストーリー完結\n\n" +
                            "制作: chitsii\n" +
                            "連絡先: X @chitsii";

            // ドラマ終了後に遅延してダイアログを表示（レイヤー競合回避）
            // 1.5秒待機: finish() + fade_in(0.5s) + GraphicRaycaster有効化(0.3s)を確実に待つ
            DOVirtual.DelayedCall(1.5f, () =>
            {
                Dialog.Ok($"{title}\n\n{detail}");
            });
            Debug.Log($"[SukutsuArena] ShowEndingCredit: {endingName}");
        }
    }
}
