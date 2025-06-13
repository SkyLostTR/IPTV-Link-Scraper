"""Simple IPTV link scraper.

The script fetches IPTV links from ``streamtest.in`` and writes them to an
``m3u`` file.  It only performs very small scraping and does not handle
pagination limits from the upstream website.
"""

import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from art import text2art
from colorama import init
from termcolor import colored

scraped_links: List[str] = []


def create_m3u(fname: str) -> None:
    """Write scraped links to an ``m3u`` file."""
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %I-%M-%S-%p")
    print("[*]Creating m3u file..........")
    with open(f"{timestamp} {fname.upper()}.m3u", "a", encoding="utf-8") as m3u_creator:
        for link in scraped_links:
            m3u_creator.write(f"{link}\n")
    print("[*]Created m3u File!")


def fetch_links(pages: int, name: str) -> None:
    """Scrape links from ``streamtest.in``."""
    page_no = 1
    for _ in range(pages):
        print(f"{page_no}/{pages}")
        url = (
            f"https://streamtest.in/logs/page/{page_no}?"
            f"filter={name}&is_public=true"
        )
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all(
            "p", class_="line-clamp-3 hover:line-clamp-10"
        )
        for link in results:
            scraped_links.append(link.text.strip())
        page_no += 1


if __name__ == "__main__":
    init()
    art = text2art("IPTV Scraper")
    print(colored(art, "cyan"))
    print(colored("Developed By Henry Richard J", "blue"))

    channel_name = input("Channel to search: ")
    pages_to_scrape = int(input("How many pages to scrape: "))

    fetch_links(pages_to_scrape, channel_name)
    create_m3u(channel_name)
