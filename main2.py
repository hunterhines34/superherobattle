import sqlite3
import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(page_title='Superhero Comparison Tool', page_icon=':superhero:', layout='wide', initial_sidebar_state='expanded')

# Connect to SQLite database
conn = sqlite3.connect('superheroes.db')
c = conn.cursor()

# Streamlit application
st.markdown("<h1 style='text-align: center;'>Superhero Comparison Tool</h1>", unsafe_allow_html=True)
st.divider()

# Get the list of superhero names from the database
superhero_names = [row[0] for row in c.execute("SELECT name FROM superheroes")]

# Sidebar for selecting superheroes
st.sidebar.header('Select Superheroes to Compare')
selected_superhero1 = st.sidebar.selectbox("Superhero #1", superhero_names)
selected_superhero2 = st.sidebar.selectbox("Superhero #2", superhero_names)

# Compare button
if st.sidebar.button('Compare'):
    # Fetch the details of the selected superheroes from the database
    superhero_data1 = c.execute("SELECT * FROM superheroes WHERE name = ?", (selected_superhero1,)).fetchone()
    superhero_data2 = c.execute("SELECT * FROM superheroes WHERE name = ?", (selected_superhero2,)).fetchone()
    
    # Convert fetched data to dictionary
    def data_to_dict(data):
        return {
            'id': data[0],
            'name': data[1],
            'intelligence': data[2],
            'strength': data[3],
            'speed': data[4],
            'durability': data[5],
            'power': data[6],
            'combat': data[7],
            'full_name': data[8],
            'aliases': data[9],
            'place_of_birth': data[10],
            'first_appearance': data[11],
            'publisher': data[12],
            'alignment': data[13],
            'gender': data[14],
            'race': data[15],
            'height': data[16],
            'weight': data[17],
            'eye_color': data[18],
            'hair_color': data[19],
            'occupation': data[20],
            'base': data[21],
            'group_affiliation': data[22],
            'relatives': data[23],
            'image_url': data[24]
        }
    
    data_dict1 = data_to_dict(superhero_data1)
    data_dict2 = data_to_dict(superhero_data2)

    # Handle null values
    for key in data_dict1:
        if data_dict1[key] is None:
            data_dict1[key] = 'N/A'
    for key in data_dict2:
        if data_dict2[key] is None:
            data_dict2[key] = 'N/A'

    # Display the data side by side in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.header(data_dict1['name'])
        st.write(f"Full Name: {data_dict1['full_name']}")
        st.write(f"Aliases: {data_dict1['aliases']}")
        st.write("Power Stats:")
        st.write(f"Intelligence: {data_dict1['intelligence']}")
        st.write(f"Strength: {data_dict1['strength']}")
        st.write(f"Speed: {data_dict1['speed']}")
        st.write(f"Durability: {data_dict1['durability']}")
        st.write(f"Power: {data_dict1['power']}")
        st.write(f"Combat: {data_dict1['combat']}")
        st.image(data_dict1['image_url'])

    with col2:
        st.header(data_dict2['name'])
        st.write(f"Full Name: {data_dict2['full_name']}")
        st.write(f"Aliases: {data_dict2['aliases']}")
        st.write("Power Stats:")
        st.write(f"Intelligence: {data_dict2['intelligence']}")
        st.write(f"Strength: {data_dict2['strength']}")
        st.write(f"Speed: {data_dict2['speed']}")
        st.write(f"Durability: {data_dict2['durability']}")
        st.write(f"Power: {data_dict2['power']}")
        st.write(f"Combat: {data_dict2['combat']}")
        st.image(data_dict2['image_url'])
    
    st.divider()
    st.markdown("<h1 style='text-align: center;'>Statistics Comparison Charts</h1>", unsafe_allow_html=True)

    # Create dataframes for the superheroes' stats
    stats = ['intelligence', 'strength', 'speed', 'durability', 'power', 'combat']
    data1 = {stat: int(data_dict1[stat]) if data_dict1[stat] != 'N/A' else 0 for stat in stats}
    data2 = {stat: int(data_dict2[stat]) if data_dict2[stat] != 'N/A' else 0 for stat in stats}

    df1 = pd.DataFrame(data1, index=[data_dict1['name']])
    df2 = pd.DataFrame(data2, index=[data_dict2['name']])

    # Concatenate dataframes for visualization
    df = pd.concat([df1, df2])

    # Create Altair charts for each statistic in a 2x2 format
    for i in range(0, len(stats), 2):
        col3, col4 = st.columns(2)
        with col3:
            chart = alt.Chart(df.reset_index()).mark_bar().encode(
                x=alt.X('index', title='Superhero'),
                y=alt.Y(stats[i], title=stats[i].capitalize()),
                color='index'
            ).properties(
                title=f'{stats[i].capitalize()} Comparison'
            )
            st.altair_chart(chart, use_container_width=True)
        if i + 1 < len(stats):
            with col4:
                chart = alt.Chart(df.reset_index()).mark_circle().encode(
                    x=alt.X('index', title='Superhero'),
                    y=alt.Y(stats[i + 1], title=stats[i + 1].capitalize()),
                    color='index',
                    size=alt.value(100)  # Make circles bigger for visibility
                ).properties(
                    title=f'{stats[i + 1].capitalize()} Comparison'
                )
                st.altair_chart(chart, use_container_width=True)

# Close the database connection
conn.close()