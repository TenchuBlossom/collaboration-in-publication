"""Change in Degree across time"""
import pandas as pd
from scipy.stats import kruskal
from scikit_posthocs import posthoc_dunn
import numpy as np
from sklearn.preprocessing import normalize

nodes_2016_df = pd.read_csv('../data/bioinformatics/graph_data/processed/2016/nodes.csv')
nodes_2017_df = pd.read_csv('../data/bioinformatics/graph_data/processed/2017/nodes_v2.csv')
nodes_2018_df = pd.read_csv('../data/bioinformatics/graph_data/processed/2018/nodes.csv')
nodes_2019_df = pd.read_csv('../data/bioinformatics/graph_data/processed/2019/nodes.csv')
nodes_2020_df = pd.read_csv('../data/bioinformatics/graph_data/processed/2020/nodes.csv')
nodes_all_df = pd.read_csv('../data/bioinformatics/graph_data/processed/all/nodes.csv')

variable = 'eigencentrality'
nodes_2016 = pd.Series(normalize(nodes_2016_df[variable].to_numpy().reshape(1, -1))[0, :])
nodes_2017 = pd.Series(normalize(nodes_2017_df[variable].to_numpy().reshape(1, -1))[0, :])
nodes_2018 = pd.Series(normalize(nodes_2018_df[variable].to_numpy().reshape(1, -1))[0, :])
nodes_2019 = pd.Series(normalize(nodes_2019_df[variable].to_numpy().reshape(1, -1))[0, :])
nodes_2020 = pd.Series(normalize(nodes_2020_df[variable].to_numpy().reshape(1, -1))[0, :])
nodes_all = pd.Series(normalize(nodes_all_df[variable].to_numpy().reshape(1, -1))[0, :])

avg_degree_2016 = nodes_2016.mean()
avg_degree_2017 = nodes_2017.mean()
avg_degree_2018 = nodes_2018.mean()
avg_degree_2019 = nodes_2019.mean()
avg_degree_2020 = nodes_2020.mean()
avg_degree_all = nodes_all.mean()

columns = ['2016', '2017', '2018', '2019', '2020', 'all']
samples = [
    nodes_2016,
    nodes_2017,
    nodes_2018,
    nodes_2019,
    nodes_2020,
    nodes_all
]

stat, p = kruskal(*samples)

alpha = 0.05
is_sig = p < alpha

# post hoc
ps = posthoc_dunn(samples, p_adjust='bonferroni')
final_stats = pd.DataFrame(ps.to_numpy(), columns=columns, index=columns)
a = 0