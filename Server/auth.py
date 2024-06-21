from DB_Connection.user_queries import UserQuery

class Authentication:
    def authenticateUser(data):
        username = data["username"]
        password = data["password"]
        print(username, password)
        print(type(username))
        json_data = UserQuery.authenticateUser(username)
        print(type(json_data))
        actual_password = json_data[0]["password"]
        if(password == actual_password):
            print(password, actual_password)
            return json_data[0]["role"]
        else:
            return "Incorrect password."
        
        