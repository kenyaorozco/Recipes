print("model file running")

from types import ClassMethodDescriptorType
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.recipe import Recipe
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipe = []


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user"
        results = connectToMySQL('recipes_schema').query_db(query)

        user = []
        for user in results:
            print(user)
            user.append(cls (user) )
        return user

    @classmethod
    def save(cls,data):
        query = "INSERT INTO user(first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"

        new_user = connectToMySQL('recipes_schema').query_db(query,data)
        return new_user


    @staticmethod
    def validate_user( data):
        is_valid = True
        print(is_valid)
        if len(data["first_name"]) < 2:
            is_valid = False
            flash("Invalid Name")
        
        if len(data["last_name"]) < 2:
            is_valid = False
            flash("Invalid last name")

        if len(data["email"]) < 1:
            is_valid = False
            flash("BOO I NEED AN EMAIL")

        if len(data["password"]) < 8:
            is_valid = False
            flash("password needs at least 8 characters")

        if (data["password"]) != (data["confirm"]):
            is_valid = False
            flash("Passwords Do NOT match")
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        if len(results) < 1:
            return False 
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return results[0]
    

    @staticmethod
    def validate_login( User ):
        is_valid = True
# test whether a field matches the pattern
        if not EMAIL_REGEX.match(User['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    @classmethod
    def show_one(cls,data):
        query="SELECT * FROM Recipe JOIN user on Recipe.user_id = user_id WHERE user.id= %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        print(results)

        one_user = cls(results[0])
        print(one_user)
        
        for recipe in results:
            recipe_data = {
                "id":recipe["id"],
                "name":recipe["name"],
                "description":recipe["description"],
                "instructions":recipe["instructions"],
                "date_made":recipe["date_made"],
                "duration":recipe["duration"],
                "user_id":recipe["user_id"],
                "first_name":recipe["first_name"],
                "created_at":recipe["created_at"],
                "updated_at":recipe["updated_at"],
            }
            one_user.recipe.append(Recipe(recipe_data))
        return one_user

    @classmethod
    def get_all_recipes_with_user(cls,data):
        query="SELECT * FROM user JOIN recipe on user.id = recipe.user_id; "
        results = connectToMySQL('recipes_schema').query_db(query,data)
        print(results)

        one_user = results
        print(one_user)
        return results
        
        # for recipe in results:
        #     recipe_data = {
        #         "id":recipe["id"],
        #         "name":recipe["name"],
        #         "description":recipe["description"],
        #         "instructions":recipe["instructions"],
        #         "date_made":recipe["date_made"],
        #         "duration":recipe["duration"],
        #         "user_id":recipe["user_id"],
        #         "first_name":recipe["first_name"],
        #         "created_at":recipe["created_at"],
        #         "updated_at":recipe["updated_at"],
        #     }
        #     one_user.recipe.append(Recipe(recipe_data))
        # return one_user

        
