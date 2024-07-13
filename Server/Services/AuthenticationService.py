from DB_Connection.AdminDBOperations import AdminDBOperation

class AuthenticationService:
    @staticmethod
    def authenticate_user(data):
        username = data["username"]
        password = data["password"]
        print(username, password)
        print(type(username))
        
        json_data = AdminDBOperation.authenticate_user_query(username)
        print(json_data)
        print(type(json_data))
        
        if json_data:
            actual_password = json_data[0]["password"]
            if password == actual_password:
                print(password, actual_password)
                return {
                    "role": json_data[0]["role"],
                    "user_id": json_data[0]["user_id"]
                }
            else:
                return "Incorrect password."
        else:
            return "User not found."
