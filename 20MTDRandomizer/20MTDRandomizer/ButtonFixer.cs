using UnityEngine;
using TMPro;

public class ButtonFixer : MonoBehaviour
{
    void Start()
    {
        TextMeshProUGUI tmpComponent = GetComponentInChildren<TextMeshProUGUI>();
        if (tmpComponent != null)
        {
            tmpComponent.text = "Archipelago";
        }
        Debug.Log("hello");
    }
}