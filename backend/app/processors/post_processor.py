import requests
from bs4 import BeautifulSoup


async def process_post(url: str):

    response = requests.get(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    text = soup.get_text()

    return text