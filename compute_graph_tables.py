import os
import pandas as pd
from tqdm import tqdm
import string
import helpers as hlp


def execute(in_path, out_dir_path):

    data = pd.read_csv(in_path)
    out_path = hlp.make_dir(out_dir_path)
    table = str.maketrans('', '', string.punctuation)

    auth_list = []
    pub_list = []
    relations_list = []
    for i in tqdm(range(len(data))):
        pub = data.iloc[i]

        if pd.isna(pub['authors']) or pd.isna(pub['title']):
            continue

        authors = [auth.translate(table).strip().lower() for auth in pub['authors'].split(',')]

        # if single author paper then do not consider it
        if len(authors) < 2:
            continue

        for auth in authors:

            new_author = {
                'name': auth
            }

            new_pub = {
                'title': pub['title'],
                'year': pub['year'],
                'citations': pub['citations']
            }

            new_relation = {
                'name': auth,
                'title': pub['title'],
                'year': pub['year'],
                'citations': pub['citations']
            }

            auth_list.append(new_author)
            pub_list.append(new_pub)
            relations_list.append(new_relation)

    auth_table = pd.DataFrame(data=auth_list, columns=['name'])
    pub_table = pd.DataFrame(data=pub_list, columns=['title', 'year', 'citations'])
    relations_table = pd.DataFrame(data=relations_list, columns=['name', 'title', 'year', 'citations'])

    auth_table.drop_duplicates(subset=['name'], inplace=True, ignore_index=True)
    pub_table.drop_duplicates(subset=['title'], inplace=True, ignore_index=True)

    auth_table.to_csv(os.path.join(out_path, 'auth_table.csv'), index=False)
    pub_table.to_csv(os.path.join(out_path, 'pub_table.csv'), index=False)
    relations_table.to_csv(os.path.join(out_path, 'relations_table.csv'), index=False)


if __name__ == '__main__':
    src = './data/plos/stage_3_processed'
    files = os.listdir(src)
    for f in files:
        file_year = f[:4]

        if file_year != 'all-':
            file_year = int(f[:4])

        execute(
            in_path=os.path.join(src, f),
            out_dir_path=['./data/plos', 'stage_4_processed', f'{file_year}']
        )