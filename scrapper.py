import json
import os
import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time


def get_chapter_link(book_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(book_url)
        time.sleep(5)
        page.wait_for_load_state('networkidle')
        html = page.content()
        browser.close()
    full_page = BeautifulSoup(html, 'html.parser')
    chapter_divs = full_page.find_all(class_=['toc-line-entry-text wst-toc-dot-bg wst-toc-dotentry'])
    chapter_data = []
    base_url = 'https://en.wikisource.org'
    for div in chapter_divs:
        link = div.find('a')
        if link:
            relative_link = link.get('href', '')
            absolute_link = base_url + relative_link if relative_link.startswith('/') else relative_link
            chapter_info = {
                'link': absolute_link,
                'title': link.get('title', ''),
                'chapter name': link.get_text(strip=True)
            }
            chapter_data.append(chapter_info)
    return chapter_data


def scrape_chapter(chapter_data, screenshot='screenshots/'):
    screenshot_path = screenshot + chapter_data['title'] + '.png'
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",headless=False)
        page = browser.new_page()
        page.goto(book_url)
        time.sleep(5)
        page.wait_for_load_state('networkidle')
        html = page.content()
        browser.close()
    full_page = BeautifulSoup(html, 'html.parser')
    full_chapter = full_page.find()
    paragraphs = full_chapter.find_all('p')
    book_name = None
    chapter_number = None
    chapter_title = None
    text_lines = []

    for i, p in enumerate(paragraphs):
        text = p.get_text(strip=True)
        if i == 0:
            book_name = text.strip()
        if i == 1 and "CHAPTER" in text.upper():
            chapter_number = text.strip()
        elif i >= 3:
            text_lines.append(text)
    return {
        "book_name": book_name,
        "chapter_number": chapter_number or "Unknown",
        "chapter_title": chapter_data['title'],
        "text_content": "\n\n".join(text_lines),
        "screenshot_path": screenshot_path,
        "source_url": chapter_data['link']
    }


def save_chapters_to_json(book_url, output_dir='chapters/', screenshot_dir='screenshots/'):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)

    # Get all chapter links
    chapters = get_chapter_link(book_url)
    chapters = chapters[8:]
    for chapter in chapters:
        print(chapter)
        chapter_data = scrape_chapter(chapter, screenshot=screenshot_dir)
        chapter_title = chapter_data['chapter_title']
        safe_filename = re.sub(r'[^\w\s-]', '', chapter_title).strip().replace(' ', '_')

        output_path = os.path.join(output_dir, f"{safe_filename}.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    book_url = 'https://en.wikisource.org/wiki/The_Gates_of_Morning'
    save_chapters_to_json(book_url)
