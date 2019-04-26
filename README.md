# tileMapDownload
基于python写的一个地图切片服务下载，目前有谷歌影像，谷歌矢量，天地图矢量，下载其他地图请修改配置和部分条件代码
# 地图矢量切片服务下载器 -- EPSG3857

## 思路整理
    1、读取配置文件 config.json 和 mecatortileinfo.json文件来获取自己配置的信息
   
    2、根据配置的经纬度范围，和起始等级来计算行列号
   
    3、循环每一级进行下载。
 
## 使用教程
    1、切片默认是按照左上角为源点进行切图，如果标准的TMS,即按照坐下角为源点切图修改mecatortileinfo.json里面的origin中的y为负号（-20037508.342787）
       和想关的切片计算  starty  endy
   
    2、下载范围在config.json中修改。lefttop和rightbottom
    
    3、起始等级在config.json中修改。startlevel为起始等级。endlevel为结束等级
   
    4、输出路径在config.json中修改。outfolder为输出路径
   
    5、如果添加路径则需要在 代码中添加相应的条件判断，目前有谷歌影像和谷歌矢量，天地图矢量和矢量标注
   
    6、最后调用 getMapTile()填入对应的参数选择下载
