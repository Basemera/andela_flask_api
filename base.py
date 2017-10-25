from app.app import api, db, app
from app.views import AddUser, Addrecipe_category, Addrecipe, Login, Token

api.add_resource(AddUser, "/user", endpoint = "add_user")
api.add_resource(AddUser, "/user/<username>", endpoint = "get_user")
api.add_resource(Addrecipe_category, "/category", endpoint = "Add_category")
api.add_resource(Addrecipe_category, "/category/<category_name>", endpoint = "Get_category")
#api.add_resource(editcategory, "/category/<category_id>", endpoint = 'edit_category')
api.add_resource(Addrecipe, "/recipe", endpoint = "Add_recipe")
api.add_resource(Login, "/login", endpoint = "login")
api.add_resource(Token, "/token", endpoint = "get_token")
api.add_resource(Addrecipe_category, "/view", endpoint = "Veiw_category")
# api.add_resource(Addrecipe_category, "/id", endpoint = "id")
if __name__ == '__main__':
    app.run(debug=True)