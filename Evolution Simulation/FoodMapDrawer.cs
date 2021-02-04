using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FoodMapDrawer : MonoBehaviour
{
    public FoodManager[] foodManagers;
    public Color backgroundColor;
    public Color foodColor;

    // Start is called before the first frame update
    void Start()
    {
        int xSize = 35;
        int ySize = 15;
        int resolution = 10;

        Texture2D texture = new Texture2D(xSize* resolution, ySize* resolution);
        GetComponent<Renderer>().material.mainTexture = texture;

        float maxFood = 0;
        for (int y = 0; y < texture.height; y++)
        {
            for (int x = 0; x < texture.width; x++)
            {
                foreach (FoodManager foodManager in foodManagers)
                {
                    float foodAtPoint = foodManager.GetFoodValue(new Vector2(
                        x - xSize / 2f * resolution, y - ySize / 2f * resolution) / resolution);
                    maxFood = Mathf.Max(foodAtPoint, maxFood);
                }
            }
        }

        for (int y = 0; y < texture.height; y++)
        {
            for (int x = 0; x < texture.width; x++)
            {
                float foodIntensity = 0;
                foreach (FoodManager foodManager in foodManagers)
                {
                    foodIntensity += foodManager.GetFoodValue(new Vector2(x-xSize/2f* resolution, y-ySize/2f* resolution) /resolution);
                }
                float displayValuePercent = foodIntensity / maxFood;
                Color color = foodColor * displayValuePercent + backgroundColor * (1-displayValuePercent);
                texture.SetPixel(x, y, color);
            }
        }
        texture.Apply();
    }
}
