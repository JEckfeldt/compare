import os

# Return list of files not matching certain size
# Also match the user agent

def getFiles(dir, excludeSize, userAgent):
    matchingFiles = []
    i = 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            filePath = os.path.join(root, file)
            # if file is valid, is not the normal size, and the userAgent is in filename
            if os.path.isfile(filePath) and os.path.getsize(filePath) != excludeSize and (userAgent in file):
                if file not in matchingFiles:
                    matchingFiles.append(filePath)
    
    return matchingFiles

path = '/home/xu/f5/testsite/json'
# userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__rv_125_0__Gecko_20100101_Firefox_125_0_'
userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_124_0_0_0_Safari_537_36'
size = 18

files = getFiles(path, size, userAgent)
print("Files with size not equal to 18 and has useragent: ")
for file in files:
    print(file)