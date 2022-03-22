using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraControl : MonoBehaviour
{

    public GameObject MainCamera;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        MainCamera.transform.position = new Vector3(
        Mathf.Clamp(transform.position.x, -15f, 25f),
        Mathf.Clamp(transform.position.y, -0.5f, 9),
        Mathf.Clamp(transform.position.z, -10f, 15));
    }
}
