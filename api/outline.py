# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "beautifulsoup4",
#     "fastapi",
#     "requests",
#     "unicorn",
# ]
# ///
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from fastapi.responses import PlainTextResponse

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/outline", response_class=PlainTextResponse)
def get_outline(country: str = Query(..., description="Country name to look up")):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code != 200:
        return f"# Error\n\nCould not fetch Wikipedia page for '{country}'."

    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    markdown = f"## Contents\n\n# {country}\n\n"
    for tag in headings:
        level = int(tag.name[1])
        text = tag.get_text(strip=True)
        if text and not text.lower().startswith("jump to"):
            markdown += f"{'#' * level} {text}\n\n"


    return markdown.strip()
