import os
import json

# Change to find different files
path = '/home/xu/f5/testsite/json'
# Firefox windows
# userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__rv_125_0__Gecko_20100101_Firefox_125_0_'
# iPhone
# userAgent = 'Mozilla_5_0__iPhone__CPU_iPhone_OS_17_4_1_like_Mac_OS_X__AppleWebKit_605_1_15__KHTML__like_Gecko__Version_17_4_1_Mobile_15E148_Safari_604_1_'
userAgent = 'Mozilla_5_0__iPhone__CPU_iPhone_OS_17_4_like_Mac_OS_X__AppleWebKit_605_1_15__KHTML__like_Gecko__CriOS_124_0_6367_71_Mobile_15E148_Safari_604_1_'
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

# takes a list of filepaths gets the unstable fonts for firefox sheets
def getFonts(files):
    results = {}
    
    # Get the base file to make comparisons
    base = next((file for file in files if 'base' in file), None)
    if base is not None:
        files.remove(base)
    print("Base: ", base)

    # load the base json data and get the original fonts
    with open(base) as jsonFile:
        data = json.load(jsonFile)
    originalSet = set(data['components']['fonts']['value'])
    
    for file in files:
        try:
            # Load file
            with open(file) as json_file:
                data = json.load(json_file)
            # Check what we want exists
            if 'components' in data and 'fonts' in data['components'] and 'value' in data['components']['fonts']:
                # Get the new elements
                try:
                    newFonts = set([value['new'] for value in data['components']['fonts']['value'].values() if 'new' in value])
                except:
                    newFonts = []
                notShared = newFonts ^ originalSet
                for font in notShared:
                    if font in results:
                        results[font] += 1
                    else:
                        results[font] = 0
            else:
                print("Required keys not found in the JSON file.", file)
        except Exception as e:
            print(file)
            print(f"Error: {e}")
    return results

# Return a count of how many attributes are appearing unstable
def countUnstable(files):
    unstable = {} # result
    # remove the base from the list
    base = next((file for file in files if 'base' in file), None)
    if base is not None:
        files.remove(base)
        
    
    for file in files:
        if not os.path.exists(file):
            print("File not found")
            continue
        try:
            with open(file, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding file ${file}")
            continue
        # Count when we see something new 
        components = data.get("components", {})
        for value in components.keys():
            if value in unstable:
                unstable[value] += 1
            else:
                unstable[value] = 1

    return unstable

# get all unstable visits from useragent
files = getFiles(path, size, userAgent)
print("Found ", len(files), " files\n")

print(getFonts(files))

print(countUnstable(files))
