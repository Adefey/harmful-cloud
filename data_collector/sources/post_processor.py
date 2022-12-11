import re
from tqdm import tqdm
import logging
logging.basicConfig(filename="logs.txt", filemode='a',
                    format="%(asctime)s %(message)s", datefmt="%I:%M:%S %p", level=logging.INFO)


def clean_string(string):
    permitted_chars = "^0-9A-Za-zА-Яа-яёЁ.!?/@#()*+-"
    string = re.sub(f"[{permitted_chars}]+", " ", string)
    return string


def dataframe_to_json(df):
    logging.info("Start creating JSON")
    json_dict = {"intents": []}
    groups = df["group"].unique()
    for group in tqdm(groups):
        posts = df.loc[df["group"] == group]["post_text"].unique()
        for post in tqdm(posts):
            comments = list(df.loc[(df["group"] == group) & (
                df["post_text"] == post)]["comment_text"])
            json_dict["intents"] += [{"tag": group,
                                      "patterns": post, "responses": comments}]
    return json_dict
