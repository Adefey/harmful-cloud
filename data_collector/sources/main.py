import sys
import json

from data_fetcher import generate_data_to_cache
from post_processor import json_to_clean_csv


def main():

    config_path = sys.argv[1]
    with open(config_path, "r", encoding="UTF-8") as file:
        config = json.load(file)
    generate_data_to_cache(config["vk_token"], config["api_version"],
                           config["group_ids"], config["cache_filename"])
    with open(config["cache_filename"], "r", encoding="UTF-8") as file:
        raw_result_json = file.read()
    result = json_to_clean_csv(raw_result_json)
    with open(config["result_path"], "w", encoding="UTF-8") as file:
        file.write(result)


if __name__ == "__main__":
    main()
