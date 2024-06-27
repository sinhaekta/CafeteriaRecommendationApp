from client import client_connection
from Admin.addMenuItem import AddMenu
from Admin.deleteMenuItem import DeleteMenu
from Admin.updateMenuItem import UpdateMenu
from Admin.viewMenuItems import ViewMenu

class AdminMenu:
    
    def __init__(self):
        pass

    def main(self):
        while True:
            self.display_admin_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                add = AddMenu()
                add.add_menu_item()
            elif choice == '2':
                delete = DeleteMenu()
                delete.delete_menu_item()
            elif choice == '3':
                update = UpdateMenu()
                update.update_menu_item()
            elif choice == '4':
                view = ViewMenu()
                view.view_menu_items()
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_admin_menu(self):
        print("Admin Menu")
        print("1. Add Menu Item")
        print("2. Delete Menu Item")
        print("3. Update Menu Item")
        print("4. View Menu Items")
        print("5. Exit")   