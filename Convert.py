import bz2
import os
import pickle
import json






DIRECTORY = "Games"
SAVEINDIRECTORY = "PositionData"

def DecompressFile(FilePath,OutputFile):
    print(f"DECOMPRESSING FILE {FilePath}")
    ReplayData = dict()
    with bz2.open(FilePath) as f:
        ReplayData = pickle.load(f)
    with open(OutputFile,"w") as f:
        JsonData = json.dumps(ReplayData)
        f.write(JsonData)
    return ReplayData




def SkimPositionalData(Data):
    SavedData = dict()
    NameRefList = dict()
    PlayerData = Data["players"]
    
    SavedData["sessionid"] = Data["sessionid"]
    SavedData["map_name"] = Data["map_name"]
    SavedData["framerate"] = Data["framerate"]
    SavedData["start_time"] = Data["start_time"]
    SavedData["players"] = Data["players"]



    PlayerPosData = dict()



    GameData = Data["data"]



    #Loop Through all the frames
    for frameData in GameData:
        teamData = frameData["teams"]
        for team in teamData:
            for player in team:
                playerID = str(player["id"])
                if playerID not in PlayerPosData:
                    PlayerPosData[playerID] = list()
                
                PlayerPosData[playerID].append(player["h"][0])


    SavedData["Data"] = PlayerPosData
    
    return SavedData


JsonData = dict()
for mapNam in os.listdir(DIRECTORY):
    for filename in os.listdir(f"{DIRECTORY}/{mapNam}"):
        Org = dict()
        if filename.endswith(".rawreplayv3"):
            Org = DecompressFile(os.path.join(f"{DIRECTORY}/{mapNam}", filename),"json.positionreplay")
            if Org['map_name'] == "mpl_combat_dyson" : mapSaveLocation = "dyson" 
            if Org['map_name'] == "mpl_combat_combustion" : mapSaveLocation = "combustion" 
            if Org['map_name'] == "mpl_combat_fission" : mapSaveLocation = "fission" 
            if Org['map_name'] == "mpl_combat_gauss" : mapSaveLocation = "surge"

        with open(f"{SAVEINDIRECTORY}/{mapSaveLocation}/{filename}.ecrs","w") as f:
            data = SkimPositionalData(Org)
            f.write(json.dumps(data))
        






