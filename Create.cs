using UnityEngine;
using System.Collections.Generic;
using System.IO;
using System;
using System.Globalization;
using System.Threading;


[RequireComponent(typeof(MeshFilter))]
[RequireComponent(typeof(MeshRenderer))]


public class Create: MonoBehaviour
{
	// ------------ Инициализация переменных ------------

    // Объекты
    public GameObject MainCamera;
    public GameObject window;

    // Материалы
    public Material oldWallMaterial;
    public Material newWallMaterial;
    public Material classicWallMaterial;

    // Словарь
//    Dictionary<int, Material> dict = new Dictionary<int, Material>()
//    {
//        [1] = newWallMaterial,
//        [2] = oldWallMaterial,
//        [3] =
//    };


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
    string path1 = "/Users/bolevard/Auto_desig/auto_home_design/point.csv";
    string path2 = "/Users/bolevard/Auto_desig/auto_home_design/furniture.csv";
    string path3 = "/Users/bolevard/Auto_desig/auto_home_design/models.csv";

    //--------------------------------------------

	// Движение объекта
	void MoveRect(GameObject wall, float x, float y, float z)
    {
		Vector3 temp = new Vector3(x, y, z);
		wall.transform.position += temp;
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
    void CreateWall(float X1, float Y1, float X2, float Y2, string wallType, Material wallMat)
    {
		// Стена
		if (wallType == "wall")
		{
			GameObject wall1 = GameObject.CreatePrimitive(PrimitiveType.Cube);
			wall1.GetComponent<Renderer>().material = wallMat;
			MoveRect(wall1, GetCordsX(X1, X2), 0.25f, GetCordsY(Y1, Y2));
			ScaleRect(wall1, ScaleX(X1, Y1, X2, Y2), 2.5f, (float)0.1);
			RotateRect(wall1, 0, Angle(X1, Y1, X2, Y2), 0);
		}

		// Окно
		else if (wallType == "window")
		{
			GameObject wall1 = GameObject.CreatePrimitive(PrimitiveType.Cube);
            wall1.GetComponent<Renderer>().material = wallMat;

			MoveRect(wall1, GetCordsX(X1, X2), -0.5f, GetCordsY(Y1, Y2));
			ScaleRect(wall1, ScaleX(X1, Y1, X2, Y2), 1, (float)0.1);
			RotateRect(wall1, 0, Angle(X1, Y1, X2, Y2), 0);

			GameObject wnd1 = Instantiate(window, new Vector3(0,0,0), Quaternion.identity);

			MoveRect(wnd1, GetCordsX(X1, X2), 0.75f, GetCordsY(Y1, Y2));
			ScaleRect(wnd1, ScaleX(X1, Y1, X2, Y2), 3.4f, ScaleX(X1, Y1, X2, Y2)*1.3f);
			RotateRect(wnd1, 0, 90-Angle(X1, Y1, X2, Y2), 0);

			GameObject wnd2 = Instantiate(window, new Vector3(0,0,0), Quaternion.identity);

			MoveRect(wnd2, GetCordsX(X1, X2), 0.75f, GetCordsY(Y1, Y2));
			ScaleRect(wnd2, ScaleX(X1, Y1, X2, Y2), 3.4f, ScaleX(X1, Y1, X2, Y2)*1.3f);
			RotateRect(wnd2, 0, 90-Angle(X1, Y1, X2, Y2), 180);
		}
    }
    // (x, z)
    // Расстановка мебели
    void CreateFurniture(float X1, float Z1, string furnType, int model)
    {
        if (model == 3){
            if(furnType == "1"){
                GameObject Chair = Instantiate(woodenChair, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Chair, X1 * 10, -1f, Z1 * 10);
            }
            if(furnType == "2"){
                GameObject Table = Instantiate(woodenTable, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Table, X1 * 10-0.2f, -1f, Z1 * 10+0.1f);
            }
            if(furnType == "3"){
                GameObject Table = Instantiate(woodenNightStand, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Table, X1 * 10, -0.8f, Z1 * 10);
            }
            if(furnType == "4"){
                GameObject Bed = Instantiate(woodenBed, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Bed, X1 * 10, -0.6f, Z1 * 10);
                RotateRect(Bed, -90f, 0, 0);
            }

            if(furnType == "5"){
                GameObject Bed = Instantiate(woodenCloset, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Bed, X1 * 10, -0.9f, Z1 * 10);

            }
        }
        else if (model == 1){
            if(furnType == "1"){
                GameObject Chair = Instantiate(newChair, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Chair, X1 * 10, -1f, Z1 * 10+0.3f);
            }
            if(furnType == "2"){
                GameObject Table = Instantiate(newTable, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Table, X1 * 10-0.2f, -1f, Z1 * 10+0.1f);
            }
            if(furnType == "3"){
                GameObject Table = Instantiate(woodenNightStand, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Table, X1 * 10, -0.8f, Z1 * 10);
            }
            if(furnType == "4"){
                GameObject Bed = Instantiate(newBed, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Bed, X1 * 10, -0.5f, Z1 * 10);
                RotateRect(Bed, -90f, 0, 0);
            }
            if(furnType == "5"){
                GameObject Bed = Instantiate(newCloset, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Bed, X1 * 10, -0.9f, Z1 * 10);
                RotateRect(Bed, 0, 0, 0);
            }
        }
        else if (model == 2){
            if(furnType == "1"){
                GameObject Chair = Instantiate(oldChair, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Chair, X1 * 10, -1f, Z1 * 10);
            }
            if(furnType == "2"){
                GameObject Table = Instantiate(oldTable, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Table, X1 * 10-0.2f, 0.3f, Z1 * 10+0.1f);
            }
            if(furnType == "3"){
                GameObject Table = Instantiate(woodenNightStand, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Table, X1 * 10, -0.8f, Z1 * 10);
            }
            if(furnType == "4"){
                GameObject Bed = Instantiate(oldBed, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Bed, X1 * 10-0.65f, -0.7f, Z1 * 10);
                RotateRect(Bed, -90f, 0, 0);
            }
            if(furnType == "5"){
                GameObject Bed = Instantiate(oldCloset, new Vector3(0, 0, 0), Quaternion.identity);
                MoveRect(Bed, X1 * 10, -1f, Z1 * 10);
                RotateRect(Bed, -90, 180, 180);
            }
        }
    }

	// Главная функция
	void Start()
	{
		// Два списка с кординатами точек
		string[] list1 = File.ReadAllLines(path1);
		string[] list2 = File.ReadAllLines(path2);
        string[] list3 = File.ReadAllLines(path3);

        // Переменные с номерами моделей
        int model1 = int.Parse(list3[0].Split(',')[0], CultureInfo.InvariantCulture.NumberFormat);
        int model2 = int.Parse(list3[0].Split(',')[1], CultureInfo.InvariantCulture.NumberFormat);
        int model3 = int.Parse(list3[0].Split(',')[2], CultureInfo.InvariantCulture.NumberFormat);

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
			    CreateWall(X1 + 1.5f, Y1, X2 + 1.5f, Y2, wallType, newWallMaterial);
			    }
			else if (model2 == 1){
			    CreateWall(X1, Y1, X2, Y2, wallType, newWallMaterial);
			}
			else{
			    CreateWall(X1 - 1.5f, Y1, X2 - 1.5f, Y2, wallType, newWallMaterial);
			}

			if(model1 == 2){
			    CreateWall(X1 + 1.5f, Y1, X2 + 1.5f, Y2, wallType, oldWallMaterial);
			    }
			else if (model2 == 2){
			    CreateWall(X1, Y1, X2, Y2, wallType, oldWallMaterial);
			}
			else{
			    CreateWall(X1 - 1.5f, Y1, X2 - 1.5f, Y2, wallType, oldWallMaterial);
			}

			if(model1 == 3){
			    CreateWall(X1 + 1.5f, Y1, X2 + 1.5f, Y2, wallType, classicWallMaterial);
			    }
			else if (model2 == 3){
			    CreateWall(X1, Y1, X2, Y2, wallType, classicWallMaterial);
			}
			else{
			    CreateWall(X1 - 1.5f, Y1, X2 - 1.5f, Y2, wallType, classicWallMaterial);
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
	}
}
