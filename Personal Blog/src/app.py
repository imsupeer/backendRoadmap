import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from .articles_manager import (
    list_articles,
    get_article,
    create_article,
    update_article,
    delete_article,
)

load_dotenv()

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = os.environ.get("SECRET_KEY")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

# ---------------- Public Pages ---------------- #


@app.route("/")
def home():
    articles = list_articles()
    return render_template("home.html", articles=articles)


@app.route("/article/<int:article_id>")
def article_page(article_id):
    article = get_article(article_id)
    if not article:
        return "Article not found.", 404
    return render_template("article.html", article=article)


# ---------------- Login and Logout ---------------- #
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return "Invalid credentials", 401
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("home"))


def admin_required(func):

    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


# ---------------- Admin Pages ---------------- #


@app.route("/admin")
@admin_required
def admin_dashboard():
    articles = list_articles()
    return render_template("admin.html", articles=articles)


@app.route("/new", methods=["GET", "POST"])
@admin_required
def new_article():
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        date_str = request.form.get("date", "")
        article_id = create_article(title, content, date_str)
        return redirect(url_for("admin_dashboard"))
    return render_template("new_article.html")


@app.route("/edit/<int:article_id>", methods=["GET", "POST"])
@admin_required
def edit_article(article_id):
    article = get_article(article_id)
    if not article:
        return "Article not found.", 404

    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        date_str = request.form.get("date", "")
        updated = update_article(article_id, title, content, date_str)
        if not updated:
            return "Article not found.", 404
        return redirect(url_for("admin_dashboard"))

    return render_template("edit_article.html", article=article)


@app.route("/delete/<int:article_id>", methods=["POST"])
@admin_required
def delete_article_route(article_id):
    deleted = delete_article(article_id)
    if not deleted:
        return "Article not found.", 404
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
