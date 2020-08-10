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
ItemParam = ItemParam.merge(clothGroup, left_on='ClothGroup', right_on='Label_ClothGroup', how='left')

# Merge item strings into ItemParam
itemSTR = sv.getItemStrings()
ItemParam = ItemParam.merge(itemSTR, on='Internal ID', how='left')

# Fill NaN with empty string & merge into single Name column
ItemParam[['Name_Clothing', 'Name_Items']] = ItemParam[['Name_Clothing', 'Name_Items']].fillna('')
ItemParam['Name'] = ItemParam['Name_Clothing'].astype(str) + ItemParam['Name_Items'].astype(str)

print(ItemParam.shape)

#print('ClothGroup ID')
#print(ItemParam['Internal ID'])

# ItemParam[['Internal ID', 'Filename', 'Name']].to_csv(r'testing.csv', index=False)

# FtrIcon / Storage Image
ItemParam['FtrIcon'] = ItemParam['Filename'].map(lambda x: f'=IMAGE("https://acnhcdn.com/latest/FtrIcon/{x}.png")')

print(ItemParam.shape)

# ClosetIcon / Closet Image

ItemParam['ClosetIcon'] = ItemParam['Filename'].map(lambda x: f'=IMAGE("https://acnhcdn.com/latest/ClosetIcon/{x}.png")')

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

# Size & Size Category
size = pd.read_csv('data/sheet-values/Size.csv')
ItemParam = ItemParam.merge(size, on='ItemSize')

print(ItemParam.shape)

# Surface
surface = pd.read_csv('data/sheet-values/Surface.csv')
ItemParam = ItemParam.merge(surface, on='ItemLayout')

print(ItemParam.shape)

# HHA Concept 1
situation1 = pd.read_csv('data/sheet-values/HHASituation1.csv')
ItemParam = ItemParam.merge(situation1, on='ItemHHASituation1', how='left')

print(ItemParam.shape)

# HHA Concept 2
situation2 = pd.read_csv('data/sheet-values/HHASituation2.csv')
ItemParam = ItemParam.merge(situation2, on='ItemHHASituation2', how='left')

print(ItemParam.shape)

# HHA Series
hhaSeries = pd.read_csv('data/sheet-values/HHATheme.csv')
ItemParam = ItemParam.merge(hhaSeries, on='ItemHHATheme', how='left')

print(ItemParam.shape)

# HHA Set
hhaSet = pd.read_csv('data/sheet-values/HHASet.csv')
ItemParam = ItemParam.merge(hhaSet, on='ItemHHASet', how='left')

print(ItemParam.shape)

# ItemParam[['ItemHHASet']].to_csv(r'ItemParam.csv', index=False)

# Tag
tag = pd.read_csv('data/sheet-values/Tag.csv')
ItemParam = ItemParam.merge(tag, on='ItemUIFurnitureCategory', how='left')

print(ItemParam.shape)

# Catalog
catalog = pd.read_csv('data/sheet-values/Catalog.csv')
ItemParam = ItemParam.merge(catalog, on='ItemCatalogType')

print(ItemParam.shape)

# Version Added
version_added = pd.Series(sv.VersionAdded)
ItemParam = ItemParam.merge(version_added.rename('Version Added'), left_on='ItemReleaseVersion', right_index=True)

print(ItemParam.shape)

# Nook Miles Exchange & Currency columns
ItemParam['Exchange_NM'] = ItemParam.apply(sv.calculateNookMilesPrice, axis=1)
ItemParam['Currency_NM'] = ItemParam.apply(sv.labelNookMiles, axis=1)

# NookMilesFrom = ['Fence', 'MileExchangeLicense', 'MileExchangeNsoPresent', 'MileExchangeOnce', 'MileExchangePhoneCase', 'MileExchangePocket40', 'MileExchangeRecipe1', 'MileExchangeRecipe2', 'MileExchangeRecipe3', 'MileExchangeRecipe4', 'MileExchangeRecipe5', 'SonkatsuReward2', 'SonkatsuRewardShop', 'SonkatsuRewardTent']
# test = ItemParam[ItemParam['ItemFrom'].isin(NookMilesFrom)]
# test[['Name', 'Exchange_NM', 'Currency_NM', 'Filename']].to_csv(r'NookMilesItems.csv', index=False)

# Import and prep Heart Crystal info
juneBride = pd.read_csv('data/csvs/CalendarEventJuneBrideExchange.csv')
juneBride.drop(columns=['UniqueID', 'DispInteriorMode', 'JuneBrideProgress'], inplace=True)
juneBride.rename(columns={'ExchangeItem': 'Internal ID', 'RequiredNum': 'Exchange_HC'}, inplace=True)

# Heart Crystals Exchange & Currency columns
ItemParam = ItemParam.merge(juneBride, on='Internal ID', how='left')
ItemParam['Currency_HC'] = ItemParam.apply(sv.labelJuneBride, axis=1)

# Fill NaN with empty string
ItemParam[['Exchange_NM', 'Exchange_HC', 'Currency_NM', 'Currency_HC']] = ItemParam[['Exchange_NM', 'Exchange_HC', 'Currency_NM', 'Currency_HC']].fillna('')

# Merge Nook Miles & Heart Crystals into Exchange & Exchange Currency columns
ItemParam['Exchange Price'] = ItemParam['Exchange_NM'].astype(str) + ItemParam['Exchange_HC'].astype(str)
ItemParam['Exchange Currency'] = ItemParam['Currency_NM'].astype(str) + ItemParam['Currency_HC'].astype(str)

ItemParam[['Exchange Price', 'Exchange Currency']] = ItemParam[['Exchange Price', 'Exchange Currency']].replace(r'^\s*$', 'NA', regex=True)

print(ItemParam.shape)

# HHA Base Points
# ItemParam : ItemFrom > ItemFrom : UniqueID :: HHABaseScore

# Import and prep HHA Base info
itemFrom = pd.read_csv('data/csvs/ItemFrom.csv')
itemFrom.drop(columns=['Name', 'UniqueID'], inplace=True)
itemFrom.rename(columns={'Label': 'ItemFrom', 'HHABaseScore': 'HHA Base Points'}, inplace=True)
itemFrom['ItemFrom'] = itemFrom['ItemFrom'].map(lambda x: x.strip('\''))

# itemFrom.to_csv(r'ItemFrom.csv', index=False)

# HHA Base Points column
ItemParam = ItemParam.merge(itemFrom, on='ItemFrom', how='left')

print(ItemParam.shape)

## WALLPAPER COLUMNS ##

roomWallParam = pd.read_csv('data/csvs/RoomWallParam.csv')
roomWallParam.replace({'Act': {'None': 'NA'}}, inplace=True)
roomWallParam.rename(columns={'Act': 'VFX Type', 'ItemTableId': 'Internal ID'}, inplace=True)

roomWindow = pd.read_csv('data/sheet-values/RoomWindow.csv')
roomWallParam = roomWallParam.merge(roomWindow, on='WindowUniqueID', how='left')

roomCurtain = pd.read_csv('data/sheet-values/RoomCurtain.csv')
roomWallParam = roomWallParam.merge(roomCurtain, on='CurtainUniqueID', how='left')

roomCurtainColor = pd.read_csv('data/sheet-values/RoomCurtainTex.csv')
roomWallParam = roomWallParam.merge(roomCurtainColor, on='CurtainTexUniqueID', how='left')

roomCeiling = pd.read_csv('data/sheet-values/RoomCeiling.csv')
roomWallParam = roomWallParam.merge(roomCeiling, on='CeilingUniqueID', how='left')

toDrop = ['AO','Light','Price','ArchUniqueID','CeilingUniqueID','CurtainTexUniqueID','CurtainUniqueID','UniqueID','ItemName','ResourceName','TextureWindow','WindowUniqueID']
roomWallParam.drop(columns=toDrop, inplace=True)

roomWallParam[['Window Color', 'Pane Type', 'Curtain Color']] = roomWallParam[['Window Color', 'Pane Type', 'Curtain Color']].fillna('NA')

ItemParam['VFX'] = ItemParam.apply(sv.wallpaperVFX, axis=1)

ItemParam = ItemParam.merge(roomWallParam, on='Internal ID', how='left')

print(ItemParam.shape)

# Add empty columns to match spreadsheet
ItemParam['Source Notes'] = ''
ItemParam['Version Unlocked'] = ''
ItemParam['Unique Entry ID'] = ''

# print(ItemParam['Internal ID'])

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

####################################
## CONSTRUCT WALLPAPER DATA FRAME ##
####################################

wallpaper = ItemParam[ItemParam['ItemUICategory']=='RoomWall'].copy()

wallpaper.rename(columns={'FtrIcon': 'Image'}, inplace=True)

tab_wallpaper = ['Name', 'Image', 'VFX', 'VFX Type', 'DIY', 'Buy', 'Sell', 'Color 1', 'Color 2', 'Exchange Price',
                 'Exchange Currency', 'ItemFrom', 'Source Notes', 'Window Type', 'Window Color', 'Pane Type',
                 'Curtain Type', 'Curtain Color', 'Ceiling Type', 'HHA Base Points', 'HHA Concept 1',
                 'HHA Concept 2', 'HHA Series', 'Tag', 'Catalog', 'Version Added', 'Version Unlocked', 'Filename',
                 'Internal ID', 'Unique Entry ID']

wallpaper_final = pd.concat([wallpaper.pop(item) for item in tab_wallpaper], axis=1)
wallpaper_final.sort_values(by=['Name'], inplace=True)

# wallpaper_final.to_csv(r'Wallpaper.csv', index=False)

#################################
## CONSTRUCT FLOORS DATA FRAME ##
#################################

floors = ItemParam[ItemParam['ItemUICategory']=='RoomFloor'].copy()

floors.rename(columns={'FtrIcon': 'Image'}, inplace=True)

tab_floors = ['Name', 'Image', 'VFX', 'DIY', 'Buy', 'Sell', 'Color 1', 'Color 2', 'Exchange Price',
            'Exchange Currency', 'ItemFrom', 'Source Notes', 'HHA Base Points', 'HHA Concept 1',
            'HHA Concept 2', 'HHA Series', 'Tag', 'Catalog', 'Version Added', 'Version Unlocked', 'Filename',
            'Internal ID', 'Unique Entry ID']

floors_final = pd.concat([floors.pop(item) for item in tab_floors], axis=1)
floors_final.sort_values(by=['Name'], inplace=True)

# floors_final.to_csv(r'Floors.csv', index=False)

###############################
## CONSTRUCT RUGS DATA FRAME ##
###############################

rugs = ItemParam[ItemParam['ItemUICategory']=='Ceiling_Rug'].copy()

rugs.rename(columns={'FtrIcon': 'Image'}, inplace=True)

tab_rugs = ['Name', 'Image', 'DIY', 'Buy', 'Sell', 'Color 1', 'Color 2', 'Size', 'Size Category',
            'Exchange Price', 'Exchange Currency', 'ItemFrom', 'Source Notes', 'HHA Base Points', 'HHA Concept 1',
            'HHA Concept 2', 'HHA Series', 'Tag', 'Catalog', 'Version Added', 'Version Unlocked', 'Filename',
            'Internal ID', 'Unique Entry ID']

rugs_final = pd.concat([rugs.pop(item) for item in tab_rugs], axis=1)
rugs_final.sort_values(by=['Name'], inplace=True)

# rugs_final.to_csv(r'Rugs.csv', index=False)

""" CLOTHING TESTING
print('Clothing shapes start here:')

# Tops
tops = ItemParam[ItemParam['ItemKind']=='Tops'].copy()
print(tops['Internal ID'])
print(tops.shape)

# Bottoms
bottoms = ItemParam[ItemParam['ItemKind']=='Bottoms'].copy()
print(bottoms.shape)

# Dress-Up
dressup = ItemParam[ItemParam['ItemKind']=='OnePiece'].copy()
print(dressup.shape)

# Headwear
headwear = ItemParam[ItemParam['ItemKind'].isin(['Cap', 'Helmet'])].copy()
print(headwear.shape)

# Accessories
accessories = ItemParam[ItemParam['ItemKind']=='Accessory'].copy()
print(accessories.shape)

# Socks
socks = ItemParam[ItemParam['ItemKind']=='Socks'].copy()
print(socks.shape)

# Shoes
shoes = ItemParam[ItemParam['ItemKind']=='Shoes'].copy()
print(shoes.shape)

# Bags
bags = ItemParam[ItemParam['ItemKind']=='Bag'].copy()
print(bags.shape)

# Umbrellas
umbrellas = ItemParam[ItemParam['ItemKind']=='Umbrella'].copy()
print(umbrellas.shape)

# Clothing Other (MarineSuits)
marinesuits = ItemParam[ItemParam['ItemKind']=='MarineSuit'].copy()
print(marinesuits.shape)

tops = tops[['Internal ID', 'ClothGroup ID']]
bottoms = bottoms[['Internal ID', 'ClothGroup ID']]
dressup = dressup[['Internal ID', 'ClothGroup ID']]
headwear = headwear[['Internal ID', 'ClothGroup ID']]
accessories = accessories[['Internal ID', 'ClothGroup ID']]
socks = socks[['Internal ID', 'ClothGroup ID']]
shoes = shoes[['Internal ID', 'ClothGroup ID']]
bags = bags[['Internal ID', 'ClothGroup ID']]
umbrellas = umbrellas[['Internal ID', 'ClothGroup ID']]
marinesuits = marinesuits[['Internal ID', 'ClothGroup ID']]

# ============================================================
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('clothing_clothGroups.xlsx', engine='xlsxwriter')

# Write each dataframe to a different worksheet.
tops.to_excel(writer, sheet_name='Tops')
bottoms.to_excel(writer, sheet_name='Bottoms')
dressup.to_excel(writer, sheet_name='Dress-Up')
headwear.to_excel(writer, sheet_name='Headwear')
accessories.to_excel(writer, sheet_name='Accessories')
socks.to_excel(writer, sheet_name='Socks')
shoes.to_excel(writer, sheet_name='Shoes')
bags.to_excel(writer, sheet_name='Bags')
umbrellas.to_excel(writer, sheet_name='Umbrellas')
marinesuits.to_excel(writer, sheet_name='Clothing Other')

# Close the Pandas Excel writer and output the Excel file.
writer.save()


## JANKY 1.4.0 UPDATE CSV FILE

newItems = ItemParam[ItemParam['Version Added']=='1.4.0'].copy()

print(newItems)

newItems[['ItemUICategory', 'Version Added', 'Filename', 'Internal ID', 'Name', 'ClosetIcon', 'FtrIcon', 'DIY', 'Buy', 'Sell', 'Color 1', 'Color 2', 'Size', 'Size Category', 'Surface', 'HHA Concept 1', 'HHA Concept 2', 'Catalog']].to_csv(r'newItems.csv', index = False)
"""