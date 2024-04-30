import os
import json

# Dir Path to search
path = '/home/xu/f5/testsite/json'
size = 18 # file size to exclude

# Windows
# Firefox
# userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__rv_125_0__Gecko_20100101_Firefox_125_0_'
# Edge
# userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_124_0_0_0_Safari_537_36_Edg_124_0_0_0_'
# Chrome
# userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_124_0_0_0_Safari_537_36'
# userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_123_0_0_0_Safari_537_36'

# Macbook (Macintosh)
# Safari
# userAgent = 'Mozilla_5_0__Macintosh__Intel_Mac_OS_X_10_15_7__AppleWebKit_605_1_15__KHTML__like_Gecko__Version_16_4_Safari_605_1_15_'
# Chrome
userAgent = 'Mozilla_5_0__Macintosh__Intel_Mac_OS_X_10_15_7__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_124_0_0_0_Safari_537_36_'
# Firefox
# userAgent = 'Mozilla_5_0__Macintosh__Intel_Mac_OS_X_10_15__rv_125_0__Gecko_20100101_Firefox_125_0_'

# iPhone
# Safari
# userAgent = 'Mozilla_5_0__iPhone__CPU_iPhone_OS_17_4_1_like_Mac_OS_X__AppleWebKit_605_1_15__KHTML__like_Gecko__Version_17_4_1_Mobile_15E148_Safari_604_1_'
# Chrome
# userAgent = 'Mozilla_5_0__iPhone__CPU_iPhone_OS_17_4_like_Mac_OS_X__AppleWebKit_605_1_15__KHTML__like_Gecko__CriOS_124_0_6367_71_Mobile_15E148_Safari_604_1_'
# userAgent = 'Mozilla_5_0__iPhone__CPU_iPhone_OS_17_4_like_Mac_OS_X__AppleWebKit_605_1_15__KHTML__like_Gecko__CriOS_124_0_6367_88_Mobile_15E148_Safari_604_1_'
# Firefox
# userAgent = 'Mozilla_5_0__iPhone__CPU_iPhone_OS_17_4_1_like_Mac_OS_X__AppleWebKit_605_1_15__KHTML__like_Gecko__FxiOS_125_2__Mobile_15E148_Safari_605_1_15_'

# Android
# Firefox
# userAgent = 'Mozilla_5_0__Android_12__Mobile__rv_82_0__Gecko_82_0_Firefox_82_0_'
# Chrome
# userAgent = 'Mozilla_5_0__Linux__Android_12__Pixel_3a__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_95_0_4638_74_Mobile_Safari_537_36_'

# Linux
# Chrome
# userAgent = 'Mozilla_5_0__X11__Linux_x86_64__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_124_0_0_0_Safari_537_36_'
# Firefox
# userAgent = 'Mozilla_5_0__X11__Ubuntu__Linux_x86_64__rv_125_0__Gecko_20100101_Firefox_125_0_'

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
        unstableFiles = [file for file in files if 'base' not in file]
        print("Unstable items: ", len(unstableFiles), '\n')
        print("Base: ", base)
        

    # load the base json data and get the original fonts
    with open(base) as jsonFile:
        baseData = json.load(jsonFile)
    originalSet = set(baseData['components']['fonts']['value'])

    for file in unstableFiles:
        try:
            # Load file
            with open(file) as json_file:
                data = json.load(json_file)
            # Check what we want exists
            if 'components' in data and 'fonts' in data['components'] and 'value' in data['components']['fonts']:
                # Get the new elements
                newFonts = set([value['new'] for value in data['components']['fonts']['value'].values() if 'new' in value])
                notShared = newFonts ^ originalSet
                for font in notShared:
                    if font in results:
                        results[font] += 1
                    else:
                        results[font] = 1
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
        unstableFiles = [file for file in files if 'base' not in file]
        print("Unstable items: ", len(unstableFiles), '\n')
        print("Base: ", base)
        
    
    for file in unstableFiles:
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
                print(file)
                unstable[value] = 1

    return unstable

# Return the number of unique values per unstable attribute
def countUniqueUnstable(files):
    uniques = set()
    # remove the base from the list
    base = next((file for file in files if 'base' in file), None)
    if base is not None:
        unstableFiles = [file for file in files if 'base' not in file]
        print("Unstable items: ", len(unstableFiles), '\n')
        print("Base: ", base)
    # Iterate through the files
    for file in unstableFiles:
        if not os.path.exists(file):
            print("File not found")
            continue
        try:
            with open(file, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding file ${file}")
            continue
        if 'components' in data and 'architecture' in data['components'] and 'value' in data['components']['architecture'] and 'new' in data['components']['architecture']['value']:
            uniques.add(data['components']['architecture']['value']['new'])
                
    return uniques


# get all unstable visits from useragent
files = getFiles(path, size, userAgent)
print("Found ", len(files), " files\n")

# f = getFonts(files)
# print(f)
# print(len(f))

print(countUnstable(files))

print(countUniqueUnstable(files))