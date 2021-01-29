"""
Creating an adjacency matrix that will capture which researchers have collaborated together on papers over all years
We can then filter the graph based on year, institute, interests ect. Edges will be weighted by the number of times
two researchers have collaborated. Nodes represent individual authors and are weighted by the h-index. H-index is a
measures both the productivity and citation impact of the publications of a scientist. Thus gives use a indication on how
influential or important an author is.

IDEAS:
- h-index of an author might be correlated to the number of collaborations an author has. I suspect positive correlation
    The higher the h-index the more collaboration edges
"""

import pandas as pd
import os
import csv
import numpy as np
from tqdm.auto import tqdm
import helpers as hlp
from multiprocessing import Pool, current_process, Manager


def execute(input_params):

    relations = input_params['relations']
    authors = input_params['authors']
    target_author = input_params['target_author']
    run_parallel = input_params['RUN_PARALLEL']
    job_num = input_params['JOB_NUM']

    worker_num = 0
    if run_parallel:
        worker_num = int(current_process().name.split('-')[1])

    auth_1_idx = np.where(relations[:, 0] == target_author[0])[0]
    auth_1_pubs = relations[auth_1_idx]


    row_data = []
    for j in range(0, len(authors)):
        auth_2 = authors[j]

        # if comparing same don't add recurrent connection
        if target_author[0] == auth_2[0]:
            continue

        # compare publications betwwen auth 1 & 2 two find colaboration
        auth_2_idx = np.where(relations[:, 0] == auth_2[0])[0]
        auth_2_pubs = relations[auth_2_idx]

        # turn authors pubs into sets. sets removed duplicates but this is okay. Authors can not
        # be published twice in the same journal and thus will not have duplicated pub ids
        auth_1_pub_set = set(auth_1_pubs[:, 1])
        auth_2_pub_set = set(auth_2_pubs[:, 1])

        common_pubs = list(auth_1_pub_set.intersection(auth_2_pub_set))

        # if found common publications then an edge weighted by the number of common publications
        if len(common_pubs) > 0:
            for common_pub in  common_pubs:
                c = np.where(auth_1_pubs[:, 1] == common_pub)[0][0]
                row_data.append([target_author[1], auth_2[1], auth_1_pubs[c, 1], auth_1_pubs[c, 2], auth_1_pubs[c, 3]])

    return row_data


if __name__ == '__main__':

    SRC_PREFIX1 = 'bioinformatics'
    SRC_PREFIX2 = 'all-'
    RUN_PARALLEL = True
    MAX_ITERATIONS = -1
    CHUNK_SIZE = 10

    DIR_CHAIN = ['data', SRC_PREFIX1, 'graph_data', SRC_PREFIX2]
    SRC = f'./data/{SRC_PREFIX1}/stage_4_processed/{SRC_PREFIX2}/'
    # Data loading and pre-processing

    auth_df = pd.read_csv(os.path.join(SRC, 'auth_table.csv'))
    auth_df['Id'] = auth_df.index.values
    auth_df = auth_df.rename(columns={'name': 'Label'})

    pub_df = pd.read_csv(os.path.join(SRC, 'pub_table.csv')).to_dict()
    relation_df = pd.read_csv(os.path.join(SRC, 'relations_table.csv'))

    # Convert to numpy arrays
    auth_array = auth_df.to_numpy()
    relations_array = relation_df.to_numpy()

    cols = ['Source', 'Target', 'Title', 'Year', 'Citations']
    csv_path = hlp.make_csv(DIR_CHAIN, 'edge_table.csv', cols)
    save_dir = hlp.make_dir(DIR_CHAIN)

    # Chunk data
    job_chain = []
    for idx, t_author in enumerate(auth_array):
        if MAX_ITERATIONS == idx and MAX_ITERATIONS != -1:
            break

        job_chain.append({
            'relations': relations_array,
            'authors': auth_array,
            'target_author': t_author,
            'RUN_PARALLEL': RUN_PARALLEL,
            'JOB_NUM': idx,
        })

    if not RUN_PARALLEL:
        with open(csv_path, 'a', newline='', encoding="utf-8") as csvout:
            writer = csv.writer(csvout, delimiter=',', quotechar='"')
            for job in tqdm(job_chain, desc=f'Computing Adj Matrix: cores=1'):
                results = execute(job)
                for r in results:
                    writer.writerow(r)
                    csvout.flush()
    else:
        with open(csv_path, 'a', newline='', encoding="utf-8") as csvout:
            writer = csv.writer(csvout, delimiter=',', quotechar='"')
            cores = os.cpu_count()
            with Pool(processes=cores) as pool:
                with tqdm(desc=f'Computing Adj Matrix: cores={cores}',total=len(job_chain)) as prog_bar:
                    for results in pool.imap(execute, job_chain, chunksize=CHUNK_SIZE):
                        for r in results:
                            writer.writerow(r)
                            csvout.flush()
                        prog_bar.update()

    auth_df = auth_df[["Id", "Label"]]
    auth_df.to_csv(os.path.join(save_dir, 'node_table.csv'), index=False)

