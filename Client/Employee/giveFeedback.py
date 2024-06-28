import json
from client import client_connection  

class Feedback:
    def __init__(self):
        pass
    
    def give_feedback(self, user_id):
        try:
            data = {"path": "fetch_employee_orders", "user_id": user_id}
            response = client_connection(json.dumps(data))  
            
            if isinstance(response, str):
                response = json.loads(response)

            if isinstance(response, dict) and response.get("status") == "success":
                orders = response.get("data", [])
                if not orders:
                    print("No orders found for this user.")
                    return
                
                print("Your Orders:")
                for order in orders:
                    print(f"Order ID: {order['order_id']}, "
                          f"Breakfast: {order['breakfast_item_name']}, "
                          f"Lunch: {order['lunch_item_name']}, "
                          f"Dinner: {order['dinner_item_name']}")
                
                order_id = input("Enter the Order ID for which you want to give feedback: ")

                feedback_list = []
                
                for meal_type in ["breakfast", "lunch", "dinner"]:
                    item_id_key = f"{meal_type}_item_id"
                    item_name_key = f"{meal_type}_item_name"
                    
                    if order[item_id_key]:
                        rating = float(input(f"Enter your rating for {meal_type.capitalize()} (0 to 5): "))
                        comment = input(f"Enter your comment for {meal_type.capitalize()}: ")
                        feedback_list.append({
                            "item_id": order[item_id_key],
                            "rating": rating,
                            "comment": comment
                        })
                    else:
                        print(f"{meal_type.capitalize()} item ID not found.")

                feedback_data = {
                    "path": "give_feedback",
                    "order_id": order_id,
                    "feedback": feedback_list
                }
                
                feedback_response = client_connection(json.dumps(feedback_data))
                if isinstance(feedback_response, str):
                    feedback_response = json.loads(feedback_response)

                if isinstance(feedback_response, dict) and feedback_response.get("status") == "success":
                    print("Feedback submitted successfully!")
                else:
                    print("Failed to submit feedback:", feedback_response.get("message"))
            else:
                print("Failed to fetch orders:", response.get("message", "Unknown error"))
        
        except Exception as e:
            print(f"Error in client: {e}")