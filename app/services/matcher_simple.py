# Simple implementation of a matching algorithm that loops over all possibilities

from typing import Dict, List

from app.models import Content, Interest, Tag, User


def match_users_to_content(users: List[User], content: List[Content]) -> Dict[str, List[Content]]:
    matched_content: Dict[str, List[Content]] = {}
    for user in users:
        matched_content[user.name] = []
        for item in content:
            if is_content_relevant(user.interests, item.tags):
                matched_content[user.name].append(item)
    return matched_content


def is_content_relevant(user_interests: List[Interest], content_tags: List[Tag]) -> bool:
    for interest in user_interests:
        for tag in content_tags:
            if interest.type == tag.type and interest.value == tag.value and interest.threshold <= tag.threshold:
                return True
    return False
