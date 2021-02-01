import pandas as pd
from scipy.stats import kruskal
from scikit_posthocs import posthoc_dunn
import numpy as np

pub_table = pd.read_csv('./data/bioinformatics/stage_4_processed/all-/pub_table.csv')
groups = pub_table.groupby('year')
years = list(groups.groups.keys())

samples = [groups.get_group(y)['citations'].dropna().to_numpy() for y in years]

# Descriptives
median = [np.median(s) for s in samples]

# Inferentials
stat, p = kruskal(*samples)

alpha = 0.05
is_sig = p < alpha

# post hoc
ps = posthoc_dunn(samples, p_adjust='bonferroni')
final_stats = pd.DataFrame(ps.to_numpy(), columns=years, index=years)

a = 0

