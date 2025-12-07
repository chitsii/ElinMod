using BepInEx;
using HarmonyLib;
using UnityEngine;

namespace Elin_AutoEatSleep
{
    [BepInPlugin("com.elin.autoeatsleep", "Elin Auto Eat & Sleep", "1.0.0")]
    public class Plugin : BaseUnityPlugin
    {
        public static Plugin Instance { get; private set; }
        public ModConfig MyConfig { get; private set; }
        public AutoEatLogic Logic { get; private set; }

        private void Awake()
        {
            Instance = this;
            MyConfig = new ModConfig(base.Config);
            Logic = new AutoEatLogic();

            var harmony = new Harmony("com.elin.autoeatsleep");

            // Explicitly patch ONLY our logic class to ensure no interference if class attributes are weird
            harmony.CreateClassProcessor(typeof(AutoEatLogic)).Patch();

            // Also patch other classes in assembly (ConfigUI, etc.) if they exist and are not already patched.
            // Using CreateClassProcessor invalidates the need for PatchAll on this specific class, but PatchAll handles others.
            // But to be SAFE and SURGICAL given the "AutoAct patching" issue, let's stick to manual patching if possible,
            // or PatchAll if we are confident no other classes conflict.
            // Attempting PatchAll again but Logic is already patched? Harmony handles idempotency.
            harmony.PatchAll();

            Logger.LogInfo("Elin Auto Eat & Sleep Mod Loaded (AutoEatLogic Renamed).");
        }

        private void Update()
        {
            // Event driven.
        }
    }
}
