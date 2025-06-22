# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "beautifulsoup4",
#     "fastapi",
#     "requests"
# ]]
# ///
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline", response_class=PlainTextResponse)
def get_outline(request: Request):
    country = request.query_params.get("country")
    if not country:
        return "# Error\n\nMissing ?country= query parameter."
    
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    res = requests.get(url)
    if res.status_code != 200:
        return f"# Error\n\nCould not fetch page for '{country}'."

    soup = BeautifulSoup(res.text, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    markdown = "## Contents\n\n"
    for tag in headings:
        level = int(tag.name[1])
        text = tag.get_text(strip=True)
        if text and not text.lower().startswith("jump to"):
            markdown += f"{'#' * level} {text}\n\n"
    
    return markdown.strip()
