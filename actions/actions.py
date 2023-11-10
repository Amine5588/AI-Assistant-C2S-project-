# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

#from typing import Any, Text, Dict, List
#from rasa_sdk import Action, Tracker
#from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests

class ActionFetchMenu(Action):
    def name(self) -> Text:
        return "action_fetch_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict[Text, Any]]:
        # Make an HTTP GET request to fetch the menu items from your Spring Boot application
        menu_url = "http://localhost:8080/menu"  # Replace with the actual URL of your menu API
        response = requests.get(menu_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            menu_items = response.json()
            # Extract just the names of the menu items from the response
            food_names = [item['name'] for item in menu_items]
            # Store the menu items in the `menu_items` slot
            return [SlotSet("menu_items", food_names)]
        else:
            dispatcher.utter_message(text="Apologies, we are experiencing some technical difficulties. Please try again later.")
        
        return []
        


class ActionCheckMenuItem(Action):
    def name(self) -> Text:
        return "action_check_menu_item"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict[Text, Any]]:
        menu_items = tracker.get_slot("menu_items")
        item = tracker.get_slot("item")


        if menu_items and item:
            # Check if the provided item exists in the menu
            if item.lower() in [menu_item.lower() for menu_item in menu_items]:
                # Item exists in the menu, continue with the normal flow
                dispatcher.utter_message(text=f"Sure! we can provide {item} for you, how many servings do you want")
                return [SlotSet("item_exists", True)]
            else:
                # Item does not exist in the menu, ask the user to choose again
                dispatcher.utter_message(text=f"Apologies, we don't have {item} in our menu. Please choose another item or say show menu to have suggestions.")
                return [SlotSet("item_exists", False), SlotSet("item", None)]
        else:
            dispatcher.utter_message(text="Apologies, we are experiencing some technical difficulties. Please try again later.")

        return []








#import requests

#class ActionRestaurantMenu(Action):
#    def name(self) -> Text:
#        return "action_restaurant_menu"
#
#    def run(self, dispatcher: CollectingDispatcher,
#            tracker: Tracker,
#            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#        url = 'http://localhost:8080/menu'

#        try:
#            response = requests.get(url)
#            menu_items = response.json()
#            # Processing the menu_items as needed and send a response back to the user
#            dispatcher.utter_message(text="Here's the menu:\n" + "\n".join([f"{item['name']} " for item in menu_items]))
#        except requests.exceptions.RequestException:
#            dispatcher.utter_message(text="Sorry, I couldn't fetch the menu at the moment. Please try again later.")

        return []
