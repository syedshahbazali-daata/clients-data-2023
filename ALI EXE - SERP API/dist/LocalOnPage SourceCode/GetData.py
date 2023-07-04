import csv
import time

import requests
from serpapi import GoogleSearch
from xextract import String
import undetected_chromedriver as uc


def count_of_word_from_string(words, strings, words_on_webpage: list):
    count = 0
    words_found = []
    for single_string in strings:
        for single_word in words:
            for single_char in str(single_string).split(" "):
                if str(single_word).lower() in single_char.lower():
                    count += 1
                    words_found.append(single_word)
    words_on_webpage.extend(words_found)

    return [count, words_found]


def serp_result_finder(query, location, api_key, words, filename):
    driver = uc.Chrome()  # open chrome driver
    driver.maximize_window()
    folder_file = r"Exports\{}".format(filename)

    with open(folder_file, "w", newline="") as f:
        csv_file = csv.writer(f)
        csv_file.writerow(
            ["Link", "Title", "Description", "H1 - HEADER", "H2 - HEADER", "H3 - HEADER", "H4 - HEADER", "H5 - HEADER",
             "H6 - HEADER",
             "BODY", "P - PARAGRAPH", "WORDS ON PAGE", "HOW MANY TIMES WORDS ON PAGE"])
    params = {
        "engine": "google",
        "q": query,
        "num": "40",
        "location": location,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]

    words = words.split(", ")
    for single in organic_results:
        title = single['title']
        link = single['link']
        description = single['snippet']
        print(link)
        print(description)

        driver.get(link)
        time.sleep(2)
        page_source = str(driver.page_source)

        h1 = String(xpath='//h1').parse_html(page_source)
        h2 = String(xpath='//h2').parse_html(page_source)
        h3 = String(xpath='//h3').parse_html(page_source)
        h4 = String(xpath='//h4').parse_html(page_source)
        h5 = String(xpath='//h5').parse_html(page_source)
        h6 = String(xpath='//h6').parse_html(page_source)
        body = String(xpath='//body').parse_html(page_source)
        p = String(xpath='//p').parse_html(page_source)

        h1_data = ", ".join(h1).strip().replace("\n", " ")
        h2_data = ", ".join(h2).strip().replace("\n", " ")
        h3_data = ", ".join(h3).strip().replace("\n", " ")
        h4_data = ", ".join(h4).strip().replace("\n", " ")
        h5_data = ", ".join(h5).strip().replace("\n", " ")
        h6_data = ", ".join(h6).strip().replace("\n", " ")
        body_data = ", ".join(body).strip().replace("\n", " ")
        p_data = ", ".join(p).strip().replace("\n", " ")

        words_available = []

        h1_counts_words = count_of_word_from_string(words, h1, words_available)
        h2_counts_words = count_of_word_from_string(words, h2, words_available)
        h3_counts_words = count_of_word_from_string(words, h3, words_available)
        h4_counts_words = count_of_word_from_string(words, h4, words_available)
        h5_counts_words = count_of_word_from_string(words, h5, words_available)
        h6_counts_words = count_of_word_from_string(words, h6, words_available)
        body_counts_words = count_of_word_from_string(words, body, words_available)
        p_counts_words = count_of_word_from_string(words, p, words_available)

        total_words = sum(
            [h1_counts_words[0], h2_counts_words[0], h3_counts_words[0], h4_counts_words[0], h5_counts_words[0],
             h6_counts_words[0], body_counts_words[0], p_counts_words[0]])

        with open(folder_file, "a", newline="") as f:
            csv_file = csv.writer(f)
            csv_file.writerow(
                [link, title, description, h1_data, h2_data, h3_data, h4_data, h5_data, h6_data, body_data, p_data,
                 ", ".join(words_available), total_words])

    driver.quit()


