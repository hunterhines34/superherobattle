import sqlite3
import requests
import streamlit as st

# Set page configuration
st.set_page_config(page_title='Superhero Comparison Tool', page_icon=':superhero:', layout='wide', initial_sidebar_state='expanded')

# Connect to SQLite database
conn = sqlite3.connect('superheroes.db')
c = conn.cursor()

# Create a table for superheroes if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS superheroes (
        id INTEGER PRIMARY KEY,
        name TEXT,
        intelligence INTEGER,
        strength INTEGER,
        speed INTEGER,
        durability INTEGER,
        power INTEGER,
        combat INTEGER,
        full_name TEXT,
        aliases TEXT,
        place_of_birth TEXT,
        first_appearance TEXT,
        publisher TEXT,
        alignment TEXT,
        gender TEXT,
        race TEXT,
        height TEXT,
        weight TEXT,
        eye_color TEXT,
        hair_color TEXT,
        occupation TEXT,
        base TEXT,
        group_affiliation TEXT,
        relatives TEXT,
        image_url TEXT
    )
''')
conn.commit()

# Function to add 30 superheroes at a time
def add_superheroes(start_id, end_id):
    api_key = ''  # Replace with your actual API key
    base_url = f'https://superheroapi.com/api/{api_key}'

    for hero_id in range(start_id, end_id + 1):
        # Check if the superhero already exists in the database
        if c.execute("SELECT COUNT(*) FROM superheroes WHERE id = ?", (hero_id,)).fetchone()[0] == 0:
            response = requests.get(f'{base_url}/{hero_id}')
            data = response.json()

            if data['response'] == 'success':
                # Extract needed data
                name = data['name']
                powerstats = data['powerstats']
                biography = data['biography']
                appearance = data['appearance']
                work = data['work']
                connections = data['connections']
                image_url = data['image']['url']

                # Insert data into the database
                c.execute('''
                    INSERT INTO superheroes (id, name, intelligence, strength, speed, durability, power, combat,
                    full_name, aliases, place_of_birth, first_appearance, publisher, alignment,
                    gender, race, height, weight, eye_color, hair_color, occupation, base,
                    group_affiliation, relatives, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    hero_id, name,
                    powerstats['intelligence'], powerstats['strength'], powerstats['speed'],
                    powerstats['durability'], powerstats['power'], powerstats['combat'],
                    biography['full-name'], ', '.join(biography['aliases']),
                    biography['place-of-birth'], biography['first-appearance'],
                    biography['publisher'], biography['alignment'],
                    appearance['gender'], appearance['race'],
                    ', '.join(appearance['height']), ', '.join(appearance['weight']),
                    appearance['eye-color'], appearance['hair-color'],
                    work['occupation'], work['base'],
                    connections['group-affiliation'], connections['relatives'],
                    image_url
                ))

    conn.commit()

# Fetch and store data from the API, 30 records at a time
for start_id in range(1, 732, 30):
    end_id = min(start_id + 29, 731)
    add_superheroes(start_id, end_id)

# Streamlit application
st.markdown("<h1 style='text-align: center;'>Superhero Comparison Tool</h1>", unsafe_allow_html=True)

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

    # Display the data side by side in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.header(selected_superhero1)
        if superhero_data1:
            st.write(f"Full Name: {superhero_data1[8]}")
            st.write(f"Aliases: {superhero_data1[9]}")
            st.write("Power Stats:")
            st.write(f"Intelligence: {superhero_data1[2]}")
            st.write(f"Strength: {superhero_data1[3]}")
            st.write(f"Speed: {superhero_data1[4]}")
            st.write(f"Durability: {superhero_data1[5]}")
            st.write(f"Power: {superhero_data1[6]}")
            st.write(f"Combat: {superhero_data1[7]}")
            st.image(superhero_data1[24])
        else:
            st.write("No data found.")

    with col2:
        st.header(selected_superhero2)
        if superhero_data2:
            st.write(f"Full Name: {superhero_data2[8]}")
            st.write(f"Aliases: {superhero_data2[9]}")
            st.write("Power Stats:")
            st.write(f"Intelligence: {superhero_data2[2]}")
            st.write(f"Strength: {superhero_data2[3]}")
            st.write(f"Speed: {superhero_data2[4]}")
            st.write(f"Durability: {superhero_data2[5]}")
            st.write(f"Power: {superhero_data2[6]}")
            st.write(f"Combat: {superhero_data2[7]}")
            st.image(superhero_data2[24])
        else:
            st.write("No data found.")

# Close the database connection
conn.close()
