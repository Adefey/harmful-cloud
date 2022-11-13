import requests
import os
import json
import logging
logging.basicConfig(format="%(asctime)s %(message)s",
                    datefmt="%I:%M:%S %p", level=logging.INFO)


STRIDE = 100


def make_request(vk_token, api_version, method, params):
    '''Делает запрос и пишет данные в кэш'''
    base_url = "https://api.vk.com/method/"
    params_str = "".join(
        [f"{key}={value}&" for key, value in params.items()] + [f"v={api_version}&access_token={vk_token}"])
    request_str = f"{base_url}{method}?{params_str}"
    response = requests.get(request_str, timeout=2)
    return response.json()


def generate_data_to_cache(vk_token, api_version, group_ids, cache_filename):
    result = {}
    # unused by now (need to store all data in RAM, better write it on the go)
    with open(cache_filename, "w", encoding="UTF-8") as file:
        file.write("{")
        for group_id in group_ids:
            posts = get_wall_post_links(vk_token, api_version, group_id)
            for post_id, post_text in posts:
                post_comments = get_post_text_comments(
                    vk_token, api_version, group_id, post_id)
                result.update({post_text: post_comments})
                string_to_file = f"{json.dumps({post_text: post_comments}, ensure_ascii=False, indent=4).replace('{','').replace('}','')},"
                file.write(string_to_file)
    with open(cache_filename, 'rb+') as file:  # Хочу удалить последний символ
        file.seek(-1, os.SEEK_END)
        file.truncate()
    with open(cache_filename, "a", encoding="UTF-8") as file:
        file.write("}")


def get_wall_post_links(vk_token, api_version, group_id):
    '''Возвращает айди постов и их тексты на стене по айди группы'''
    wall = make_request(vk_token, api_version, "wall.get", {
                        "owner_id": group_id, "count": 1})
    try:
        post_count = int(wall["response"]["count"])
    except KeyError:
        print(
            f"KeyError. Maybe the response is wrong format; Check it:\n{wall}")
    posts = []
    logging.info(
            f"Start revieve of ids and texts of number of posts: {post_count}")
    for i in range(0, post_count+STRIDE, STRIDE):
        wall = make_request(vk_token, api_version, "wall.get", {
            "owner_id": group_id, "count": STRIDE, "offset": i})
        wall_items = wall["response"]["items"]
        posts.extend([(post["id"], post["text"]) for post in wall_items])
        logging.info(
            f"Got new wall posts batch. Total wall posts (for this group) count: {len(posts)}")
    return posts


def get_post_text_comments(vk_token, api_version, group_id, post_id):
    '''Возвращает список текстов комментариев по айди на пост'''
    comments = make_request(vk_token, api_version, "wall.getComments", {
        "owner_id": group_id, "post_id": post_id, "count": 1})
    try:
        comment_count = int(comments["response"]["count"])
    except KeyError:
        print(
            f"KeyError. Maybe the response is wrong format; Check it:\n{comments}")
    comments_text = []
    logging.info(
            f"Start revieve of texts of number of comments: {comment_count}")
    for i in range(0, comment_count+STRIDE, STRIDE):
        comments = make_request(vk_token, api_version, "wall.getComments", {
            "owner_id": group_id, "post_id": post_id, "count": STRIDE, "offset": i})
        comments_items = comments["response"]["items"]
        comments_text.extend([comments_item["text"].strip() for comments_item in comments_items])
        logging.info(
            f"Got new comments batch. Total comment (for this post) count: {len(comments_text)}")

    return comments_text
