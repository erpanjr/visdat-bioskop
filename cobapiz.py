import streamlit as st
import plotly.express as px
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Dashboard Sales Pizza", page_icon="🎞️", layout="wide")
st.title("🎞️ Dashboard Sales Pizza")

# File upload
fl = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"])

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(fl)

    st.sidebar.header("Filter")

    # Create filter for pizza_id
    pizza_id = st.sidebar.multiselect("Pick your ID Pizza", df["pizza_id"].unique())
    if not pizza_id:
        df2 = df.copy()
    else:
        df2 = df[df["pizza_id"].isin(pizza_id)]

    # Create filter for order_id
    order_id = st.sidebar.multiselect("Pick the ID Order ", df2["order_id"].unique())
    if not order_id:
        df3 = df2.copy()
    else:
        df3 = df2[df2["order_id"].isin(order_id)]

    # Create filter for order_date
    order_date = st.sidebar.multiselect("Pick the Date Order", df3["order_date"].unique())
    if not order_date:
        filtered_df = df3.copy()
    else:
        filtered_df = df3[df3["order_date"].isin(order_date)]

    # Calculate summary statistics from the filtered DataFrame
    total_orders = filtered_df['pizza_id'].count()
    total_votes = filtered_df['order_id'].sum()

    # Display Summary Boxes
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px;'>"
                    f"<h2>{total_orders}</h2>"
                    f"<h5>Total Titles</h5></div>",
                    unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px;'>"
                    f"<h2>{total_votes}</h2>"
                    f"<h5>Total Votes</h5></div>",
                    unsafe_allow_html=True)


    # Group by genre and sum the number of titles (assuming 'title' is the number of titles)
    title_df = filtered_df.groupby(by=["genre"], as_index=False)["title"].count()

    col1, col2 = st.columns((1, 1))

    with col1:
        st.subheader("Title by Genre")
        fig = px.bar(title_df, y="genre", x="title", text='title', template="seaborn", orientation='h')
        st.plotly_chart(fig, use_container_width=True, height=400)

    with col2:
        st.subheader("Users Rating by Genre")
        fig = px.pie(filtered_df, values="users_rating", names="genre", hole=0.5)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True, height=400)

else:
    st.warning("Please upload a file to proceed.")