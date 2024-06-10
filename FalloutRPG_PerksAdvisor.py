import streamlit as st
import json
from bs4 import BeautifulSoup
from PIL import Image
import os

def filter_perks(str_value, per_value, end_value, cha_value, int_value, agi_value, lck_value, level_value, immune_to_radiation, robot, ghul):
    filtered_perks = []

    # Prepare a list of values
    values = [str_value, per_value, end_value, cha_value, int_value, agi_value, lck_value, level_value]

    # Iterate through elements and add them to the list
    for perk in perks:
        # Check if attribute requirements are met
        if check_requirements(perk["requirements"], values, immune_to_radiation, robot, ghul):
            perk["max_level"] = perk["rank"]["max"]  # Add the maximum rank level as max_level
            filtered_perks.append(perk)

    return filtered_perks

def check_requirements(requirements, values, immune_to_radiation, robot, ghul):
    # Check if all requirements are met
    for attr, value in requirements.items():
        if attr in ["Level", "immune_to_Radiation", "robot", "ghul"]:
            continue  # Skip these requirements, they are not related to attribute values
        elif attr == "STR" and values[0] < value:
            return False
        elif attr == "PER" and values[1] < value:
            return False
        elif attr == "END" and values[2] < value:
            return False
        elif attr == "CHA" and values[3] < value:
            return False
        elif attr == "INT" and values[4] < value:
            return False
        elif attr == "AGI" and values[5] < value:
            return False
        elif attr == "LCK" and values[6] < value:
            return False
        elif attr == "Level" and values[7] < value:
            return False

    # Check additional conditions
    if immune_to_radiation and not requirements.get("immune_to_Radiation", False):
        return False
    if robot and not requirements.get("robot", False):
        return False
    if ghul and not requirements.get("ghul", False):
        return False

    return True

def display_requirements(requirements):
    if not requirements:
        return ""

    requirements_text = ", ".join([f"{attr} {value}" for attr, value in requirements.items()])
    return f"Requirement: {requirements_text}"

# Load data from JSON file
with open('extracted_items.json', 'r', encoding='utf-8') as file:
    perks = json.load(file)

# Display parameters on the left side
level_value = st.sidebar.number_input("Level", value=1, min_value=1)

st.sidebar.title("S.P.E.C.I.A.L. Attributes:")
str_value = st.sidebar.number_input("Strength", value=1, min_value=1)
per_value = st.sidebar.number_input("Perception", value=1, min_value=1)
end_value = st.sidebar.number_input("Endurance", value=1, min_value=1)
cha_value = st.sidebar.number_input("Charisma", value=1, min_value=1)
int_value = st.sidebar.number_input("Intelligence", value=1, min_value=1)
agi_value = st.sidebar.number_input("Agility", value=1, min_value=1)
lck_value = st.sidebar.number_input("Luck", value=1, min_value=1)
immune_to_radiation = st.sidebar.checkbox("Resistant to radiation")
robot = st.sidebar.checkbox("Robot")
ghul = st.sidebar.checkbox("Ghul")

# Automatically filter perks based on parameter changes
filtered_perks = filter_perks(str_value, per_value, end_value, cha_value, int_value, agi_value, lck_value, level_value, immune_to_radiation, robot, ghul)

# Display the number of perks found
st.header(f"Perks Found: {len(filtered_perks)}")

# Display perks
for perk in filtered_perks:
    st.markdown("""---""")

    # Display image and description
    col1, col2 = st.columns([1, 3])
    with col1:
        img_path = perk.get("img", "")
        if img_path:
            try:
                img = Image.open(os.path.normpath(img_path))
                st.image(img, caption='', use_column_width=True)
            except Exception as e:
                st.error(f"Error loading image: {e}")
                # Display the maximum rank level

    with col2:
        st.subheader(f"{perk['name']} (Max {perk['max_level']} Lvl)")
        
        # Display description
        soup = BeautifulSoup(perk.get("description", ""), "html.parser")
        st.write(soup.get_text())

        # Display requirements
        requirements = perk.get("requirements", {})
        requirements_text = display_requirements(requirements)
        if requirements_text:
            st.write(requirements_text)

    st.markdown('</div>', unsafe_allow_html=True)
