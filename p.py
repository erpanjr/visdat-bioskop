import streamlit as st
import plotly.express as px
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard IMDb Indonesian Film", page_icon="🎞️", layout="wide")
st.title("🎞️ Dashboard IMDb Indonesian Film")

# For testing, reading from a local file
df = pd.read_excel('film.xlsx')

st.sidebar.header("Filter")

# Create filter for genre
genre = st.sidebar.multiselect("Pick your genre", df["genre"].unique())
if not genre:
    df2 = df.copy()
else:
    df2 = df[df["genre"].isin(genre)]

# Create filter for year
min_year = int(df2["year"].min())
max_year = int(df2["year"].max())
year = st.sidebar.slider("Pick the year range", min_year, max_year, (min_year, max_year))
df3 = df2[(df2["year"] >= year[0]) & (df2["year"] <= year[1])]

# Create filter for rentang usia
rating = st.sidebar.multiselect("Pilih Rating Usia", df3["rating"].unique())
if not rating:
    filtered_df = df3.copy()
else:
    filtered_df = df3[df3["rating"].isin(rating)]

# Display filtered data
st.subheader("Filtered Data")
st.write(filtered_df)

def calculate_statistics(filtered_df):
    # Calculate summary statistics from the filtered DataFrame
    total_orders = filtered_df['title'].count()
    total_votes = filtered_df['votes'].sum()
    total_votes_rounded = round(total_votes, 2)
    total_avg_rating = filtered_df['users_rating'].mean()

    return total_orders, total_votes_rounded, total_avg_rating

# Memanggil fungsi dan menyimpan hasil
total_orders, total_votes_rounded, total_avg_rating = calculate_statistics(filtered_df)

# Membuat bar plot
plt.figure(figsize=(8, 6))
sns.barplot(x=['Total Titles', 'Total Votes', 'Average User Rating'],
            y=[total_orders, total_votes_rounded, total_avg_rating])
plt.title('Summary Statistics')
plt.xlabel('Statistics')
plt.ylabel('Value')
plt.show()

# Memanggil fungsi dan menyimpan hasil
total_orders, total_votes_rounded, total_avg_rating = calculate_statistics(filtered_df)

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
                f"<h2>{total_votes_rounded}</h2>"
                f"<h5>Total Votes</h5></div>",
                unsafe_allow_html=True)

with col3:
    st.markdown(f"<div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px;'>"
                f"<h2>{round(total_avg_rating, 2)}</h2>"
                f"<h5>Average User Rating</h5></div>",
                unsafe_allow_html=True)

# Group by genre and sum the number of titles (assuming 'title' is the number of titles)
title_df = filtered_df.groupby(by=["genre"], as_index=False)["title"].count()

col1, col2 = st.columns((1, 1))

with col1:
    fig = filtered_df.groupby('genre').size().reset_index(name="Count")
    chart = (
        alt.Chart(fig)
        .mark_bar()
        .encode(
            x=alt.X("Count", type="quantitative", title="Judul Film"),
            y=alt.Y("genre", type="nominal", title="Genre", sort='-x'),
        )
    )
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.subheader("Users Rating by Genre")
    genre_count_df = filtered_df['genre'].value_counts().reset_index()
    genre_count_df.columns = ['genre', 'count']
    fig = px.pie(genre_count_df, values="count", names="genre", hole=0.5)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True, height=400)

# Create visualizations
st.title("Data Analysis and Visualization")

# Create two columns for visualizations
col1, col2 = st.columns(2)

# Visualization 1: Jumlah Judul per Tahun
with col1:
    st.subheader("Jumlah Judul per Tahun")
    title_per_year_df = filtered_df.groupby(by=["year"], as_index=False)["title"].count()
    fig1 = px.line(title_per_year_df, x="year", y="title", markers=True, title="Jumlah Judul per Tahun")
    st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Jumlah Judul per Rating Usia
with col2:
    st.subheader("Jumlah Judul per Rating Usia")
    title_per_rating_df = filtered_df.groupby(by=["rating"], as_index=False)["title"].count()
    fig2 = px.bar(title_per_rating_df, x="rating", y="title", text='title', title="Jumlah Judul per Rating Usia")
    st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Distribusi Rating Pengguna
with col1:
    st.subheader("Distribusi Rating Pengguna")
    fig3 = px.histogram(filtered_df, x="users_rating", nbins=20, title="Distribusi Rating Pengguna")
    st.plotly_chart(fig3, use_container_width=True)

# Optional: Display filtered data
with col2:
    st.subheader("Filtered Data")
    st.write(filtered_df)

# Custom Plot using Matplotlib and Seaborn
# st.header('Assalamualaikum')
# fig, ax = plt.subplots(figsize=(10, 5))  # Adjusted the figsize
# colors = sns.color_palette("husl", len(filtered_df['directors'].unique()))
# sns.barplot(x="directors", y="count of title", data=filtered_df, ax=ax, palette=colors)
# ax.set_ylabel('Number of Titles')
# ax.set_xlabel('Directors')
# i = 0
# text = filtered_df['votes'].round(2).astype(int).to_list()
# for rect in ax.patches:
#     height = rect.get_height()
#     ax.text(rect.get_x() + rect.get_width() / 2., rect.get_y() + height * 3 / 4., 
#             str(text[i]) + ' votes', ha='center', va='bottom', rotation=0, color='white', fontsize=12)
#     i += 1
# st.pyplot(fig)
