from Employee.CheckNotification import Notification
from Employee.OrderFood import FoodOrder
from Employee.GiveFeedback import Feedback
from Employee.DiscardItemFeedback import DiscardFeedback
from Employee.UpdateProfile import UserProfile

class EmployeeMenu:
    def __init__(self, user_id):
        self.user_id = user_id

    def main(self):
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ")

            if choice == '1':
                view = Notification()
                view.check_notification()
            elif choice == '2':
                order = FoodOrder()
                order.order_food(self.user_id)
            elif choice == '3':
                order = Feedback()
                order.give_feedback(self.user_id)
            elif choice == '4':
                discard_feedback = DiscardFeedback()
                discard_feedback.view_discard_item_notifications(self.user_id)
            elif choice == '5':
                profile = UserProfile()
                profile.update_profile(self.user_id)
            elif choice == '6':
                print("Thank You for using the Cafeteria App!!")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        print("\nEmployee Menu")
        print("1. View Today's Menu")
        print("2. Order Food")
        print("3. Give Feedback for your Food")
        print("4. Give Feedback for Discard Item")
        print("5. Update your Profile")
        print("6. Exit")