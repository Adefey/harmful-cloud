import requests
import os
import json
import logging
logging.basicConfig(format="%(asctime)s %(message)s",
                    datefmt="%I:%M:%S %p", level=logging.INFO)


STRIDE = 100
TIMEOUT = 10


def make_request(vk_token, api_version, method, parameters):
    '''Делает запрос и пишет данные в кэш'''
    base_url = "https://api.vk.com/method/"
    param_dict = parameters
    param_dict.update({"v": api_version, "access_token": {vk_token}})
    request_method_str = f"{base_url}{method}"
    try:
        response = requests.get(
            request_method_str, params=param_dict, timeout=TIMEOUT).json()
    except Exception as exception:
        raise RuntimeError(
            f"Request error. Could not connect to server with timeout={TIMEOUT}; Check it:\n{exception}") from exception
    if "error" in response:
        raise RuntimeError(
            f"Request error. Server returned error status; Check it:\n{response}")
    return response


def generate_data_to_cache(vk_token, api_version, group_ids, cache_filename):
    with open(cache_filename, "w", encoding="UTF-8") as file:
        file.write("{")
        for group_id in group_ids:
            posts = get_wall_post_links(vk_token, api_version, group_id)
            for post_id, post_text in posts:
                post_comments = get_post_text_comments(
                    vk_token, api_version, group_id, post_id)
                string_to_file = f"{json.dumps({post_text: post_comments}, ensure_ascii=False, indent=4).replace('{','').replace('}','')},"
                file.write(string_to_file)
    with open(cache_filename, 'rb+') as file:  # Хочу удалить последний символ
        file.seek(-1, os.SEEK_END)
        file.truncate()
    with open(cache_filename, "a", encoding="UTF-8") as file:
        file.write("}")


def get_wall_post_links(vk_token, api_version, group_id):
    '''Возвращает айди постов и их тексты на стене по айди группы'''
    try:
        wall = make_request(vk_token, api_version, "wall.get", {
                            "owner_id": group_id, "count": 1})
    except RuntimeError as exception:
        logging.info(f"Error occured while fetching posts:\n{exception}")
        return []
    post_count = int(wall["response"]["count"])
    posts = []
    logging.info(
        f"Start revieve of ids and texts of number of posts: {post_count}")
    for i in range(0, post_count, STRIDE):
        try:
            wall = make_request(vk_token, api_version, "wall.get", {
                "owner_id": group_id, "count": STRIDE, "offset": i})
        except RuntimeError as exception:
            logging.info(f"Error occured while fetching posts:\n{exception}")
            return []
        wall_items = wall["response"]["items"]
        posts.extend([(post["id"], post["text"]) for post in wall_items])
        logging.info(
            f"Got new wall posts batch. Total wall posts (for this group) count: {len(posts)}")
    return posts


def get_post_text_comments(vk_token, api_version, group_id, post_id):
    '''Возвращает список текстов комментариев по айди на пост'''
    try:
        comments = make_request(vk_token, api_version, "wall.getComments", {
            "owner_id": group_id, "post_id": post_id, "count": 1})
    except RuntimeError as exception:
        logging.info(f"Error occured while fetching comments:\n{exception}")
        return []
    comment_count = int(comments["response"]["count"])
    comments_text = []
    logging.info(
        f"Start revieve of texts of number of comments: {comment_count}")
    for i in range(0, comment_count, STRIDE):
        try:
            comments = make_request(vk_token, api_version, "wall.getComments", {
                "owner_id": group_id, "post_id": post_id, "count": STRIDE, "offset": i})
        except RuntimeError as exception:
            logging.info(f"Error occured while fetching comments:\n{exception}")
            return []
        comments_items = comments["response"]["items"]
        comments_text.extend([comments_item["text"]
                             for comments_item in comments_items])
        logging.info(
            f"Got new comments batch. Total comment (for this post) count: {len(comments_text)}")

    return comments_text
