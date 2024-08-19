from typing import List

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models import Content, User

from .services.loader import load_json_to_db
from .services.matcher import match_users_to_content

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index() -> str:
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            try:
                json_data = file.read()
                load_json_to_db(json_data)
                flash("File successfully uploaded and processed")
            except Exception as e:
                flash(f"Error processing file: {str(e)}")
            return redirect(url_for("main.index"))

    users: List[User] = User.query.all()
    content: List[Content] = Content.query.all()
    matched_content = match_users_to_content(users, content)
    return render_template("index.html", matched_content=matched_content)


@main.route("/users")
def users() -> str:
    all_users: List[User] = User.query.all()
    return render_template("users.html", users=all_users)


@main.route("/content")
def content() -> str:
    all_content: List[Content] = Content.query.all()
    return render_template("content.html", content=all_content)
