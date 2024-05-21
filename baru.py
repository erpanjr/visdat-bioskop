import streamlit as st
import plotly.express as px
import pandas as pd
import  altair as alt

st.set_page_config(page_title="Dashboard IMDb Indonesian Film", page_icon="🎞️", layout="wide")
st.markdown("<h1 style='text-align: center; color: aqua;'>🎞️ Dashboard Film Indonesia pada IMDb</h1>", unsafe_allow_html=True)


df = pd.read_excel('film.xlsx')

st.sidebar.markdown(
    """
    <div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #ddd; color: #000000;">
        <h4 style="color: #000000;">"Dashboard ini menampilkan visualisasi untuk sekumpulan data Film Indonesia 🎬. Dataset ini berisi informasi tentang film-film Indonesia yang terdaftar di IMDb. Setiap film memiliki detail seperti judul, tahun rilis, genre, rating, dan ulasan pengguna. Dashboard ini memberikan wawasan tentang tren film Indonesia selama beberapa tahun terakhir, dengan analisis tentang rating rata-rata, jumlah ulasan, dan genre yang populer"</h4>
        <p style="color: #000000;">Gunakan filter di bawah ini untuk menyesuaikan data yang ditampilkan.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Filter")

# fltr genre
genre = st.sidebar.multiselect("🎞️Pilih Genre ", df["genre"].unique())
if not genre:
    df2 = df.copy()
else:
    df2 = df[df["genre"].isin(genre)]

# fltr slidebar taun
min_year = int(df2["year"].min())
max_year = int(df2["year"].max())
year = st.sidebar.slider("🎱Pilih Rentang Tahun", min_year, max_year, (min_year, max_year))
df3 = df2[(df2["year"] >= year[0]) & (df2["year"] <= year[1])]
    
  
# rentang usia
rating = st.sidebar.multiselect("🙋Pilih Pengelompokan Usia ", df3["rating"].unique())
if not rating:
    filtered_df = df3.copy()
else:
    filtered_df = df3[df3["rating"].isin(rating)]

  
bahasa = st.sidebar.multiselect("🎢Pilih bahasa film", df3["languages"].unique())
if not bahasa:
    filtered_df = df3.copy()
else:
    filtered_df = df3[df3["languages"].isin(bahasa)]


def calculate_statistics(filtered_df):
    # variabel card boxx
    total_orders = filtered_df['title'].count()
    total_votes = filtered_df['votes'].sum()
    total_votes_rounded = round(total_votes, 3)  # Membatasi jumlah angka di belakang koma menjadi 3
    total_avg_rating = filtered_df['users_rating'].mean()

    # mengembalikan hasil jika diperlukan
    return total_orders, total_votes_rounded, total_avg_rating

# Memanggil fungsi dan menyimpan hasil
total_orders, total_votes_rounded, total_avg_rating = calculate_statistics(filtered_df)

# dsplay summary
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px; background-color: #303337;'>
            <h2 style="color: #2e86c1;"><i class="fa fa-film"></i> {}</h2>
            <h5 style="color: #2e86c1;">Total Film</h5>
        </div>
        """.format(total_orders),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px; background-color: #303337;'>
            <h2 style="color: #28a745;"><i class="fa fa-users"></i> {}</h2>
            <h5 style="color: #28a745;">Total Partisipan IMDb</h5>
        </div>
        """.format(total_votes_rounded),
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px; background-color: #303337;'>
            <h2 style="color: #e74c3c;"><i class="fa fa-star"></i> {}</h2>
            <h5 style="color: #e74c3c;">Rata-Rata Seluruh Rating</h5>
        </div>
        """.format(round(total_avg_rating, 2)),
        unsafe_allow_html=True
    )

# css rapli
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)

# dsplay filter data
st.markdown("<h3 style='text-align: center; color: yellow;'>Data Dengan Filter Order</h3>", unsafe_allow_html=True)

# xpander e rapli
with st.expander("Show Filtered Data"):
    filtered_df['year'] = pd.to_datetime(filtered_df['year'], format='%Y')  # Konversi ke tipe data datetime
    filtered_df['year'] = filtered_df['year'].dt.strftime('%Y')  # Ubah format tahun menjadi YYYY
    st.write(filtered_df)



# Group by genre 
title_df = filtered_df.groupby(by=["genre"], as_index=False)["title"].count().nlargest(5, 'title')
title_df = title_df.sort_values(by='title', ascending=True)  # Sort for the highest count on top


col1, col2 = st.columns((1, 1))

with col1:
    st.markdown("<h4 style='text-align: center; color: yellow;'>5 Genre Teratas Dengan Film Terbanyak</h4>", unsafe_allow_html=True)

    fig = px.bar(title_df, x="title", y="genre", text='title', template="seaborn", orientation='h')
    fig.update_layout(xaxis_title='Jumlah Judul', yaxis_title='Genre')
    st.plotly_chart(fig, use_container_width=True, height=400)


with col2:
    st.markdown("<h4 style='text-align: center; color: yellow;'>Persentase Jumlah Ulasan Berdasarkan Genre</h4>", unsafe_allow_html=True)
    
    # Hitung jumlah votes untuk setiap genre
    votes_per_genre_df = filtered_df.groupby(by=["genre"], as_index=False)["votes"].sum().nlargest(8, 'votes')
    
    # Buat grafik pai dengan Plotly Express
    fig = px.pie(votes_per_genre_df, values="votes", names="genre", hole=0.5)
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

# njupuk lima genre teratas berdasarkan rata-rata peringkat pengguna
top_5_genres = avg_rating_per_genre_df.nlargest(5, 'users_rating')

# urutan DataFrame berdasarkan rata-rata peringkat pengguna secara menurun
top_5_genres = top_5_genres.sort_values(by='users_rating', ascending=False)

# warna yg akan digunakan untuk setiap bar
colors = px.colors.qualitative.Set3[:5]  # Menggunakan palet warna Set3 dari Plotly Express

# Buat horizontal bar chart dengan Plotly Express
fig = px.bar(top_5_genres, y="genre", x="users_rating", 
             title="5 Genre Teratas dengan Rating Terbaik",
             labels={"users_rating": "Rata-Rata Nilai Rating", "genre": "Genre"},
             color="genre", color_discrete_sequence=colors)

st.plotly_chart(fig, use_container_width=True)


#(Bar Chart)
title_per_director_df = filtered_df.groupby(by=["directors"], as_index=False)["title"].count().nlargest(5, 'title')
title_per_director_df = title_per_director_df.sort_values(by='title', ascending=False)
fig4 = px.bar(title_per_director_df, x="title", y="directors", text='title', orientation='h',
              color='directors', color_discrete_sequence=px.colors.qualitative.Bold)
fig4.update_layout(title="5 Sutradara Teratas dengan Film Terbanyak", xaxis_title="Judul Film", yaxis_title="Sutradara")
st.plotly_chart(fig4, use_container_width=True)


# Menggabungkan data rating dengan jumlahnya
negara = df.groupby("rating").size().reset_index(name="Count")
negara_top5 = negara.nlargest(8, 'Count')
# Membuat pie chart dengan Plotly Express
fig = px.pie(negara_top5, values='Count', names='rating', title='Persentase Jumlah Film Berdasarkan Kelompok Umur(pie)')
st.plotly_chart(fig, use_container_width=True)