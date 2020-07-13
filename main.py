import pandas as pd
import importlib
import sheet_values as sv

ItemParam = pd.read_csv('data/csvs/ItemParam.csv')

########################################
## ADD UNIVERSAL COLUMNS TO ITEMPARAM ##
########################################

ItemParam.rename(columns={'UniqueID': 'Internal ID', 'Label': 'Filename'}, inplace=True)

# DIY
# Buy Price
# Sell Price
# Color 1
# Color 2
# Size
# Surface

# HHA Situation / Concept
situation = pd.read_csv('data/sheet-values/HHASituation.csv')
ItemParam = ItemParam.merge(situation, on='ItemHHASituation1')

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

tab_housewares = ['HHA Concept 1', 'Catalog', 'Version Added', 'Filename', 'Internal ID']

housewares_final = pd.concat([housewares.pop(item) for item in tab_housewares], axis=1)

print(housewares_final.tail())

# housewares[['ItemUIFurnitureCategory']].to_csv(r'testing.csv', index = False)