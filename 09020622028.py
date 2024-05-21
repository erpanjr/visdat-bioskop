import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Coffe Shop Skull",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
df_reshaped = pd.read_excel('coffee-sales.xlsx')

# Convert "Order Date" column to datetime
df_reshaped['Order Date'] = pd.to_datetime(df_reshaped['Order Date'])
df_reshaped['year'] = df_reshaped['Order Date'].dt.year
year_list = df_reshaped['year'].unique().tolist()

# Sidebar
with st.sidebar:
    st.title('Coffee Sales Dashboard')

    # Filter Tahun
    selected_year = st.selectbox('Pilih Tahun', ['All'] + sorted(year_list))
    if selected_year != 'All':
        df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    else:
        df_selected_year = df_reshaped

    # Filter Jenis Kopi
    product_list = list(df_selected_year["Product Coffee Type"].unique())
    selected_product = st.selectbox('Pilih jenis kopi', ['All'] + sorted(product_list))
    if selected_product != 'All':
        df_selected_product = df_selected_year[df_selected_year["Product Coffee Type"] == selected_product]
    else:
        df_selected_product = df_selected_year

    # Filter Negara
    city_list = list(df_selected_product["Customer Country"].unique())
    selected_city = st.multiselect('Pilih Negara', sorted(city_list))
    if selected_city:
        df_selected_city = df_selected_product[df_selected_product["Customer Country"].isin(selected_city)]
    else:
        df_selected_city = df_selected_product

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'sum({input_color}):Q',
                             legend=None,
                             scale=alt.Scale()),  # Ubah skema warna jika diperlukan
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    return heatmap

# Choropleth map
def make_choropleth(input_df, selected_year, selected_countries):
    if selected_countries:
        filtered_data = input_df[(input_df['year'] == selected_year) & (input_df['Customer Country'].isin(selected_countries))]
        aggregated_data = filtered_data.groupby('Customer Country')['Order Quantity'].sum().reset_index()

        choropleth = px.choropleth(aggregated_data, 
                                   locations='Customer Country', 
                                   locationmode="country names",
                                   color='Order Quantity',
                                   color_continuous_scale='Viridis',
                                   labels={'Order Quantity': 'Total Pemesanan'},
                                   scope='world',  # Set scope to 'world'
                                   projection='natural earth',  # Set the projection
                                   hover_name='Customer Country',  # Set the hover information
                                   hover_data={'Order Quantity': True}
                                  )
        choropleth.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=0, r=0, t=30, b=0),
            height=400
        )

        # Set fitbounds to 'locations' for auto-computation
        choropleth.update_geos(fitbounds="locations")

        return choropleth
    else:
        return None

# Horizontal Bar Chart
def make_horizontal_bar_chart(input_df, input_y, input_x, chart_title):
    # Aggregate the data to sum up the product sizes for each country
    aggregated_df = input_df.groupby(input_y)[input_x].sum().reset_index()

    bar_chart = alt.Chart(aggregated_df).mark_bar().encode( 
        x=alt.X(f'{input_x}:Q', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=100)),
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=100)),
        tooltip=[f'{input_y}:O', f'{input_x}:Q']
    ).properties(width=700, height=300, title=chart_title).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    return bar_chart

# Treemap
def make_treemap(input_df):

    treemap = alt.Chart(input_df).mark_rect().encode(
        alt.X('Product Roast Type:N', axis=alt.Axis(title="")),
        alt.Y('Product Unit Price:Q', axis=alt.Axis(title="")),
        color=alt.Color('Product Roast Type:N', scale=alt.Scale(domain=['Light', 'Medium', 'Dark']), legend=None),
        size='Product Price per 100g:Q',  # Size based on product price per 100g
        tooltip=['Product Roast Type:N', 'Product Unit Price:Q', 'Product Price per 100g:Q']  # Add product price per 100g to tooltip
    ).properties(width=700, height=300, title="Jumlah Penjualan Kopi")

    return treemap

#donat chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Montserrat", fontSize=20, fontWeight=700).encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

# Sort df_selected_city DataFrame
df_selected_city_sorted = df_selected_city.sort_values('Product Size (kg)', ascending=False)


total_orders = df_selected_city['Order Quantity'].sum()
total_profit = df_selected_city['Product Profit'].sum()
total_order_size = df_selected_city['Product Size (kg)'].sum()
total_product_price = df_selected_city['Product Price per 100g'].sum()
total_unit_price = df_selected_city['Product Unit Price'].sum()
    # Display Summary Boxes
st.markdown("<br>", unsafe_allow_html=True)



col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Perbandingn Presentase Pemesanan')
    if selected_city:
        for country in selected_city:
            st.write(f"### {country}")
            country_data = df_selected_city[df_selected_city['Customer Country'] == country]
            percentage = (country_data.shape[0] / df_selected_city.shape[0]) * 100
            rounded_percentage = round(percentage, 1)
            st.altair_chart(make_donut(rounded_percentage, "Pemesanan", "blue"), use_container_width=True)
with col[1]:
    st.markdown('#### Total Pemesanan')
    
    choropleth_map = make_choropleth(df_selected_city, selected_year, selected_city)
    if choropleth_map:
        st.plotly_chart(choropleth_map)

    st.altair_chart(make_heatmap(df_selected_city, 'year', 'Customer Country', 'Order Quantity'), use_container_width=True)

    st.altair_chart(make_treemap(df_selected_city), use_container_width=True)
    
    st.altair_chart(make_horizontal_bar_chart(df_selected_city_sorted, 'Customer Country', 'Product Size (kg)', "Jumlah Pesanan tiap customer (kg)"), use_container_width=True)
with col[2]:
    st.markdown('#### Summary Metrics', unsafe_allow_html=True)

    # Total Orders
    st.markdown(f"<div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px;'>"
                f"<h2>{round(total_orders, 5)}</h2>"
                f"<h5>Total Orders</h5></div>",
                unsafe_allow_html=True)

    # Total Product Profit
    st.markdown(f"<div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px;'>"
                f"<h2>{round(total_profit, 5)}</h2>"
                f"<h5>Total Product Profit</h5></div>",
                unsafe_allow_html=True)

    # Total Order Size (kg)
    st.markdown(f"<div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px;'>"
                f"<h2>{round(total_order_size, 5)}</h2>"
                f"<h5>Total Order Size (kg)</h5></div>",
                unsafe_allow_html=True)

    # Total Product Price
    st.markdown(f"<div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px;'>"
                f"<h2>{round(total_product_price, 5)}</h2>"
                f"<h5>Total Product Price</h5></div>",
                unsafe_allow_html=True)

    # Total Unit Price
    st.markdown(f"<div style='text-align: center; border: 2px solid #000000; padding: 10px; border-radius: 5px;'>"
                f"<h2>{round(total_unit_price, 5)}</h2>"
                f"<h5>Total Unit Price</h5></div>",
                unsafe_allow_html=True)

# Add spacing after Summary Metrics
st.markdown("<br><br><br>", unsafe_allow_html=True)