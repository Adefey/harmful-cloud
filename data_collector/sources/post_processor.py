import json
import re
from tqdm import tqdm
import pandas as pd


def clean_string(string):
    permitted_chars = "^0-9A-Za-zА-Яа-яёЁ.!?/@#()*+-"
    string = re.sub(f"[{permitted_chars}]+", " ", string)
    return string


def json_to_clean_csv(json_string):
    data = json.loads(json_string)
    data_frame_list = []
    for post, comments in tqdm(data.items()):
        for comment in comments:
            if comment != "":
                if post != "":
                    data_frame_list.append({"post_text": clean_string(
                        post), "comment_text": clean_string(comment)})
    data_frame = pd.DataFrame(data_frame_list)
    return data_frame.to_csv()
