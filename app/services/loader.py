import json
from typing import Any, Dict

from app import db
from app.models import Content, Interest, Tag, User


def load_json_to_db(json_data: bytes) -> None:
    data: Dict[str, Any] = json.loads(json_data)

    if "name" in data:  # User JSON
        user = User(name=data["name"])
        db.session.add(user)
        for interest in data["interests"]:
            i = Interest(type=interest["type"], value=interest["value"], threshold=interest["threshold"], user=user)
            db.session.add(i)
    elif "id" in data:  # Content JSON
        content = Content(id=data["id"], title=data["title"], content=data["content"])
        db.session.add(content)
        for tag in data["tags"]:
            t = Tag(type=tag["type"], value=tag["value"], threshold=tag["threshold"], content=content)
            db.session.add(t)
    else:
        raise ValueError("Invalid JSON structure")

    db.session.commit()
