import re
from tqdm import tqdm
import logging
logging.basicConfig(filename="logs.txt", filemode='w',
                    format="%(asctime)s %(message)s", datefmt="%I:%M:%S %p", level=logging.INFO)


def clean_string(string):
    permitted_chars = "^0-9A-Za-zА-Яа-яёЁ!,:;_.!?/@#()*+-"
    string = re.sub(f"[{permitted_chars}]+", " ", string)
    return string


def dataframe_to_json(df):
    logging.info("Start creating JSON")
    json_dict = {"intents": []}
    groups = df["group"].unique()
    for group in tqdm(groups):
        posts = list(df.loc[df["group"] == group]["post_text"].unique())
        json_dict["intents"] += [{"group": group, "texts": posts}]
    return json_dict
