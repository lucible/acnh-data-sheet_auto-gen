import pandas as pd
import re

def stripString(df):
    df['label'] = df['label'].map(lambda x: re.sub(r'[a-zA-Z_0]*', '', x))
    df['text'] = df['text'].map(lambda x: x.strip(' 	2\\0Ā촃Ȁ촃Ѐ촃촀'))
    return df

def getInGameNames():
    items = ['STR_ItemName_00_Ftr.csv', 'STR_ItemName_01_Art.csv', 'STR_ItemName_15_Cap.csv', 'STR_ItemName_19_Umbrella.csv', 'STR_ItemName_20_Tool.csv', 'STR_ItemName_30_Insect.csv', 'STR_ItemName_31_Fish.csv', 'STR_ItemName_32_DiveFish.csv', 'STR_ItemName_33_Shell.csv', 'STR_ItemName_34_Fossil.csv', 'STR_ItemName_36_InsectToy.csv', 'STR_ItemName_37_FishToy.csv', 'STR_ItemName_40_Plant.csv', 'STR_ItemName_41_Turnip.csv', 'STR_ItemName_50_RoomWall.csv', 'STR_ItemName_51_RoomFloor.csv', 'STR_ItemName_52_RoomRug.csv', 'STR_ItemName_61_HouseDoorDeco.csv', 'STR_ItemName_62_HousePost.csv', 'STR_ItemName_70_Craft.csv', 'STR_ItemName_80_Etc.csv', 'STR_ItemName_81_Event.csv', 'STR_ItemName_82_Music.csv', 'STR_ItemName_83_Fence.csv', 'STR_ItemName_84_Bromide.csv', 'STR_ItemName_85_BridgeSlope.csv', 'STR_ItemName_86_Poster.csv', 'STR_ItemName_90_Money.csv', 'STR_ItemName_91_PhotoStudioList.csv']
    clothing = ['STR_OutfitGroupName_Accessory.csv', 'STR_OutfitGroupName_Bag.csv', 'STR_OutfitGroupName_Bottoms.csv', 'STR_OutfitGroupName_Cap.csv', 'STR_OutfitGroupName_Helmet.csv', 'STR_OutfitGroupName_MarineSuit.csv', 'STR_OutfitGroupName_OnePiece.csv', 'STR_OutfitGroupName_Shoes.csv', 'STR_OutfitGroupName_Socks.csv', 'STR_OutfitGroupName_Tops.csv']

    # Get object name strings
    itemGroup = pd.concat([pd.read_csv(f'data/string/item/{file}', dtype=object) for file in items])

    # Get clothing name strings
    clothingGroup = pd.concat([pd.read_csv(f'data/string/outfit/groupname/{file}', dtype=object) for file in clothing])

    # Remove object plural strings
    itemGroup.drop(itemGroup[itemGroup['label'].str.endswith('_pl').fillna(True)].index, inplace=True)

    # print(itemGroup.shape)
    # print(clothingGroup.shape)
    
    # Merge object & clothing name tables
    gameSTR = pd.concat([itemGroup, clothingGroup])

    # print(gameSTR.shape)
    
    # Strip label to ID only and remove yucky chars from name string
    gameSTR = stripString(gameSTR)
    
    # Cast label to int64
    gameSTR = gameSTR.astype({'label': 'int64'})
    
    # Rename column 'text' to 'Name'
    gameSTR.rename(columns={'text': 'Name'}, inplace=True)
    
    return gameSTR