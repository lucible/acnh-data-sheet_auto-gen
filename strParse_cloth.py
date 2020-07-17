import pandas as pd
import re

def stripString(df):
    df['label'] = df['label'].map(lambda x: re.sub(r'[a-zA-Z_0]*', '', x))
    df['text'] = df['text'].map(lambda x: x.strip(' 	2\\0Ā촃Ȁ촃Ѐ촃촀'))
    return df

def getClothingStrings():
    clothing = ['STR_OutfitGroupName_Accessory.csv', 'STR_OutfitGroupName_Bag.csv', 'STR_OutfitGroupName_Bottoms.csv', 'STR_OutfitGroupName_Cap.csv', 'STR_OutfitGroupName_Helmet.csv', 'STR_OutfitGroupName_MarineSuit.csv', 'STR_OutfitGroupName_OnePiece.csv', 'STR_OutfitGroupName_Shoes.csv', 'STR_OutfitGroupName_Socks.csv', 'STR_OutfitGroupName_Tops.csv']

    # Get clothing name strings
    clothingSTR = pd.concat([pd.read_csv(f'data/string/outfit/groupname/{file}', dtype=object) for file in clothing])
    
    # Strip label to ID only and remove yucky chars from name string
    clothingSTR = stripString(clothingSTR)
    
    # Cast label to int64
    clothingSTR = clothingSTR.astype({'label': 'int64'})
    
    # Rename column 'text' to 'Name'
    clothingSTR.rename(columns={'text': 'Name', 'label' : 'UniqueID'}, inplace=True)
    
    return clothingSTR