
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
            print(menu_items)
        return []