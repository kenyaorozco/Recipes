print("server file running")
from flask_app import app
from flask_app.controllers import user_controller
from flask_app.controllers import recipe_controller
# EDIT CONTROLLERS


            
if __name__ == "__main__":
    app.run(debug=True) 