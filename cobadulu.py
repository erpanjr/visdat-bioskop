import streamlit as st
import plotly.express as px
import pandas as pd
import  altair as alt

st.set_page_config(page_title="Dashboard IMDb Indonesian Film", page_icon="🎞️", layout="wide")
st.markdown("<h1 style='text-align: center; color: aqua;'>🎞️ Dashboard Film Indonesia pada IMDb</h1>", unsafe_allow_html=True)


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



def calculate_statistics(filtered_df):
    # Calculate summary statistics from the filtered DataFrame
    total_orders = filtered_df['title'].count()
    total_votes = filtered_df['votes'].sum()
    total_votes_rounded = round(total_votes, 2)  # Membatasi jumlah angka di belakang koma menjadi 2
    total_avg_rating = filtered_df['users_rating'].mean()

    # Mengembalikan hasil jika diperlukan
    return total_orders, total_votes_rounded, total_avg_rating

# Memanggil fungsi dan menyimpan hasil
total_orders, total_votes_rounded, total_avg_rating = calculate_statistics(filtered_df)

# Display Summary Boxes
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px;'>"
                f"<h2>{total_orders}</h2>"
                f"<h5>Total Film</h5></div>",
                unsafe_allow_html=True)

with col2:
    st.markdown(f"<div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px;'>"
                f"<h2>{total_votes_rounded}</h2>"
                f"<h5>Total Partisipan IMDb</h5></div>",
                unsafe_allow_html=True)

with col3:
    st.markdown(f"<div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px;'>"
                f"<h2>{round(total_avg_rating, 2)}</h2>"
                f"<h5>Rata-Rata Seluruh Rating</h5></div>",
                unsafe_allow_html=True)

# Display filtered data
st.markdown("<h3 style='text-align: center; color: yellow;'>Data Dengan Filter Order</h3>", unsafe_allow_html=True)

st.write(filtered_df)
# Group by genre and sum the number of titles (assuming 'title' is the number of titles)
title_df = filtered_df.groupby(by=["genre"], as_index=False)["title"].count().nlargest(5, 'title')
title_df = title_df.sort_values(by='title', ascending=True)  # Sort for the highest count on top

st.markdown("<h2 style='text-align: center; color: aqua;'>🎞️ Dashboard Film Indonesia pada IMDb</h2>", unsafe_allow_html=True)

col1, col2 = st.columns((1, 1))

with col1:
    st.markdown("<h4 style='text-align: center; color: yellow;'>5 Genre Teratas Dengan Film Terbanyak</h4>", unsafe_allow_html=True)

    fig = px.bar(title_df, x="title", y="genre", text='title', template="seaborn", orientation='h')
    fig.update_layout(xaxis_title='Jumlah Judul', yaxis_title='Genre')
    st.plotly_chart(fig, use_container_width=True, height=400)


with col2:
    st.markdown("<h4 style='text-align: center; color: yellow;'>Genre Teratas Dengan Rating Terbaik</h4>", unsafe_allow_html=True)
    rating_df = filtered_df.groupby(by=["genre"], as_index=False)["users_rating"].mean().nlargest(8, 'users_rating')
    fig = px.pie(rating_df, values="users_rating", names="genre", hole=0.5)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True, height=400)

# Group by title and calculate average of users rating
average_rating_per_title = filtered_df.groupby("title")["users_rating"].mean().reset_index()

# Sort values by average rating and select top 5
top_5_titles = average_rating_per_title.nlargest(5, 'users_rating', keep='all').sort_values('users_rating', ascending=True)

# Create horizontal bar chart with Plotly Express
fig = px.bar(top_5_titles, 
             x='users_rating', 
             y='title', 
             orientation='h',
             title='5 Judul Film Dengan Rating Terbaik',
             labels={'users_rating': 'Rata-Rata Nilai Rating', 'title': 'Judul Film'},
             text='users_rating')  # Menetapkan nilai rata-rata sebagai teks untuk ditampilkan di atas setiap bar
fig.update_traces(marker_color='skyblue')
fig.update_layout(xaxis_title='Rata-Rata Rating Pengguna', yaxis_title='Judul Film')
st.plotly_chart(fig, use_container_width=True)


title_per_rating_df = filtered_df.groupby(by=["rating"], as_index=False)["title"].count().nlargest(5, 'title')
fig2 = px.bar(title_per_rating_df, x="rating", y="title", text='title', 
              title="5 Pengelompokan Umur Teratas dengan Film Terbanyak")
fig2.update_layout(xaxis_title='Kelompok Usia', yaxis_title='Jumlah Judul')
st.plotly_chart(fig2, use_container_width=True)


# Hitung rata-rata peringkat pengguna untuk setiap genre
avg_rating_per_genre_df = filtered_df.groupby(by=["genre"], as_index=False)["users_rating"].mean()

# Ambil lima genre teratas berdasarkan rata-rata peringkat pengguna
top_5_genres = avg_rating_per_genre_df.nlargest(5, 'users_rating')

# Urutkan DataFrame berdasarkan rata-rata peringkat pengguna secara menurun
top_5_genres = top_5_genres.sort_values(by='users_rating', ascending=False)

# Tentukan warna yang akan digunakan untuk setiap bar
colors = px.colors.qualitative.Set3[:5]  # Menggunakan palet warna Set3 dari Plotly Express

# Buat horizontal bar chart dengan Plotly Express
fig = px.bar(top_5_genres, y="genre", x="users_rating", 
             title="5 Genre Teratas dengan Rating Terbaik",
             labels={"users_rating": "Rata-Rata Nilai Rating", "genre": "Genre"},
             color="genre", color_discrete_sequence=colors)

st.plotly_chart(fig, use_container_width=True)


# Visualization 4: Count of Titles per Director (Bar Chart)
title_per_director_df = filtered_df.groupby(by=["directors"], as_index=False)["title"].count().nlargest(5, 'title')
title_per_director_df = title_per_director_df.sort_values(by='title', ascending=False)
fig4 = px.bar(title_per_director_df, x="title", y="directors", text='title', orientation='h',
              color='directors', color_discrete_sequence=px.colors.qualitative.Bold)
fig4.update_layout(title="5 Sutradara Teratas dengan Film Terbanyak", xaxis_title="Judul Film", yaxis_title="Sutradara")
st.plotly_chart(fig4, use_container_width=True)


# Menggabungkan data rating dengan jumlahnya
negara = df.groupby("rating").size().reset_index(name="Count")


# Memilih 5 data teratas
negara_top5 = negara.nlargest(8, 'Count')

# Membuat pie chart dengan Plotly Express
fig = px.pie(negara_top5, values='Count', names='rating', title='kelompok Umur dengan Film (pie)')
st.plotly_chart(fig, use_container_width=True)
