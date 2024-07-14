from Chef.rollOutMenu import RollMenu
from Chef.viewRecommendation import Recommendation
from Chef.sendNotification import Notification
from Chef.viewDiscardMenu import DiscardMenu
from Chef.manageDiscardMenu import DiscardMenuManagement
from Admin.viewMenuItems import ViewMenu

class ChefMenu:
    def __init__(self):
        pass

    def main(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                view = ViewMenu()
                view.view_menu_items()
            elif choice == '2':
                view = Recommendation()
                view.view_recommendation()
            elif choice == '3':
                roll = RollMenu()
                roll.roll_menu_item()
            elif choice == '4':
                notify = Notification()
                notify.send_notification()
            elif choice == '5':
                discard = DiscardMenu()  
                discard.view_discard_menu() 
            elif choice == '6':
                manage = DiscardMenuManagement()
                manage.manage_discard_menu()
            elif choice == '7':
                print("Thank You for using the Cafeteria App!!")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        print("\nChef Menu")
        print("1. View Menu")
        print("2. View Recommendation")
        print("3. Roll out Menu")
        print("4. Send notification")
        print("5. View Discard Menu")
        print("6. Manage Discard Menu")
        print("7. Exit\n")
