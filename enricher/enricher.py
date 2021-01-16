"""Enrich Url from Search Engine Results
"""
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from googlesearch import search
import random
from lxml.html import fromstring
import requests
import re
import tldextract


def get_netloc(url):
    """Clean url to get just domain of an url by stripping 'http', 'www' and so on

    Args:
        url (string): Url

    Returns:
        string: formatted url
    """
    netloc = ''
    url = str(url).lower()
    url = url.replace('https:', '')
    url = url.replace('http:', '')
    if len(url.split('.')) > 1:
        split_array = url.split('//')
        if len(split_array) > 1:
            netloc = split_array[len(split_array) - 1]
        else:
            netloc = url
        split_path = netloc.split('/')
        if len(split_path) > 1:
            netloc = split_path[0]
        netloc = netloc.replace('www.', '')
        netloc = netloc.replace('ww.', '')
        netloc = netloc.replace('\\', '')
        if netloc.startswith('.') and netloc.count('.') > 1:
            netloc = netloc.lstrip('.')
        return netloc
    else:
        netloc = None
        return netloc


def google_search(word):
    """Search in google for a keyword (company name)

    Args:
        word (string): google search query

    Returns:
        string: google search result for a word in parameter
    """
    try:
        container = [i for i in search(word, stop=3)]
        return remove_social_site_links(container)
    except Exception as exe:
        # Too many requests error
        return None


def result_from_bing(company_name):
    """Search in bing for a keyword (company name)

    Args:
        company_name (string): bing search query

    Returns:
        string: bing search result for word in parameter
    """
    try:
        container = []
        session = HTMLSession()
        url = "https://www.bing.com/search?q=" + \
            "+".join(company_name.split(' '))
        resp = session.get(url)
        response = resp.text
        if response != []:
            soup = BeautifulSoup(response, "lxml")
            results = soup.find("ol", {"id": "b_results"})
            for link in results.find_all('a', href=True):
                container.append(link['href'])
        return remove_social_site_links(container)
    except:
        return None


def remove_social_site_links(container):
    """Remove unwanted url from search engine result like linkedin, twitter, facebook urls

    Args:
        container (list): list with search results

    Returns:
        url: selected url
    """
    exclude_list = ['facebook', 'twitter',
                    'linkedin', 'youtube', 'wikipedia', '#']
    try:
        if container not in ('', 'NA'):
            filtered_data = [item for item in container if all(
                filter_word not in item for filter_word in exclude_list)]
            return filtered_data[0]
        else:
            return None
    except:
        return None


def get_company_url(company_name):
    """Initiates a thread to search in web for url

    Args:
        company_name (string): company name whose url is to be enriched

    Returns:
        string: appropriate url for the company from searched list
    """
    google_result = google_search(company_name)
    search_result = google_result
    if google_result in ('NA', '', None):
        bing_result = result_from_bing(company_name)
        search_result = bing_result
    try:
        ext = tldextract.extract(search_result)
        search_result = '.'.join([item for item in ext if item != ''])
    except:
        pass

    return search_result


def enrich_from_web(df):
    """Split the task to multiple threads to make execution fast

    Args:
        df (dataframe): dataframe with partners whose url needs to be enriched

    Returns:
        dataframe: url enriched dataframe
    """
    from concurrent.futures import ThreadPoolExecutor

    name_list = df['SpecialName'].to_list()
    name_list = [sname + ' IT' for sname in name_list]
    with ThreadPoolExecutor(max_workers=12) as pool:
        container = list(pool.map(get_company_url, name_list))
    df['EnrichedUrl'] = container
    return df


def enrich_url(df):
    """Enrich Url from search engine

    Args:
        df (dataframe): Description

    Returns:
        dataframe: Enriched dataframe with url enriched from Email and Web
    """
    df = df.assign(EnrichedUrl="")
    df = enrich_from_web(df)
    return df
