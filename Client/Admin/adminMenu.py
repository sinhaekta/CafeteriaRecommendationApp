from client import client_connection
from Admin.addMenuItem import addMenu
from Admin.deleteMenuItem import deleteMenu
from Admin.updateMenuItem import updateMenu
from Admin.viewMenuItems import viewMenu

class admin_menu:
    
    def __init__(self):
        pass

    def main(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                add = addMenu()
                add.add_menu_item()
            elif choice == '2':
                delete = deleteMenu()
                delete.delete_menu_item()
            elif choice == '3':
                update = updateMenu()
                update.update_menu_item()
            elif choice == '4':
                view = viewMenu()
                view.view_menu_items()
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        print("Admin Menu")
        print("1. Add Menu Item")
        print("2. Delete Menu Item")
        print("3. Update Menu Item")
        print("4. View Menu Items")
        print("5. Exit")
    
    