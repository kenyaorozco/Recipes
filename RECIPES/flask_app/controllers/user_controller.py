print("controller file running")

from flask import render_template,redirect,request,session, Flask,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 


@app.route("/")
def main_page():
    session.clear()
    return render_template("main.html")


@app.route("/register")
def register_page():
    return render_template("main.html")

@app.route("/home")
def home_page():
    return redirect("/")

@app.route("/register/submit",methods=["post"])
def registration():

    data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password": request.form["password"],
        "confirm": request.form["confirm"]
    }
    if not User.validate_user(data):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data["password"] = pw_hash

    new_user = User.save(data)
    session["new_user"] = new_user
    print(f"new user is {new_user}")
    return render_template("register.html")



@app.route("/register/submit")
def confirmation():
    return render_template("register.html")

@app.route("/login",methods=["post"])
def login_page():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect("/")

    session['new_user'] = user_in_db.id
    return redirect('/dashboard')

@app.route("/dashboard")
def main_board():
    if "new_user" not in session:
        return redirect('/')
    
    data = {
        "id": session["new_user"]
    }
    recipes= User.get_all_recipes_with_user(data)
    # all_recipes = Recipe.get_all()
    user_in_db = User.get_by_id(data)


    # new_recipe = Recipe.save(data)

    return render_template("dashboard.html",user_in_db=user_in_db,recipes=recipes)



# @app.route("/create")
# def create_new():
#     return render_template("recipe.html")

# @app.route("/create/recipe",methods=['post'])
# def add_recipes():
#     data = {
#         "name":request.form["name"],
#         "description":request.form["description"],
#         "instructions":request.form["instructions"],
#         "date_made":request.form["date_made"],
#         "duration":request.form["duration"],
#     }
#     new_recipe = Recipe.save(data)
#     return redirect("/dashboard",new_recipe=new_recipe)

# @app.route("/submit")
# def submit_recipe():
#     return redirect("/dashboard")

# @app.route("/edit")
# def edit_recipe():
#     # user_in_db = User.get_by_id(data)

#     # session['new_user'] = user_in_db.id

#     return render_template("viewRecipe.html")

@app.route("/logout")
def logout():
    return redirect("/")