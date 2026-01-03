using HarmonyLib;
using UnityEngine;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// アリーナ関連のHarmonyパッチまとめ
    /// </summary>
    public static class ArenaZonePatches
    {
        /// <summary>
        /// ゾーンがアクティブになった時のパッチ
        /// アリーナから敗北・勝利して戻った時に自動でアリーナマスターと会話を開始
        /// </summary>
        [HarmonyPatch(typeof(Zone), nameof(Zone.Activate))]
        public static class ArenaZoneActivatePatch
        {
            [HarmonyPostfix]
            public static void Postfix(Zone __instance)
            {
                // 自動会話フラグがあるか確認
                // Zone IDチェックは外し、フラグの存在のみで判断（誤爆リスクは低いと判断）
                if (!EClass.player.dialogFlags.ContainsKey("sukutsu_auto_dialog"))
                    return;

                int masterUid = EClass.player.dialogFlags["sukutsu_auto_dialog"];
                if (masterUid <= 0)
                    return;

                Debug.Log($"[SukutsuArena] Auto-dialog triggered for master UID: {masterUid}");

                // フラグをクリア
                EClass.player.dialogFlags["sukutsu_auto_dialog"] = 0;

                // アリーナマスターを探す
                // マップロード直後なのでFindで取れるはずだが、取れない場合は現在のマップからIDで探す
                Chara master = EClass.game.cards.Find(masterUid) as Chara;
                if (master == null || !master.ExistsOnMap)
                {
                    // UIDで見つからない場合、現在のマップにいる同IDのキャラを探す
                    foreach (var c in EClass._map.charas)
                    {
                        if (c.id == "sukutsu_arena_master")
                        {
                            master = c;
                            break;
                        }
                    }
                }

                if (master != null && master.ExistsOnMap)
                {
                    Debug.Log($"[SukutsuArena] Showing dialog with {master.Name}");
                    master.ShowDialog();
                }
                else
                {
                    Debug.LogWarning($"[SukutsuArena] Arena Master {masterUid} not found or not on map (searching local map also failed)");

                    // デバッグ用：マップ上のキャラ一覧を出力
                    Debug.Log($"[SukutsuArena] Current map charas: {EClass._map.charas.Count}");
                }
            }
        }

        /// <summary>
        /// アリーナ戦闘ゾーンでは自動復活（ゲームオーバー回避）を有効にするパッチ
        /// </summary>
        [HarmonyPatch(typeof(Zone), "get_ShouldAutoRevive")]
        public static class ArenaZoneRevivePatch
        {
            [HarmonyPostfix]
            public static void Postfix(Zone __instance, ref bool __result)
            {
                if (__instance.instance is ZoneInstanceArenaBattle)
                {
                    // アリーナバトル中は強制的に復活可能（ゲームオーバーにならない）
                    // 実際の復活処理と退出はZoneEventArenaBattle.OnCharaDieで行う
                    __result = true;
                }
            }
        }
    }
}
