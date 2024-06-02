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

# UserAgents

# Windows/Chrome
# userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_125_0_0_0_Safari_537_36_'
# Windows/Firefox
userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__rv_125_0__Gecko_20100101_Firefox_125_0_'

# Android/Chrome
# userAgent = 'Mozilla_5_0__Linux__Android_10__K__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_125_0_0_0_Mobile_Safari_537_36_'

# Dir Path to search
path = '/home/xu/f5/fpCollector/json'

# File Limit
fileLimit = 6000


# Define a function to extract the date and time from the file name
def extractDateTime(file_name):
    match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})', file_name)
    if match:
        return datetime.strptime(match.group(), '%Y-%m-%dT%H-%M-%S')
    else:
        return datetime.min  # Default value if date is not found 

# Function to recursively search for "original" and "new" values
def find_original_and_new(obj):
    if isinstance(obj, dict):
        if 'original' in obj:
            return obj['original'], obj.get('new')
        for value in obj.values():
            original, new = find_original_and_new(value)
            if original is not None:
                return original, new
    elif isinstance(obj, list):
        for item in obj:
            original, new = find_original_and_new(item)
            if original is not None:
                return original, new
    return None, None

# get the first 10000 files from a list matching a userAgent (Minus the base)
def getAllFiles(dir, userAgent, isChrome):
    matching = []
    limit = 1
    try:
        # Get all files with useragent
        for root, dirs, files, in os.walk(dir):
            for file in files:
                filePath = os.path.join(root, file)
                if os.path.isfile(filePath):
                    if isChrome:
                        if userAgent in file and 'base' not in file and limit <= fileLimit and 'Edg' not in file:
                            matching.append(filePath)
                            limit = limit + 1
                    else:
                        if userAgent in file and 'base' not in file and limit <= fileLimit:
                            matching.append(filePath)
                            limit = limit + 1
    except Exception as e:
        print(f"Error: {e}")
    return matching

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
        if 'components' in data:
            components = data.get("components", {})
            for value in components.keys():
                if value in changes:
                    changes[value] += 1
                    # print(value, file)
                else:
                    print(value, file)
                    changes[value] = 1
    return changes

# get the fonts that are changing in the files
def getFonts(files):
    originalLen = 0

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
                if (len(uniqueOriginal) > originalLen):
                    originalLen = len(uniqueOriginal)
                frozenUnique = frozenset(uniqueNew)
                frozenOriginal = frozenset(uniqueOriginal)
                uniqueFontLists.add(frozenUnique)
                uniqueFontLists.add(frozenOriginal)
                for font in uniqueChanged:
                    results[font] = results.get(font, 0) + 1
                # clear the sets for the next file
                uniqueNew.clear()
                uniqueOriginal.clear()
                uniqueChanged.clear()

        except Exception as e:
            print(file)
            print(f"Error: {e}")
    sorted_dict = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    return originalLen

def getUniqueValues(files):
    uniques = {}
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
        if "components" in data:
            components = data.get("components", {})
            for component, value in components.items():
                original, new = find_original_and_new(value)
                uniques.setdefault(component, set()).add(original)
                uniques.setdefault(component, set()).add(new)

                
    return uniques

def getUniqueVisitorIds(files):
    uniques = set()
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
        if "visitorId" in data:
            uniques.add(data["visitorId"]["original"])
            uniques.add(data["visitorId"]["new"])


                
    return uniques


# gets number of changes for userAgent
def findNumChanges():
    files = getAllFiles(path, userAgent, False)
    sortedFiles = sorted(files, key=extractDateTime)
    changedFiles = getChangedFiles(sortedFiles)
    print("UserAgent: ", userAgent)
    print("Files sorted: ", len(sortedFiles))
    print("Number of changes: ", changedFiles)

findNumChanges()


 