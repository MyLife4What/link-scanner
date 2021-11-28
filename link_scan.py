import sys
import urllib
import urllib.error
import urllib.request
from typing import List

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


def get_links(web_url):
    """Find all links on page at the given url.

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """
    hyperlink_list = []
    browser.get(web_url)
    all_tags = browser.find_elements("tag name", "a")
    for link in all_tags:
        web_url = link.get_attribute('href')
        if web_url:
            if '#' in web_url:
                hyperlink_list.append(web_url.split('#')[0])
            elif '?' in web_url:
                hyperlink_list.append(web_url.split('?')[0])
            else:
                hyperlink_list.append(web_url)
    return hyperlink_list


def is_valid_url(web_url: str) -> bool:
    """Check if the url is valid and reachable.

    Returns:
        True if the URL is OK, False otherwise.
    """
    try:
        urllib.request.urlopen(web_url)
        return True
    except urllib.error.HTTPError:
        return False


def invalid_urls(url_list: List[str]) -> List[str]:
    """Validate the urls in url_list and return a new list containing the invalid or unreachable urls."""
    invalid_urls_list = []
    for url in url_list:
        if not is_valid_url(url):
            invalid_urls_list.append(url)
    return invalid_urls_list


if __name__ == "__main__":
    # path to webdriver
    browser: WebDriver = webdriver.Chrome(r'C:\Users\User\ISP\link-scanner\chromedriver.exe')
    args_amount = len(sys.argv)
    url = sys.argv[1]

    if args_amount != 2 or not is_valid_url(url):
        print("Usage:  python3 link_scan.py [url]")
        browser.quit()
    all_link = get_links(url)
    print()

    for link in all_link:
        print(link)

    bad_links = invalid_urls(all_link)
    if len(bad_links) > 0:
        print("\nBad Links:")
        for link in bad_links:
            print(link)
        browser.quit()

