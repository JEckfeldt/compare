import os
import json
import re
from datetime import datetime

# The f5 fonts we need
fonts = [
  'Andale Mono', 'Arial Narrow', 'Arial Unicode MS', 'Batang', 'Bell MT', 'Brush Script', 'Brush Script MT', 'Calibri', 'Charter', 'Courier', 'Courier New',
  'Curlz MT',
  'DejaVu Sans',
  'DejaVu Sans Mono',
  'DejaVu Serif Condensed',
  'Droid Sans',
  'Droid Sans Fallback',
  'Droid Serif',
  'Forte',
  'Futura',
  'Geneva',
  'Hei',
  'Leelawadee',
  'Levenim MT',
  'Liberation Sans',
  'Liberation Sans Narrow',
  'Marlett',
  'Meiryo UI',
  'Microsoft Uighur',
  'Microsoft YaHei UI',
  'MS Mincho',
  'MS UI Gothic',
  'NanumGothic',
  'Nirmala UI',
  'Palatino',
  'Papyrus',
  'PMingLiU',
  'PT Serif',
  'SimHei',
  'STIXVariants',
  'STSong',
  'Traditional Arabic',
  'Urdu Typesetting',
  'Verdana',
  'Wingdings',
  'Wingdings 3',
  'Helkevtrica',
]

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
# userAgent = 'Mozilla_5_0__Macintosh__Intel_Mac_OS_X_10_15_7__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_124_0_0_0_Safari_537_36_'
# Firefox
userAgent = 'Mozilla_5_0__Macintosh__Intel_Mac_OS_X_10_15__rv_125_0__Gecko_20100101_Firefox_125_0_'

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


# Define a function to extract the date and time from the file name
def extractDateTime(file_name):
    match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})', file_name)
    if match:
        return datetime.strptime(match.group(), '%Y-%m-%dT%H-%M-%S')
    else:
        return datetime.min  # Default value if date is not found 

# get the first 10000 files from a list matching a userAgent (Minus the base)
def getAllFiles(dir, userAgent):
    matching = []
    limit = 1
    try:
        # Get all files with useragent
        for root, dirs, files, in os.walk(dir):
            for file in files:
                filePath = os.path.join(root, file)
                if os.path.isfile(filePath):
                    if userAgent in file and 'base' not in file and limit <= 10000:
                        matching.append(filePath)
                        limit = limit + 1
    except Exception as e:
        print(f"Error: {e}")
    return matching

# Return list of files not matching certain size
def getUnstableFiles(dir, excludeSize, userAgent):
    matchingFiles = []
    i = 1
    try:
        # Walk through the directory
        for root, dirs, files in os.walk(dir):
            for file in files:
                filePath = os.path.join(root, file)
                # if file is valid, is not the normal size, and the userAgent is in filename
                if os.path.isfile(filePath):
                    if os.path.getsize(filePath) != excludeSize and (userAgent in file) and 'base' not in file and i <= 10000:
                        if file not in matchingFiles:
                            matchingFiles.append(filePath)
                            i = i + 1   

    except Exception as e:
        print(f"Error: {e}")
    return matchingFiles

# count how many times the file size changed
def getChangedFiles(files):
    numChanges = 0
    prevFileSize = None
    
    for file in files:
        if prevFileSize is not None and os.path.getsize(file) != prevFileSize:
            # print(file)
            # get the unstable attribute for the file and create a changes object
            numChanges = numChanges + 1
        prevFileSize = os.path.getsize(file)

    return numChanges

# count how many times attributes are changed in a file
def getChangedAttributes(files):
    changes = {}
    prevFileSize = None
    
    for file in files:
        # print(file)
        if prevFileSize is not None and os.path.getsize(file) != prevFileSize:
            # print(file)
            # get the unstable attribute for the file and create a changes object
            if not os.path.exists(file):
                print("File not found")
                continue
            try:
                with open(file, 'r') as jsonFile:
                    data = json.load(jsonFile)
            except json.JSONDecodeError:
                print(f"Error decoding file ${file}")
                continue
            # Count when we see something new 
            components = data.get("components", {})
            for value in components.keys():
                if value in changes:
                    changes[value] += 1
                else:
                    changes[value] = 1

        prevFileSize = os.path.getsize(file)

    return changes

# gets the unstable fonts for firefox sheets
def getFonts(files):
    results = {}

    for file in unstableFiles:
        try:
            # Load file
            with open(file) as json_file:
                data = json.load(json_file)
            # Check what we want exists
            if 'components' in data and 'fonts' in data['components'] and 'value' in data['components']['fonts']:
                # Get the new elements
                newFonts = set([value['new'] for value in data['components']['fonts']['value'].values() if 'new' in value])
                baseFonts set([value['original'] for value in data['components']['fonts']['value'].values() if 'original' in value])
                notShared = newFonts ^ baseFonts
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
                # print(file)
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
        if 'components' in data and 'canvas' in data['components'] and 'value' in data['components']['canvas'] and 'text' in data['components']['canvas']['value']:
            uniques.add(data['components']['canvas']['value']['text']['new'])
                
    return uniques


# # get all unstable visits from useragent
# files = getFiles(path, size, userAgent)
# print("Found ", len(files), " files\n")

# gets number of changes for userAgent
def findNumChanges():
    files = getAllFiles(path, userAgent)
    sorted_file_names = sorted(files, key=extractDateTime)
    print("UserAgent: ", userAgent)
    print("Files sorted: ", len(sorted_file_names))
    print("Number of changes: ", getChangedFiles(sorted_file_names))
    print("Unstable Attributes: ", countUnstable(getUnstableFiles(path, size, userAgent)))
    print("Changes for Unstable Attributes: ", getChangedAttributes(sorted_file_names))
    print("Changes for fonts: ", getFonts(sorted_file_names))

findNumChanges()

# def compareWindowsEdg():
#     windowsFiles = getAllFiles(path, 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_124_0_0_0_Safari_537_36_Edg_124_0_0_0_', True)
#     chromeFiles = getAllFiles(path, 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_124_0_0_0_Safari_537_36', False)
#     combined = windowsFiles + chromeFiles
#     print("combined len: ", len(combined))
#     sortedCombined = sorted(combined, key=extractDateTime)
#     print("Number of changes: ", getChangedFiles(sortedCombined))
#     print("Changes for Unstable Attributes: ", getChangedAttributes(sortedCombined))
# compareWindowsEdg()

