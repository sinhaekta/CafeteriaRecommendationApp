from Employee.checkNotification import Notification
from Employee.orderFood import FoodOrder
from Employee.giveFeedback import Feedback

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
                print("Exiting....")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        print("Employee Menu")
        print("1. Check Notification")
        print("2. Order Items")
        print("3. Give Feedback")
        print("4. Exit")
