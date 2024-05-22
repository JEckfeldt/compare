import os
import json
import re
from datetime import datetime

# The f5 fonts we need
f5Fonts = [
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
userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__rv_125_0__Gecko_20100101_Firefox_125_0_'
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
    prevFileSize = None
    changes = []
    for file in files:
        if prevFileSize is not None and os.path.getsize(file) != prevFileSize:
            # print(file)
            # get the unstable attribute for the file and create a changes object
            changes.append(file)
        prevFileSize = os.path.getsize(file)

    return changes

# count what attributes are changed when the file size changes
def getChangedAttributes(files):
    changes = {}
    prevFileSize = None
    
    for file in files:
        if not os.path.exists(file):
            print("File not found")
            continue
        try:
            with open(file, 'r') as jsonFile:
                data = json.load(jsonFile)
        except json.JSONDecodeError:
            print(f"Error decoding file ${file}")
            continue
        # see what attributes are changing
        components = data.get("components", {})
        for value in components.keys():
            if value in changes:
                changes[value] += 1
            else:
                changes[value] = 1

    return changes

# get the fonts that are changing in the files
def getFonts(files):
    baseFonts = {}
    newFonts = {}
    testFonts = set(f5Fonts)
    uniqueOriginal = set()
    uniqueNew = set()
    uniqueFontLists = set()
    results = {}
    for file in files:
        try:
            # Load file
            with open(file) as json_file:
                data = json.load(json_file)
            # Check if the fonts are in the file (They changed)
            if 'components' in data and 'fonts' in data['components'] and 'value' in data['components']['fonts']:
                # Get the fonts
                for fontId, fontData in data['components']['fonts']['value'].items():
                    if "original" in fontData:
                        baseFonts[fontData["original"]] = baseFonts.get(fontData["original"], 0) + 1
                        uniqueOriginal.add(fontData["original"])
                    if "new" in fontData:
                        uniqueNew.add(fontData["new"])
                        newFonts[fontData["new"]] = newFonts.get(fontData["new"], 0) + 1
                # compare the fonts of current file, and log them
                uniqueChanged = uniqueNew ^ uniqueOriginal
                frozenUnique = frozenset(uniqueNew)
                uniqueFontLists.add(frozenUnique)
                for font in uniqueChanged:
                    results[font] = results.get(font, 0) + 1
                    results["changes"] = results.get("changes", 0) + 1 
                # clear the sets for the next file
                uniqueNew.clear()
                uniqueOriginal.clear()
                uniqueChanged.clear()

        except Exception as e:
            print(file)
            print(f"Error: {e}")

    return uniqueFontLists


# gets number of changes for userAgent
def findNumChanges():
    files = getAllFiles(path, userAgent)
    sortedFiles = sorted(files, key=extractDateTime)
    changedFiles = getChangedFiles(sortedFiles)
    print("UserAgent: ", userAgent)
    print("Files sorted: ", len(sortedFiles))
    print("Number of changes: ", len(changedFiles))
    print("Changes for Attributes: ", getChangedAttributes(sortedFiles))
    print("Changes for fonts: ", len(getFonts(sortedFiles)))

findNumChanges()


