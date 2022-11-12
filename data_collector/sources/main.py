import sys
import json

from data_fetcher import generate_data
from post_processor import json_to_clean_csv


def main():

    config_path = sys.argv[1]
    with open(config_path, "r", encoding="UTF-8") as file:
        config = json.load(file)
    raw_result = generate_data(
        config["vk_token"], config["api_version"], config["group_ids"])
    raw_result_json = json.dumps(raw_result, ensure_ascii=False, indent=4)
    with open(config["raw_result_path"], "w", encoding="UTF-8") as file:
        file.write(raw_result_json)
    result = json_to_clean_csv(raw_result_json)
    with open(config["result_path"], "w", encoding="UTF-8") as file:
        file.write(result)


if __name__ == "__main__":
    main()
