import pandas as pd

# Load in dataset
data = pd.read_csv("data/original_dataset.csv", sep=";")

# Remove all rows with Populatie = 20100
data.drop(data[data.Populatie == 20100].index, inplace=True)
# Drop populatie column
data.drop('Populatie', axis=1, inplace=True)
# Drop total columns
data = data[~data.Vervoerwijzen.str.contains("T")]
data = data[~data.Reismotieven.str.contains("T")]

# rename columns to convenient names
data.rename(columns={"ID": "id", "Vervoerwijzen": "vervoerwijzen", "Reismotieven": "reismotieven", 
"RegioS": "regio", "Perioden": "jaar", "Verplaatsingen_1": "verplaatsingen1", "Afstand_2": "afstand2", 
"Reisduur_3": "reisduur3", "Afstand_4": "afstand4", "ReisduurPerVerplaatsing_5": "reisduurPerVerplaatsing5",
"Verplaatsingen_6": "verplaatsingen6", "Afstand_7": "afstand7", "Reisduur_8": "reisduur8"}, inplace=True)

# Replace keys
# Get the keys we want to replace the values of: Vervoerwijzen, Reismotieven, RegioS, Perioden
columns = data.columns[1:5].tolist()

for column in columns:
    column_str = str(column)
    file_name = "data/" + column_str + ".csv"
    meta_data = pd.read_csv(file_name, sep=";")
    # Drop the total row in the meta data (contains "T")
    meta_data = meta_data[~meta_data.Key.str.contains("T")]


    for index, row in data.iterrows():
        # Check if the data row contains a key of the metadata
        if str(row[column_str]) in meta_data['Key'].tolist():
            # find the row index of the meta
            row_index = meta_data.index[meta_data['Key'] == str(row[column_str])].tolist()
            # select the row with the index found
            meta = meta_data.loc[row_index]['Title'].tolist()
            # Replace the key with the value
            data.at[index, column_str] = meta[0]

print(data)

data.to_csv("data/dataset.csv")
