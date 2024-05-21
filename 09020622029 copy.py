import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import plotly.express as px


st.set_page_config(page_title = "Data Ipan",layout = 'wide')

df = pd.ExcelFile('Raw-Data-coffee-sales.xlsx')
orders =  pd.read_excel(df,'orders')
customers =  pd.read_excel(df,'customers')
products =  pd.read_excel(df,'products')

# st.title("DASHBOARD COFFEE SALES")
st.markdown("<h1 style='text-align: center; color: grey;'>Dashboard Coffee Sales</h1>", unsafe_allow_html=True)
with st.sidebar:
    country = list(orders['Country'].unique())[::-1]
    select_country = st.multiselect("select country",country, default=country)
    orders = orders[orders['Country'].isin(select_country)]

    dates = list(pd.to_datetime(orders['Order Date']).dt.date.unique())[::-1]
    dates.sort()
    date1, date2 = st.slider('Select date', min_value=dates[0], value=(dates[0],dates[len(dates)-1]) ,max_value=dates[len(dates)-1], format='MMM DD, YYYY')
    orders = orders[pd.to_datetime(orders['Order Date']).dt.date.between(left=date1,right=date2)]
    print(orders.to_string)
    
st.write("5 kota dengan penjualan tertinggi")
st.markdown("<h2 style='text-align: center; color: grey;'>5 Kota Dengan Penjualan Teratas</h2>", unsafe_allow_html=True)
joinan = pd.merge(orders, customers,on="Customer ID")
joinan = joinan.groupby("City").size().reset_index(name="Count")
joinan = joinan.sort_values(by='Count', ascending=False)  
chart = (
    alt.Chart(joinan[:5])
    .mark_bar()
    .encode(
        x=alt.X("Count", type="quantitative", title="Jumlah Terjual"),
        y=alt.Y("City", type="nominal", title="Kota",sort='-x'),
    )
)
st.altair_chart(chart, use_container_width=True)


st.write("Most City Sales")
type = orders.groupby("Coffee Type").size().reset_index(name="Count")
chart = (
    alt.Chart(type)
    .mark_bar()
    .encode(
        x=alt.X("Count", type="quantitative", title=""),
        y=alt.Y("Coffee Type", type="nominal", title="",sort='-x'),
    )
)
st.altair_chart(chart, use_container_width=True)

negara = orders.groupby("Country").size().reset_index(name="Count")
fig = px.pie(negara,values=negara['Count'],names=negara['Country'])
st.plotly_chart(fig, use_container_width=True)

st.write ("Target Sales")
fig = px.choropleth(negara, locations='Country', locationmode='country names', color='Count')
st.plotly_chart(fig, use_container_width=True)

# chart = (
#     alt.Chart(negara)
#     .mark_area()
#     .encode(
#         x=alt.X("OrderDate", type="temporal", title="OrderDate"),
#         y=alt.Y("Count", type="quantitative", title="Count"),
#         tooltip=["OrderDate", "Count"],
#         color=alt.Color("Country", title="Country")
#     )
# )
st.write ("Most Product Sales")
st.altair_chart(chart, use_container_width=True)