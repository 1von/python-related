# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '2017C43'
__createtime__ = '2018/2/24 0024'
"""
import math
import requests
from cordiate_convert import gcj02_to_wgs84,test_print
import geojson
import sys
import os

def getpoly(kw):
    url = 'http://restapi.amap.com/v3/config/district?'
    parms = {
        'key': inputkey,
        'keywords': kw,
        'subdistrict': sd,
        'extensions': 'all',
        'output': 'json'
    }
    response = requests.get(url, params=parms)
    data = response.json()
    return data

def gcj_convert(i):
    ii = gcj02_to_wgs84(i)
    ii2 = ii.split(',')
    out = [float(ii2[0]),float(ii2[1])]
    return out


def getpolylon(data):
    lonlat = data['districts'][0]['polyline']
    name = data['districts'][0]['name']
    s = lonlat.split('|')
    out = []
    for i in s:
        ss = i.split(';')
        sss = list(map(lambda x:gcj_convert(x), ss))
        temp_poly = geojson.Polygon([sss])
        if len(s)<=1:
            temp_pro = dict(name = name)
        else:
            temp_pro = dict(name = name+str(s.index(i)))
        temp_featrue = geojson.Feature(geometry=temp_poly, properties=temp_pro)
        out.append(temp_featrue)
    return out


# def tofile(d, file):
#     indx = ['lon', 'lat']
#     for di in d:
#         with open(file + str(d.index(di)) + '.csv', 'w') as f:
#             f.write('idd,lon,lat\n')
#             ii = 1
#             for i in di:
#                 f.write(str(ii) + ',' + i + '\n')
#                 ii += 1

Path = os.getcwd()
inputkey = 'e7866dc4a248a50ed6d01bf3cfdcaa4d'
# kws = ['缙云','杭州','金华','丽水','舟山','台州']
kws = sys.argv[1:]
print(kws)
sd = 2
p0=[]
for kw in kws:
    area = kw
    darea = getpoly(area)
    # p0=darea['districts'][0]['polyline']
    p0.extend(getpolylon(darea))
feature_collection = geojson.FeatureCollection(p0)
with open(Path+"/temp.json", 'w+') as f:
    dump = geojson.dump(feature_collection, f)
    f.close()


# print(p0[0])
test_print()