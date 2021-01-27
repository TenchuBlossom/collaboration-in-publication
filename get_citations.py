"""
Bioinformatics journal does not allow scraping of citation numbers. SO we have to scrape google scholar by publication.
title to cross-reference respective citations numbers
"""
from serpapi import GoogleSearch
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import re

# TODO - Extract by publication name Onlu consider rows where both year and citations are nan
# TODO - Extract year of publication using regex get 4
# TODO - Change year if it is different
# TODO - Do parameter checks so program does crash and waste requests


def extract_results(response):
    citations = np.NaN
    year = np.NaN

    if response.get('organic_results') is None:
        return year, citations


    if response.get('organic_results')[0].get('inline_links') is not None:
        if response.get('organic_results')[0].get('inline_links').get('cited_by') is not None:
            if response.get('organic_results')[0].get('inline_links').get('cited_by').get('total') is not None:
                citations = response.get('organic_results')[0].get('inline_links').get('cited_by').get('total')

    if response.get('organic_results')[0].get('publication_info') is not None:
        if response.get('organic_results')[0].get('publication_info').get('summary') is not None:
            sum = response.get('organic_results')[0].get('publication_info').get('summary')
            match = re.search('\d{4}', sum)
            if match:
                match = match.group(0)
                if match:
                    year = match

    return year, citations


def main():
    SRC_FILE = '2020_bi_articles.csv'
    SRC_DIR = './data/bioinformatics/stage_1_processed/'
    API_KEY = 'c147329ae023a633d287a8fe2c777d54d570c1a0eea992f219ce7e14045c3608'
    MAX = 700

    data = pd.read_csv(os.path.join(SRC_DIR, SRC_FILE))
    params = {
        'engine': 'google_scholar',
        'q': '',
        'api_key': API_KEY,
        'num': 1
    }
    
    with tqdm(total=MAX) as progress_bar:
        iterations = 0
        for i in range(len(data)):
    
            if not np.isnan(data['year'].iloc[i]) or not np.isnan(data['citations'].iloc[i]):
                continue
    
            pub_title = data['title'].iloc[i]
    
            # Get response here
            params['q'] = f'title: {pub_title}'
            search = GoogleSearch(params)
            response = search.get_dict()
    
            year, citations = extract_results(response)
    
            data['year'].iat[i] = year
            data['citations'].iat[i] = citations
            
            iterations += 1
            progress_bar.update()
            
            if iterations == MAX:
                print(f'\nEarly Termination at {iterations} Iterations')
                break
    data.to_csv(os.path.join('./data/bioinformatics/stage_2_processed', SRC_FILE), index=False)


if __name__ == '__main__':
    main()



