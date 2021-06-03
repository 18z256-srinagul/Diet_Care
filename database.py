import mysql.connector as mc
import FoodFilter as foodpy
from datetime import datetime
'''
password is hidden for privacy purposes
'''
Password = '****************'
Cure=[]
nutr = list()
problem = list()
TotalEnergy = dict()
FoodValues={}
DeficiencyToFoodMap={
    "Water":"Water",
    "Protein":"Protein",
    "Fat":"TotalFat",
    "Fibre":"TotalFibre",
    "Carbohydrates":"Carbohydrates",
    "vitamin-b1": "VitB1",
    "vitamin-b2": "VitB2",
    "vitamin-b3": "VitB3",
    "vitamin-b5": "VitB5",
    "vitamin-b6": "VitB6",
    "vitamin-b7": "VitB7",
    "vitamin-b9": "VitB9",
    "calcium": "Calcium",
    "copper":"Copper",
    "iron":"Iron",
    "magnesium":"Magnesium",
    "potassium":"Potassium",
    "sodium":"Sodium",
    "zinc":"Zinc",
    "sugar":"TotalFreeSugars",
    "phosphorous":"Phosphorous"
}

Columns=["Water","Protein","TotalFat","TotalFibre","Carbohydrates","Energy","VitB1","VitB2","VitB3",
"VitB5","VitB6","VitB7","VitB9","Arsenic","Calcium","Cobalt","Copper","Iron","Leadd","Magnesium",
"Mercury","Phosphorous","Potassium","Sodium","Zinc","TotalStarch","Fructose","Glucose",
"Sucrose","TotalFreeSugars"]

Analysis=["Water","Protein","TotalFat","TotalFibre","Carbohydrates","Energy","VitB1","VitB6","Calcium","Copper","Iron"
    ,"TotalStarch","TotalFreeSugars"]


FoodMap = {
    "A":"Cereals and Millets",
    "B":"Grain Legumes",
    "C":"Green Leafy Vegetables",
    "D":"Other Vegetables",
    "E":"Fruits",
    "F":"Roots and Tubers",
    "G":"Condiments and Spices",
    "H":"Nuts and Oil seeds",
    "I":"Sugars",
    "J":"Mushrooms",
    "K":"Miscellaneous",
    "L":"Milk products",
    "M":"Egg products",
    "N":"Chicken",
    "O":"Animal Meats",
    "P":"Fishes",
    "Q":"Shell fishes",
    "R":"Marine Molluscs",
    "S":"Freshwater fish and shell fish",
    "T":"Soups,sauses and Gravies",
    "UB":"Baked Products",
    "US":"Snacks",
    "UC":"Chocolates and confectionaries",
    "UF":"Fast foods",
    "UD":"Beverages",
}
Units = {"Water": "g",
         "Protein":"g",
         "TotalFat":"g",
         "TotalFibre":"g",
         "Carbohydrates":"g",
         "Energy":"kJ",
         "VitB1":"mg",
         "VitB2":"mg",
         "VitB3":"g",
         "VitB5":"mg",
         "VitB6":"mg",
         "VitB7":"micro g",
         "VitB9":"micro g",
         "Arsenic":"micro g",
         "Calcium":"mg",
         "Cobalt":"mg",
         "Copper":"mg",
         "Iron":"mg",
         "Leadd":"mg",
         "Magnesium":"mg",
         "Mercury":"micro g",
         "Phosphorous":"mg",
         "Potassium":"mg",
         "Sodium":"mg",
         "Zinc":"mg",
         "TotalStarch":"g",
         "Fructose":"g",
         "Glucose":"g",
         "Sucrose":"g",
         "TotalFreeSugars":"g"
    }


def CreateDatabase(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS Dietcare")

def InsertUser(username,password,email,age):
    conn = mc.connect(user="root", host="localhost",database="dietcare", passwd=Password)
    cursor = conn.cursor()
    query = "INSERT INTO Login ( Username,Password,EmailID,Age ) VALUES (%s,%s,%s,%s);"
    data = (username,password,email,age)
    cursor.execute(query,data)
    conn.commit()
    cursor.close()

def isUser(username,password):
    conn = mc.connect(user="root", host="localhost", database="dietcare", passwd=Password)
    cursor = conn.cursor()
    query = "SELECT * FROM Login WHERE Username = %s and Password = %s"
    data = (username, password)
    cursor.execute(query, data)
    fetch = cursor.fetchone()
    if fetch == None or len(fetch) == 0:
        cursor.close()
        return 0
    cursor.close()
    return 1
    # conn.commit()

def SelectedDeficiencyRes():
    global problem
    return problem

def SelectedFoodResuts():
    global nutr,TotalEnergy
    return nutr,TotalEnergy


def profileFetch(UserLogin):
    conn = mc.connect(user="root", host="localhost", database="dietcare", passwd=Password)
    cursor = conn.cursor()
    user = UserLogin
    if len(user) != 0 :
        query = "SELECT Username, Password, EmailID, Age FROM Login WHERE Username = '"+user[0]+"' and Password = '"+user[1]+"';"
        cursor.execute(query)
        fetch = cursor.fetchall()
        conn.close()
        if len(list(fetch)) != 0:
            return list(fetch[0])
        else:
            return []
    else:
        conn.close()
        return []

def UpdateValues(username,password,email,age,UserLoginuser,UserLoginpass):
    conn = mc.connect(user="root", host="localhost", database="dietcare", passwd=Password)
    cursor = conn.cursor()
    userid2=""
    if UserLoginuser != "" and UserLoginpass!= "":
        query="SELECT UserID FROM Login WHERE Username = '"+UserLoginuser+"' and Password = '"+UserLoginpass+"';"
        cursor.execute(query)
        userid = cursor.fetchone()
        userid = list(userid)[0]
        userid2 = userid

    if username != "" and userid2 != "" :
        query = "UPDATE Login SET Username = '"+username+"' WHERE UserID = "+str(userid2)+";"
        cursor.execute(query)
        conn.commit()

    if password != "" and userid2 != "":
        query = "UPDATE Login SET Password = '"+password+"' WHERE UserID = "+str(userid2)+";"
        cursor.execute(query)
        conn.commit()

    if email != "" and userid2 != "":
        query = "UPDATE Login SET EmailID = '"+email+"' WHERE UserID = "+str(userid2)+";"
        cursor.execute(query)
        conn.commit()

    if age != "0" and userid2 != "":
        query = "UPDATE Login SET Age = '"+age+"' WHERE UserID = "+str(userid2)+";"
        cursor.execute(query)
        conn.commit()

    conn.close()

def UserFoodStats(username):
    conn = mc.connect(user="root", host="localhost", database="dietcare", passwd=Password)
    cursor = conn.cursor()
    foods=[]
    global Analysis
    cursor.execute("SELECT UserID from Login WHERE Username = '" + username + "';")
    fetch = cursor.fetchone()
    fetch = list(fetch)[0]
    UserID = fetch
    query = "SELECT FoodName FROM UserFood WHERE UserID = "+str(UserID)
    cursor.execute(query)
    fetch = cursor.fetchall()
    for i in fetch:
        foods.append(list(i)[0])
    ntr = dict()
    for nutrients in Analysis:
        max1 = 0
        maxFood = ""
        for food in foods:
            query = "SELECT FoodName," + nutrients + " FROM FoodDetails WHERE FoodName = '" + food + "';"
            cursor.execute(query)
            fetch = cursor.fetchall()
            for i in fetch:
                if list(i)[1] > max1:
                    max1 = list(i)[1]
                    maxFood = list(i)[0]
        ntr[nutrients] = maxFood
    conn.close()
    return ntr

def FoodActivity(username):
    conn = mc.connect(user="root", host="localhost", database="dietcare", passwd=Password)
    cursor = conn.cursor()
    cursor.execute("SELECT UserID from Login WHERE Username = '" + username + "';")
    fetch = cursor.fetchone()
    fetch = list(fetch)[0]
    UserID = fetch

    query = "SELECT Date, Time, FoodName FROM UserFood WHERE UserID = '"+str(UserID)+"';"
    cursor.execute(query)
    fetch = cursor.fetchall()
    data=[]
    for i in fetch:
        i = list(i)
        temp = dict()
        time1 = i[0]+" , "+i[1]
        food1 = i[2]
        temp[time1] = food1
        data.append(temp)
    conn.close()
    return data


def UserStatsInsert(foods,username):
    conn = mc.connect(user="root", host="localhost", database="dietcare", passwd=Password)
    cursor = conn.cursor()
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M:%S")
    cursor.execute("SELECT UserID from Login WHERE Username = '"+username+"';")
    fetch = cursor.fetchone()
    fetch = list(fetch)[0]
    UserID = fetch

    for food in foods:
        query = "INSERT INTO UserFood VALUES (%s,%s,%s,%s);"
        data = (UserID,food,date,time)
        cursor.execute(query,data)
        conn.commit()
    conn.close()


def SelectedFood(foods):
    conn = mc.connect(user="root", host="localhost", database="dietcare", passwd=Password)
    cursor = conn.cursor()
    global nutr,Columns,TotalEnergy

    for food in foods:
        query = "SELECT * FROM FoodDetails WHERE FoodName = '" + food + "';"
        cursor.execute(query)
        fetch = cursor.fetchall()
        temp=dict()
        temp2 = dict()
        for var in range(len(Columns)):
            temp2[Columns[var]+" ("+Units[Columns[var]]+") "] = list(fetch[0])[var+2]
        temp2 = dict(sorted(temp2.items(), key=lambda item: item[1], reverse=True))
        temp[food] = temp2
        nutr.append(temp)
    conn.close()

    for i in nutr:
        for j, k in i.items():
            for l in k.keys():
                TotalEnergy[l] = 0

    for i in nutr:
        for j, k in i.items():
            for l in k.keys():
                TotalEnergy[l] = round(TotalEnergy[l] + k[l], 3)

    return nutr

def FetchFoods():
    conn = mc.connect(user="root", host="localhost",database="dietcare", passwd=Password)
    cursor = conn.cursor()
    for keys in FoodMap.keys():
        query = "SELECT FoodName FROM FoodDetails WHERE FoodID LIKE '"+keys+"%';"
        cursor.execute(query)
        fetch = cursor.fetchall()
        l=[]
        for val in fetch:
            l.append(val[0])
        FoodValues[FoodMap[keys]] = l
    cursor.close()
    return FoodValues

def InsertFood(value,cursor,db):
    query = "INSERT INTO FoodDetails VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    data_val = (value[0],value[1],float(value[2]),float(value[3]),float(value[4]),float(value[5]),float(value[6]),float(value[7]),float(value[8]),float(value[9]),float(value[10]),float(value[11]),float(value[12]),float(value[13]),float(value[14]),float(value[15]),float(value[16]),float(value[17]),float(value[18]),float(value[19]),float(value[20]),float(value[21]),float(value[22]),float(value[23]),float(value[24]),float(value[25]),float(value[26]),float(value[27]),float(value[28]),float(value[29]),float(value[30]),float(value[31]))
    print(data_val)
    print("===PLEASE DISABLE THE COMMENTS BELOW FOR INSERTING (CAUTION: THIS CAUSES CHANGES IN DATABASE) ===")
    # cursor.execute(query,data_val)
    # db.commit()

def InsertDisease(diseases,cursor,db):
    query = "INSERT INTO Disease VALUES (%s,%s);"
    data = (diseases[0],diseases[1])
    print(data)
    print("===PLEASE DISABLE THE COMMENTS BELOW FOR INSERTING (CAUTION: THIS CAUSES CHANGES IN DATABASE) ===")
    # cursor.execute(query,data)
    # db.commit()

def InsertDeficiency(data,cursor,db):
    query = "INSERT INTO Deficiency VALUES (%s,%s,%s);"
    values = (data[0], data[1], data[2])
    print(values)
    print("===PLEASE DISABLE THE COMMENTS BELOW FOR INSERTING (CAUTION: THIS CAUSES CHANGES IN DATABASE) ===")
    # cursor.execute(query,data)
    # db.commit()

def FetchDeficiency1():
    conn = mc.connect(user="root", host="localhost", database="dietcare", passwd=Password)
    cursor = conn.cursor()
    query = "SELECT DISTINCT OrganAffected FROM Deficiency"
    cursor.execute(query)
    fetch = cursor.fetchall()
    OrganAffected=dict()
    for organ in fetch:
        org = list(organ)[0]
        query1 = "SELECT Problem FROM deficiency WHERE OrganAffected = '"+str(org)+"';"
        cursor.execute(query1)
        fetch1 = cursor.fetchall()
        temp = []
        for probs in fetch1:
            prob = list(probs)[0]
            temp.append(prob)
        OrganAffected[org] = temp
    conn.close()
    return OrganAffected


def FetchTopNutFood(nutrition):
    conn = mc.connect(user="root", host="localhost", database="dietcare", passwd=Password)
    cursor = conn.cursor()
    query = "SELECT FoodName,"+str(nutrition)+" FROM FoodDetails ORDER BY "+str(nutrition)+" DESC LIMIT 0,10"
    cursor.execute(query)
    fetch = cursor.fetchall()
    foo=[]
    for food in fetch:
        f = list(food)[0] + "  " + "       ( "+str(food[1])+"   "+Units[str(nutrition)]+" ) "
        foo.append(f)
    conn.close()
    return foo

def SelectedDeficiency(deficiency):
    conn = mc.connect(user="root", host="localhost", database="dietcare", passwd=Password)
    cursor = conn.cursor()
    global problem,Cure
    for probs in deficiency:
        query = "SELECT Deficiency FROM deficiency WHERE Problem = '" + probs + "';"
        cursor.execute(query)
        fetch = cursor.fetchall()
        for var in fetch:
            Cure.append(list(var)[0])

        temp = dict()
        temp2 = dict()
        temp2[DeficiencyToFoodMap[str(list(fetch[0])[0])]] = FetchTopNutFood(DeficiencyToFoodMap[str(list(fetch[0])[0])])
        temp[probs.title()] = temp2
        problem.append(temp)
    conn.close()

def CreateTables(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Login ( "
                   "UserID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,"
                   "Username VARCHAR(25),"
                   "Password VARCHAR(30),"
                   "EmailID VARCHAR (30),"
                   "Age TINYINT );")
    # cursor.execute("CREATE TABLE IF NOT EXISTS Consultation ( "
    #                "ProfessionalID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,"
    #                "ProfessionalUsername VARCHAR(25),"
    #                "ProfessionalPassword VARCHAR(30),"
    #                "ProfessionalQualification VARCHAR (30),"
    #                "ProfessionalAge TINYINT,"
    #                "NoofSessionAttended INT,"
    #                "ConsultedUser VARCHAR(25) );")
    cursor.execute("CREATE TABLE IF NOT EXISTS FoodDetails ( "
                   "FoodID VARCHAR(10) PRIMARY KEY,"
                   "FoodName VARCHAR(150),"
                   "Water FLOAT,"
                   "Protein FLOAT,"
                   "TotalFat FLOAT,"
                   "TotalFibre FLOAT,"
                   "Carbohydrates FLOAT,"
                   "Energy FLOAT,"
                   "VitB1 FLOAT,"
                   "VitB2 FLOAT,"
                   "VitB3 FLOAT,"
                   "VitB5 FLOAT,"
                   "VitB6 FLOAT,"
                   "VitB7 FLOAT,"
                   "VitB9 FLOAT,"
                   "Arsenic FLOAT,"
                   "Calcium FLOAT,"
                   "Cobalt FLOAT,"
                   "Copper FLOAT,"
                   "Iron FLOAT,"
                   "Leadd FLOAT,"
                   "Magnesium FLOAT,"
                   "Mercury FLOAT,"
                   "Phosphorous FLOAT,"
                   "Potassium FLOAT,"
                   "Sodium FLOAT,"
                   "Zinc FLOAT,"
                   "TotalStarch FLOAT,"
                   "Fructose FLOAT,"
                   "Glucose FLOAT,"
                   "Sucrose FLOAT,"
                   "TotalFreeSugars FLOAT );")

    cursor.execute("CREATE TABLE IF NOT EXISTS UserFood ( "
                   "UserID INT ,"
                   "FoodName VARCHAR(150),"
                   "Date VARCHAR(12),"
                   "Time VARCHAR(10) );")

    # cursor.execute("CREATE TABLE IF NOT EXISTS Disease("
    #                "Disease VARCHAR(100),"
    #                "Medicine VARCHAR(100) );")

    cursor.execute("CREATE TABLE IF NOT EXISTS Deficiency("
                   "Problem VARCHAR(100),"
                   "OrganAffected VARCHAR(20),"
                   "Deficiency VARCHAR(30) );")


conn = mc.connect( user="root", host="localhost",passwd=Password)
cursor = conn.cursor()

'''data = foodpy.csv_Fooddata
disease = foodpy.diseases

CreateDatabase(cursor)'''

cursor.execute("use dietcare")
'''
CreateTables(cursor)

for food in data:
    InsertFood(food,cursor,conn)

data_val=[]

for key in disease.keys():
    for value in disease[key]:
        temp=[]
        temp.append(key)
        temp.append(value)
        data_val.append(tuple(temp))

for value in data_val:
    InsertDisease(value,cursor,conn)

data_val=[]
deficit = foodpy.deficit


for value in deficit:
    InsertDeficiency(value,cursor,conn)
'''
foodfun = FetchFoods()