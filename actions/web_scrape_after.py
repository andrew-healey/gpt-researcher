"""Selenium web scraping module."""
from __future__ import annotations

import logging
import asyncio
from pathlib import Path
from sys import platform

from bs4 import BeautifulSoup




from complexity import visit






from fastapi import WebSocket

import processing.text as summary

from config import Config
from processing.html import extract_hyperlinks, format_hyperlinks

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

FILE_DIR = Path(__file__).parent.parent
CFG = Config()


async def async_browse(url: str, question: str, websocket: WebSocket) -> str:
    """Browse a website and return the answer and links to the user

    Args:
        url (str): The url of the website to browse
        question (str): The question asked by the user
        websocket (WebSocketManager): The websocket manager

    Returns:
        str: The answer and links to the user
    """
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=8)

    print(f"Scraping url {url} with question {question}")
    await websocket.send_json(
        {"type": "logs", "output": f"🔎 Browsing the {url} for relevant about: {question}..."})

    try:
        text, driver = await loop.run_in_executor(executor, scrape_text_with_selenium, url)
        summary_text = await loop.run_in_executor(executor, summary.summarize_text, url, text, question)

        # print("Writing to file", f"AFTER/pages/{url.replace('/', '-')}.html")

        with open(f"AFTER/pages/{url.replace('/', '-')}.html", "w") as f:
            f.write(text)
        with open(f"AFTER/summaries/{url.replace('/', '-')}.html", "w") as f:
            f.write(summary_text)

        await websocket.send_json(
            {"type": "logs", "output": f"📝 Information gathered from url {url}: {summary_text}"})

        return f"Information gathered from url {url}: {summary_text}"
    except Exception as e:
        print(f"An error occurred while processing the url {url}: {e}")
        return f"Error processing the url {url}: {e}"

def browse_website(url: str, question: str):
    """Browse a website and return the answer and links to the user

    Args:
        url (str): The url of the website to browse
        question (str): The question asked by the user

    Returns:
        Tuple[str, WebDriver]: The answer and links to the user and the webdriver
    """

    if not url:
        return "A URL was not specified, cancelling request to browse website.", None

    page_source, text = scrape_text_with_selenium(url)
    summary_text = summary.summarize_text(url, text, question)

    links = scrape_links_with_selenium(page_source, url)

    # write_to_file('research-{0}.txt'.format(url), summary_text + "\nSource Links: {0}\n\n".format(links))

    return f"Answer gathered from website: {summary_text} \n \n Links: {links}"

def scrape_text_with_selenium(url: str):
    """Scrape text from a website using selenium

    Args:
        url (str): The url of the website to scrape

    Returns:
        Tuple[str, str]: The html and the text scraped from the website
    """
    logging.getLogger("selenium").setLevel(logging.CRITICAL)

    page_source,text = visit(url)

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return page_source, text



def scrape_links_with_selenium(page_source: str, url: str) -> list[str]:
    """Scrape links from a website using selenium

    Args:
        driver (WebDriver): The webdriver to use to scrape the links

    Returns:
        List[str]: The links scraped from the website
    """
    soup = BeautifulSoup(page_source, "html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    hyperlinks = extract_hyperlinks(soup, url)

    return format_hyperlinks(hyperlinks)[:5]