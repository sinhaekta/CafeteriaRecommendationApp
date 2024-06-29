from Chef.rollOutMenu import RollMenu
from Chef.viewRecommendation import Recommendation
from Chef.sendNotification import Notification
from Chef.viewDiscardMenu import DiscardMenu
from Admin.viewMenuItems import ViewMenu

class ChefMenu:
    def __init__(self):
        pass

    def main(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                roll = RollMenu()
                roll.roll_menu_item()
            elif choice == '2':
                view = Recommendation()
                view.view_recommendation()
            elif choice == '3':
                notify = Notification()
                notify.send_notification()
            elif choice == '4':
                view = ViewMenu()
                view.view_menu_items()
            elif choice == '5':
                discard = DiscardMenu()  
                discard.view_discard_menu() 
            elif choice == '6':
                print("Exiting....")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        print("Chef Menu")
        print("1. Roll out Menu")
        print("2. View Recommendation")
        print("3. Send notification")
        print("4. View Menu")
        print("5. View Discard Menu")
        print("6. Exit")
