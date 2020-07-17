import math
import pandas as pd
import sheet_values as sv

ItemParam = pd.read_csv('data/csvs/ItemParam.csv')

########################################
## ADD UNIVERSAL COLUMNS TO ITEMPARAM ##
########################################

ItemParam.rename(columns={'UniqueID': 'Internal ID', 'Label': 'Filename', 'Price': 'Buy'}, inplace=True)

ItemParam['Filename'] = ItemParam['Filename'].map(lambda Filename: Filename.strip('\''))

print(ItemParam.shape)

# Import ItemClothGroup & prep for data merge
clothGroup = pd.read_csv('data/csvs/ItemClothGroup.csv')
clothGroup['Label'] = clothGroup['Label'].map(lambda label: label.strip('\''))
clothGroup.rename(columns={'UniqueID': 'ClothGroup ID', 'Label': 'Label_ClothGroup', 'Name': 'Name_CG'}, inplace=True)

# Merge clothing strings with ItemClothGroup
clothSTR = sv.getClothingStrings()
clothGroup = clothGroup.merge(clothSTR, on='ClothGroup ID', how='left')

# Merge clothing strings into ItemParam
ItemParam = ItemParam.merge(clothGroup, left_on='ClothGroup', right_on='Label_ClothGroup')

# Merge item strings into ItemParam
itemSTR = sv.getItemStrings()
ItemParam = ItemParam.merge(itemSTR, on='Internal ID', how='left')

# ItemParam[['Internal ID', 'Filename', 'Name_Items', 'Name_Clothing']].to_csv(r'testing.csv', index=False)
"""
# FtrIcon / Storage Image
ItemParam['FtrIcon'] = ItemParam['Filename'].map(lambda x: f'=IMAGE("https://acnhcdn.com/latest/FtrIcon/{x}.png")')

print(ItemParam.shape)

# DIY
ItemParam['DIY'] = ItemParam['CaptureDiyIcon'].map(lambda x: 'Yes' if x == 1 else 'No')

print(ItemParam.shape)

# Sell
ItemParam['Sell'] = ItemParam['Buy'].map(lambda price: math.floor(price * 0.25))

print(ItemParam.shape)

# Color 1 / Color 2
ItemParam = ItemParam.replace({'Color1': 'LightBlue', 'Color2': 'LightBlue'}, 'Aqua')
ItemParam.rename(columns={'Color1': 'Color 1', 'Color2': 'Color 2'}, inplace=True)

print(ItemParam.shape)

# Size
size = pd.read_csv('data/sheet-values/Size.csv')
ItemParam = ItemParam.merge(size, on='ItemSize')

print(ItemParam.shape)

# Surface
surface = pd.read_csv('data/sheet-values/Surface.csv')
ItemParam = ItemParam.merge(surface, on='ItemLayout')

print(ItemParam.shape)

# HHA Concept 1
situation1 = pd.read_csv('data/sheet-values/HHASituation1.csv')
ItemParam = ItemParam.merge(situation1, on='ItemHHASituation1')

print(ItemParam.shape)

# HHA Concept 2
situation2 = pd.read_csv('data/sheet-values/HHASituation2.csv')
ItemParam = ItemParam.merge(situation2, on='ItemHHASituation2')

print(ItemParam.shape)

# Tag
tag = pd.read_csv('data/sheet-values/Tag.csv')
ItemParam = ItemParam.merge(tag, on='ItemUIFurnitureCategory')

print(ItemParam.shape)

# Catalog
catalog = pd.read_csv('data/sheet-values/Catalog.csv')
ItemParam = ItemParam.merge(catalog, on='ItemCatalogType')

print(ItemParam.shape)

# Version Added
version_added = pd.Series(sv.VersionAdded)
ItemParam = ItemParam.merge(version_added.rename('Version Added'), left_on='ItemReleaseVersion', right_index=True)

print(ItemParam.shape)
"""
#####################################
## CONSTRUCT HOUSEWARES DATA FRAME ##
#####################################
"""
housewares = ItemParam[ItemParam['ItemUICategory']=='Floor'].copy()

housewares['Image'] = housewares['Filename'].map(lambda x: f'=IMAGE("https://acnhcdn.com/latest/FtrIcon/{x}.png")')

tab_housewares = ['Name', 'Image', 'DIY', 'Buy', 'Sell', 'Color 1', 'Color 2', 'Size', 'Surface', 'HHA Concept 1', 'HHA Concept 2', 'Tag', 'Catalog', 'Version Added', 'Filename', 'Internal ID']

housewares_final = pd.concat([housewares.pop(item) for item in tab_housewares], axis=1)

print(housewares_final.tail())

# housewares[['ItemUIFurnitureCategory']].to_csv(r'testing.csv', index = False)
"""
###############################
## CONSTRUCT RUGS DATA FRAME ##
###############################

#rugs = ItemParam[ItemParam['ItemUICategory']=='RoomFloor']

# rugs.rename(columns={'FtrIcon': 'Image'}, inplace=True)

# tab_rugs = ['Name', 'Image', 'DIY', 'Buy', 'Sell', 'Color 1', 'Color 2', 'Size', 'Size Category',
#             'Miles Price', 'Source', 'Source Notes', 'HHA Base', 'HHA Concept 1', 'HHA Concept 2',
#             'HHA Series', 'Tag', 'Catalog', 'Version Added', 'Version Unlocked', 'Filename',
#             'Internal ID', 'Unique Entry ID']

# rugs_final = pd.concat([rugs.pop(item) for item in tab_rugs], axis=1)

# print(rugs_final.tail())