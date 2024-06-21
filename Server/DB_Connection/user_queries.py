def view_recommended_menu(cls):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT item_id, comment FROM Comment")
                feedback = cursor.fetchall()
                print("Number of feedback rows fetched:", len(feedback)) 

                item_rating = {}

                for feed in feedback:
                    item_id, comment = feed
                    sentiment = TextBlob(comment).sentiment.polarity
                    if item_id in item_rating:
                        item_rating[item_id].append(sentiment)
                    else:
                        item_rating[item_id] = [sentiment]

                print("Item Ratings:", item_rating)  

                average_score = {item_id: sum(scores) / len(scores) for item_id, scores in item_rating.items()}

                recommended_items = sorted(average_score.items(), key=lambda x: x[1], reverse=True)

                print("Recommended Items:", recommended_items) 

                recommended_items_json = json.dumps(recommended_items)

                return recommended_items_json  

        except Exception as e:
            print("Error occurred:", e)
            traceback.print_exc()

            return json.dumps({"error": str(e)})