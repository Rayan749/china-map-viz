import json

import streamlit as st
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import JsCode, ThemeType
from streamlit_echarts import Map as ste_map
from streamlit_echarts import st_pyecharts
import requests

#
# with open("geo/合肥市.geojson", "r") as f:
#     map_geo = ste_map("合肥", json.loads(f.read()))

#
# print(ctx)
#
# with open("geo/中华人民共和国.geojson", "r") as f:
#


st.set_page_config(layout="wide", page_title="China Map Viz")

map_theme_dict = {
    "light": ThemeType.LIGHT,
    "dark": ThemeType.DARK,
    "white": ThemeType.WHITE,
    "chalk": ThemeType.CHALK,
    "essos": ThemeType.ESSOS,
    "infographic": ThemeType.INFOGRAPHIC,
    "macarons": ThemeType.MACARONS,
    "purple_passion": ThemeType.PURPLE_PASSION,
    "roma": ThemeType.ROMA,
    "romantic": ThemeType.ROMANTIC,
    "shine": ThemeType.SHINE,
    "vintage": ThemeType.VINTAGE,
    "walden": ThemeType.WALDEN,
    "westeros": ThemeType.WESTEROS,
    "wonderland": ThemeType.WONDERLAND,
    "halloween": ThemeType.HALLOWEEN,
}

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 30rem !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    with st.expander("图表设置", expanded=True):
        title = st.text_input("图表标题", "China Map Viz")

        area_options = ["全国", "省份", "城市"]
        area_option = st.segmented_control("区域选择", area_options, selection_mode="single", default=area_options[2],
                                           )
        province_selector_disabled: bool = False
        city_selector_disabled: bool = False
        if area_option == "全国":
            province_selector_disabled: bool = True
            city_selector_disabled: bool = True

            ctx = requests.get("https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json").content
            map_geo = ste_map("全国", json.loads(ctx))
            map_type = area_option

        if area_option == "省份":
            city_selector_disabled: bool = True

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            province_selector = st.selectbox("省份", ["安徽"], disabled=province_selector_disabled)
        with col_a2:
            city_selector = st.selectbox("城市", ["合肥"], disabled=city_selector_disabled)

        if area_option == "省份":
            ctx = requests.get("https://geo.datav.aliyun.com/areas_v3/bound/340000_full.json").content
            map_geo = ste_map(str(province_selector), json.loads(ctx))
            map_type = province_selector

        if area_option == "城市":
            ctx = requests.get("https://geo.datav.aliyun.com/areas_v3/bound/340100_full.json").content
            map_geo = ste_map(str(city_selector), json.loads(ctx))
            map_type = city_selector

    with st.expander("展示数据", expanded=True):
        data = st.text_area("展示数据",
                            "(瑶海区,2),(庐阳区,4),(蜀山区,5),(包河区,7),(长丰县,8),(肥东县,9),(肥西县,1),(庐江县,2),(巢湖市,10)",
                            label_visibility="collapsed")

    # with st.expander("区域设置"):

    with st.expander("图例设置", expanded=True):
        # st.text("")
        options = ["是", "否"]
        col4, col5, col6 = st.columns(3)
        with col4:
            is_show_symbols = st.segmented_control("是否展示标签", options, selection_mode="single", default=options[0])
        with col5:
            st.space()
        with col6:
            symbols_font_size_disabled: bool = False
            if is_show_symbols == '否':
                symbols_font_size_disabled: bool = True
            symbols_font_size = st.text_input("字体大小", "14", key="symbols_font_size",
                                              disabled=symbols_font_size_disabled)

        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            is_pieces_show = st.segmented_control("是否分组展示", options, selection_mode="single", default=options[0])
        with col_p2:
            lb_min = st.text_input("分组最小值", "0")
        with col_p3:
            lb_max = st.text_input("分组最大值", "20")

        symbols_name = st.text_input("图例名称", "样例")
        st.text("选择图例颜色和字体大小")
        col1, col2, col3 = st.columns(3)
        with col1:
            start_color = st.color_picker("起始颜色", "#c8e3fd")
        with col2:
            end_color = st.color_picker("终止颜色", "#5ed1f5")
        with col3:
            font_size = st.text_input("字体大小", "20", key="lb_font_size")

    with st.expander("主题设置"):
        theme_option = [ThemeType.LIGHT, ThemeType.DARK, ThemeType.WHITE, ThemeType.CHALK, ThemeType.ESSOS,
                        ThemeType.INFOGRAPHIC, ThemeType.MACARONS, ThemeType.PURPLE_PASSION, ThemeType.ROMA,
                        ThemeType.ROMANTIC, ThemeType.SHINE, ThemeType.VINTAGE, ThemeType.WALDEN, ThemeType.WESTEROS,
                        ThemeType.WONDERLAND, ThemeType.HALLOWEEN]
        map_theme_option = st.selectbox("地图主题", options=theme_option)


def data_process(raw_data: str) -> list[tuple]:
    raw_data = (raw_data.strip()
                .replace(" ", "")
                .replace("\n", "")
                .replace("\t", "")
                .replace("\r", "")
                .replace("（", ")")
                .replace("）", ")")
                )
    raw_data = [i.replace("(", "").replace(")", "") for i in raw_data.split("),")]
    raw_data = [i.split(",") for i in raw_data]
    data_v2 = []
    for item in raw_data:
        key = item[0]
        try:
            value = int(item[1])
            data_v2.append((key, value))
        except TypeError:
            pass

    return data_v2


data = data_process(data)

is_show_symbols_map = True if is_show_symbols == "是" else False
is_pieces_show = True if is_pieces_show == "是" else False
lb_max = int(lb_max)
lb_min = int(lb_min)

lb_font_size = int(font_size)
syb_font_size = int(symbols_font_size)
map_theme = map_theme_dict.get(map_theme_option)

c_map = (
    Map(init_opts=opts.InitOpts(width="900px", height="72px", theme=map_theme, ))
    .add("", data, str(map_type), is_map_symbol_show=False, label_opts=opts.LabelOpts(
        is_show=is_show_symbols_map,
        position="inside",  # 位置调整
        font_size=syb_font_size,
        formatter=JsCode('''function(params){
                                            if (params['value']){return params['name'] + ':' + params['value']}
                                            else{return ''}
                                            }''')),
# series_layout_by="column",
         )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            max_=lb_max,
            min_=lb_min,
            is_show=True,
            split_number=5,
            is_piecewise=is_pieces_show,
            range_text=[symbols_name, ""],
            precision=0,
            is_calculable=True,
            range_color=[start_color, end_color],
            pos_bottom="10%",
            pos_left="20%",
            textstyle_opts=opts.TextStyleOpts(font_size=font_size),

        )

    )
)

if title != "":
    st.title(title)
    # st.markdown(f"<p style='text-align: center; font-size:40px'>{title}</p>", unsafe_allow_html=True)

st_pyecharts(c_map, map=map_geo, width="1200px", height="800px")
