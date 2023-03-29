import requests
import logging
from random import shuffle
import re
import time
from functools import reduce
logging.basicConfig(handlers=[logging.FileHandler("logs.txt", mode="w", encoding="UTF-8"), logging.StreamHandler()],
                    format="%(asctime)s %(message)s", datefmt="%I:%M:%S %p", level=logging.INFO)


STRIDE = 75
TIMEOUT = 100
EXECUTE_COUNT = 25


def clean_string(string):
    if string is None:
        string = "Имя группы не получено (Наверное произошла ошибка при groups.getById)"
    permitted_chars = "^0-9A-Za-zА-Яа-яёЁ!,:;._!?/@#()*+-"
    string = re.sub(f"[{permitted_chars}]+", " ", string)
    return string


def make_request(vk_token, api_version, method, parameters):
    '''Делает запрос в vk api'''
    time.sleep(0.1)  # не знаю, на всякий случай
    base_url = "https://api.vk.com/method/"
    param_dict = parameters
    param_dict.update(
        {"v": api_version, "access_token": vk_token.get_next_token()})
    request_method_str = f"{base_url}{method}"
    pairs = list(param_dict.items())
    query_string = "&".join([f"{pair[0]}={pair[1]}" for pair in pairs])
    logging.info(f"{request_method_str}?{query_string}")
    try:
        response = requests.get(
            request_method_str, params=param_dict, timeout=TIMEOUT).json()
    except Exception as exception:
        raise RuntimeError(
            f"Request error. Server error. Could not get needed data with timeout={TIMEOUT}; Check it:\n{exception}") from exception
    if "error" in response:
        raise RuntimeError(
            f"Request error. Server returned error status; Check it:\n{response}")
    return response


def prepare_group_ids(vk_token, api_version, approx_count):
    group_ids = []
    count = approx_count / 59  # Всего у нас 59 случаем поиска, для каждого надо вернуть список айди некоторой длины. Из расчета, что на каждую группу максимум 1500 постов - approx_count=590; count=10; количество текстов=590*1500=885000 записей. Больше в колаб не влезет. Ну и хрен с ним, сделаю approx_count больше, все равно половина пабликов пустые
    for letter in range(ord('a'), ord('z')):
        response = make_request(vk_token, api_version, "groups.search", {
                                "q": chr(letter), "type": "group", "count": count, "sort": 2})
        result = [item["id"] for item in response["response"]
                  ["items"] if item["is_closed"] == 0]
        logging.info(f"For letter: {chr(letter)}\nGroups: {result}")
        group_ids += result
    for letter in range(ord('а'), ord('я')):
        response = make_request(vk_token, api_version, "groups.search", {
                                "q": chr(letter), "type": "group", "count": count, "sort": 2})
        result = [item["id"] for item in response["response"]
                  ["items"] if item["is_closed"] == 0]
        logging.info(f"For letter: {chr(letter)}\nGroups: {result}")
        group_ids += result
    group_ids = list(set(group_ids))
    group_ids += [
        193207811,
        59336460,
        153502007,
        109863468,
        149279263,
        40427933,
        160594974,
        56443935,
        123002442,
        92204627,
    ]  # Бауманское наследие не забыто!
    logging.info(f"Group ids (all): {group_ids}")
    logging.info(f"Total: {len(group_ids)}")
    shuffle(group_ids)
    return group_ids


def generate_data_to_cache(vk_token, api_version, group_ids, cache_filename):
    '''Пишет данные в CSV кэш'''
    with open(cache_filename, "w", encoding="UTF-8") as file:
        file.write("group|post_text\n")
        for group_id in group_ids:
            group_name = get_group_name(vk_token, api_version, group_id)
            logging.info(f"Group: {group_name}")
            group_name_clean = clean_string(group_name)
            posts = get_wall_post_links(vk_token, api_version, group_id)
            for post in posts:
                post_text_clean = clean_string(post[1])  # [1] Текст поста
                file.write(f"{group_name_clean}|{post_text_clean}\n")
                # пусть посты будут не очень короткие, но и не очень длинные
                if (len(post_text_clean) > 10) and (len(post_text_clean) < 2000):
                    file.write(f"{group_name_clean}|{post_text_clean}\n")


def get_group_name(vk_token, api_version, group_id):
    try:
        response = make_request(vk_token, api_version, "groups.getById", {
            "group_id": group_id})
    except RuntimeError as exception:
        logging.info(f"Error occured while fetching group name:\n{exception}")
        return None
    group_name = response["response"][0]["name"]
    return group_name


def get_wall_post_links(vk_token, api_version, group_id):
    '''Возвращает айди постов и их тексты на стене по айди группы'''
    try:
        wall = make_request(vk_token, api_version, "wall.get", {
                            "owner_id": -group_id, "count": 1})
    except RuntimeError as exception:
        logging.info(f"Error occured while fetching post count:\n{exception}")
        return []
    post_count = int(wall["response"]["count"])
    post_count = post_count if post_count < 1501 else 1501
    posts = []
    logging.info(
        f"Start revieve of ids and texts of number of posts for group {group_id}: {post_count}")

    for i in range(0, post_count, EXECUTE_COUNT*STRIDE):
        vkscript_code = "var posts = []; "
        queries = [
            f"posts.push(API.wall.get({{'owner_id':{-group_id},'count':{STRIDE}, 'offset':{j}}})); " for j in range(i, i+EXECUTE_COUNT*STRIDE, STRIDE)]
        vkscript_code = vkscript_code + " ".join(queries)
        vkscript_code = f"{vkscript_code} return posts;"
        try:
            wall = make_request(vk_token, api_version, "execute", {
                "code": vkscript_code})
        except RuntimeError as exception:
            logging.info(
                f"Error occured while fetching posts (may be this batch was too big...):\n{exception}")
            continue
        try:
            wall_items = [wall_result["items"]
                          for wall_result in wall["response"]]
        except Exception as exception:
            print(
                f"Server responded, but the response was inappropriate;\nResponse:\n{wall}\nException:\n{exception}")
            continue
        wall_items = list(reduce(lambda x, y: x + y, wall_items))
        posts.extend([(post["id"], post["text"]) for post in wall_items])
        logging.info(
            f"Got new wall posts batch. Total wall posts for group {group_id}: {len(posts)}")
    return posts


def get_post_text_comments_execute(vk_token, api_version, group_id, post_ids):
    '''Возвращает первые 100 комментариев для EXECUTE_COUNT постов одновременно'''
    vkscript_code = "var comments = []; "
    queries = [
        f"comments.push(API.wall.getComments({{'owner_id':{-group_id},'post_id':{post_id}, 'count':100}})); " for post_id in post_ids]
    vkscript_code = vkscript_code + " ".join(queries)
    vkscript_code = f"{vkscript_code} return comments;"
    try:
        comments_list = make_request(vk_token, api_version, "execute", {
                                     "code": vkscript_code})
    except RuntimeError as exception:
        logging.info(f"Error occured while fetching comments:\n{exception}")
        return []
    comments_items = comments_list["response"]
    logging.info(
        f"Got new comments array batch. Total comment[{STRIDE}] arrays for group {-group_id}: {len(comments_items)}")
    return [[comment["text"] for comment in comments_item["items"]] for comments_item in comments_items]
