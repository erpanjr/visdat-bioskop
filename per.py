import time  #

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np  # import np
import pandas as pd  # import pd
import plotly.express as px  # import chart
import plotly.graph_objects as go
import streamlit as st
import altair as alt
import math
from PIL import Image

import seaborn as sns
from pandas import DataFrame

st.set_page_config(
    page_title="Update - RectoGadget",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.set_option("deprecation.showPyplotGlobalUse", False)

st.markdown(f"<html style='scroll-behavior: smooth;'></html>", unsafe_allow_html=True)

dataset_url = "https://raw.githubusercontent.com/fernandatsaqif/hape_visdat/main/clean/smartphone.csv"


@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)


phone = get_data()

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
> Sections Introduction
1. [Top 5 Smartphone dengan Harga Tertinggi](#top-5-smartphone-dengan-harga-tertinggi)
2. [Peminatan penjualan berdasarkan prosesor](#peminatan-penjualan-berdasarkan-prosesor)
3. [Best Rated phones](#best-rated-phones)
4. [Distribution of Processors by Manufacturer and Brand](#distribution-of-processors-by-manufacturer-and-brand)
""",
    unsafe_allow_html=True,
)

# Set Dashboard Title
st.title("Smartphone Dashboard Sales")
st.markdown('<style>div.block-container{padding-top:1rem}</style>',unsafe_allow_html=True)

col1, col2 = st.columns((2))

#membuat sidebar
st.sidebar.header("Choose your filter: ")

#Create filter for brand name
country = st.sidebar.multiselect("Pick your brand",phone["brand_name"].unique())
if not country:
    phone2 = phone.copy()
else:
    phone2 = phone[phone["brand_name"].isin(country)]

#Create filter for Rating
roast = st.sidebar.multiselect("Pick your Rating",phone2["rating"].unique())
if not roast:
    phone3 = phone2.copy()
else:
    phone3 = phone2[phone2["rating"].isin(roast)]

#Create filter for Prosesor
size = st.sidebar.multiselect("Pick your Prosesor",phone3["processor_brand"].unique())
if not size:
    phone4 = phone3.copy()
else:
    phone4 = phone3[phone3["processor_brand"].isin(size)]

#Create filter for refresh rate
loyalty = st.sidebar.multiselect("Refresh rate phone?",phone4["refresh_rate"].unique())

st.sidebar.header("(for section 1 & 2)")

# Filter based on country, roast, size, and loyalty card
if not country and not roast and not size and not loyalty:
    filtere_phone = phone
elif not roast and not size and not loyalty:
    filtere_phone = phone[phone["brand_name"].isin(country)]
elif not country and not size and not loyalty:
    filtere_phone = phone[phone["rating"].isin(roast)]
elif not country and not roast and not loyalty:
    filtere_phone = phone[phone["processor_brand"].isin(size)]
elif roast and size and loyalty:
    filtere_phone = phone4[phone4["rating"].isin(roast) & phone4["processor_brand"].isin(size) & phone4["refresh_rate"].isin(loyalty)]
elif country and size and loyalty:
    filtere_phone = phone4[phone4["brand_name"].isin(country) & phone4["processor_brand"].isin(size) & phone4["refresh_rate"].isin(loyalty)]
elif country and roast and loyalty:
    filtere_phone = phone4[phone4["brand_name"].isin(country) & phone4["rating"].isin(roast) & phone4["refresh_rate"].isin(loyalty)]
elif roast and loyalty:
    filtere_phone = phone4[phone4["rating"].isin(roast) & phone4["refresh_rate"].isin(loyalty)]
elif country and loyalty:
    filtere_phone = phone4[phone4["brand_name"].isin(country) & phone4["refresh_rate"].isin(loyalty)]
elif size and loyalty:
    filtere_phone = phone4[phone4["processor_brand"].isin(size) & phone4["refresh_rate"].isin(loyalty)]
else:
    filtere_phone = phone4

col1, col2 = st.columns((2))

category_df = filtere_phone.groupby(by = ["model"], as_index = False)["price"].sum()
category_df = category_df.sort_values(by = ["price"], ascending=False,)
category_df = category_df.head(5)

#Chart HP paling termahal
with col1:
    st.subheader("Top 5 Smartphone dengan Harga Tertinggi")
    fig = px.bar(category_df, x = "model", y = "price", text = ['Rp{:,.2f}'.format(x) for x in category_df["price"]], template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

# topChartHarga = filtere_phone.groupby(by="model", as_index=False)[
# "price"
# ].sum()
# topChartHarga = topChartHarga.sort_values(by="price", ascending=False,)
# topChartHarga = topChartHarga.head(5)

# with col1:
#     fig = px.bar(
#         topChartHarga,
#         x="model",
#         y="price",
#         title="Top 5 Smartphone dengan Harga Tertinggi",
#         template="seaborn",
#         barmode="group",
#         text="price",
#         labels={"price": "", "model": ""},
#     )
# fig.update_traces(texttemplate="%{text}", textposition="inside")
# st.plotly_chart(fig, use_container_width=True)

# Grafik Penjualan berdasarkan wilayah
with col2:
    st.subheader("Peminatan penjualan berdasarkan prosesor")
    fig = px.pie(filtere_phone, values = "price", names = "processor_brand", hole = 0.5)
    fig.update_traces(text = filtere_phone["processor_brand"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

# RATINGS

st.header("Best Rated phones")

rating_col_1, rating_col_2 = st.columns([3, 9])
with rating_col_1:
    st.write("\n")
    st.write("Insert amount")
    color = st.select_slider(
        "Set the number of data to be displayed",
        options=[5, 10, 15, 20, 25, 30, 40, 50],
        key="rating_1",
    )
    st.write(f"Top {color} \n phone Ratings")
with rating_col_2:
    rating_5, rating_4, rating_3, rating_2, rating_1 = st.tabs(
        [
            "Rating :five:",
            "Rating :four:",
            "Rating :three:",
            "Rating :two:",
            "Rating :one:",
        ]
    )


# FUNC DOT PLOTS RATING
def dot_plots_rating_phone(rating, bestnum):
    rating_filtered = phone.loc[(phone["rating"] == rating)]
    sort_rating_price = rating_filtered.sort_values("price", ascending=False)
    data_rating = sort_rating_price.head(bestnum)
    fig = px.scatter(
        data_rating,
        y="brand_name",
        x="price",
        color="brand_name",
        symbol="brand_name",
        hover_data=rating_filtered,
    )
    fig.update_traces(marker_size=10)
    st.plotly_chart(fig, use_container_width=True)


with rating_5:
    dot_plots_rating_phone(rating=5, bestnum=color)

with rating_4:
    dot_plots_rating_phone(rating=4, bestnum=color)

with rating_3:
    dot_plots_rating_phone(rating=3, bestnum=color)

with rating_2:
    dot_plots_rating_phone(rating=2, bestnum=color)

with rating_1:
    dot_plots_rating_phone(rating=1, bestnum=color)

# FUNC PIE CHART
def pie_chart(columns, by, values, labels, names, color, title):
    fig = px.pie(
        phone.loc[(phone[columns] == by)],
        values=values,
        labels=labels,
        names=names,
        color=color,
        title=f"{title}",
    )

    fig.update_layout(xaxis_title=option, yaxis_title="Count of " + option)
    st.plotly_chart(fig, use_container_width=True)


# FUNC BAR CHART
def bar_chart(by, columns, return1, return2, title, orientation):
    value_counts = phone[phone[by] == option][columns].value_counts().reset_index()

    value_counts.columns = [return1, return2]

    fig = px.bar(
        value_counts,
        x=value_counts.columns[0],
        y=value_counts.columns[1],
        text=value_counts.columns[1],
        color=value_counts.columns[0],
        title=f"{title}",
        orientation=orientation,
    )

    fig.update_layout(
        xaxis_title=value_counts.columns[0],
        yaxis_title="Count of " + value_counts.columns[0],
    )

    st.plotly_chart(fig, use_container_width=True)


# FUNC SELECT BOX CUSTOM
def select_box(title, column, key):
    data = st.selectbox(title, phone[column].unique(), key=key)
    return data

st.header(
    "Distribution of Processors by Manufacturer and Brand"
)  # Processor Distribution by Manufacturer and Brand, Processor Distribution by Manufacturer and Brand.

option = select_box(
    title="Choose a column to plot count. Try Selecting Brand ",
    column="brand_name",
    key="procie",
)
procie_1, procie_2 = st.columns([6, 6])

with procie_1:
    # procie_type_count = phone.groupby('brand')['processor_brand'].value_counts()
    procie_value_count = (
        phone[phone["brand_name"] == option]["processor_brand"]
        .value_counts()
        .reset_index()
    )

    fig = px.scatter(
        procie_value_count,
        x="processor_brand",
        y="count",
        size="count",
        color="processor_brand",
        hover_name="processor_brand",
        title=f"Distribution of Processor Brand \nby {option} Brand",
    )

    fig.update_layout(
        xaxis_title="Processor Brand", yaxis_title="Count of Processor Brand"
    )

    st.plotly_chart(fig, use_container_width=True)


with procie_2:
    bar_chart(
        by="brand_name",
        columns="processor_speed",
        return1="Processor Speed",
        return2="Count",
        title=f"Distribution of Processor Generation Usage \nby {option} Brand",
        orientation="v",
    )