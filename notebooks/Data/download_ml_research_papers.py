import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm
import argparse

SAVE_TO = '/Users/janek/Documents/gpt_project/papers/'
YEARS_OF_INTEREST = np.arange(2010, 2023, 1).tolist()
CONFERENCES = ['nips', 'icml', 'iclr']


def make_directory(save_path):
    if '.pdf' in save_path:
        save_path = '/'.join(save_path.split('/')[:-1])
    if not os.path.exists(save_path):
        os.mkdir(save_path)


def save_file(full_url, save_to):
    make_directory(save_to)
    with open(save_to, 'wb') as f:
        f.write(requests.get(full_url).content)


def get_nips_papers(year):
    BASE = 'https://papers.nips.cc/'
    CONFERENCE = 'nips'
    nips_save_to = SAVE_TO + f'{CONFERENCE}/' + f'{year}/'

    # parse html
    # for each year retrive list of links to paper pages
    response = requests.get(BASE + f'paper_files/paper/{year}')
    soup = BeautifulSoup(response.text, "html.parser")
    # 'paper title' is NIPS specific
    paper_links = soup.findAll("a", {'title': 'paper title'})
    for link in paper_links:  # for each paper page retrive links to paper pdfs
        response2 = requests.get(BASE + link["href"])
        soup2 = BeautifulSoup(response2.text, "html.parser")
        # 'Paper-Conference' is NIPS specific
        pdf_links = soup2.select("a[href$='.pdf']")
        pdf_links = [l for l in pdf_links if 'Paper' in l]
        for pdf_link in pdf_links:
            # we expect to see only one pdf file thus [0]
            pdf_link_href = pdf_link['href']
            link_to_download = urljoin(BASE, pdf_link_href)

            # download
            fname = link_to_download.split('/')[-1]
            save_file(link_to_download, nips_save_to + fname)
            print(f'downloaded: {link_to_download}')


def get_icml_papers():
    return


def get_iclr_papers():
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test argparse')
    parser.add_argument('--years', nargs='+', required=True, type=str,
                        help='years for which to download files')
    parser.add_argument('--conference', required=True, type=str,
                        help='conference for which to download files')

    args = parser.parse_args()
    for year in args.years:
        year = int(year)

        if year not in YEARS_OF_INTEREST:
            raise ValueError(
                f"{year} is a wrong Year. These are allowed years: {YEARS_OF_INTEREST}")

        if args.conference == 'nips':
            get_nips_papers(year)
        elif args.conference == 'icml':
            get_icml_papers(year)
        elif args.conference == 'iclr':
            get_iclr_papers(year)
        else:
            raise ValueError(f"These are allowed conferences: {CONFERENCES}")
