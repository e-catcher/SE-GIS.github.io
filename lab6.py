import streamlit as st
import fiona
from shapely.geometry import Point

def city_list():
    list = []
    c = fiona.open("china_cities_prj\china_cities_prj.shp", 'r')
    for i in c:
        list.append(i["properties"]["城市名"])
    c.close()
    return list

def get_index(cities, city):
    number = cities.index(city)
    return number

def city_to_point(city_number):
    c = fiona.open("china_cities_prj\china_cities_prj.shp", 'r')
    return Point([c[city_number]["properties"]["经度"], c[city_number]["properties"]["纬度"]])

def in_or_out(city, distance, cities):
    city_number = get_index(cities, city)
    selected_city_point = city_to_point(city_number)
    selected_city_point_buffer = selected_city_point.buffer(distance/100)
    list_name = []
    list_distance = []
    for i in range(338):  
        this_point = city_to_point(i)
        if this_point.within(selected_city_point_buffer):
            list_name.append(cities[i])
            list_distance.append(selected_city_point.distance(this_point))
    list_name.remove(city)
    list_distance.remove(0)
    return list_name, list_distance

def output(city, distance, cities, flag):
    list_name, list_distance = in_or_out(city, distance, cities)
    text = f"在{city}周围{distance}公里内，有{len(list_name)}个城市："
    text += """
          
"""
    for i in range(len(list_name)):
        text += f"{list_name[i]}"
        text += """
              
"""
    if flag:
        closest_city, closest_distance = closest(list_name, list_distance)
        text += f"其中，最近的城市是{closest_city}，距离为{100*closest_distance:.2f}公里。"
    return text

def closest(list_name, list_distance):
    min_distance = min(list_distance)
    min_indedx = get_index(list_distance, min_distance)
    return list_name[min_indedx], min_distance

def main():
    st.title("查询某地周边的城市")
    with st.form("my_form"):
        cities = city_list()
        city = st.selectbox("选择一个城市", cities)
        distance = st.number_input(
            "输入邻近距离（公里，0~1000）",
            value = 300,
            format = "%d",
            min_value = 0,
            max_value = 1000)
        flag = st.checkbox("显示最近的城市和距离")
        submitted = st.form_submit_button("查询")
    if submitted:
        st.write(output(city, distance, cities, flag))
            
main()
