using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

namespace _20MTDRandomizer;

[BepInPlugin("com.oig.20MTDArchipelago", "20MTDArchipelago", "1.0.0")]
[BepInProcess("MinutesTillDawn.exe")]
public class Plugin : BaseUnityPlugin
{
    internal static new ManualLogSource Logger;

    private bool patchSuccessful = false;

    private GameObject archipelagoMenu;

    private void Awake()
    {
        // Plugin startup logic
        Logger = base.Logger;

        try
        {
            Harmony.CreateAndPatchAll(typeof(Patch.GetPowerupPoolPatch));

            patchSuccessful = true;
        }
        catch (System.Exception e)
        {
            Logger.LogError($"an error occurred during plugin 20MTDArchipelago initialization: {e.Message}");
        }

        Logger.LogInfo($"Plugin 20MTDArchipelago is loaded!");
    }

    private void Start()
    {
        if (patchSuccessful)
        {
            CreateArchipelagoButtonAndMenu();
        }
    }

    private void OnDestroy()
    {
        Harmony.UnpatchAll();
    }

    //create archipelago button in main menu
    private void CreateArchipelagoButtonAndMenu()
    {
        GameObject originalButton = GameObject.Find("Canvas/TitleScreen/MainMenuButtons/ButtonQuit");
        GameObject archipelagoButton = Instantiate(originalButton, originalButton.transform.parent);

        // ((RectTransform)originalButton.transform).anchoredPosition += new Vector2(0, 20);
        // ((RectTransform)archipelagoButton.transform).anchoredPosition += new Vector2(0, -20);

        archipelagoButton.name = "ArchipelagoButton";
        // archipelagoButton.GetComponentInChildren<TextMeshProUGUI>().text = "Archipelago";
        archipelagoButton.AddComponent<ButtonFixer>();
        archipelagoButton.GetComponent<Button>().onClick.AddListener(ToggleArchipelagoMenu);

        GameObject originalMenu = GameObject.Find("Canvas/TitleScreen/OptionsMenu");
        archipelagoMenu = Instantiate(originalMenu, originalMenu.transform.parent);

        archipelagoMenu.name = "ArchipelagoMenu";
        Destroy(archipelagoMenu.transform.GetChild(1).gameObject);
        Destroy(archipelagoMenu.transform.GetChild(2).gameObject);

        for (int i = 0; i < 8; i++)
        {
            Destroy(archipelagoMenu.transform.GetChild(0).GetChild(0).GetChild(i).gameObject);
        }

        // archipelagoMenu.transform.GetChild(0).GetChild(0).GetChild(8).GetComponent<Button>().onClick.AddListener(ToggleArchipelagoMenu);

        //create server address input field, port input field, slot name input field, connect button
        GameObject serverAddressInput = new GameObject("ServerAddressInput");
        serverAddressInput.transform.SetParent(archipelagoMenu.transform);
        serverAddressInput.AddComponent<InputField>();
    }

    private void ToggleArchipelagoMenu()
    {
        archipelagoMenu.SetActive(!archipelagoMenu.activeSelf);
    }
}
