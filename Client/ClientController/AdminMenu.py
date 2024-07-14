from Client import client_connection
from Admin.AddMenuItem import AddMenu
from Admin.DeleteMenuItem import DeleteMenu
from Admin.UpdateMenuItem import UpdateMenu
from Admin.ViewMenuItems import ViewMenu

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
                print("Thank You for using the Cafeteria App!!")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_admin_menu(self):
        print("\nAdmin Menu")
        print("1. Add Menu Item")
        print("2. Delete Menu Item")
        print("3. Update Menu Item")
        print("4. View Menu Items")
        print("5. Exit\n")   