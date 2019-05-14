from urllib import request
import urllib.request
import mecatorUtil
import os
import random
import math
import configparser
import json
from tqdm import tqdm

MecatorConfig =""
GlobalConfig = ""
#地图地址
mapUrl =""

allLevels = []

#三次回调就跳过
count = 0


#读取配置文件
def getConfig(filePath):
    with open(filePath,"r",encoding="UTF-8") as jsonFile:
        config = json.loads(jsonFile.read())
    return config

#计算行列号
def calculateRowAndCol():
    ox = MecatorConfig["tileInfo"]["origin"]["x"]
    oy = MecatorConfig["tileInfo"]["origin"]["y"]
    leftTop = mecatorUtil.lonLat2Mercator(GlobalConfig["lefttop"][0],GlobalConfig["lefttop"][1])
    leftTopX = leftTop[0]
    leftTopY = leftTop[1]

    rightBottom = mecatorUtil.lonLat2Mercator(GlobalConfig["rightbottom"][0],GlobalConfig["rightbottom"][1])
    rightBottomX = rightBottom[0]
    rightBottomY = rightBottom[1]

    allTotal = 0
    for i in range(GlobalConfig[ "startlevel"],GlobalConfig["endlevel"]+1):
        lod = MecatorConfig["lods"][i]
        startX = math.floor(abs(leftTopX - ox) / (lod["resolution"] * 256));
        endX = math.floor(abs(rightBottomX - ox) / (lod["resolution"] * 256));
        startY = math.floor(abs(oy - leftTopY) / (lod["resolution"] * 256));
        endY = math.floor(abs(oy - rightBottomY) / (lod["resolution"] * 256));
        item = {"zoom":i,"startX":startX,"endX":endX,"startY":startY,"endY":endY}

        total = (endX - startX + 1) * (endY - startY + 1);
        allTotal += total
        allLevels.append(item)

    print("................一共%d张瓦片........."%allTotal)

#下载
def downLoad():
    global count
    calculateRowAndCol()

    rootPath = GlobalConfig["outfolder"]
    if not os.path.exists(rootPath):
        os.mkdir(rootPath)
    for item in allLevels:
        #创建等级文件夹
        levelDirPath = rootPath +os.path.sep+ str(item["zoom"])
        if not os.path.isdir(levelDirPath):
            os.mkdir(levelDirPath)
        #X循环
        for x in tqdm(range(item["startX"],item["endX"]+1)):
            xDirPath = levelDirPath+os.path.sep+str(x)
            if not os.path.isdir(xDirPath):
                os.mkdir(xDirPath)
            #y循环
            for y in range(item["startY"],item["endY"]+1):
                if not os.path.exists(xDirPath+os.path.sep+str(y)+".png"):
                    imgUrl = mapUrl.replace("{z}", str(item["zoom"])).replace("{x}", str(x)).replace("{y}", str(y))
                    saveImg(imgUrl, xDirPath, str(y))
                    count = 0
        print(end='\r')
        print(".............%d等级下载完成..........."%(item["zoom"]))

    print("..............全部下载完成！！！.............")



#写入图片
def saveImg(imgUrl,path,name):
    global count
    try:
        if(count>=3):
            return
        req = urllib.request.Request(imgUrl)
        req.add_header('User-Agent', random.choice(GlobalConfig["agents"]))  # 换用随机的请求头
        img = urllib.request.urlopen(req,timeout=60)

        f = open(path+os.path.sep+name+".png","ab")
        f.write(img.read())
        f.close()
        count = 0
    except Exception:
        if(count<3):
            count = count + 1
            saveImg(imgUrl, path, name)

#获取地图地址
def getMapTile(type):
    global mapUrl
    if(type == "google_ras"):
        mapUrl = GlobalConfig["googlemap"]["raster"]
    elif (type == "goole_vec"):
        mapUrl = GlobalConfig["googlemap"]["vector"]
    elif (type == "tianditu_vec"):
        mapUrl = GlobalConfig["tianditu"]["vec"]
    elif (type == "tianditu_cva"):
        mapUrl = GlobalConfig["tianditu"]["cva"]
    elif (type == "arcgis"):
         mapUrl = GlobalConfig["arcgis"]["line"]
    elif(type == "" or type == None):
        print("没有选择下载图层")
        return
    print("................当前地图地址 %s ........."%mapUrl)

    downLoad()

def initConfig():
    global GlobalConfig
    global MecatorConfig
   #加载config文件
    GlobalConfig = getConfig("config.json")

    print("................下载地图等级为 %d等级--到--%d等级............" % (GlobalConfig["startlevel"], GlobalConfig["endlevel"]))
    print("................地图切片保存路径--%s " % GlobalConfig['outfolder'])

    #加载墨卡托配置文件
    MecatorConfig = getConfig("mecatortileinfo.json")

if __name__ == '__main__':
    initConfig() #初始化配置
    getMapTile("arcgis")
