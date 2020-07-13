import pandas as pd
import importlib
import math
import sheet_values as sv

ItemParam = pd.read_csv('data/csvs/ItemParam.csv')

########################################
## ADD UNIVERSAL COLUMNS TO ITEMPARAM ##
########################################

ItemParam.rename(columns={'UniqueID': 'Internal ID', 'Label': 'Filename', 'Price': 'Buy'}, inplace=True)

ItemParam['Filename'] = ItemParam['Filename'].map(lambda Filename: Filename.strip('\''))

# DIY
ItemParam['DIY'] = ItemParam['CaptureDiyIcon'].map(lambda x: 'Yes' if x == 1 else 'No')

# Sell
ItemParam['Sell'] = ItemParam['Buy'].map(lambda price: math.floor(price * 0.25))

# Color 1 / Color 2
ItemParam = ItemParam.replace({'Color1': 'LightBlue', 'Color2': 'LightBlue'}, 'Aqua')
ItemParam.rename(columns={'Color1': 'Color 1', 'Color2': 'Color 2'}, inplace=True)

# Size
size = pd.read_csv('data/sheet-values/Size.csv')
ItemParam = ItemParam.merge(size, on='ItemSize')

# Surface
surface = pd.read_csv('data/sheet-values/Surface.csv')
ItemParam = ItemParam.merge(surface, on='ItemLayout')

# HHA Concept 1
situation1 = pd.read_csv('data/sheet-values/HHASituation1.csv')
ItemParam = ItemParam.merge(situation1, on='ItemHHASituation1')

# HHA Concept 2
situation2 = pd.read_csv('data/sheet-values/HHASituation2.csv')
ItemParam = ItemParam.merge(situation2, on='ItemHHASituation2')

# Tag
tag = pd.read_csv('data/sheet-values/Tag.csv')
ItemParam = ItemParam.merge(tag, on='ItemUIFurnitureCategory')

# Catalog
catalog = pd.read_csv('data/sheet-values/Catalog.csv')
ItemParam = ItemParam.merge(catalog, on='ItemCatalogType')

# Version Added
version_added = pd.Series(sv.VersionAdded)
ItemParam = ItemParam.merge(version_added.rename('Version Added'), left_on='ItemReleaseVersion', right_index=True)

#####################################
## CONSTRUCT HOUSEWARES DATA FRAME ##
#####################################

housewares = ItemParam[ItemParam['ItemUICategory']=='Floor']

tab_housewares = ['DIY', 'Sell', 'HHA Concept 1', 'Catalog', 'Version Added', 'Filename', 'Internal ID']

housewares_final = pd.concat([housewares.pop(item) for item in tab_housewares], axis=1)

print(housewares_final.tail())

# housewares[['ItemUIFurnitureCategory']].to_csv(r'testing.csv', index = False)