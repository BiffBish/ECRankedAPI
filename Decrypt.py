import bz2
import pickle
import os
import json






def InMap(Pos,Map):
    if Pos[0] < Map[0][0] or Pos[0] > Map[0][1] or Pos[2] < Map[1][0] or Pos[2] > Map[1][1]:
        return False
    return True

def CaculateDeaths(Data):
    DeathTotal = dict()
    TotalDeaths = 0
    MapSize = [[-50,50],[-30,40]]
    print("Caculating Deaths")
    NameRefList = dict()
    PlayerData = Data["players"]
    print(f"There are {len(PlayerData)} Players")

    #Player data is a Dict
    for key, value in PlayerData.items():
        PlayerID = value["playerID"]
        UserName = value["name"]
        NameRefList[str(PlayerID)] = UserName
        DeathTotal[str(PlayerID)] = 0
    

    GameData = Data["data"]
    print(f"There are {len(GameData)} Frames")
 
    PlayerPosition = dict()
    PrevPosition = ""
    print()


    #Loop Through all the frames
    for frameData in GameData:
        teamData = frameData["teams"]
        for team in teamData:
            for player in team:
                PlayerPosition[str(player["id"])] = player["h"][0]
                #print(player["h"][0])


        if PrevPosition == "":
            PrevPosition = PlayerPosition
            continue

        for key,value in PlayerPosition.items():
            #print(value)
            PosVarance = 5
            if key in PrevPosition:
                NowPos = value
                PrevPos = PrevPosition[key]
                if abs(NowPos[0] - PrevPos[0]) > PosVarance or abs(NowPos[1] - PrevPos[1]) > PosVarance or abs(NowPos[1] - PrevPos[1]) > PosVarance:
                    if(InMap(PrevPos,MapSize)):
                       TotalDeaths += 1
                       print(f"Death of {NameRefList[key]}") 
                       DeathTotal[key] += 1


                    TotalDeaths += 1
                    #print(f"Death of {key}") 


        PrevPosition = PlayerPosition
        PlayerPosition = dict()


    for playerID, deaths in DeathTotal.items():
        print(f"{NameRefList[playerID]} : {deaths}")
    print(TotalDeaths)
    pass




































JsonData = dict()
DIRECTORY = "Games"
for filename in os.listdir(DIRECTORY):
    if filename.endswith(".rawreplayv3"):
        print("DECOMPRESSING FILE")
        ReplayData = dict()
        FilePath = os.path.join(DIRECTORY, filename)
        with bz2.open(FilePath) as f:
            ReplayData = pickle.load(f)
        with open("json.json","w") as f:
            JsonData = json.dumps(ReplayData)
            f.write(JsonData)
    
        print("Finished")
        CaculateDeaths(ReplayData)



