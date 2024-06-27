from Employee.checkNotification import Notification

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
                print("Give feedback")
            elif choice == '3':
                print("Exiting....")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        print("Employee Menu")
        print("1. Check Notification")
        print("2. Give Feedback")
        print("3. Exit")
