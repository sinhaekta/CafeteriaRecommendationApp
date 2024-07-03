from Employee.checkNotification import Notification
from Employee.orderFood import FoodOrder
from Employee.giveFeedback import Feedback
from Employee.discardItemFeedback import DiscardFeedback
from Employee.updateProfile import UserProfile

class EmployeeMenu:
    def __init__(self):
        pass

    def main(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                view = Notification()
                view.check_notification()
            elif choice == '2':
                order = FoodOrder()
                order.order_food()
            elif choice == '3':
                order = Feedback()
                user_id = int(input("Enter your user ID: "))
                order.give_feedback(user_id)
            elif choice == '4':
                discard_feedback = DiscardFeedback()
                discard_feedback.view_discard_item_notifications()
            elif choice == '5':
                profile = UserProfile()
                profile.update_profile()
            elif choice == '6':
                print("Exiting....")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        print("Employee Menu")
        print("1. Check Notification")
        print("2. Order Items")
        print("3. Give Feedback")
        print("4. Give Feedback on Discard Item")
        print("5. Update your Profile")
        print("6. Exit")