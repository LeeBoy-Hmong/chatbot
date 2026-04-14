from faq_data import intent_map as intent_map

def reply(user_quesion: str) -> str:
    message = user_quesion.lower()
##  ai_response =  # Placeholder for my AI
    for intent_names, intent_data in intent_map.items():
        if any(keyword in message for keyword in intent_data["keywords"]):
            return intent_data["response"]
    # for intent_names, intent_data in intent_map.items():  # loops through my dictionary list "intent_names = location / hours" & "intent_data = keywords / response".
    #     if any(keyword in message for keyword in intent_data["keywords"]):
    #         if intent_data["use_ai"] == True:
    #             return ai_response(message)
    #         else:
    #             return intent_data["response"]
        

    return "Sorry, I do not have the answer for that yet, I'm still learning. Please email one our members for further information."
