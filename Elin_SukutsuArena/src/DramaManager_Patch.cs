using HarmonyLib;
using System;
using System.Collections.Generic;
using System.Linq;
using Elin_SukutsuArena.Commands;
using UnityEngine;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// DramaManagerへのHarmonyパッチ
    /// 新しいアクション「modInvoke」を追加し、C#メソッド呼び出しを可能にする
    /// focusChara アクションにnullチェックを追加
    /// </summary>
    [HarmonyPatch(typeof(DramaManager))]
    public static class DramaManager_Patch
    {
        /// <summary>
        /// DramaManager.ParseLine の前に focusChara を安全なバージョンに差し替え
        /// </summary>
        [HarmonyPrefix]
        [HarmonyPatch("ParseLine")]
        public static void ParseLine_Prefix(DramaManager __instance, Dictionary<string, string> item)
        {
            try
            {
                if (!item.ContainsKey("action"))
                    return;

                string[] actionParts = item["action"].Split('/');
                string action = actionParts[0];

                // focusChara を安全なバージョンに差し替え
                if (action == "focusChara")
                {
                    string charaId = item.ContainsKey("param") ? item["param"] : "";

                    // 先にキャラの存在をチェック
                    bool charaExists = false;
                    if (EClass._map != null && !string.IsNullOrEmpty(charaId))
                    {
                        foreach (var c in EClass._map.charas)
                        {
                            if (c.id == charaId)
                            {
                                charaExists = true;
                                break;
                            }
                        }
                    }

                    if (!charaExists)
                    {
                        Debug.LogWarning($"[ArenaFocusChara] Character not found on map: {charaId}, replacing with safe wait");
                        // キャラがいない場合は wait アクションに差し替え
                        item["action"] = "wait";
                        item["param"] = "0.1";
                    }
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[ArenaPatch] Error in ParseLine_Prefix: {ex}");
            }
        }

        /// <summary>
        /// DramaManager.ParseLine の後にカスタムアクションを処理
        /// ArenaCommandRegistry にディスパッチ
        /// </summary>
        [HarmonyPostfix]
        [HarmonyPatch("ParseLine")]
        public static void ParseLine_Postfix(DramaManager __instance, Dictionary<string, string> item)
        {
            try
            {
                if (!item.ContainsKey("action"))
                    return;

                string[] actionParts = item["action"].Split('/');
                string action = actionParts[0];

                // modInvoke または invoke* の場合のみ処理
                if (action != "modInvoke" && action != "invoke*")
                    return;

                string param = item.ContainsKey("param") ? item["param"] : "";
                if (string.IsNullOrEmpty(param))
                {
                    Debug.LogError("[ArenaModInvoke] Missing param for modInvoke action");
                    return;
                }

                // jumpカラムを取得
                string jump = item.ContainsKey("jump") ? item["jump"] : "";

                // switch_flag コマンドの特別処理
                // PendingJumpTargetを使用してジャンプ先を動的に決定
                if (param.StartsWith("switch_flag("))
                {
                    var method = new DramaEventMethod(() =>
                    {
                        // action は空（jumpFuncで処理するため）
                    });
                    method.action = null;
                    method.jumpFunc = () =>
                    {
                        // switch_flag を実行してジャンプ先を決定
                        SwitchFlagCommand.PendingJumpTarget = null;
                        HandleModInvoke(__instance, param);
                        var target = SwitchFlagCommand.PendingJumpTarget;
                        Debug.Log($"[ArenaModInvoke] switch_flag jumpFunc returning: {target ?? "(null)"}");
                        return target ?? "";
                    };
                    __instance.AddEvent(method);
                }
                // jumpがある場合はjumpFuncを使用
                else if (!string.IsNullOrEmpty(jump))
                {
                    // CWLと同様のパターン: jumpFuncで条件に基づいてジャンプを制御
                    var method = new DramaEventMethod(() =>
                    {
                        HandleModInvoke(__instance, param);
                    });
                    method.action = null;
                    method.jumpFunc = () =>
                    {
                        HandleModInvoke(__instance, param);
                        // LastConditionResultがtrueならjumpを返す、falseなら空文字
                        return ArenaCommandRegistry.LastConditionResult ? jump : "";
                    };
                    __instance.AddEvent(method);
                }
                else
                {
                    // jumpがない場合は通常のイベント追加
                    __instance.AddEvent(delegate
                    {
                        HandleModInvoke(__instance, param);
                    });
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[ArenaModInvoke] Error in ParseLine_Postfix: {ex}");
            }
        }

        /// <summary>
        /// modInvoke アクションのハンドラ
        /// ArenaCommandRegistry にディスパッチ
        /// </summary>
        private static void HandleModInvoke(DramaManager manager, string param)
        {
            try
            {
                Debug.Log($"[ArenaModInvoke] HandleModInvoke: param='{param}'");

                var (methodName, args) = ParseMethodCall(param);

                // デバッグ用: check_quest系のコマンドを表示
                if (methodName.StartsWith("check_"))
                {
                    Msg.Say($"[modInvoke] {methodName}({string.Join(",", args)})");
                }
                if (string.IsNullOrEmpty(methodName))
                {
                    Debug.LogError($"[ArenaModInvoke] Invalid format: {param}");
                    return;
                }

                Debug.Log($"[ArenaModInvoke] Method: {methodName}, Args: [{string.Join(", ", args)}]");

                // ArenaCommandRegistry にディスパッチ
                bool handled = ArenaCommandRegistry.TryExecute(methodName, manager, args);

                if (!handled)
                {
                    Debug.LogWarning($"[ArenaModInvoke] Unknown command: {methodName}");
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[ArenaModInvoke] Error handling modInvoke: {ex}");
            }
        }

        /// <summary>
        /// メソッド呼び出し形式の文字列をパース
        /// 例: "methodName(arg1, arg2)" -> ("methodName", ["arg1", "arg2"])
        /// </summary>
        private static (string name, string[] args) ParseMethodCall(string param)
        {
            var openParen = param.IndexOf('(');
            if (openParen < 0)
            {
                return (null, Array.Empty<string>());
            }

            var name = param.Substring(0, openParen).Trim();
            var argsStr = param.Substring(openParen + 1, param.Length - openParen - 2);

            if (string.IsNullOrWhiteSpace(argsStr))
            {
                return (name, Array.Empty<string>());
            }

            var args = argsStr.Split(',').Select(s => s.Trim()).ToArray();
            return (name, args);
        }
    }
}
