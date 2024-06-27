import json
from client import client_connection

class AddMenu:
    
    def __init__(self, max_attempts=2):
        self.max_attempts = max_attempts
        
    def add_menu_item(self):
        
        for attempt in range(1, self.max_attempts + 1):
            try:
                name = input("Enter item name: ")
                if not name:
                    raise ValueError("Item name cannot be empty.")
                
                price = float(input("Enter item price: ")) 
                if price <= 0:
                    raise ValueError("Price must be a positive number.")
                
                description = input("Enter item description: ")
                if not description:
                    raise ValueError("Item description cannot be empty.")
                
                category = input("Enter item category (breakfast, lunch, dinner, all day): ").lower()
                if category not in ["breakfast", "lunch", "dinner", "all day"]:
                    raise ValueError("Invalid category. Must be one of: breakfast, lunch, dinner, all day.")
                
                request_data = {
                    "name": name,
                    "price": price,
                    "description": description,
                    "category": category,
                    "path": "add_menu_item"
                }
                
                request_json = json.dumps(request_data)

                response = client_connection(request_json)
                response_data = json.loads(response)  
                
                if response_data.get("status") == "success":
                    print(response_data.get("message"))  
                    return  

                else:
                    print("Error:", response_data.get("message"))  
                    if attempt < self.max_attempts:
                        print("Please try again.")

            except ValueError as ve:
                print("Input validation error:", ve)
                if attempt < self.max_attempts:
                    print("Please try again.")

            except Exception as e:
                print("Error occurred:", e)
                return

        print(f"Maximum attempts ({self.max_attempts}) reached. Exiting.")
