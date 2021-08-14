from types import CodeType
from typing import Counter
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import bz2
import pickle
from mpl_toolkits.mplot3d import Axes3D
import pygame
from colormap import colormap , colormap2, colormap3

Sensitivity = 1
FloorValue = 5
Gridlines = False
RotateRight = False
FlipXY = False

# MAP = "surge"
# xBounds = [-60,150]
# yBounds = [-50,60]
# zBounds = [-100,100]
# quality = [200*6,90*6]
# FlipXY = False
# MapBounds = [-60,150,-50,60]
# Resolution = 6
# RotateRight = False

# MAP = "fission"
# xBounds = [-80,130]
# yBounds = [-30,30]
# zBounds = [-100,100]
# quality = [200*6,90*6]
# FlipXY = False
# MapBounds = [-80,130,-30,30]
# Resolution = 6
# RotateRight = False
# Sensitivity = 40
# FloorValue = 0

# MAP = "combustion"
# xBounds = [-30,60]
# yBounds = [-100,100]
# zBounds = [-100,100]
# quality = [200*6,90*6]
# FlipXY = False
# MapBounds = [-30,60,-100,100]
# Resolution = 6
# RotateRight = True

MAP = "dyson"
xBounds = [-100,100]
yBounds = [-40,40]
zBounds = [-100,100]
quality = [200*6,90*6]
MapBounds = [-100,100,-40,40]
Resolution = 6
FlipXY = False



"mpl_combat_dyson"
"mpl_combat_combustion"
"mpl_combat_fission"
"mpl_combat_surge"
# returns JSON object as 
# a dictionary
xpos = []
ypos = []
zpos = []
positions = dict()
for filename in os.listdir(f"PositionData/{MAP}"):
    if filename.endswith(".positionreplay"): 
        filePath = os.path.join(f"PositionData/{MAP}", filename)
        print(filePath)
        print("decompressing")
        with open(filePath, 'rb') as f:
            Replaydata = json.load(f)

        #python_file = open(filePath, "r")
        #Replaydata = json.load(python_file)
        #python_file.close()
        PlayerNameRef = dict()
        for userID, playerdata in Replaydata["players"].items():
            PlayerNameRef[str(playerdata["playerID"])] = playerdata["name"]

        for id,playerData in Replaydata["Data"].items():
            if int(id) <= 3:
               continue

            # if PlayerNameRef[str(id)] != "Slaughter_32":
            #    continue
            
            for position in playerData:
                if position[0] == 0 and position[2] == 0:
                    continue

                if not FlipXY and (position[0] < xBounds[0] or position[0] > xBounds[1] or position[2] < yBounds[0] or position[2] > yBounds[1] or position[1] < zBounds[0] or position[1] > zBounds[1]):
                    continue
                #if FlipXY and (position[2] < xBounds[0] or position[2] > xBounds[1] or position[0] < yBounds[0] or position[0] > yBounds[1] or position[1] < zBounds[0] or position[1] > zBounds[1]):
                 #   continue
                if FlipXY:


                    xpos.append(0-position[2])
                    ypos.append(position[0])
                else:
                    xpos.append(position[0])
                    ypos.append(position[2])
                #zpos.append(headPos)
            if PlayerNameRef[str(id)] not in positions:
                positions[PlayerNameRef[str(id)]] = list()
            positions[PlayerNameRef[str(id)]].append(playerData)
            
        print(f"Map Data Processed {filePath}")

#len(xpos)
#print(xpos)
print("Json Data Processed")

#fig, ax = plt.subplots()








WindowWidth = MapBounds[1] - MapBounds[0]
WindowHeight = MapBounds[3] - MapBounds[2]

HeatMap = []
for x in range((WindowWidth)*Resolution):
    HeatMap.append([])
    for y in range((WindowHeight)*Resolution):
        HeatMap[x].append(0)

def isInBox(position,box):
    return position[0] > box[0] and position[0] < box[2] and position[2] > box[1] and position[2] < box[3]
        
print("Caculating BoxValues")

SensorBoxes = dict()
SensorBoxes["FarSpawnBlue"] = [-40,-40,-30,-30]
SensorBoxes["FarSpawnOrange"] = [30,-40,40,-30]
SensorBoxes["NearSpawnBlue"] = [-20,20,-10,30]
SensorBoxes["NearSpawnOrange"] =[10,20,20,30]

Tally = dict()
for name,positionlist in positions.items():
    if name != "Slaughter_32_":
       continue
    for boxName,BoxValues in SensorBoxes.items():
        for positiongamelist in positionlist:
            InTally = False
            box = BoxValues
            for position in positiongamelist:
                if position[0] > box[0] and position[0] < box[2] and position[2] > box[1] and position[2] < box[3]:
                    if not InTally:
                        if boxName not in Tally:
                            Tally[boxName] = 0
                        Tally[boxName] += 1
                        InTally = True
                else:
                    if InTally:
                        InTally = False





for boxName, value in Tally.items():
    print(f"{boxName}: {value}")

Deaths = []
for name,positionlist in positions.items():
    for positiongamelist in positionlist:
        InTally = False
        oldPos = (position[0],position[2])
        for position in positiongamelist:
            if position[0] > MapBounds[0] and position[0] < MapBounds[1] and position[2] > MapBounds[2] and position[2] < MapBounds[3]:
                if not InTally:
                    InTally = True
            else:
                if InTally:
                    Deaths.append(oldPos)
                    InTally = False
            oldPos = (position[0],position[2])


##### NORMAL
for xval,yval in zip(xpos,ypos):
    xmid = MapBounds[1]-MapBounds[0]
    ymid = MapBounds[1]-MapBounds[0]

    x = round((xval- MapBounds[0])*Resolution)-1
    y = round((yval- MapBounds[2])*Resolution)-1
    #print(x,y)
    HeatMap[x][y] += 1


# ###### DEATHS
# for xval,yval in Deaths:
#     xmid = MapBounds[1]-MapBounds[0]
#     ymid = MapBounds[1]-MapBounds[0]

#     x = round((xval- MapBounds[0])*Resolution)-1
#     y = round((yval- MapBounds[2])*Resolution)-1
#     #print(x,y)
#     print(xval,yval)
#     HeatMap[x][y] += 1



#quit()

# pygame.init()

# Set up the drawing window
if RotateRight:
    screen = pygame.display.set_mode([WindowHeight*Resolution, WindowWidth*Resolution])
else:
    screen = pygame.display.set_mode([WindowWidth*Resolution, WindowHeight*Resolution])

# Run until the user asks to quit
running = True
while running:
    print("Frame")
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center

    for x in range(WindowWidth*Resolution):
        #HeatMap.append([])
        for y in range(WindowHeight*Resolution):
            #HeatMap[x].append(0)
            value = HeatMap[x][y]
            Color = 0
            if value > 0:
                Color = (value+Sensitivity) + FloorValue
            
            if Color>255:
                Color = 255

            # if x % (1*Resolution) == 0 or y % (1*Resolution) == 0:
            #     Color = 50
            
            if (x % (10*Resolution) == 0 or y % (10*Resolution) == 0) and Gridlines:
                Color = 100
            
            
            if (x == ((0-MapBounds[0])*Resolution) or y == ((0-MapBounds[2])*Resolution)) and Gridlines:
                Color = 255
            if RotateRight:
                pygame.draw.rect(screen, colormap3[255-Color], [(WindowHeight*Resolution)-y, x, 1, 1])
            else:
                pygame.draw.rect(screen, colormap3[255-Color], [x, y, 1, 1])



    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()





# colo = np.random.randn(10, 1000)*1000
  
# # creating 3d figures
# fig = plt.figure(figsize=(10, 10))
# ax = Axes3D(fig)
  
# # configuring colorbar
# color_map = cm.ScalarMappable(cmap=cm.gray)
# color_map.set_array(colo)
  
# # creating the heatmap
# img = ax.scatter(x, y, z, marker='s',
#                  s=100, color='gray')
# plt.colorbar(color_map)
  
# # adding title and labels
# ax.set_title("3D Heatmap")
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# ax.set_zlabel('Z-axis')
  
# # displaying plot
# plt.show()