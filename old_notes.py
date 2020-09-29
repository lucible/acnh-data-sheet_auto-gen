# Add empty columns to match spreadsheet
# ItemParam['Source Notes'] = ''
# ItemParam['Version Unlocked'] = ''
# ItemParam['Unique Entry ID'] = ''
# ItemParam['Stack Size'] = ''

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
"""
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

##################################
## CONSTRUCT FENCING DATA FRAME ##
##################################

fencing = ItemParam[ItemParam['ItemKind']=='Fence'].copy()

fencing.rename(columns={'FtrIcon': 'Image'}, inplace=True)

tab_fencing = ['Name', 'Image', 'DIY', 'Stack Size', 'Buy', 'Sell', 'ItemFrom', 'Source Notes',
			   'Version Added', 'Version Unlocked', 'Filename', 'Internal ID', 'Unique Entry ID']

fencing_final = pd.concat([fencing.pop(item) for item in tab_fencing], axis=1)
fencing_final.sort_values(by=['Name'], inplace=True)

# fencing_final.to_csv(r'Fencing.csv', index=False)

##################################
## CONSTRUCT RECIPES DATA FRAME ##
##################################

recipes = ItemParam[ItemParam['DIY']=='Yes'].copy()

recipes.rename(columns={'DIYRecipeIcon': 'Image', 'Internal ID': 'Crafted Item Internal ID'}, inplace=True)

tab_recipes = ['Name', 'Image', 'Version Added', 'Crafted Item Internal ID', 'Filename']

recipes_final = pd.concat([recipes.pop(item) for item in tab_recipes], axis=1)
recipes_final.sort_values(by=['Name'], inplace=True)

# recipes_final.to_csv(r'Recipes.csv', index=False)
"""
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

"""