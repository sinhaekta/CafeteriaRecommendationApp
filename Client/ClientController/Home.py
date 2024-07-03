import json
from getpass import getpass
from client import client_connection
from ClientController.adminMenu import AdminMenu
from ClientController.chefMenu import ChefMenu
from ClientController.employeeMenu import EmployeeMenu

class CafeteriaApp:
    def __init__(self):
        self.username = None
        self.password = None

    def display_homepage(self):
        print("Welcome to the Cafeteria Recommendation Engine")
        print("Please log in:")

    def get_user_input(self):
        self.username = input("Username: ")
        self.password = getpass("Password: ")

    def authenticate_user(self, user_data):
        response = client_connection(user_data)
        return response

    def to_json(self):
        data = {
            "username": self.username,
            "password": self.password,
            "path": "auth"
        }
        return json.dumps(data)

    def main(self):
        self.display_homepage()
        self.get_user_input()
        user_data = self.to_json()
        response = self.authenticate_user(user_data)

        role = response.strip('"')
        if role == "admin":
            menu = AdminMenu()
            menu.main()
        elif role == "chef":
            menu = ChefMenu()
            menu.main()
        elif role == "employee":
            menu = EmployeeMenu()
            menu.main()
        else:
            print("Invalid role.")

if __name__ == "__main__":
    app = CafeteriaApp()
    app.main()
