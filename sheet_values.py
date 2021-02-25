import pandas as pd
import math
import re

VersionAdded = ['1.0.0',
                '1.0.0',
                '1.0.0',
                '1.1.0',
                '1.2.0',
                '1.3.0',
                '1.4.0',
                '1.5.0',
                '1.6.0',
                '1.7.0',
                '1.8.0',
                '1.9.0']


def stripString(df):
    df['label'] = df['label'].map(lambda x: re.sub(r'[a-zA-Z_]*', '', x))
    return df


def getItemStrings():
    path = 'data/game_parsed/acnh-strings-usen/Item'
    # items = ['STR_ItemName_00_Ftr.csv', 'STR_ItemName_01_Art.csv', 'STR_ItemName_19_Umbrella.csv', 'STR_ItemName_20_Tool.csv', 'STR_ItemName_30_Insect.csv', 'STR_ItemName_31_Fish.csv', 'STR_ItemName_32_DiveFish.csv', 'STR_ItemName_33_Shell.csv', 'STR_ItemName_34_Fossil.csv', 'STR_ItemName_36_InsectToy.csv', 'STR_ItemName_37_FishToy.csv', 'STR_ItemName_40_Plant.csv', 'STR_ItemName_41_Turnip.csv', 'STR_ItemName_50_RoomWall.csv', 'STR_ItemName_51_RoomFloor.csv', 'STR_ItemName_52_RoomRug.csv', 'STR_ItemName_61_HouseDoorDeco.csv', 'STR_ItemName_62_HousePost.csv', 'STR_ItemName_70_Craft.csv', 'STR_ItemName_80_Etc.csv', 'STR_ItemName_81_Event.csv', 'STR_ItemName_82_Music.csv', 'STR_ItemName_83_Fence.csv', 'STR_ItemName_84_Bromide.csv', 'STR_ItemName_85_BridgeSlope.csv', 'STR_ItemName_86_Poster.csv', 'STR_ItemName_90_Money.csv', 'STR_ItemName_91_PhotoStudioList.csv']
    items = ['STR_ItemName_00_Ftr.csv', 'STR_ItemName_01_Art.csv', 'STR_ItemName_19_Umbrella.csv', 'STR_ItemName_20_Tool.csv', 'STR_ItemName_30_Insect.csv', 'STR_ItemName_31_Fish.csv', 'STR_ItemName_32_DiveFish.csv', 'STR_ItemName_33_Shell.csv', 'STR_ItemName_34_Fossil.csv', 'STR_ItemName_36_InsectToy.csv', 'STR_ItemName_37_FishToy.csv', 'STR_ItemName_40_Plant.csv', 'STR_ItemName_41_Turnip.csv', 'STR_ItemName_50_RoomWall.csv', 'STR_ItemName_51_RoomFloor.csv', 'STR_ItemName_52_RoomRug.csv', 'STR_ItemName_61_HouseDoorDeco.csv', 'STR_ItemName_62_HousePost.csv', 'STR_ItemName_70_Craft.csv', 'STR_ItemName_80_Etc.csv', 'STR_ItemName_81_Event.csv', 'STR_ItemName_82_Music.csv', 'STR_ItemName_83_Fence.csv', 'STR_ItemName_84_Bromide.csv', 'STR_ItemName_85_BridgeSlope.csv', 'STR_ItemName_86_Poster.csv']

    # Get object name strings
    itemSTR = pd.concat([pd.read_csv(f'{path}/{file}', dtype=object, sep=';') for file in items])

    # Remove object plural strings
    itemSTR = itemSTR[~itemSTR['label'].str.endswith('_pl').fillna('')]

    # Strip label to ID only and remove yucky chars from name string
    itemSTR = stripString(itemSTR)

    # Cast label to int64
    itemSTR = itemSTR.astype({'label': 'int64'})

    # Rename columns
    itemSTR.rename(columns={'English': 'Name_Items', 'label': 'Internal ID'}, inplace=True)

    return itemSTR


def getClothingStrings():
    path = 'data/game_parsed/acnh-strings-usen/Outfit/GroupName'
    clothing = ['STR_OutfitGroupName_Accessory.csv', 'STR_OutfitGroupName_Bag.csv', 'STR_OutfitGroupName_Bottoms.csv', 'STR_OutfitGroupName_Cap.csv', 'STR_OutfitGroupName_Helmet.csv', 'STR_OutfitGroupName_MarineSuit.csv', 'STR_OutfitGroupName_OnePiece.csv', 'STR_OutfitGroupName_Shoes.csv', 'STR_OutfitGroupName_Socks.csv', 'STR_OutfitGroupName_Tops.csv']

    # Get clothing name strings
    clothingSTR = pd.concat([pd.read_csv(f'{path}/{file}', dtype=object, sep=';') for file in clothing])
    
    # Strip label to ID only and remove yucky chars from name string
    clothingSTR = stripString(clothingSTR)

    # Cast label to int64
    clothingSTR = clothingSTR.astype({'label': 'int64'})

    # Rename column 'text' to 'Name'
    clothingSTR.rename(columns={'English': 'Name_Clothing', 'label' : 'ClothGroup ID'}, inplace=True)
    
    return clothingSTR


def filenameToClothGroup(item, sequence):
    options = [label for label in sequence.values() if item.startswith(label)]
    if not options:
        return ''
    return max(options, key=len)


def dividedBy20(row):
    if row['Filename'] == 'BellExchangeTicket':
        return 500
    return row['Buy'] / 20


def calculateNookMilesPrice(row):
    NookMilesFrom = ['Fence', 'MileExchangeLicense', 'MileExchangeNsoPresent', 'MileExchangeOnce', 'MileExchangePhoneCase', 'MileExchangePocket40', 'MileExchangeRecipe1', 'MileExchangeRecipe2', 'MileExchangeRecipe3', 'MileExchangeRecipe4', 'MileExchangeRecipe5', 'SonkatsuReward2', 'SonkatsuRewardShop', 'SonkatsuRewardTent']
    switcher = {
        0: (lambda x: 1000),
        1: dividedBy20,
        2: dividedBy20,
        3: dividedBy20,
        4: dividedBy20,
        5: dividedBy20,
        6: (lambda x: 800),
        7: (lambda x: 1500),
        8: (lambda x: 2000),
        9: (lambda x: 3000),
        10: (lambda x: 5000),
        11: dividedBy20,
        12: dividedBy20,
        13: dividedBy20
    }

    if row['ItemFrom'] not in NookMilesFrom:
        return ''
    func = switcher.get(NookMilesFrom.index(row['ItemFrom']), lambda: '')
    return func(row)


def labelNookMiles(row):
    if row['Exchange_NM'] == '':
        return ''
    return 'Nook Miles'


def labelJuneBride(row):
    if math.isnan(row['Exchange_HC']):
        return ''
    return 'Heart Crystals'


def wallpaperVFX(row):
    if row['ResName'].startswith(('\'RoomSpWall', '\'RoomSpFloor')):
        return 'Yes'
    return 'No'
