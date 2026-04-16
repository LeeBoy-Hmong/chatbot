# Holds the mapping to all of FAQ inquires.
intent_map = {
    "location" : {
        "keywords": ["location", "where", "find you", "address", "address"],
        "response": "You can find us at the DragonStar Market parking lot, Booth 16. Located in Brooklyn Park, MN.\n""We are also located at the Brooklyn Park Farmers Market in the North Hennepin Community College on W. Broadway Ave.",
        "use_ai": False
    },
    "hours" : {
        "keywords" : ["business hours", "hours", "location hours", "closing time", "opening time", "times", "time"],
        "response" : "We are open 7:00am to 5:00pm, every Friday, Saturday, and Sunday, at the Drag Star Supermarket - from June 12th to October 31st.\n""We are also open 1:00pm - 6:00pm at the Brooklyn Park Farmers Market - from July 8th to October 7th. ",
        "use_ai": False
    },
    "prices" : {
        "keywords" : ["prices", "price", "cost", "costs", "expensive", "cheap"],
        "response" : "None",
        "use_ai" : True
    },
    "payment" : {
        "keywords" : ["pay", "currency", "checkout"],
        "response" : "We accept USD ($) as well as credit and debit cards. Please note that all payments are processed in person at the time of purchase upon arrival at the shop.",
        "use_ai": False
    },
    "vegetables" : {
        "keywords" : ["vegetable", "vegetables", "produce", "products"],
        "response" : "None",
        "use_ai" : True
    },
    "contact": {
        "keywords" : ["contact", "email", "e-mail", "gmail", "get in touch", "get ahold of ", "get a hold of", "Reach"],
        "response" : "If you would like to contact us, or have a special inquiry, you may reach us at info@goliexeegardens.com.\n""We'll have someone get in touch with you as soon as we can.",
        "use_ai" : False
    }
}