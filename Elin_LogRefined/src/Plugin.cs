using BepInEx;
using HarmonyLib;
using EvilMask.Elin.ModOptions;

namespace Elin_LogRefined
{
    [BepInPlugin(ModGuid, "Log Refined", "0.23.252")]
    [BepInDependency("evilmask.elinplugins.modoptions", BepInDependency.DependencyFlags.SoftDependency)]
    public class Plugin : BaseUnityPlugin
    {
        public const string ModGuid = "elin_log_refined";

        private void Awake()
        {
            ModConfig.LoadConfig(Config);
            var harmony = new Harmony(ModGuid);
            harmony.PatchAll();
        }

        private void Start()
        {
            foreach (var obj in ModManager.ListPluginObject)
            {
                var plugin = obj as BaseUnityPlugin;
                if (plugin.Info.Metadata.GUID == "evilmask.elinplugins.modoptions")
                {
                    InitModOptions();
                    break;
                }
            }
        }

        private void InitModOptions()
        {
            var bridge = new ModOptionsBridge();
            var controller = ModOptionController.Register(ModGuid, "elin_log_refined", bridge);
            bridge.SetTranslations(controller);
        }
    }
}
