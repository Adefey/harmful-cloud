import json
import re
from tqdm import tqdm
import pandas as pd


def clean_string(string):
    chars_to_delete = "\n\t\r1234567890"
    chars_to_replace_space = "!&?@.,:/"
    string = re.sub(f"[{chars_to_delete}]", "", string)
    string = re.sub(f"[{chars_to_replace_space}]", " ", string)
    return string


def json_to_clean_csv(json_string):
    data_frame = pd.DataFrame(columns=["post_text", "comment_text"])
    data = json.loads(json_string)
    for post, comments in tqdm(data.items()):
        for comment in comments:
            if comment != "":
                if post != "":
                    data_frame = data_frame.append({"post_text": clean_string(
                        post), "comment_text": clean_string(comment)}, ignore_index=True)
    return data_frame.to_csv()
