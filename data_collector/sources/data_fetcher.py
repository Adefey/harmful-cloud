import requests

STRIDE = 100


def make_request(vk_token, api_version, method, params):
    '''Делает запрос и возвращает JSON (params - словарь)'''
    base_url = "https://api.vk.com/method/"
    params_str = "".join(
        [f"{key}={value}&" for key, value in params.items()] + [f"v={api_version}&access_token={vk_token}"])
    request_str = f"{base_url}{method}?{params_str}"
    response = requests.get(request_str, timeout=1)
    return response.json()


def generate_data(vk_token, api_version, group_ids):
    result = {}
    for group_id in group_ids:
        posts = get_wall_post_links(vk_token, api_version, group_id)
        for post_id, post_text in posts:
            post_comments = get_post_text_comments(
                vk_token, api_version, group_id, post_id)
            result.update({post_text: post_comments})
    return result


def get_wall_post_links(vk_token, api_version, group_id):
    '''Возвращает айди постов и их тексты на стене по айди группы'''
    wall = make_request(vk_token, api_version, "wall.get", {
                        "owner_id": group_id, "count": 1})
    post_count = int(wall["response"]["count"])
    posts = []
    for i in range(0, post_count+STRIDE, STRIDE):
        wall = make_request(vk_token, api_version, "wall.get", {
            "owner_id": group_id, "count": STRIDE, "offset": i*STRIDE})
        wall_items = wall["response"]["items"]
        posts += [(post["id"], post["text"].strip()) for post in wall_items]
    return posts


def get_post_text_comments(vk_token, api_version, group_id, post_id):
    '''Возвращает список текстов комментариев по айди на пост'''
    comments = make_request(vk_token, api_version, "wall.getComments", {
        "owner_id": group_id, "post_id": post_id, "count": 1})
    comment_count = int(comments["response"]["count"])
    comments_text = []
    for i in range(0, comment_count+STRIDE, STRIDE):
        comments = make_request(vk_token, api_version, "wall.getComments", {
            "owner_id": group_id, "post_id": post_id, "count": STRIDE, "offset": i*STRIDE})
        comments_items = comments["response"]["items"]
        comments_text += [comments_item["text"].strip()
                          for comments_item in comments_items]

    return comments_text
