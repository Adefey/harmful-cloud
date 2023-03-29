import sys
import json
import time

from data_fetcher import generate_data_to_cache, prepare_group_ids


class token_container:
    def __init__(self, token_list):
        self.token_list = token_list
        self.cur_token_id = 0

    def get_next_token(self):
        if self.cur_token_id > (len(self.token_list) - 1):
            self.cur_token_id = 0
        self.cur_token_id += 1
        return self.token_list[self.cur_token_id-1]


def main():
    config_path = sys.argv[1]
    with open(config_path, "r", encoding="UTF-8") as file:
        config = json.load(file)
    tokens = token_container(config["vk_token"])
    group_ids = prepare_group_ids(tokens, config["api_version"], 3000)
    time.sleep(5)
    generate_data_to_cache(
        tokens, config["api_version"], group_ids, config["cache_filename"])
    print("SUCCESS")


if __name__ == "__main__":
    main()
