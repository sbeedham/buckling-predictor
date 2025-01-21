import streamlit as st
import math

# Function to calculate the value
def calculate_value(val1, val2, val3, val4, val5, val6):

    try:
        # Convert all input values to appropriate types
        size = int(val1)
        spacing = float(val2)
        shoulder = int(val3)
        line = float(val4) + 5
        sft = float(val5)
        youngs = 215000
        length = 10
        fastening = val6
        thermal = 0.0000115

        # Set inertia and area based on size
        if size == 41:
            inertia = 2670000
            area = 5190
        elif size == 47:
            inertia = 3000000
            area = 5928
        elif size == 50:
            inertia = 3300000
            area = 6470
        elif size == 53:
            inertia = 4540000
            area = 6749
        elif size == 60:
            inertia = 4900000
            area = 7770
        elif size == 68:
            inertia = 6020000
            area = 8602

        # Set torsion based on fastening type
        if fastening == "Dogspike and Timber":
            torsion = 2000
        elif fastening == "Screwspike and Timber":
            torsion = 3500
        elif fastening == "Elastic and Timber":
            torsion = 5000
        elif fastening == "Elastic and Steel":
            torsion = 7000
        elif fastening == "Elastic and Concrete":
            torsion = 9000

        # Set lateral stiffness based on shoulder
        if shoulder == 0:
            lateral = 1100
        elif shoulder == 100:
            lateral = 2500
        elif shoulder == 200:
            lateral = 3500
        elif shoulder == 300:
            lateral = 4000

        # Calculations
        rail = ((2 * 3.14159265 * 3.14159265 * youngs * inertia) / (length * length)) / 1000000
        sleeper = ((3.14159265 * 3.14159265 * torsion) / ((10 * (spacing / 1000)))) * (math.sqrt((3.14159265 * length) / (line / 1000)))
        ballast = (lateral * length * length) / (3.14159265 * 3.14159265 * (line / 1000))
        force = rail + sleeper + ballast
        temp = force / (2 * youngs * area * thermal)
        result = sft + temp

        return result

    except ValueError:
        # In case of invalid input
        st.error("Please enter valid numbers.")
        return None

# Streamlit-based UI
st.title("Buckling Predictor Tool")

# Inputs
size = st.selectbox("Select Rail Size (kg)", [41, 47, 50, 53, 60, 68])
spacing = st.text_input("Sleeper Spacing (mm)")
shoulder = st.selectbox("Ballast Shoulder (mm)", [0, 100, 200, 300])
misalignment = st.text_input("Initial Misalignment (mm)")
sft = st.text_input("Stress Free Temperature (C)")
fastening = st.selectbox("Fastening Type", ["Dogspike and Timber", "Screwspike and Timber", "Elastic and Timber", "Elastic and Steel", "Elastic and Concrete"])

# When the submit button is clicked
if st.button("Submit"):
    result = calculate_value(size, spacing, shoulder, misalignment, sft, fastening)
    if result is not None:
        st.success(f"Predicted Buckling Temperature: {result:.2f} °C")
