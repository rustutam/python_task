import argparse
import os
import pathlib
import sys
import urllib.request
import threading
import re
from typing import Optional
from urllib.error import URLError, HTTPError


def load_content(url: str) -> Optional[bytes]:
    try:
        return urllib.request.urlopen(url, timeout=10).read()
    except (HTTPError, URLError):
        return None


def get_articles(articles: int):
    page = load_content("https://habr.com").decode()
    reg = r'href="(.+?)".*?"tm-article-snippet__title-link"><span>(.+?)<'
    contents = re.finditer(reg, page)
    n = 0
    while n < articles:
        content = next(contents).groups()
        yield content
        n += 1


def load_article_image(link, page_name, out_dir):
    page = load_content('https://habr.com' + link).decode()

    begin = page.find(r'class="tm-article-body"')
    end = page.rfind(r'<br/>')
    if end == -1:
        end = page.rfind(r'/p')

    reg = r'<img src="(.+?)"'
    img_links = re.findall(reg, page[begin:end])

    for i in page_name:
        invalid = ['<', '>', '\\', '|', '/', ':', '*', '"', '?']
        if i in invalid:
            page_name = page_name.replace(i, '')

    if len(img_links) != 0:

        if not os.path.exists(out_dir / pathlib.Path(page_name)):
            os.makedirs(out_dir / pathlib.Path(page_name))

        for image in img_links:
            image_name = re.search('.+/(.+)', image)
            with open(out_dir / pathlib.Path(page_name) /
                      pathlib.Path(image_name.group(1)), 'wb') as f:
                f.write(load_content(image))


def run_scraper(threads: int, articles: int, out_dir: pathlib.Path) -> None:
    lock = threading.Lock()

    arts = iter(get_articles(articles))

    def get_art():
        with lock:
            try:
                return next(arts)
            except StopIteration:
                return None

    def th():
        while True:
            link = get_art()
            if not link:
                break
            load_article_image(link[0], link[1], out_dir)

    for _ in range(threads):
        threading.Thread(target=th).start()


def main():
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        usage=f'{script_name} [ARTICLES_NUMBER] THREAD_NUMBER OUT_DIRECTORY',
        description='Habr parser',
    )
    parser.add_argument(
        '-n', type=int, default=25, help='Number of articles to be processed',
    )
    parser.add_argument(
        'threads', type=int, help='Number of threads to be run',
    )
    parser.add_argument(
        'out_dir', type=pathlib.Path, help='Directory to download habr images',
    )
    args = parser.parse_args()
    run_scraper(args.threads, args.n, args.out_dir)


if __name__ == '__main__':
    main()
