print("controller file running")

from crypt import methods
from flask import render_template,redirect,request,session, Flask,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe



@app.route("/create")
def create_new():
    return render_template("recipe.html")

@app.route("/create/recipe",methods=['post'])
def add_recipes():
    print('creating recipe')
    data = {
        "name":request.form["name"],
        "description":request.form["description"],
        "instructions":request.form["instructions"],
        "date_made":request.form["date_made"],
        "duration":request.form["duration"],
        "user_id": session["new_user"]
    }
    if not Recipe.validate_submit(data):
        return redirect("/create")

    new_recipe = Recipe.save(data)
    print(f"new recipe added {new_recipe}")
    return redirect("/dashboard")

@app.route("/submit")
def submit_recipe():
    return redirect("/dashboard")

@app.route("/edit/<int:id>")
def edit_recipe(id):
    data = {
        "id":id
    }

    one_recipe = Recipe.get_one(data)

    # edit_recipe=Recipe.edit(data)
    return render_template("editRecipe.html",one_recipe=one_recipe)


@app.route("/edit/<int:id>",methods=['post'])
def update_recipe(id):
    data = {
        "description":request.form["description"],
        "instructions":request.form["instructions"],
        "date_made":request.form["date_made"],
        "duration":request.form["duration"],
    }
    edit_recipe=Recipe.edit(data)

    return redirect('/dashboard',edit_recipe=edit_recipe)


@app.route("/view/<int:id>")
def view_recipe(id):
    data = {
        "id":id
        
    }
    one_recipe = Recipe.get_one(data)
    return render_template("viewRecipe.html",one_recipe=one_recipe)

@app.route("/delete/<int:id>")
def delete_recipe(id):
    data = {
        "id": id
    }
    Recipe.delete_recipe(data)
    return redirect("/dashboard")