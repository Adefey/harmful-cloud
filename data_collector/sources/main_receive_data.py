import sys
import json

from data_fetcher import generate_data_to_cache


def main():
    config_path = sys.argv[1]
    with open(config_path, "r", encoding="UTF-8") as file:
        config = json.load(file)
    generate_data_to_cache(config["vk_token"], config["api_version"],
                           config["group_ids"], config["cache_filename"])


if __name__ == "__main__":
    main()
