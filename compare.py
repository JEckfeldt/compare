import os
import json

# Change to find different files
path = '/home/xu/f5/testsite/json'
userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__rv_125_0__Gecko_20100101_Firefox_125_0_'
size = 18

# Return list of files not matching certain size
# Also match the user agent
def getFiles(dir, excludeSize, userAgent):
    matchingFiles = []
    i = 0
    try:
        # Walk through the directory
        for root, dirs, files in os.walk(dir):
            for file in files:
                filePath = os.path.join(root, file)
                # if file is valid, is not the normal size, and the userAgent is in filename
                if os.path.isfile(filePath):
                    if os.path.getsize(filePath) != excludeSize and (userAgent in file):
                        if file not in matchingFiles:
                            matchingFiles.append(filePath)
    except Exception as e:
        print(f"Error: {e}")
    return matchingFiles

# get files that are different from the base
files = getFiles(path, size, userAgent)
print("Found ", len(files), " files\n")

# Get the base file to make comparisons
base = next((file for file in files if 'base' in file), None)
files.remove(base)
print('Base file: ', base)

# load the base json data and get the original fonts
with open(base) as jsonFile:
    data = json.load(jsonFile)
originalFonts = data['components']['fonts']['value']
originalSet = set(originalFonts)
print(originalSet)

results = {}


try:
    # Load file
    with open(files[27]) as json_file:
        data = json.load(json_file)
    # Check what we want exists
    if 'components' in data and 'fonts' in data['components'] and 'value' in data['components']['fonts']:
        # Get the new elements
        newFonts = [value['new'] for value in data['components']['fonts']['value'].values() if 'new' in value]
    else:
        print("Required keys not found in the JSON file.", file)
except Exception as e:
    print(f"Error: {e}")
for font in newFonts:
    if font not in originalSet:
        results[font] = results[font] + 1

print(results)