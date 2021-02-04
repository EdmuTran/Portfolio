using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Grapher : MonoBehaviour
{
    public GameObject bar;
    public GameObject graph;
    public Text maxValDisplay;

    public List<GameObject> bars;

    // Start is called before the first frame update
    void Start()
    {
        bars = new List<GameObject>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    float maxVal = 0;

    public void AddDataPoint(float value)
    {
        if (maxVal == 0)
        {
            maxVal = value;
        }

        GameObject dataPoint = Instantiate(bar);
        dataPoint.transform.SetParent(graph.transform);
        bars.Add(dataPoint);


        float oldMax = maxVal;
        maxVal = Mathf.Max(maxVal,value);

        dataPoint.GetComponent<RectTransform>().SetSizeWithCurrentAnchors(RectTransform.Axis.Vertical, value / oldMax * 100);
        
        float scaleChange = oldMax / maxVal;

        if (scaleChange < 1)
        {
            foreach (GameObject b in bars)
            {
                RectTransform rt = b.GetComponent<RectTransform>();
                rt.SetSizeWithCurrentAnchors(RectTransform.Axis.Vertical, rt.rect.height * scaleChange);
            }
        }

        maxValDisplay.text = maxVal.ToString();
    }
}
