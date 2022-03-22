using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RayCastHit : MonoBehaviour
{
    public Ray ray;
    public RaycastHit hit;
    public LayerMask mask;
    public float movefloat = 0.01f;

    // RayCasting
    GameObject RayCastFunc(){
        ray = GetComponent<Camera>().ScreenPointToRay(Input.mousePosition);
        if (Physics.Raycast(ray, out hit, 100f, mask)) {
            GameObject obj = hit.transform.parent.gameObject;
            return obj;
        }
        else {
            GameObject obj = hit.transform.parent.gameObject;
            obj.name = "None";
            return obj;
        }
    }

    // Поворот мебели
    void Rotate(GameObject obj){
        Vector3 cenLocal = obj.GetComponent<BoxCollider>().center;
        Vector3 cenGlobal = obj.transform.TransformPoint(cenLocal);
        obj.transform.RotateAround(cenGlobal, Vector3.up, 45f);
    }

    // Передвижение мебели
    void Move(GameObject obj, float x, float z){
        obj.transform.position += new Vector3(x, 0, z);
    }

    void Update(){
        if(Input.GetMouseButtonDown(0) && RayCastFunc().name != "None"){
            GameObject obj = RayCastFunc();
            Rotate(obj);
        }
        if (Input.GetKey("up") && RayCastFunc().name != "None"){
            GameObject obj = RayCastFunc();
            Move(obj, 0, -movefloat);
        }
        if (Input.GetKey("down") && RayCastFunc().name != "None"){
            GameObject obj = RayCastFunc();
            Move(obj, 0, movefloat);
        }
        if (Input.GetKey("left") && RayCastFunc().name != "None"){
            GameObject obj = RayCastFunc();
            Move(obj, movefloat, 0);
        }
        if (Input.GetKey("right") && RayCastFunc().name != "None"){
            GameObject obj = RayCastFunc();
            Move(obj, -movefloat, 0);
        }
    }
}
