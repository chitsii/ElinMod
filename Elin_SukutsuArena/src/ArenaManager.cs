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
            int contribution = ArenaContext.I.Player.Contribution;

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
        /// Rank D 昇格報酬: 銅貨稼ぎの加護
        /// - 回避+5
        /// - 運+3
        /// </summary>
        public static void GrantRankDBonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 回避+5 (Element ID: 152 = DV)
            pc.elements.ModBase(152, 5);
            // 運+3 (Element ID: 78 = LUC)
            pc.elements.ModBase(78, 3);

            Msg.Say("【銅貨稼ぎの加護】回避+5、運+3 を獲得！");
            Debug.Log("[SukutsuArena] Granted Rank D bonus: DV+5, LUC+3");
        }

        /// <summary>
        /// Rank C 昇格報酬: 闘技場の鴉の加護
        /// - クリティカル率向上（器用+5）
        /// - スタミナ+10
        /// </summary>
        public static void GrantRankCBonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 器用+5 (Element ID: 73 = DEX) - クリティカルに影響
            pc.elements.ModBase(73, 5);
            // スタミナ+10 (Element ID: 151 = Stamina)
            pc.elements.ModBase(151, 10);

            Msg.Say("【闘技場の鴉の加護】器用+5、スタミナ+10 を獲得！");
            Debug.Log("[SukutsuArena] Granted Rank C bonus: DEX+5, Stamina+10");
        }

        /// <summary>
        /// Rank B 昇格報酬: 銀翼の加護
        /// - 全主要ステータス+3
        /// - 魔法耐性+10
        /// </summary>
        public static void GrantRankBBonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 主要ステータス全て+3
            // STR=70, END=71, DEX=73, PER=74, LER=75, WIL=76, MAG=77, CHA=79
            int[] mainStats = { 70, 71, 73, 74, 75, 76, 77, 79 };
            foreach (int statId in mainStats)
            {
                pc.elements.ModBase(statId, 3);
            }

            // 魔法耐性+10 (Element ID: 955 = resMagic)
            pc.elements.ModBase(955, 10);

            Msg.Say("【銀翼の加護】全ステータス+3、魔法耐性+10 を獲得！");
            Debug.Log("[SukutsuArena] Granted Rank B bonus: All stats+3, Magic Resist+10");
        }

        /// <summary>
        /// Rank A 昇格報酬: 黄金の戦鬼の加護（影の自己を倒した証）
        /// - 筋力+5
        /// - 魔力+5
        /// - 回避+5
        /// - PV+5
        /// </summary>
        public static void GrantRankABonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 筋力+5 (Element ID: 70 = STR)
            pc.elements.ModBase(70, 5);
            // 魔力+5 (Element ID: 77 = MAG)
            pc.elements.ModBase(77, 5);
            // 回避+5 (Element ID: 152 = DV)
            pc.elements.ModBase(152, 5);
            // PV+5 (Element ID: 153 = PV)
            pc.elements.ModBase(153, 5);

            Msg.Say("【黄金の戦鬼】筋力+5、魔力+5、回避+5、PV+5 を獲得！");
            Debug.Log("[SukutsuArena] Granted Rank A bonus: STR+5, MAG+5, DV+5, PV+5");
        }

        /// <summary>
        /// Rank E 昇格報酬: 鉄屑の加護（カインを倒した証）
        /// - 筋力+3
        /// - PV+5
        /// </summary>
        public static void GrantRankEBonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 筋力+3 (Element ID: 70 = STR)
            pc.elements.ModBase(70, 3);
            // PV+5 (Element ID: 153 = PV)
            pc.elements.ModBase(153, 5);

            Msg.Say("【鉄屑の加護】筋力+3、PV+5 を獲得！");
            Debug.Log("[SukutsuArena] Granted Rank E bonus: STR+3, PV+5");
        }

        /// <summary>
        /// Rank F 昇格報酬: 泥犬の加護（冷気を生き延びた証）
        /// - 耐久+3
        /// - 冷気耐性+5
        /// </summary>
        public static void GrantRankFBonus()
        {
            var pc = EClass.pc;
            if (pc == null) return;

            // 耐久+3 (Element ID: 71 = END)
            pc.elements.ModBase(71, 3);
            // 冷気耐性+5 (Element ID: 951 = resCold)
            pc.elements.ModBase(951, 5);

            Msg.Say("【泥犬の加護】耐久+3、冷気耐性+5 を獲得！");
            Debug.Log("[SukutsuArena] Granted Rank F bonus: END+3, Cold Resist+5");
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

            // 魔力+5 (Element ID: 77 = MAG)
            pc.elements.ModBase(77, 5);
            // 回避+5 (Element ID: 152 = DV)
            pc.elements.ModBase(152, 5);
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

            // 回避+3 (Element ID: 152 = DV)
            pc.elements.ModBase(152, 3);
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
            // 器用+3 (Element ID: 73 = DEX)
            pc.elements.ModBase(73, 3);
            // PV+3 (Element ID: 153 = PV)
            pc.elements.ModBase(153, 3);

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
    }
}
