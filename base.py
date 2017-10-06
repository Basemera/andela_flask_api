from app.app import api, db, app
from app.views import AddUser, Addrecipe_category, Addrecipe, Login

api.add_resource(AddUser, "/user", endpoint = "add_user")
api.add_resource(Addrecipe_category, "/category", endpoint = "Add_category")
api.add_resource(Addrecipe, "/recipe", endpoint = "Add_recipe")
api.add_resource(Login, "/login", endpoint = "login")
api.add_resource(Addrecipe_category, "/view", endpoint = "Veiw_category")
# api.add_resource(Addrecipe_category, "/id", endpoint = "id")
if __name__ == '__main__':
    app.run(debug=True)