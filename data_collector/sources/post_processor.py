import json
import re
from tqdm import tqdm
import pandas as pd
import logging
logging.basicConfig(filename="logs.txt", filemode='a', format="%(asctime)s %(message)s", datefmt="%I:%M:%S %p", level=logging.INFO)

def clean_string(string):
    permitted_chars = "^0-9A-Za-zА-Яа-яёЁ.!?/@#()*+-"
    string = re.sub(f"[{permitted_chars}]+", " ", string)
    return string


def json_to_dataframe(json_string):
    logging.info(f"Start parsing JSON")
    data = json.loads(json_string)
    logging.info(f"JSON is parsed")
    data_frame_list = []
    for post, comments in tqdm(data.items()):
        for comment in comments:
            if comment != "":
                if post != "":
                    data_frame_list.append({"post_text": clean_string(
                        post), "comment_text": clean_string(comment)})
    logging.info(f"Start transforming to dataframe with {len(data_frame_list)} entries")
    data_frame = pd.DataFrame(data_frame_list)
    logging.info(f"Dataframe is ready with {len(data_frame)} entries")
    return data_frame
