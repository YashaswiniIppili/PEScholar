import mysql.connector
import streamlit as st
import pandas as pd

# Establish MySQL connection without specifying database initially
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password=''
)
cursor = conn.cursor()

# Create the database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS dbms_project")

# Switch to the 'dbms_project' database
conn.database = 'dbms_project'

# Create Professors, Citations, and Publications tables (if not exist)
cursor.execute('''CREATE TABLE IF NOT EXISTS professors (
                    scholar_id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255),
                    affiliation VARCHAR(255),
                    email_domain VARCHAR(255)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS citations (
                    scholar_id VARCHAR(255),
                    citedby INT,
                    citedby5y INT,
                    hindex INT,
                    hindex5y INT,
                    i10index INT,
                    i10index5y INT,
                    cites_per_year_2023 VARCHAR(10),
                    cites_per_year_2022 VARCHAR(10),
                    cites_per_year_2021 VARCHAR(10),
                    cites_per_year_2020 VARCHAR(10),
                    cites_per_year_2019 VARCHAR(10),
                    cites_per_year_2018 VARCHAR(10),
                    cites_per_year_2017 VARCHAR(10),
                    cites_per_year_2016 VARCHAR(10),
                    cites_per_year_2015 VARCHAR(10),
                    cites_per_year_2014 VARCHAR(10),
                    FOREIGN KEY (scholar_id) REFERENCES professors(scholar_id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS publications (
                    scholar_id VARCHAR(255),
                    title TEXT,
                    pub_year VARCHAR(10),
                    author TEXT,
                    journal TEXT,
                    publisher TEXT,
                    conference TEXT,
                    num_citations INT,
                    pub_url TEXT,
                    FOREIGN KEY (scholar_id) REFERENCES professors(scholar_id)
                )''')

# Commit changes
conn.commit()
conn.close()

st.title('Professor Information System')

# Establish MySQL connection to perform queries
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='dbms_project'
)
cursor = conn.cursor()

# Query all professor names from the 'professors' table
cursor.execute("SELECT name FROM professors")
professor_names = [row[0] for row in cursor.fetchall()]

# User input: Select a professor from the dropdown
selected_professor = st.selectbox('Select a professor:', professor_names)

# User input: Select information category
selected_category = st.selectbox('Select category:', ['About', 'Citations', 'Publications'])

# Function to retrieve data based on selected professor and category
def retrieve_data(selected_professor, selected_category):
    if selected_category == 'About':
        cursor.execute(f"SELECT * FROM professors WHERE name = '{selected_professor}'")
    elif selected_category == 'Citations':
        cursor.execute(f"SELECT * FROM citations WHERE scholar_id IN (SELECT scholar_id FROM professors WHERE name = '{selected_professor}')")
    elif selected_category == 'Publications':
        cursor.execute(f"SELECT * FROM publications WHERE scholar_id IN (SELECT scholar_id FROM professors WHERE name = '{selected_professor}')")

    result = cursor.fetchall()
    return result

# Display information in tabular format
if st.button('Get Information'):
    result = retrieve_data(selected_professor, selected_category)

    if result:
        st.write(f'{selected_category} for {selected_professor}:')
        if selected_category == 'About':
            df = pd.DataFrame([result[0]], columns=[desc[0] for desc in cursor.description])
        else:
            df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
        st.write(df)
    else:
        st.write('No information available.')

# Close MySQL connection
conn.close()
