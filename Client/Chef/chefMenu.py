from Chef.rollOutMenu import rollMenu
from Chef.viewRecommendation import recommendation

class chef_menu:
    def __init__(self):
        pass

    def main(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                roll = rollMenu()
                roll.roll_menu_item()
            elif choice == '2':
                view = recommendation()
                view.view_recommendation()
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        print("Chef Menu")
        print("1. Roll out Menu")
        print("2. View Recommendation")
        print("3. Exit")
