
# -*- coding: utf-8 -*-
import json
# import requests
import numpy as np

import math

key = 'your key here'  # 这里填写你的百度开放平台的key
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率


def wgs84togcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]

def gcj02towgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def gcj02tobd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
        0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
        0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False

for date in ['2015-10-12','2015-10-13','2015-10-14','2015-10-15','2015-10-16','2015-10-17','2015-10-18','2015-10-19','2015-10-20','2015-10-21']:
    filename = '2015-10.taxi/'+date+'/part-r-00000' # txt文件和当前脚本在同一目录下，所以不用写具体路径
    # 2015-08.taxi/2015-08-04/part-r-00000
    number = []
    on_time = []
    on_GPS=[]
    on_difference=[]
    on_longitude=[]
    on_latitude=[]
    off_time=[]
    off_GPS=[]
    off_difference=[]
    off_longitude=[]
    off_latitude=[]
    distance=[]

    with open(filename, 'r', encoding='utf-8', errors='ignore') as file_to_read:
      while True:
        lines = file_to_read.readline() # 整行读取数据
        if not lines:
          break
          pass
        number_tmp, on_time_tmp, on_GPS_tmp, on_difference_tmp,on_longitude_tmp,on_latitude_tmp,off_time_tmp,off_GPS_tmp,off_difference_tmp,off_longitude_tmp,off_latitude_tmp,distance_tmp = [i for i in lines.split(',')] # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
        number.append(number_tmp)  # 添加新读取的数据
        on_time.append(on_time_tmp)
        on_GPS.append(on_GPS_tmp)
        on_difference.append(on_difference_tmp)
        on_longitude.append(float(on_longitude_tmp))
        on_latitude.append(float(on_latitude_tmp))
        off_time.append(off_time_tmp)
        off_GPS.append(off_GPS_tmp)
        off_difference.append(off_difference_tmp)
        off_longitude.append(float(off_longitude_tmp))
        off_latitude.append(float(off_latitude_tmp))
        distance.append(distance_tmp)
    on_longitude = np.array(on_longitude) # 将数据从list类型转换为array类型。
    on_latitude = np.array(on_latitude)
    off_longitude = np.array(off_longitude)
    off_latitude = np.array(off_latitude)
    total_on= np.vstack([on_longitude, on_latitude])
    total_on= np.transpose(total_on)
    total_off= np.vstack([off_longitude, off_latitude])
    total_off= np.transpose(total_off)
    total_on2=[];
    total_off2=[];


    for i in total_on:
        [longitude_gcj, latitude_gcj] = wgs84togcj02(i[0], i[1])
        #[longitude_baidu, latitude_baidu] = gcj02tobd09(longitude_gcj, latitude_gcj)
        total_on2.append([longitude_gcj, latitude_gcj])

    for i in total_off:
        [longitude_gcj, latitude_gcj] = wgs84togcj02(i[0], i[1])
        #[longitude_baidu, latitude_baidu] = gcj02tobd09(longitude_gcj, latitude_gcj)
        total_off2.append([longitude_gcj, latitude_gcj])
    # /home/yanglan/Documents/ridesharing/raw_data/2015-08.taxi/2015-08-03/part-r-00000.txt
    # /code/
    f= open('/home/yanglan/Documents/ridesharing/code/ridesharing_for_py36/first_outbound_next_inbound/2015-09_10/'+date[0:4] + date[5:7] + date[8:10] + "_gaode_offboard_t.txt", "w")
    g= open('/home/yanglan/Documents/ridesharing/code/ridesharing_for_py36/first_outbound_next_inbound/2015-09_10/'+date[0:4] + date[5:7] + date[8:10] + "_gaode_onboard_t.txt", "w")

    for j in range(0, np.shape(total_on)[0]):
        li= ','.join([number[j], on_time[j],on_GPS[j],on_difference[j],str(total_on2[j][0]),str(total_on2[j][1]),off_time[j],off_GPS[j],off_difference[j],str(total_off2[j][0]),str(total_off2[j][1]),distance[j]])
        if total_on2[j][0]>=113.810 and total_on2[j][0]<=113.818 and total_on2[j][1]>=22.619 and total_on2[j][1]<=22.626:
                f. write(li)
        if total_off2[j][0]>=113.810 and total_off2[j][0]<=113.818 and total_off2[j][1]>=22.619 and total_off2[j][1]<=22.626:
                g. write(li)



