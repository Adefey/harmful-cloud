import sys
import json

from post_processor import json_to_dataframe


def main():
    config_path = sys.argv[1]
    with open(config_path, "r", encoding="UTF-8") as file:
        config = json.load(file)
    with open(config["cache_filename"], "r", encoding="UTF-8") as file:
        raw_result_json = file.read()
    result = json_to_dataframe(raw_result_json)
    result.to_csv(config["result_path"])


if __name__ == "__main__":
    main()
