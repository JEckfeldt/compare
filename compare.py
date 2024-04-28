import os

# Return list of files not matching certain size
# Also match the user agent
def getFiles(dir, excludeSize, userAgent):
    matchingFiles = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            print(file)
            filePath = os.path.join(root, file)
            # if file is valid, is not the normal size, and the userAgent is in filename
            if os.path.isfile(filePath) and os.path.getsize(filePath != excludeSize) and (userAgent in file):
                matchingFiles.append(filePath)
    
    return matchingFiles

dir = '/home/xu/f5/testsite/json'
userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__rv_125_0__Gecko_20100101_Firefox_125_0_'
size = 18

files = getFiles(dir, size, userAgent)
print("Files with size not equal to", size, "bytes:")
for file in files:
    print(file)