from faq_data import intent_map as intent_map

def reply(user_quesion: str) -> str:

    message = user_quesion.lower()

    for intent_names, intent_data in intent_map.items():  # loops through my dictionary list "intent_names = location / hours" & "intent_data = keywords / response".
        if any(keyword in message for keyword in intent_data["keywords"]):
            return intent_data["response"]
        
    return "Sorry, I do not have the answer for that yet, I'm still learning. Please email one our members for further information."