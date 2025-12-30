using System;
using System.Reflection;
using System.Collections.Generic;

namespace Elin_AutoOfferingAlter
{
    public static class ModUtilRegister
    {
        /// <summary>
        /// Clones a SourceThing.Row (or any object) using MemberwiseClone (Shallow Copy).
        /// This is effective for elin rows to carry over internal references.
        /// </summary>
        public static T CloneRow<T>(T source) where T : class
        {
            if (source == null) return null;
            MethodInfo cloneMethod = typeof(object).GetMethod("MemberwiseClone", BindingFlags.NonPublic | BindingFlags.Instance);
            return (T)cloneMethod.Invoke(source, null);
        }

        /// <summary>
        /// Finds a SourceThing.Row by ID in the things source.
        /// </summary>
        public static SourceThing.Row FindThing(SourceThing things, string id)
        {
            // Try map first for O(1)
            if (things.map.TryGetValue(id, out var row)) return row;

            // Fallback to searching rows (in case map isn't rebuilt yet, though unlikely for things)
            foreach (var r in things.rows)
            {
                if (r.id == id) return r;
            }
            return null;
        }

        /// <summary>
        /// Registers a new row into the SourceThing.
        /// Safe to call multiple times (checks existence).
        /// </summary>
        public static void RegisterThing(SourceThing things, SourceThing.Row newRow)
        {
            if (things.map.ContainsKey(newRow.id))
            {
                // Already registered
                return;
            }

            things.rows.Add(newRow);
            things.map.Add(newRow.id, newRow);
        }

        /// <summary>
        /// Registers a new item by cloning a base item, properly configuring it, and adding it to source.
        /// </summary>
        public static void RegisterFromBase(SourceThing things, string baseId, string newId, Action<SourceThing.Row> configure)
        {
            var baseRow = FindThing(things, baseId);
            if (baseRow == null)
            {
                if (ModConfig.EnableLog.Value) Plugin.Log.LogError($"Base item '{baseId}' not found.");
                return;
            }

            var newRow = CloneRow(baseRow);
            if (newRow == null) return;

            newRow.id = newId;
            configure?.Invoke(newRow);

            RegisterThing(things, newRow);
            if (ModConfig.EnableLog.Value) Plugin.Log.LogInfo($"Injected custom item: {newId}");
        }

        /// <summary>
        /// Ensures the player knows the recipe for the given item ID.
        /// Call this in OnLoad or OnStartNewGame.
        /// </summary>
        public static void LearnRecipe(string recipeId)
        {
            if (EClass.player == null || EClass.player.recipes == null) return;

            if (!EClass.player.recipes.knownRecipes.ContainsKey(recipeId))
            {
                // false = not alerted? or simple add. In user code it was false.
                EClass.player.recipes.Add(recipeId, false);
            }
        }
    }
}
