'''
Bioinformatics dataset are not seperated by year correctly and have missing values
'''
import os
import pandas as pd

# TODO - Keep rows with missing data, we can still use them for graph structure
# TODO - Give rows with missing years the year of the file
# TODO - Merge bioinformatics datasets
# TODO - Group by year

SRC = './data/bioinformatics/stage_2_processed'
YEARS = [2016, 2017, 2018, 2019, 2020]
SAMPLE = dict(
    active=False,
    size=450
)

dir = './data/bioinformatics/stage_3_processed'
if not os.path.exists(dir):
    os.mkdir(dir)
    
merged_data = None
files = os.listdir(SRC)
for f in files:
    file_year = int(f[:4])
    data = pd.read_csv(os.path.join(SRC, f))
    data['year'].fillna(file_year, inplace=True)
    
    if merged_data is None:
        merged_data = data

    else:
        merged_data = merged_data.append(data, sort=False)

groups = merged_data.groupby(['year'])

data_of_interest = []
for year in YEARS:
    data = groups.get_group(year)
    data.to_csv(os.path.join(dir, f'{year}-bi-articles.csv'), index=False)

merged_data = merged_data[merged_data['year'].isin(YEARS)]

if SAMPLE['active']:
    merged_data = merged_data.groupby(['year'], group_keys=False).apply(lambda x: x.sample(SAMPLE['size']))

merged_data.to_csv(os.path.join(dir, 'all-bi-articles.csv'), index=False)

