import streamlit as st
import sqlite3

# Function to create a connection to the SQLite database
def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

# Function to create a table in the database if it doesn't exist
def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'Not Started',
        priority TEXT DEFAULT 'Medium',
        estimated_hours INTEGER DEFAULT 0,
        milestones TEXT,
        meta_tags TEXT,
        issues TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Function to add a new project
def add_project(project_name, description, priority, estimated_hours, milestones, meta_tags, issues):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
    INSERT INTO projects (project_name, description, priority, estimated_hours, milestones, meta_tags, issues)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (project_name, description, priority, estimated_hours, milestones, meta_tags, issues))
    conn.commit()
    conn.close()

# Function to retrieve all projects
def get_projects():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM projects')
    projects = c.fetchall()
    conn.close()
    return projects

# Function to delete a project
def delete_project(project_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('DELETE FROM projects WHERE project_id = ?', (project_id,))
    conn.commit()
    conn.close()

# Create the database and table when the app starts
create_table()

# Streamlit app layout
st.title('Comprehensive Project Management App')

# Tabs for navigation
tab1, tab2 = st.tabs(["Projects", "Add New Project"])

# Display existing projects
with tab1:
    st.subheader('List of Projects')
    projects = get_projects()
    if projects:
        for project in projects:
            st.markdown(f"**Project Name**: {project[1]}")
            st.markdown(f"**Description**: {project[2]}")
            st.markdown(f"**Status**: {project[3]}")
            st.markdown(f"**Priority**: {project[4]}")
            st.markdown(f"**Estimated Hours**: {project[5]}")
            st.markdown(f"**Milestones**: {project[6]}")
            st.markdown(f"**Meta Tags**: {project[7]}")
            st.markdown(f"**Issues**: {project[8]}")
            st.divider()
            if st.button(f"Delete Project {project[0]}", key=f"delete_{project[0]}"):
                delete_project(project[0])
                st.success(f"Project '{project[1]}' deleted successfully!")
    else:
        st.write("No projects found.")

# Form to add a new project
with tab2:
    st.subheader('Add New Project')
    project_name = st.text_input("Project Name:")
    description = st.text_area("Project Description:")
    
    # Priority dropdown
    priority = st.selectbox("Priority", options=["Low", "Medium", "High"])
    
    # Estimated hours input
    estimated_hours = st.number_input("Estimated Hours", min_value=0, step=1)
    
    # Milestones input
    milestones = st.text_area("Project Milestones (comma-separated):")
    
    # Meta tags input
    meta_tags = st.text_input("Meta Tags (comma-separated):")
    
    # Issues input
    issues = st.text_area("Known Issues:")

    # Button to add the project
    if st.button("Add Project"):
        if project_name:
            add_project(project_name, description, priority, estimated_hours, milestones, meta_tags, issues)
            st.success(f"Project '{project_name}' added successfully!")
        else:
            st.error("Please enter a project name.")
