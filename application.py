from flask import Flask, render_template, redirect, url_for,request
import database as db

UserLogin=[]
Defresults=[]
Organ=dict()


app = Flask(__name__)
@app.route("/")
def home():
    return render_template("main_home.html")

@app.route("/about")
def about():
    return render_template("About.html")

@app.route("/login",methods=["GET","POST"])
def login():
    global UserLogin
    if len(UserLogin) != 0:
        return redirect(url_for("home2"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if db.isUser(username,password) == 1:
            UserLogin.append(username)
            UserLogin.append(password)
            return redirect(url_for("home2"))
        else:
            return redirect(url_for("loginfail"))
    return render_template("login.html")

@app.route("/loginfail")
def loginfail():
    return render_template("loginfail.html")

@app.route("/help")
def help():
    return render_template("Help.html")

@app.route("/home")
def home2():
    return render_template("home.html")

@app.route("/logout")
def logout():
    global UserLogin
    UserLogin.clear()
    return render_template("main_home.html")

@app.route("/profile",methods=["GET","POST"])
def profile():
    global UserLogin
    resultPro = db.profileFetch(UserLogin)
    username = ""
    password = ""
    email=""
    age=0
    if len(resultPro) == 0:
        username = ""
        password = ""
        email = ""
        age = 0
    else:
        username = resultPro[0]
        password = resultPro[1]
        email = resultPro[2]
        age = resultPro[3]

    if request.method == "POST":
        username1 = request.form.get("Username")
        password1 = request.form.get("Password")
        email1 = request.form.get("Email")
        age1 = request.form.get("Age")
        try:
            db.UpdateValues(username1,password1,email1,age1,UserLogin[0],UserLogin[1])
        except:
            pass

    return render_template("profile.html",username=username,password=password,email=email,age=age)

@app.route("/resultsDiet",methods=["POST","GET"])
def resultsDiet():
    global SelFoodRes
    if request.method == "POST":
        SelFoodRes.clear()
        return redirect("/home")
    SelFoodRes,TotalFood = db.SelectedFoodResuts()
    return render_template("resultsDiet.html",food=SelFoodRes,totalFood = TotalFood)

@app.route("/statistics")
def statistics():
    global UserLogin
    UserStats = dict()
    UserStats = db.UserFoodStats(UserLogin[0])
    UserTable = db.FoodActivity(UserLogin[0])
    return render_template("statistics.html",foodstat = UserStats,table=UserTable)

@app.route("/fooddetails",methods=["GET","POST"])
def fooddetails():
    if request.form.get('legumes'):
        global UserLogin,UserStats
        db.SelectedFood(request.form.getlist('legumes'))
        db.UserStatsInsert(request.form.getlist('legumes'), UserLogin[0])
        return redirect(url_for("resultsDiet"))

    cereals = db.foodfun['Cereals and Millets']
    legumes = db.foodfun['Grain Legumes']
    vegetables = db.foodfun['Green Leafy Vegetables']
    other_vegetables = db.foodfun['Other Vegetables']
    fruits = db.foodfun['Fruits']
    tubers = db.foodfun['Roots and Tubers']
    spices = db.foodfun['Condiments and Spices']
    nuts = db.foodfun['Nuts and Oil seeds']
    sugars = db.foodfun['Sugars']
    mushrooms = db.foodfun['Mushrooms']
    misc = db.foodfun['Miscellaneous']
    milk = db.foodfun['Milk products']
    egg = db.foodfun['Egg products']
    chicken = db.foodfun['Chicken']
    meat = db.foodfun['Animal Meats']
    fishes = db.foodfun['Fishes']
    shell_fishes = db.foodfun['Shell fishes']
    marine_molluscs = db.foodfun['Marine Molluscs']
    freshwater_fishes = db.foodfun['Freshwater fish and shell fish']
    soups = db.foodfun['Soups,sauses and Gravies']
    baked = db.foodfun['Baked Products']
    snacks = db.foodfun['Snacks']
    chocolates = db.foodfun['Chocolates and confectionaries']
    fast_food = db.foodfun['Fast foods']
    beverages = db.foodfun['Beverages']

    return render_template("foodanalyse.html",cereals = cereals,legumes = legumes,vegetables = vegetables,other_vegetables = other_vegetables,fruits=fruits,tubers = tubers,spices=spices,nuts=nuts,sugars=sugars,mushrooms=mushrooms,misc=misc,milk=milk,egg=egg,chicken=chicken,meat=meat,fishes=fishes,shell_fishes=shell_fishes,marine_molluscs=marine_molluscs,freshwater_fishes=freshwater_fishes,soups=soups,baked=baked,snacks=snacks,chocolates=chocolates,fast_food=fast_food,beverages=beverages)

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("Username")
        password = request.form.get("Password")
        email = request.form.get("Email")
        age = request.form.get("Age")
        age = int(age)
        db.InsertUser(username, password, email, age)
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/DeficiencyResults",methods=["POST","GET"])
def DeficiencyResults():
    global Defresults
    if request.method == "POST":
        Defresults.clear()
        return redirect("/home")
    Defresults = db.SelectedDeficiencyRes()
    return render_template("DeficiencyResults.html",results = Defresults)

@app.route("/Deficiency",methods=["POST","GET"])
def Deficiency():
    if request.form.get('problemslist'):
        db.SelectedDeficiency(request.form.getlist('problemslist'))
        return redirect(url_for("DeficiencyResults"))

    global Organ
    Organ = db.FetchDeficiency1()
    return render_template("Deficiency.html",organ = Organ)


if __name__ == "__main__":
    app.run(debug=True)

#Total no of lines of code:
#Python : 710
# HTML: 1293
# Total : 2003