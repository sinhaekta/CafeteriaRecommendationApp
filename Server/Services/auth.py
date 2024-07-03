from DB_Connection.adminQueries import AdminQuery

class Authentication:
    @staticmethod
    def authenticate_user(data):
        try:
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                raise ValueError("Username and password must be provided.")

            json_data = AdminQuery.authenticate_user_query(username)
            
            if not json_data:
                raise ValueError("User not found.")

            actual_password = json_data[0].get("password")
            if not actual_password:
                raise ValueError("Password not found for the user.")

            if password == actual_password:
                return json_data[0].get("role", "Role not found.")
            else:
                return "Incorrect password."

        except ValueError as ve:
            return str(ve)
        except KeyError as ke:
            return f"Missing key: {ke}"
        except IndexError:
            return "No data found for the provided username."
        except Exception as e:
            return f"An error occurred: {e}"
