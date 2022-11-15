print("model file running")

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

# from ..controllers.user_controller import 
# from flask_app.models.user import User

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.duration = data['duration']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data["user_id"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes_schema.Recipe;"
        results = connectToMySQL('recipes_schema').query_db(query)
        print(results)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe)  ) 
        return recipes

    @classmethod
    def save(cls,data):
        query ="INSERT INTO Recipe(name,description,instructions,date_made,duration,created_at,updated_at,user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(duration)s,NOW(),NOW(),%(user_id)s);"

        new_recipe = connectToMySQL('recipes_schema').query_db(query,data)
        print(new_recipe)

        return new_recipe

    @staticmethod
    def validate_submit(data):
        is_valid = True
        print(is_valid)

        if len(data["name"]) < 2:
            is_valid = False
            flash("Invalid Name")
        
        if len(data["description"]) < 2:
            is_valid = False
            flash("Add more details pls")

        if len(data["instructions"]) < 20:
            is_valid = False
            flash("Ima need more instruction")

        # if data["duration"] != 0 or data["duration"] != 1:
        #     is_valid = False
        #     flash("Please select one ")

        return is_valid

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes_schema.recipe where id = %(id)s;"

        result = connectToMySQL('recipes_schema').query_db(query,data)

        recipe = cls(result[0])

        return recipe

    @classmethod
    def edit(cls,data):
        query = "UPDATE recipe SET description=%(description)s, instructions=%(instructions)s, duration=%(duration)s, date_made=NOW(),updated_at=NOW() WHERE id=%(id)s;"

        connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE  FROM recipe WHERE id = %(id)s"

        connectToMySQL('recipes_schema').query_db(query, data)