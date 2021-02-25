import pandas as pd
import sheet_values as sv
import logging
import argparse
import math
import sys

columns_standard = ['FtrIcon',
					'ClosetIcon',
					'DIYRecipeIcon',
					'DIY',
                    'Stack Size',
                    'ItemKind',
                    'ItemFrom',
					'Buy',
					'Sell',
					'Color 1',
					'Color 2',
					'Size',
					'Size Category',
					'Surface',
					'Exchange Price',
					'Exchange Currency',
					'HHA Base Points',
					'HHA Concept 1',
					'HHA Concept 2',
					'HHA Series',
					'HHA Set',
					'Tag',
					'Catalog',
					'Version Added',
					'Filename',
					'Internal ID']

columns_wallpaper = ['VFX',
					 'VFX Type',
					 'Window Type',
					 'Window Color',
					 'Pane Type',
					 'Curtain Type',
					 'Curtain Color',
					 'Ceiling Type']

def prep_JuneBride(csv_path):
    # Import and prep Heart Crystal info
    juneBride = pd.read_csv(f'{csv_path}/CalendarEventJuneBrideExchange.csv')
    juneBride.drop(columns=['UniqueID', 'DispInteriorMode', 'JuneBrideProgress'], inplace=True)
    juneBride.rename(columns={'ExchangeItem': 'Internal ID', 'RequiredNum': 'Exchange_HC'}, inplace=True)
    return juneBride

def prep_ItemFrom(csv_path):
    itemFrom = pd.read_csv(f'{csv_path}/ItemFrom.csv')
    itemFrom.drop(columns=['Name', 'UniqueID'], inplace=True)
    itemFrom.rename(columns={'Label': 'ItemFrom', 'HHABaseScore': 'HHA Base Points'}, inplace=True)
    itemFrom['ItemFrom'] = itemFrom['ItemFrom'].map(lambda x: x.strip('\''))
    return itemFrom

def prep_ItemKind(csv_path):
    itemKind = pd.read_csv(f'{csv_path}/ItemKind.csv')
    itemKind.drop(columns=['Name', 'UniqueID'], inplace=True)
    itemKind.rename(columns={'Label': 'ItemKind', 'MultiHoldMaxNum': 'Stack Size'}, inplace=True)
    itemKind['ItemKind'] = itemKind['ItemKind'].map(lambda x: x.strip('\''))
    return itemKind

def prep_RoomWallParam(csv_path):
    roomWallParam = pd.read_csv(f'{csv_path}/RoomWallParam.csv')
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

    return roomWallParam

def build_item_list(yes_strings_mm_baby):
    csv_path = './data/game_parsed/csv'

    ItemParam = pd.read_csv(f'{csv_path}/ItemParam.csv', low_memory = False)

    logging.info(ItemParam.shape)

    ItemParam.rename(columns={'UniqueID': 'Internal ID', 'Label': 'Filename', 'Price': 'Buy'}, inplace=True)

    ItemParam['Filename'] = ItemParam['Filename'].map(lambda Filename: Filename.strip('\''))

    logging.info(ItemParam.shape)

    # Import ItemClothGroup & normalize data
    clothGroup = pd.read_csv(f'{csv_path}/ItemClothGroup.csv')
    clothGroup['Label'] = clothGroup['Label'].map(lambda label: label.strip('\''))
    clothGroup.rename(columns={'UniqueID': 'ClothGroup ID', 'Label': 'Label_ClothGroup', 'Name': 'Name_CG'}, inplace=True)

    if yes_strings_mm_baby is True:
        # Merge ItemClothGroup with clothing strings
        clothSTR = sv.getClothingStrings()
        clothGroup = clothGroup.merge(clothSTR, on='ClothGroup ID', how='left')
        clothGroup.replace({'Label_ClothGroup': {'ShoesKneeEngineerboots_': 'ShoesKneeEngineerboots',
                                                'TopsTexTopCoatLPoncho': 'TopsTexTopCoatLPompom',
                                                'TopsTexTopCoatHWorkapron': 'TopsTexTopCoatLWorkapron',
                                                'TopsTexTopCoatHDiner': 'TopsTexTopCoatLDiner',
                                                'TopsTexOnepieceBlongLHippie': 'TopsTexTopCoatLPoncho'}}, inplace=True)

    # Prep for merge by creating Label_ClothGroup column from Filename column
    ItemParam['Label_ClothGroup'] = ItemParam['Filename'].apply(sv.filenameToClothGroup, args=(clothGroup['Label_ClothGroup'],))

    # Merge ItemParam with ItemClothGroup (aka clothing strings etc)
    ItemParam = ItemParam.merge(clothGroup, left_on='Label_ClothGroup', right_on='Label_ClothGroup', how='left')

    if yes_strings_mm_baby is True:
        # Merge item strings into ItemParam
        itemSTR = sv.getItemStrings()
        ItemParam = ItemParam.merge(itemSTR, on='Internal ID', how='left')

        # Fill NaN with empty string & merge into single Name column
        ItemParam[['Name_Clothing', 'Name_Items']] = ItemParam[['Name_Clothing', 'Name_Items']].fillna('')
        ItemParam['Name'] = ItemParam['Name_Clothing'].astype(str) + ItemParam['Name_Items'].astype(str)

    logging.info(ItemParam.shape)

    # FtrIcon / Storage Image
    ItemParam['FtrIcon'] = ItemParam['Filename'].map(lambda x: f'=IMAGE("https://acnhcdn.com/latest/FtrIcon/{x}.png")')

    # ClosetIcon / Closet Image
    ItemParam['ClosetIcon'] = ItemParam['Filename'].map(lambda x: f'=IMAGE("https://acnhcdn.com/latest/ClosetIcon/{x}.png")')

    # DIYRecipeIcon / DIY Recipe Image
    ItemParam['DIYRecipeIcon'] = ItemParam['Filename'].map(lambda x: f'=IMAGE("https://acnhcdn.com/latest/DIYRecipeIcon/{x}.png")')

    # DIY
    ItemParam['DIY'] = ItemParam['CaptureDiyIcon'].map(lambda x: 'Yes' if x == 1 else 'No')

    logging.info(ItemParam.shape)

    # Sell
    ItemParam['Sell'] = ItemParam['Buy'].map(lambda price: math.floor(price * 0.25))

    logging.info(ItemParam.shape)

    # Color 1 / Color 2
    ItemParam = ItemParam.replace({'Color1': 'LightBlue', 'Color2': 'LightBlue'}, 'Aqua')
    ItemParam.rename(columns={'Color1': 'Color 1', 'Color2': 'Color 2'}, inplace=True)

    logging.info(ItemParam.shape)

    # Size & Size Category
    size = pd.read_csv('data/sheet-values/Size.csv')
    ItemParam = ItemParam.merge(size, on='ItemSize')

    logging.info(ItemParam.shape)

    # Surface
    surface = pd.read_csv('data/sheet-values/Surface.csv')
    ItemParam = ItemParam.merge(surface, on='ItemLayout')

    logging.info(ItemParam.shape)

    # HHA Concept 1
    situation1 = pd.read_csv('data/sheet-values/HHASituation1.csv')
    ItemParam = ItemParam.merge(situation1, on='ItemHHASituation1', how='left')

    logging.info(ItemParam.shape)

    # HHA Concept 2
    situation2 = pd.read_csv('data/sheet-values/HHASituation2.csv')
    ItemParam = ItemParam.merge(situation2, on='ItemHHASituation2', how='left')

    logging.info(ItemParam.shape)

    # HHA Series
    hhaSeries = pd.read_csv('data/sheet-values/HHATheme.csv')
    ItemParam = ItemParam.merge(hhaSeries, on='ItemHHATheme', how='left')

    logging.info(ItemParam.shape)

    # HHA Set
    hhaSet = pd.read_csv('data/sheet-values/HHASet.csv')
    ItemParam = ItemParam.merge(hhaSet, on='ItemHHASet', how='left')

    logging.info(ItemParam.shape)

    # Tag
    tag = pd.read_csv('data/sheet-values/Tag.csv')
    ItemParam = ItemParam.merge(tag, on='ItemUIFurnitureCategory', how='left')

    logging.info(ItemParam.shape)

    # Catalog
    catalog = pd.read_csv('data/sheet-values/Catalog.csv')
    ItemParam = ItemParam.merge(catalog, on='ItemCatalogType')

    logging.info(ItemParam.shape)

    # Version Added
    version_added = pd.Series(sv.VersionAdded)
    ItemParam = ItemParam.merge(version_added.rename('Version Added'), left_on='ItemReleaseVersion', right_index=True)

    logging.info(ItemParam.shape)

    # Nook Miles Exchange & Currency columns
    ItemParam['Exchange_NM'] = ItemParam.apply(sv.calculateNookMilesPrice, axis=1)
    ItemParam['Currency_NM'] = ItemParam.apply(sv.labelNookMiles, axis=1)

    # Heart Crystals Exchange & Currency columns
    ItemParam = ItemParam.merge(prep_JuneBride(csv_path), on='Internal ID', how='left')
    ItemParam['Currency_HC'] = ItemParam.apply(sv.labelJuneBride, axis=1)

    # Fill NaN with empty string
    ItemParam[['Exchange_NM', 'Exchange_HC', 'Currency_NM', 'Currency_HC']] = ItemParam[['Exchange_NM', 'Exchange_HC', 'Currency_NM', 'Currency_HC']].fillna('')

    # Merge Nook Miles & Heart Crystals into Exchange & Exchange Currency columns
    ItemParam['Exchange Price'] = ItemParam['Exchange_NM'].astype(str) + ItemParam['Exchange_HC'].astype(str)
    ItemParam['Exchange Currency'] = ItemParam['Currency_NM'].astype(str) + ItemParam['Currency_HC'].astype(str)
    ItemParam[['Exchange Price', 'Exchange Currency']] = ItemParam[['Exchange Price', 'Exchange Currency']].replace(r'^\s*$', 'NA', regex=True)

    logging.info(ItemParam.shape)

    # HHA Base Points column
    ItemParam = ItemParam.merge(prep_ItemFrom(csv_path), on='ItemFrom', how='left')

    logging.info(ItemParam.shape)

    # Stack Size column
    # TO DO: complete this??
    ItemParam = ItemParam.merge(prep_ItemKind(csv_path), on='ItemKind', how='left')

    logging.info(ItemParam.shape)

    # VFX (Wallpaper)
    ItemParam['VFX'] = ItemParam.apply(sv.wallpaperVFX, axis=1)

    # VFX Type, Window Type, etc
    ItemParam = ItemParam.merge(prep_RoomWallParam(csv_path), on='Internal ID', how='left')

    logging.info(ItemParam.shape)

    # Stack Size
    # TO DO: complete this??

    logging.info('Item Table Completed.')
    return ItemParam

def write_to_csv(yes_strings_mm_baby, no_write, version):
    if yes_strings_mm_baby is True:
        columns_standard.insert(0, 'Name')

    columns_standard.insert(0, 'ItemUICategory')

    columns = columns_standard + columns_wallpaper

    print('Building full item list...')

    full_list = build_item_list(yes_strings_mm_baby)
    
    print('Full item list built!')

    if version:
        final_list = full_list[full_list['Version Added']==version].copy()
        final_list = final_list[columns]
        
        if no_write:
            final_list.to_csv(f'./output/NewItems_v{version}.csv', index = False)
            print(f'Item list written to ./output/NewItems_v{version}.csv')
    else:
        final_list = full_list[columns]

        if no_write:
            final_list.to_csv(r'./output/ACNH-Item-List.csv', index = False)
            print('Item list written to ./output/ACNH-Item-List.csv')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument('-ns', '--no-strings', dest='strings', action='store_false', help='creates an item table without referencing the string files')
    parser.add_argument('-nw', '--no-write', dest='no_write', action='store_false', help='disables writing item table to file')
    parser.add_argument('-u', '--update', dest='update', type=str, help='creates an item table with only the items from the specified update')
    parser.set_defaults(strings=True, no_write=True, update=False)

    args = parser.parse_args()

    write_to_csv(args.strings, args.no_write, args.update)

    print('Script has finished running.')
