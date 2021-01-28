import pandas as pd
import helpers as hlp
import os
from tqdm import tqdm

def execute(in_path, out_dir_path):

    auth_table = pd.read_csv(os.path.join(in_path, 'auth_table.csv'))
    auth_table['Id'] = auth_table.index.values
    auth_table = auth_table.rename(columns={'name': 'Label'})
    
    relations_table = pd.read_csv(os.path.join(in_path, 'relations_table.csv'))
    relations_table = relations_table.rename(columns={'name': 'Label'})

    pub_table = pd.read_csv(os.path.join(in_path, 'pub_table.csv'))
    out_path = hlp.make_dir(out_dir_path)

    edge_table = []
    for i in tqdm(range(len(auth_table)), desc='Computing Adjacency Matrix:'):
        auth_1 = auth_table['Label'].iloc[i]
        auth_1_pubs = relations_table[relations_table['Label'] == auth_1]['title'].to_list()

        for j in range(len(auth_table)):
            auth_2 = auth_table['Label'].iloc[j]

            # if comparing same don't add recurrent connection
            if auth_1 == auth_2:
                continue

            # compare publications betwwen auth 1 & 2 two find colaboration
            auth_2_pubs = relations_table[relations_table['Label'] == auth_2]['title'].to_list()

            # turn authors pubs into sets. sets removed duplicates but this is okay. Authors can not
            # be published twice in the same journal and thus will not have duplicated pub ids
            auth_1_pub_set = set(auth_1_pubs)
            auth_2_pub_set = set(auth_2_pubs)

            common_pubs = pub_table[pub_table['title'].isin(list(auth_1_pub_set.intersection(auth_2_pub_set)))]

            for k in range(len(common_pubs)):
                new_entry = {
                    'Target': auth_table['Id'].iat[i],
                    'Source': auth_table['Id'].iat[j],
                    'title': common_pubs['title'].iloc[k],
                    'year': common_pubs['year'].iloc[k],
                    'citations': common_pubs['citations'].iloc[k],
                }
                edge_table.append(new_entry)

            a = 0


if __name__ == '__main__':

    execute(
        in_path='./data/plos/stage_4_processed/all-',
        out_dir_path=['./data/plos', 'graph_data', 'all-']
    )