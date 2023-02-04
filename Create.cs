using UnityEngine;
using System.Collections.Generic;
using System.IO;
using System;
using System.Globalization;
using System.Threading;
using UnityEditor;
using UnityEditor.Formats.Fbx.Exporter;
using System.Collections;


[RequireComponent(typeof(MeshFilter))]
[RequireComponent(typeof(MeshRenderer))]


public class Create: MonoBehaviour
{
	// ------------ Инициализация переменных ------------

    // Объекты
    public GameObject MainCamera;
    public GameObject s_window;
    public GameObject l_window;
    public GameObject window;

    public GameObject newParent;
    public GameObject oldParent;
    public GameObject clsParent;


    // Материалы
    public Material oldWallMaterial;
    public Material newWallMaterial;
    public Material classicWallMaterial;


    public string[] list4;
    public string[] list5;

    // Мебель
    public GameObject woodenNightStand;

    public GameObject newBed;
    public GameObject newChair;
    public GameObject newTable;
    public GameObject newCloset;

    public GameObject woodenBed;
    public GameObject woodenChair;
    public GameObject woodenTable;
    public GameObject woodenCloset;


    public GameObject oldBed;
    public GameObject oldChair;
    public GameObject oldTable;
    public GameObject oldCloset;

    // Путь к файлам
    string path1 = "auto_home_design/point.csv";
    string path2 = "auto_home_design/furniture.csv";
    string path3 = "auto_home_design/models.csv";
    string path4 = "auto_home_design/save_models.csv";
    string path5 = "auto_home_design/features.csv";

    public float wall_scale = 4f; // max 4 / min 2/ default 4
    public float win_scale = 4f; // max 8 / min 1/ default 4
    public int win_type = 1;

    public GameObject[,] dict_;





	// Движение объекта
	void MoveRect(GameObject wall, float x, float y, float z)
    {
		Vector3 temp = new Vector3(x, y, z);
		wall.transform.position += temp;
	}

	public void ExportGameObjects(GameObject objects, string name)
    {
        string filePathNew = Path.Combine("auto_home_design/", name+".fbx");
        ModelExporter.ExportObject(filePathNew, objects);
//        Console.WriteLine("auto_home_design/", name+".fbx");
    }

	
	// Масштабирование объекта
	void ScaleRect(GameObject wall, float x, float y, float z)
	{
		Vector3 temp = new Vector3(x - 1, y - 1, z - 1);
		wall.transform.localScale += temp;
	}

	// Вращение объекта
	void RotateRect(GameObject wall, float x, float y, float z)
	{
		Vector3 temp = new Vector3(x - 1, y - 1, z - 1);
		wall.transform.Rotate(x, y, z);
	}

	// Функция для расчёта угла поворота стены
	float Angle(float X1, float Y1, float X2, float Y2)
	{
		float ang = (float)(System.Math.Acos((X2 - X1) / System.Math.Sqrt(System.Math.Pow((X2 - X1), 2)
		 + System.Math.Pow((Y2 - Y1), 2)))) * 180 / (float)3.14;
		if (Y1 < Y2)
        {
			ang = 180 - ang;
        }
		return ang;
	}

    // Функции изменения X и Y
	float GetCordsX(float X1, float X2)
    {
		float X = (X1 + X2) / 2 * 10;
		return X;
    }
	float GetCordsY(float Y1, float Y2)
	{
		float Y = (Y1 + Y2) / 2 * 10;
		return Y;
	}
	float ScaleX(float X1, float Y1, float X2, float Y2)
    {
		double LN = Math.Sqrt(Convert.ToDouble((X2 - X1) * (X2 - X1) + (Y2 - Y1) * (Y2 - Y1))) * 10;
		return (float)LN;
    }
    //---------------------

    // Построение стены
    void CreateWall(float X1, float Y1, float X2, float Y2, string wallType, Material wallMat, int model)
    {

        Debug.Log(win_type);
        Debug.Log(win_scale);
        Debug.Log(wall_scale);
		float coef = 0.45f;

		float add_wall_scale = (float) ((wall_scale - (coef * win_scale)) / 2);
		float add_wall_down_y_pos = (float) (add_wall_scale / 2);
		float add_wall_up_y_pos = (float) (add_wall_scale * 1.5 + (coef * win_scale));

		float window_pos_y = (float) ((coef * win_scale) / 2 + add_wall_down_y_pos * 2);

		// Стена
		if (wallType == "wall")
		{
			GameObject wall1 = GameObject.CreatePrimitive(PrimitiveType.Cube);
			wall1.GetComponent<Renderer>().material = wallMat;
			MoveRect(wall1, GetCordsX(X1, X2), (float) wall_scale/2, GetCordsY(Y1, Y2));
			ScaleRect(wall1, ScaleX(X1, Y1, X2, Y2), wall_scale, (float)0.1); //
			RotateRect(wall1, 0, Angle(X1, Y1, X2, Y2), 0);
			if (model == 1){
			    wall1.transform.parent = newParent.gameObject.transform;
			}
			else if (model == 2){
			    wall1.transform.parent = oldParent.gameObject.transform;
			}
			else {
			    wall1.transform.parent = clsParent.gameObject.transform;
			}
		}

		// Окно
		else if (wallType == "window")
		{
			GameObject wall1 = GameObject.CreatePrimitive(PrimitiveType.Cube);
            wall1.GetComponent<Renderer>().material = wallMat;

			MoveRect(wall1, GetCordsX(X1, X2), add_wall_down_y_pos, GetCordsY(Y1, Y2)); // -0.5
			ScaleRect(wall1, ScaleX(X1, Y1, X2, Y2),add_wall_scale, (float)0.1);
			RotateRect(wall1, 0, Angle(X1, Y1, X2, Y2), 0);

			GameObject wall2 = GameObject.CreatePrimitive(PrimitiveType.Cube);
            wall2.GetComponent<Renderer>().material = wallMat;

			MoveRect(wall2, GetCordsX(X1, X2), add_wall_up_y_pos, GetCordsY(Y1, Y2)); // -0.5
			ScaleRect(wall2, ScaleX(X1, Y1, X2, Y2), add_wall_scale, (float)0.1);
			RotateRect(wall2, 0, Angle(X1, Y1, X2, Y2), 0);

			GameObject wnd1 = Instantiate(window, new Vector3(0,0,0), Quaternion.identity);

			MoveRect(wnd1, GetCordsX(X1, X2), window_pos_y, GetCordsY(Y1, Y2));
			ScaleRect(wnd1, ScaleX(X1, Y1, X2, Y2), win_scale, ScaleX(X1, Y1, X2, Y2)*1.3f);
			RotateRect(wnd1, 0, 90-Angle(X1, Y1, X2, Y2), 0);

			GameObject wnd2 = Instantiate(window, new Vector3(0,0,0), Quaternion.identity);

			MoveRect(wnd2, GetCordsX(X1, X2), window_pos_y, GetCordsY(Y1, Y2));
			ScaleRect(wnd2, ScaleX(X1, Y1, X2, Y2), win_scale, ScaleX(X1, Y1, X2, Y2)*1.3f);
			RotateRect(wnd2, 0, 90-Angle(X1, Y1, X2, Y2), 180);

			if (model == 1){
			    wall1.transform.parent = newParent.gameObject.transform;
			    wall2.transform.parent = newParent.gameObject.transform;
			    wnd1.transform.parent = newParent.gameObject.transform;
			    wnd2.transform.parent = newParent.gameObject.transform;
			}
			else if (model == 2){
			    wall1.transform.parent = oldParent.gameObject.transform;
			    wall2.transform.parent = oldParent.gameObject.transform;
			    wnd1.transform.parent = oldParent.gameObject.transform;
			    wnd2.transform.parent = oldParent.gameObject.transform;
			}
			else {
			    wall1.transform.parent = clsParent.gameObject.transform;
			    wall2.transform.parent = clsParent.gameObject.transform;
			    wnd1.transform.parent = clsParent.gameObject.transform;
			    wnd2.transform.parent = clsParent.gameObject.transform;
			}
		}
    }
    // (x, z)
    // Расстановка мебели
    void CreateFurniture(float X1, float Z1, string furnType, int model)
    {
        GameObject Chair = Instantiate(dict_[model-1, Int16.Parse(furnType)-1], new Vector3(0, 0, 0), Quaternion.identity);
        MoveRect(Chair, X1 * 10, 0, Z1 * 10);
        Chair.transform.parent = clsParent.gameObject.transform;
    }

	// Главная функция
	void Start()
	{

        dict_ = new GameObject[3,5];

        dict_[0, 0] = newChair;
        dict_[0, 1] = newTable;
        dict_[0, 2] = woodenNightStand;
        dict_[0, 3] = newBed;
        dict_[0, 4] = newCloset;

        dict_[1, 0] = oldChair;
        dict_[1, 1] = oldTable;
        dict_[1, 2] = woodenNightStand;
        dict_[1, 3] = oldBed;
        dict_[1, 4] = oldCloset;

        dict_[2, 0] = woodenChair;
        dict_[2, 1] = woodenTable;
        dict_[2, 2] = woodenNightStand;
        dict_[2, 3] = woodenBed;
        dict_[2, 4] = woodenCloset;

		newParent = new GameObject("New");
		oldParent = new GameObject("Old");
		clsParent = new GameObject("Classic");

		// Два списка с кординатами точек
		string[] list1 = File.ReadAllLines(path1);
		string[] list2 = File.ReadAllLines(path2);
        string[] list3 = File.ReadAllLines(path3);

        list4 = File.ReadAllLines(path4);
        list5 = File.ReadAllLines(path5);


        // Переменные с номерами моделей
        int model1 = int.Parse(list3[0].Split(',')[0], CultureInfo.InvariantCulture.NumberFormat);
        int model2 = int.Parse(list3[0].Split(',')[1], CultureInfo.InvariantCulture.NumberFormat);
        int model3 = int.Parse(list3[0].Split(',')[2], CultureInfo.InvariantCulture.NumberFormat);

        wall_scale = float.Parse(list5[0].Split(',')[0], CultureInfo.InvariantCulture.NumberFormat);
        win_scale = float.Parse(list5[0].Split(',')[1], CultureInfo.InvariantCulture.NumberFormat) * 4;
        win_type = int.Parse(list5[0].Split(',')[2], CultureInfo.InvariantCulture.NumberFormat);



        if (list4.Length > 0){
            list4 = list4[0].Split(',');
        }

        if (win_type == 1) {
            window = l_window;
        }
        else {
            window = s_window;
        }

		Thread.CurrentThread.CurrentCulture = CultureInfo.InvariantCulture;

        // Главный цикл для построения стен
		for (int i = 0; i < list1.Length; i++)
		{
			// Переменные
			float X1 = float.Parse(list1[i].Split(',')[0], CultureInfo.InvariantCulture.NumberFormat);
			float Y1 = float.Parse(list1[i].Split(',')[1], CultureInfo.InvariantCulture.NumberFormat);
			float X2 = float.Parse(list1[(i + 1) %
			list1.Length].Split(',')[0], CultureInfo.InvariantCulture.NumberFormat);
			float Y2 = float.Parse(list1[(i + 1) %
			list1.Length].Split(',')[1], CultureInfo.InvariantCulture.NumberFormat);
			string wallType = list1[i].Split(',')[2];

            // Построение
			if(model1 == 1){
			    CreateWall(X1 + 1.5f, Y1, X2 + 1.5f, Y2, wallType, newWallMaterial, 1);
			    }
			else if (model2 == 1){
			    CreateWall(X1, Y1, X2, Y2, wallType, newWallMaterial, 1);
			}
			else{
			    CreateWall(X1 - 1.5f, Y1, X2 - 1.5f, Y2, wallType, newWallMaterial, 1);
			}

			if(model1 == 2){
			    CreateWall(X1 + 1.5f, Y1, X2 + 1.5f, Y2, wallType, oldWallMaterial, 2);
			    }
			else if (model2 == 2){
			    CreateWall(X1, Y1, X2, Y2, wallType, oldWallMaterial, 2);
			}
			else{
			    CreateWall(X1 - 1.5f, Y1, X2 - 1.5f, Y2, wallType, oldWallMaterial, 2);
			}

			if(model1 == 3){
			    CreateWall(X1 + 1.5f, Y1, X2 + 1.5f, Y2, wallType, classicWallMaterial, 3);
			    }
			else if (model2 == 3){
			    CreateWall(X1, Y1, X2, Y2, wallType, classicWallMaterial, 3);
			}
			else{
			    CreateWall(X1 - 1.5f, Y1, X2 - 1.5f, Y2, wallType, classicWallMaterial, 3);
			}
		}

        // Главный цикл для построения мебели
		for (int i = 0; i < list2.Length; i++)
		{
			// Переменные
			float X1 = float.Parse(list2[i].Split(',')[0], CultureInfo.InvariantCulture.NumberFormat);
			float Y1 = float.Parse(list2[i].Split(',')[1], CultureInfo.InvariantCulture.NumberFormat);
            string furnType = list2[i].Split(',')[2];

			// Построение
			CreateFurniture(X1 + 1.5f, Y1, furnType, model1);
			CreateFurniture(X1, Y1, furnType, model2);
			CreateFurniture(X1 - 1.5f, Y1, furnType, model3);
		}

		for (int i = 0; i < list4.Length; i++){
            if (list4[i] == "tick_new"){
                ExportGameObjects(newParent, "new");
            }
            else if (list4[i] == "tick_cls"){
                ExportGameObjects(clsParent, "cls");
            }
            else if (list4[i] == "tick_old"){
                ExportGameObjects(oldParent, "old");
            }
        }

	}
}
