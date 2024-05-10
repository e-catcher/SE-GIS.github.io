import pyproj
from pyproj import CRS
from pyproj import Transformer
import streamlit as st

def xy():
    #构建以东经121°27′52″为中央子午线的高斯-克吕格投影坐标系统
    lon_0 = 121+27/60+52/3600
    proj4 = f"+proj=tmerc +lon_0={lon_0}"
    #计算上海2000坐标系原点（东经121°28′01″、北纬31°14′07″）的投影坐标（x和y）
    transformer = Transformer.from_crs(4490,proj4,always_xy=True)
    x_coords = 121+28/60+1/3600
    y_coords = 31+14/60+7/3600
    return transformer.transform(x_coords, y_coords)

def WGS84(lon, lat):
    lon_0 = 121+27/60+52/3600
    proj4 = f"+proj=tmerc +lon_0={lon_0} +x_0={-xy()[0]} +y_0={-xy()[1]} +ellps=WGS84"
    crs = CRS.from_proj4(proj4)
    transformer1 = Transformer.from_crs(4490,proj4,always_xy=True)
    new_lon, new_lat = transformer1.transform(lon, lat)
    return round(new_lon,2), round(new_lat,2)

def IAU76(lon, lat):
    lon_0 = 121+27/60+52/3600
    proj4 = f"+proj=tmerc +lon_0={lon_0} +x_0={-xy()[0]} +y_0={-xy()[1]} +ellps=IAU76"
    crs = CRS.from_proj4(proj4)
    transformer2 = Transformer.from_crs(4490,proj4,always_xy=True)
    new_lon, new_lat = transformer2.transform(lon, lat)
    return round(new_lon,2), round(new_lat,2)

def main():
    st.title("计算上海2000坐标系的东偏与北偏")
    if st.button("计算"):
        st.write(xy())
    
    st.title("CGCS2000地理坐标转上海2000投影坐标")
    with st.form("my_form"):
        lon = st.number_input(
            "输入经度120~122", min_value = 120.0, max_value = 122.0, value = 121.456, format = "%f")
        lat = st.number_input(
            '输入纬度30~32', min_value = 30.0, max_value = 32.0, value = 31.038, format = "%f")
        ellps = st.radio("选择坐标参照系统", ["WGS84", "IAU76"])
        
        if st.form_submit_button('提交'):    
            if ellps == "WGS84":
                st.write(WGS84(lon, lat))
            if ellps == "IAU76":
                st.write(IAU76(lon, lat))

main()
