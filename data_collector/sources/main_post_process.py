from post_processor import json_to_dataframe
import sys
import json
from sqlalchemy import create_engine
import logging
logging.basicConfig(filename="logs.txt", filemode='a',
                    format="%(asctime)s %(message)s", datefmt="%I:%M:%S %p", level=logging.INFO)


def main():
    config_path = sys.argv[1]
    with open(config_path, "r", encoding="UTF-8") as file:
        config = json.load(file)
    with open(config["cache_filename"], "r", encoding="UTF-8") as file:
        logging.info("Start reading file")
        raw_result_json = file.read()
        logging.info("File is read")
    result = json_to_dataframe(raw_result_json)
    if config["save_to_disc"] == "yes":
        logging.info("Saving to CSV file")
        result.to_csv(config["result_path"])
        logging.info("CSV file is saved")
    if config["save_to_mariadb"] == "yes":
        user = config["MYSQL_USER"]
        password = config["MYSQL_PASSWORD"]
        host = "mariadb"
        database = config["MYSQL_DATABASE"]
        port = config["MYSQL_TCP_PORT"]
        logging.info("Connecting to database")
        database_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
        engine = create_engine(database_uri, pool_recycle=1800)
        result.to_sql('posts', con=engine)
        engine.dispose()
        logging.info("Data is saved to database")
    print("SUCCESS")


if __name__ == "__main__":
    main()
