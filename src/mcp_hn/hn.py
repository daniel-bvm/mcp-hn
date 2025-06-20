import requests
from typing import List, Dict, Union, Any

BASE_API_URL = "http://hn.algolia.com/api/v1"
DEFAULT_NUM_STORIES = 10

DEFAULT_NUM_COMMENTS = 10
DEFAULT_COMMENT_DEPTH = 2

def _validate_comments_is_list_of_dicts(comments: List[Any]) -> bool:
    return isinstance(comments, list) and len(comments) > 0 and not isinstance(comments[0], int)

def _get_story_info(story_id: int) -> Dict:
    url = f"{BASE_API_URL}/items/{story_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def _format_story_details(story: Union[Dict, int], basic: bool = True) -> Dict:
    if isinstance(story, int):
        story = _get_story_info(story)
    output = {
        "id": story["story_id"],
        "author": story["author"],
    }
    if "title" in story:
        output["title"] = story["title"]
    if "points" in story:
        output["points"] = story["points"]
    if "url" in story:
        output["url"] = story["url"]
    if not basic:
        if _validate_comments_is_list_of_dicts(story["children"]):
            story = _get_story_info(story["story_id"])
        output["comments"] = [
            _format_comment_details(child) for child in story["children"]
        ]
    return output

def _format_comment_details(comment: Dict, depth: int = DEFAULT_COMMENT_DEPTH, num_comments: int = DEFAULT_NUM_COMMENTS) -> Dict:
    output = {
        "author": comment["author"],
        "text": comment["text"],
    }
    if depth > 1 and len(comment["children"]) > 0:
        output["comments"] = [
            _format_comment_details(child, depth - 1, num_comments) for child in comment["children"][:num_comments]
        ]
    return output

def get_stories(story_type: str, num_stories: int = DEFAULT_NUM_STORIES):
    story_type = story_type.lower().strip()
    if story_type not in ["top", "new", "ask_hn", "show_hn"]:
        raise ValueError("story_type must be one of: top, new, ask_hn, show_hn")

    # Map story type to appropriate API parameters
    api_params = {
        "top": {"endpoint": "search", "tags": "front_page"},
        "new": {"endpoint": "search_by_date", "tags": "story"},
        "ask_hn": {"endpoint": "search", "tags": "ask_hn"},
        "show_hn": {"endpoint": "search", "tags": "show_hn"}
    }

    params = api_params[story_type]
    url = f"{BASE_API_URL}/{params['endpoint']}?tags={params['tags']}&hitsPerPage={num_stories}"
    response = requests.get(url)
    response.raise_for_status()
    return [_format_story_details(story) for story in response.json()["hits"]]

def search_stories(query: str, num_results: int = DEFAULT_NUM_STORIES, search_by_date: bool = False):
    if search_by_date:
        url = f"{BASE_API_URL}/search_by_date?query={query}&hitsPerPage={num_results}&tags=story"
    else:
        url = f"{BASE_API_URL}/search?query={query}&hitsPerPage={num_results}&tags=story"
    response = requests.get(url)
    response.raise_for_status()
    return [_format_story_details(story) for story in response.json()["hits"]]

def get_story_info(story_id: int) -> Dict:
    story = _get_story_info(story_id)
    return _format_story_details(story, basic=False)

def _get_user_stories(user_name: str, num_stories: int = DEFAULT_NUM_STORIES) -> List[Dict]:
    url = f"{BASE_API_URL}/search?tags=author_{user_name},story&hitsPerPage={num_stories}"
    response = requests.get(url)
    response.raise_for_status()
    return [_format_story_details(story) for story in response.json()["hits"]]

def get_user_info(user_name: str, num_stories: int = DEFAULT_NUM_STORIES) -> Dict:
    url = f"{BASE_API_URL}/users/{user_name}"
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    response["stories"] = _get_user_stories(user_name, num_stories)
    return response
