"""Change in Degree across time"""
import pandas as pd
from scipy.stats import kruskal
from scikit_posthocs import posthoc_dunn

nodes_2016 = pd.read_csv('../data/bioinformatics/graph_data/processed/2016/nodes.csv')
nodes_2017 = pd.read_csv('../data/bioinformatics/graph_data/processed/2017/nodes.csv')
nodes_2018 = pd.read_csv('../data/bioinformatics/graph_data/processed/2018/nodes.csv')
nodes_2019 = pd.read_csv('../data/bioinformatics/graph_data/processed/2019/nodes.csv')
nodes_2020 = pd.read_csv('../data/bioinformatics/graph_data/processed/2020/nodes.csv')
nodes_all = pd.read_csv('../data/bioinformatics/graph_data/processed/giant component/gaint_nodes.csv')

variable = 'Weighted Degree'

avg_degree_2016 = nodes_2016[variable].mean()
avg_degree_2017 = nodes_2017[variable].mean()
avg_degree_2018 = nodes_2018[variable].mean()
avg_degree_2019 = nodes_2019[variable].mean()
avg_degree_2020 = nodes_2020[variable].mean()
avg_degree_all = nodes_all[variable].mean()
columns = ['2016', '2017', '2018', '2019', '2020', 'all']
samples = [
    nodes_2016[variable],
    nodes_2017[variable],
    nodes_2018[variable],
    nodes_2019[variable],
    nodes_2020[variable],
    nodes_all[variable]
]

stat, p = kruskal(*samples)

alpha = 0.05
is_sig = p < alpha

# post hoc
ps = posthoc_dunn(samples, p_adjust='bonferroni')
final_stats = pd.DataFrame(ps.to_numpy(), columns=columns, index=columns)
a = 0
