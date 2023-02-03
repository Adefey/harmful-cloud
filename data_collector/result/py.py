import json

def post_post_process(data):
    actual_data = data["intents"]
    result = []
    for entity in actual_data:
        result += [{"from" : "post", "text" : entity["patterns"]}]
        for comment in entity["responses"]:
            result += [{"from" : "comment", "text" : comment}]

    return result

with open("data.json", "r") as file:
    data = json.load(file)

data = post_post_process(data)

with open("data_new.json", "w") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
