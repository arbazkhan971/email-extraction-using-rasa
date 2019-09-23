# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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
#         dispatcher.utter_message("Hello World!")
#
#         return []
from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction,REQUESTED_SLOT

class ActionRegisterUser(FormAction):

    def name(self):
        print("Inside name:")
        return "register_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("Inside required_slots:")    
        return ["name","email","number"]



    def validate_name(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        print("Inside validate function")
        print("Inside validate function name ",value)

        name = value
        if isinstance(value,str):
            return {"name": value}
        else:
            dispatcher.utter_template("utter_wrong_name", tracker)
            return {"name": None}

    def validate_email(self, value, dispatcher, tracker, domain):
        """Check to see if an email entity was actually picked up by duckling."""
        print("Inside validate function of email")
        print("Inside validate function of email ",value)

        if any(tracker.get_latest_entity_values("email")):
            # entity was picked up, validate slot
            return {"email": value}
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_template("utter_wrong_email", tracker)
            return {"email": None}
            
    def validate_number(self, value, dispatcher, tracker, domain):
        """Check to see if an email entity was actually picked up by duckling."""
        print("Inside validate function of number")
        print("Inside validate function of number ",value)

        if any(tracker.get_latest_entity_values("number")):
            # entity was picked up, validate slot
            return {"number": value}
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_template("utter_wrong_number", tracker)
            return {"number": None}
    
    


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        print("slot mapping")

        return {
            "name": self.from_entity(entity="name", intent=["user_info"]),
            "email": [
                self.from_entity(entity="email"),
                self.from_text(intent="user_info"),
                ],
            "number": [
                self.from_entity(entity="number"),
                self.from_text(intent="user_info"),
                ]    
        }
    
    
    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker,domain: Dict[Text, Any]):
        dispatcher.utter_template("utter_submit", tracker)
        print("Inside submit:")
        return []
