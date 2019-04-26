import math
def lonLat2Mercator(lon, lat):
    xy = []
    x = lon * 20037508.342789 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    y = y * 20037508.34789 / 180
    xy.append(x)
    xy.append(y)
    return xy
def mercator2lonLat(mercatorX, mercatorY):
    xy = []
    x = mercatorX / 20037508.34 * 180
    y = mercatorY / 20037508.34 * 180
    y = 180 / math.pi * (2 * math.atan(math.exp(y * math.pi / 180)) - math.PI / 2)
    xy.append(x)
    xy.append(y)
    return xy