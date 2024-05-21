import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import plotly.express as px


st.set_page_config(page_title = "Data Kelompok Ipan",layout = 'wide')

datafield =  pd.read_excel('RApli ko.xlsx')

# st.title("")
st.markdown("<h1 style='text-align: center; color: grey;'>Dashboard Riwayat Film Indonesia yang Tercatat Pada IMDB</h1>", unsafe_allow_html=True)
st.markdown('<style>div.block-container{padding-top:1rem}</style>',unsafe_allow_html=True)
with st.sidebar:
    country = list(datafield['genre'].unique())[::-1]
    select_country = st.multiselect("select country",country, default=country)
    datafield = datafield[datafield['genre'].isin(select_country)]

    rating = list(datafield['rating'].unique())[::-1]
    select_rating = st.multiselect("select country",rating, default=rating)
    datafield = datafield[datafield['rating'].isin(select_rating)]

    dates = list(datafield['year'].unique())[::-1]
    dates.sort()
    date1, date2 = st.slider('Select date', min_value=dates[0], value=(2010, dates[len(dates)-1]), max_value=dates[len(dates)-1])
    datafield = datafield[datafield["year"].between(left=date1,right=date2)]


col = st.columns((6, 2), gap='medium')

with col[0]:  
    st.markdown("<h2 style='text-align: center; color: grey;'>5 Genre Dengan Jumlah Film Teratas</h4>", unsafe_allow_html=True)
    st.write("5 kota dengan penjualan tertinggi")
    # joinan = pd.merge(orders, customers,on="Customer ID")
    # joinan = joinan.groupby("City").size().reset_index(name="Count")
    # joinan = joinan.sort_values(by='Count', ascending=False)  
    dt = datafield.groupby('genre').size().reset_index(name="Count")
    chart = (
        alt.Chart(dt)
        .mark_bar()
        .encode(
            x=alt.X("Count", type="quantitative", title="Judul Film"),
            y=alt.Y("genre", type="nominal", title="Genre",sort='-x'),
        )
    )
    st.altair_chart(chart, use_container_width=True)

    dt = datafield.groupby('genre').size().reset_index(name="Count")
    chart = (
        alt.Chart(dt)
        .mark_bar()
        .encode(
            x=alt.X("Count", type="quantitative", title="Judul Film"),
            y=alt.Y("title", type="nominal", title="Genre",sort='-x'),
        )
    )
    st.altair_chart(chart, use_container_width=True)


with col[1]:  
    st.title("hgyguhguhj")
# st.write("Most City Sales")
# type = orders.groupby("Coffee Type").size().reset_index(name="Count")
# chart = (
#     alt.Chart(type)
#     .mark_bar()
#     .encode(
#         x=alt.X("Count", type="quantitative", title=""),
#         y=alt.Y("Coffee Type", type="nominal", title="",sort='-x'),
#     )
# )
# st.altair_chart(chart, use_container_width=True)

# negara = orders.groupby("Country").size().reset_index(name="Count")
# fig = px.pie(negara,values=negara['Count'],names=negara['Country'])
# st.plotly_chart(fig, use_container_width=True)

# st.write ("Target Sales")
# fig = px.choropleth(negara, locations='Country', locationmode='country names', color='Count')
# st.plotly_chart(fig, use_container_width=True)

# # chart = (
# #     alt.Chart(negara)
# #     .mark_area()
# #     .encode(
# #         x=alt.X("OrderDate", type="temporal", title="OrderDate"),
# #         y=alt.Y("Count", type="quantitative", title="Count"),
# #         tooltip=["OrderDate", "Count"],
# #         color=alt.Color("Country", title="Country")
# #     )
# # )
# st.write ("Most Product Sales")
# st.altair_chart(chart, use_container_width=True)