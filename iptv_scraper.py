"""Simple IPTV link scraper.

The script fetches IPTV links from ``streamtest.in`` and writes them to an
``m3u`` file.  It only performs very small scraping and does not handle
pagination limits from the upstream website.
"""

import argparse
import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from art import text2art
from colorama import init
from termcolor import colored


def create_m3u(links: List[str], fname: str) -> str:
    """Write scraped ``links`` to an ``m3u`` file and return its path."""
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %I-%M-%S-%p")
    out_file = f"{timestamp} {fname.upper()}.m3u"
    print("[*]Creating m3u file..........")
    with open(out_file, "w", encoding="utf-8") as m3u_creator:
        for link in links:
            m3u_creator.write(f"{link}\n")
    print("[*]Created m3u File!")
    return out_file


def fetch_links(pages: int, name: str) -> List[str]:
    """Scrape links from ``streamtest.in``."""
    scraped_links: List[str] = []
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}
    for page_no in range(1, pages + 1):
        print(f"{page_no}/{pages}")
        url = (
            f"https://streamtest.in/logs/page/{page_no}?"
            f"filter={name}&is_public=true"
        )
        try:
            response = session.get(url, timeout=10, headers=headers)
            response.raise_for_status()
        except requests.RequestException as exc:
            print(f"Request failed: {exc}")
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all(
            "p", class_="line-clamp-3 hover:line-clamp-10"
        )
        for link in results:
            scraped_links.append(link.text.strip())
    return scraped_links


def main() -> None:
    """CLI entry point."""
    init()
    parser = argparse.ArgumentParser(description="Scrape IPTV links")
    parser.add_argument("channel", help="Channel to search for")
    parser.add_argument(
        "-p", "--pages", type=int, default=1, help="Number of pages to scrape"
    )
    args = parser.parse_args()

    art = text2art("IPTV Scraper")
    print(colored(art, "cyan"))
    print(colored("Developed By Henry Richard J", "blue"))

    links = fetch_links(args.pages, args.channel)
    if links:
        create_m3u(links, args.channel)


if __name__ == "__main__":
    main()
