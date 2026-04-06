import json
import requests

from base64 import b64encode
from bs4 import BeautifulSoup

from config import SAVE_FILE_PATH


def get_kpop_news() -> list[str]:
    with open(SAVE_FILE_PATH, 'r') as save_file:
        save_data = json.load(save_file)
    last_checked_articles: list[str] = save_data["kpop_news"]["last_checked_articles"]
    reached_last_checked_article: bool = False

    get_request_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
    allkpop_page_1_response = requests.get("https://www.allkpop.com/", headers=get_request_headers)
    allkpop_page_1 = BeautifulSoup(allkpop_page_1_response.text, "html.parser")
    article_elements = allkpop_page_1.select('div .title a')
    article_links: list[str] = []
    for article_element in article_elements:
        article_link = article_element["href"]
        if article_link in last_checked_articles:
            reached_last_checked_article = True
            break
        article_links.append(article_link)

    if not reached_last_checked_article:
        first_article_timestamp_element = allkpop_page_1.find('div', id='load-more-articles-btn')
        first_article_timestamp = first_article_timestamp_element['data-first-ts']
        page_counter = 1
        while not reached_last_checked_article:
            post_request_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0', "content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
            unencoded_body = f"mode=more_stories&page={page_counter}&first_ts={first_article_timestamp}&ad_flag=home&view=a&feed=a&sort=n&period=a&my_vote_info=[]&keyword="
            print("unencoded_body: ", unencoded_body)
            encoded_body = b64encode(bytes(unencoded_body, 'utf-8')).decode('utf-8')
            print("encoded_body: ", encoded_body)
            post_request_body = f"en_data={encoded_body}"
            print("post_request_body: ", post_request_body)
            allkpop_page_response = requests.post("https://www.allkpop.com/", headers=post_request_headers, data=post_request_body)
            print("allkpop_page_response: ", allkpop_page_response)
            allkpop_page_articles_text = allkpop_page_response.text
            print("---------")
            print("allkpop_page_articles_text: ", allkpop_page_articles_text)
            print("---------")
            allkpop_page_articles = allkpop_page_response.json()
            print("allkpop_page_articles: ", allkpop_page_articles)

            for article in allkpop_page_articles:
                article_link = article["article_link"]
                print("article_link: ", article_link)
                if article_link in last_checked_articles:
                    reached_last_checked_article = True
                    break
                article_links.append(article_link)

            page_counter = page_counter + 1


    article_links.reverse()
    return article_links