import sys
import string
import yaml
from bson.json_util import dumps
from yaml.loader import SafeLoader
from call_database import get_database

### read data from file path ###
def readFile(FilePath: str) -> str:
    result = ""
    with open(FilePath) as s :
        line = s.readlines()
        for data in line :
            data.replace("\t","____")
            result += data
    s.close()
    return result,line

### Collecting each character into dict ###
def CountAlPhaBet(word: str) -> dict:
    alphabet = string.ascii_lowercase
    count_cha = dict()
    for cha in word:
        if cha in alphabet :
            if cha not in count_cha:
                count_cha[cha] = 1
            else :
                count_cha[cha] += 1
    return count_cha

### Write text into new file from target path ###
def WriteFile(TargetPath,data : str):
    with open(TargetPath,'w') as t :
        for line in data:
            if len(line) > 1:
                t.writelines(line)
                print(line.replace("\n",""))
    t.close()

### Read data from database (MongoDB Only !!!!) ####
def ReadFromDB(schema,table : str) -> list:
    dbname = get_database(schema)
    collection_name = dbname[table]
    item_details = collection_name.find()
    return [item for item in item_details]


### Create json file ####
def CreateJSON(data,SavePath :str):
    with open(SavePath, "w") as f:
        for document in data:
            f.write(dumps(document) + "\n")


### Read config file ###
def ReadConfig(ConfigPath: str):
    with open(ConfigPath) as f:
        data = yaml.load(f, Loader=SafeLoader)
        source, target = data['SourcePath'], data['TargetPath']
        if data['DB']['enable']:
            schema = data['DB']['Schema']
            table = data['DB']['Table']
            jsonpath = data['DB']['JSONPath']
            collection = ReadFromDB(schema,table)
            CreateJSON(collection,jsonpath)
        else :
            Data,line = readFile(source)
            WriteFile(target,line)
            print(CountAlPhaBet(Data))
    return




if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print('Error Invalid argument')
    elif len(sys.argv) == 2 :
        ReadConfig(sys.argv[1])
    elif len(sys.argv) == 3 :
        source,target = sys.argv[1],sys.argv[2]
        data,line = readFile(source)
        WriteFile(target,line)
        print(CountAlPhaBet(data))
    elif len(sys.argv) == 5 :
        source,target,schema,table = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
        ReadFromDB(schema,table)
    else :
        print('Check your argument!!, something missing')