from collections import defaultdict
from typing import Dict, List, Tuple

from app.models import Content, Interest, Tag, User


def match_users_to_content(users: List[User], content: List[Content]) -> Dict[str, List[Content]]:
    # Create a lookup dictionary for content based on tag type and value
    content_lookup: Dict[Tuple[str, str], List[Tuple[int, int]]] = defaultdict(list)
    for i, item in enumerate(content):
        for j, tag in enumerate(item.tags):
            content_lookup[(tag.type, tag.value)].append((i, j))

    # Iterate over users and their tags, and only check matching content
    matched_content: Dict[str, List[Content]] = {}
    for user in users:
        content_ids = set()
        for tag in user.interests:
            for content_id, tag_id in content_lookup[(tag.type, tag.value)]:
                if content[content_id].tags[tag_id].threshold >= tag.threshold:
                    content_ids.add(content_id)

        matched_content[user.name] = [content[content_id] for content_id in content_ids]

    return matched_content
