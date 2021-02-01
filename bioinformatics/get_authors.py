import pandas as pd
from scholarly import scholarly
import numpy as np
from tqdm import tqdm

MAX_COMMUNITIES = 10

nodes = pd.read_csv('../data/bioinformatics/graph_data/processed/giant component/gaint_nodes.csv')
auth_table = pd.read_csv('../data/bioinformatics/stage_4_processed/all-/auth_table.csv')

groups = nodes.groupby('modularity_class')
sorted_groups = groups.size().sort_values(ascending=False)

interests = []
affiliations = []
h_indexes = []
for j in range(len(sorted_groups)):
    group_id = sorted_groups.index[j]
    group_df = groups.get_group(group_id)

    for i in tqdm(range(len(group_df)), desc=f'Iteration: {j} Community Group: {group_id}'):
        auth = auth_table["name"].iloc[group_df['Id'].iloc[i]]

        try:
            search_q = next(scholarly.search_author(auth), None)
            if search_q is None:
                interests.append(np.nan)
                h_indexes.append(np.nan)
                affiliations.append(np.nan)
                continue

            author = scholarly.fill(search_q, sections=['basics', 'indices'])
            interest = author.get('interests')
            affiliation = author.get('affiliation')
            h_index = author.get('hindex')

            if interest is None:
                interest = np.nan

            if affiliation is None:
                affiliation = np.nan

            if h_index is None:
                h_index = np.nan

            interests.append(interest)
            affiliations.append(affiliation)
            h_indexes.append(h_index)

        except Exception:
            interests.append(np.nan)
            h_indexes.append(np.nan)
            affiliations.append(np.nan)


    # if j == MAX_COMMUNITIES:
    #     break

#
nodes['Interest'] = interests
nodes['affiliation'] = affiliations
nodes['h_index'] = h_indexes

nodes.to_csv('../data/bioinformatics/graph_data/processed/giant component/gaint_nodes_auth.csv', index=False)

