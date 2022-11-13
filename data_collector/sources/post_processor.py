import json
import pandas as pd


def clean_string(string):
    string = string.strip()
    chars_to_delete = "\n\t\r!&?-+=@.,:/1234567890"
    for char in chars_to_delete:
        string = string.replace(char, " ")
    return string


def json_to_clean_csv(json_string):
    data_frame = pd.DataFrame(columns=["post_text", "comment_text"])
    data = json.loads(json_string)
    for post, comments in data.items():
        for comment in comments:
            if (comment != "") and (post != ""):
                data_frame = data_frame.append({"post_text": clean_string(
                    post), "comment_text": clean_string(comment)}, ignore_index=True)
    return data_frame.to_csv()
