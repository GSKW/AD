using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class RayCastUI : MonoBehaviour
{
    public Vector3[] dots = new Vector3[500];
    public GameObject[] lines = new GameObject[500];
    int i = 0;
    public Material mt;

    void DrawLine(Vector3 start, Vector3 end, Color color, float duration = 0.2f)
         {
             GameObject myLine = new GameObject();
             myLine.transform.position = start;
             myLine.AddComponent<LineRenderer>();
             LineRenderer lr = myLine.GetComponent<LineRenderer>();
             lr.material = mt;
             lr.SetColors(color, color);
             lr.SetWidth(0.6f, 0.6f);
             lr.SetPosition(0, start);
             lr.SetPosition(1, end);
             GameObject.Destroy(myLine, duration);
         }

    void Update()
    {
        if (Input.GetButtonDown("Fire1"))
        {
            Vector3 mousePos = Input.mousePosition;
            {
                mousePos.x = mousePos.x/50;
                mousePos.y = mousePos.y/50;
                dots[i] = mousePos;
                i++;
            }
            for(int j = 0; j < i; j++){
                DrawLine(dots[j], dots[0], Color.white, 1000f);
                if (j >= 2){
                    DrawLine(dots[j-1], dots[j], Color.white, 1000f);
                    DrawLine(dots[j], dots[0], Color.white, 1000f);
                    Debug.Log("+");
                }
            }
        }
    }
}
