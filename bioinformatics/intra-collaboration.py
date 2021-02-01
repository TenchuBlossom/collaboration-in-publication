import pandas as pd
from scipy.stats import kruskal
from scikit_posthocs import posthoc_dunn
import numpy as np

pub_2016_df = pd.read_csv('../data/bioinformatics/stage_3_processed/2016-bi-articles.csv')
pub_2017_df = pd.read_csv('../data/bioinformatics/stage_3_processed/2017-bi-articles.csv')
pub_2018_df = pd.read_csv('../data/bioinformatics/stage_3_processed/2018-bi-articles.csv')
pub_2019_df = pd.read_csv('../data/bioinformatics/stage_3_processed/2019-bi-articles.csv')
pub_2020_df = pd.read_csv('../data/bioinformatics/stage_3_processed/2020-bi-articles.csv')

pub_2016_df.dropna(axis=0, inplace=True)
pub_2017_df.dropna(axis=0, inplace=True)
pub_2018_df.dropna(axis=0, inplace=True)
pub_2019_df.dropna(axis=0, inplace=True)
pub_2020_df.dropna(axis=0, inplace=True)

pub_2016_auths = [len(x.split(',')) for x in pub_2016_df['authors'].values]
pub_2017_auths = [len(x.split(',')) for x in pub_2017_df['authors'].values]
pub_2018_auths = [len(x.split(',')) for x in pub_2018_df['authors'].values]
pub_2019_auths = [len(x.split(',')) for x in pub_2019_df['authors'].values]
pub_2020_auths = [len(x.split(',')) for x in pub_2020_df['authors'].values]

pub_2016_auths_mean = np.mean(pub_2016_auths)
pub_2017_auths_mean = np.mean(pub_2017_auths)
pub_2018_auths_mean = np.mean(pub_2018_auths)
pub_2019_auths_mean = np.mean(pub_2019_auths)
pub_2020_auths_mean = np.mean(pub_2020_auths)

pub_2016_cits = pub_2016_df['citations'].to_numpy().tolist()
pub_2017_cits = pub_2017_df['citations'].to_numpy().tolist()
pub_2018_cits = pub_2018_df['citations'].to_numpy().tolist()
pub_2019_cits = pub_2019_df['citations'].to_numpy().tolist()
pub_2020_cits = pub_2020_df['citations'].to_numpy().tolist()

samples = [
    pub_2016_auths,
    pub_2017_auths,
    pub_2018_auths,
    pub_2019_auths,
    pub_2020_auths
]
# Statistical Difference
columns = ['2016', '2017', '2018', '2019', '2020']
stat, p = kruskal(*samples)

alpha = 0.05
is_sig = p < alpha

# post hoc
ps = posthoc_dunn(samples, p_adjust='bonferroni')
sigs = np.zeros(shape=(len(ps), len(ps)))
for i in range(len(ps)):
    for j in range(len(ps)):
        sigs[i, j] = 1 if ps.iloc[i, j] < alpha else 0

final_stats_sigs = pd.DataFrame(sigs, columns=columns, index=columns)
final_stats = pd.DataFrame(ps.to_numpy(), columns=columns, index=columns)

# Correlation
corr_2016 = np.corrcoef(pub_2016_auths, pub_2016_cits)[0, 1]
corr_2017 = np.corrcoef(pub_2017_auths, pub_2017_cits)[0, 1]
corr_2018 = np.corrcoef(pub_2018_auths, pub_2018_cits)[0, 1]
corr_2019 = np.corrcoef(pub_2019_auths, pub_2019_cits)[0, 1]
corr_2020 = np.corrcoef(pub_2020_auths, pub_2020_cits)[0, 1]

a = 0