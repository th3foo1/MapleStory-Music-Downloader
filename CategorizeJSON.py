import os
import json
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askdirectory
from collections import defaultdict

def jsonParse(jsonFiles, outputFolder):
    # Create a dictionary to hold the data
    categorziedData = defaultdict(list)

    # Loop through all JSON files
    for jsonFile in jsonFiles:
        
        # Read and open JSON file
        with open(jsonFile, 'r') as file:
            data = json.load(file)

        # Check if the data is single object
        if isinstance(data, dict):
            data = [data]

        for entry in data:
            mapName = entry.get("mark")
            categorziedData[mapName].append(entry)

    # Output each category to its own JSON file
    for mark, entries in categorziedData.items():
        outputFilename = f'{mark}.json'
        
        with open(os.path.join(outputFolder, outputFilename), 'w') as outputFile:
            json.dump(entries, outputFile, indent=4)
    
    


if __name__ == '__main__':
    print('Please choose the JSON file(s):')
    jsonFile = askopenfilenames()
    
    print('Please choose the destination folder:')
    outputFolder = askdirectory()
    jsonParse(jsonFile, outputFolder)