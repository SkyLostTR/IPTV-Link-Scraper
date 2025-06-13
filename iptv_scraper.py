"""Interactive IPTV log scraper.

This tool fetches IPTV links from ``streamtest.in`` and optionally filters
them by channel name.  Results can be written to an ``m3u`` playlist.  The
script supports both a command line interface and an interactive menu.

Developed by Henry Richard J.  Maintained by Erin Andaç Kıran (@SkyLostTR).
"""

import argparse
import datetime
from typing import List, Optional

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


def print_links(links: List[str]) -> None:
    """Pretty-print scraped ``links``."""
    if not links:
        print(colored("[!] No links found", "red"))
        return
    for idx, link in enumerate(links, 1):
        print(colored(f"{idx:3}: {link}", "green"))


def confirm_save() -> bool:
    """Return ``True`` if the user wants to save the result."""
    choice = input(colored("Save results to an m3u file? [y/N]: ", "yellow"))
    return choice.strip().lower().startswith("y")


def interactive_menu() -> None:
    """Run the interactive text menu."""
    art = text2art("IPTV Scraper")
    print(colored(art, "cyan"))
    print(colored("Developed By Henry Richard J", "blue"))
    print(colored("Maintained By Erin Andaç Kıran (@SkyLostTR)", "blue"))

    while True:
        print(colored("\n1) Scrape logs", "cyan"))
        print(colored("2) Scrape logs with channel filter", "cyan"))
        print(colored("3) Quit", "cyan"))
        choice = input(colored("Select an option: ", "yellow")).strip()

        if choice == "1":
            pages = int(input(colored("Pages to scrape: ", "yellow")))
            links = fetch_links(pages, "")
            print_links(links)
            if links and confirm_save():
                create_m3u(links, "logs")
        elif choice == "2":
            name = input(colored("Channel name: ", "yellow"))
            pages = int(input(colored("Pages to scrape: ", "yellow")))
            links = fetch_links(pages, name)
            print_links(links)
            if links and confirm_save():
                create_m3u(links, name)
        elif choice == "3":
            break
        else:
            print(colored("Invalid choice!", "red"))


def main(argv: Optional[List[str]] = None) -> None:
    """CLI entry point."""
    init()
    parser = argparse.ArgumentParser(description="Scrape IPTV links")
    parser.add_argument("channel", nargs="?", help="Channel to search for")
    parser.add_argument(
        "-p", "--pages", type=int, default=1, help="Number of pages to scrape"
    )
    args = parser.parse_args(argv)

    if args.channel:
        art = text2art("IPTV Scraper")
        print(colored(art, "cyan"))
        print(colored("Developed By Henry Richard J", "blue"))
        print(colored("Maintained By Erin Andaç Kıran (@SkyLostTR)", "blue"))

        links = fetch_links(args.pages, args.channel)
        print_links(links)
        if links and confirm_save():
            create_m3u(links, args.channel)
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
