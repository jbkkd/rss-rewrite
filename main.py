from typing import Any
from flask import Flask, Response, send_from_directory
from werkzeug.utils import secure_filename
import requests
from urllib.parse import quote


app: Flask = Flask(__name__)


import re

@app.route("/<path:rss_url>")
def rewrite_rss(rss_url: str) -> Response:
    """
    Given an rss url, rewrite the urls to pipe them through archive.md.
    """
    rss_feed = requests.get(rss_url)
    modified_xml = re.sub(r'<link>(.*?)</link>', lambda match: f'<link>{replace_link(match.group(1))}</link>', rss_feed.text)
    return Response(modified_xml, mimetype="application/xml")


@app.route("/rail/<path:filename>")
def serve_rail(filename: str = "") -> Any:
    """
    Serve files from the 'rail' directory.
    """
    if not filename:
        filename = "index.html"
    filename = secure_filename(filename)
    return send_from_directory("rail", filename)


def replace_link(link: str | None) -> str:
    """
    Given a link, replace it with the archive.md version of it.
    Example:
    https://example.com/content
    becomes
    https://archive.ph/?run=1&url=https://example.com/content
    """
    if not link:
        return ""
    return f"https://archive.ph/?run=1&url={quote(link)}"


if __name__ == "__main__":
    app.run(host='0.0.0.0')