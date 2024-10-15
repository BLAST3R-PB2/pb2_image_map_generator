from PIL import Image
import os
import math

# Set the input and output folders
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# File paths
IMAGE_FILE_NAME = os.path.join(INPUT_FOLDER, "flytrap.jpeg")
RESIZED_FILE_NAME = os.path.join(INPUT_FOLDER, "flytrap_resized.jpg")
HEX_FILE_NAME = os.path.join(INPUT_FOLDER, 'pixel_colors_hex.txt')
MAP_FILE_NAME = os.path.join(OUTPUT_FOLDER, "image_map.xml")

## CHANGE THIS VALUE TO INCREASE PIXEL COUNT
MAX_HEIGHT = 50

# Open the image
img = Image.open(IMAGE_FILE_NAME)

# Resize the image if needed
if img.height > MAX_HEIGHT:
    new_size = (img.width // (img.height // MAX_HEIGHT), img.height // (img.height // MAX_HEIGHT))  # Reduce size
    img_resized = img.resize(new_size)
else:
    img_resized = img

# Save the resized image in the input folder
img_resized.save(RESIZED_FILE_NAME)

# Get pixel data
pixel_data = img_resized.load()
width, height = img_resized.size

# Create a list to store the hex color data of every pixel
hex_colors = []

for y in range(height):
    for x in range(width):
        r, g, b = pixel_data[x, y]  # Get RGB values
        hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)  # Convert to HEX
        hex_colors.append(hex_color)

# Save the hex colors to a file in the input folder
with open(HEX_FILE_NAME, 'w') as f:
    for color in hex_colors:
        f.write(color + '\n')

print(f"Resized image saved as '{RESIZED_FILE_NAME}' and HEX color data saved in '{HEX_FILE_NAME}'.")

# Create PB2 Map
img = Image.open(RESIZED_FILE_NAME)

# Create the movables (pixels)
pixel_size = 10
width, height = img.size

# Calculate the offset to center the grid on (0, 0)
x_offset = -(width // 2) * pixel_size
y_offset = -(height // 2) * pixel_size

# Start writing the XML data
xml_data = []

PLAYER_NAME = "BLAST3R"

# Dynamic zoom calculation
reference_zoom = 25   # The zoom percentage that works well
reference_height = 100  # The height where zoom=30 is comfortable

ZOOM_PERCENTAGE = math.ceil(reference_zoom * (reference_height / MAX_HEIGHT))
ZOOM_PERCENTAGE = min(100, ZOOM_PERCENTAGE)

PLAYER_LOCATION = height * 10 // 2 + 150

player_data = f'''
<player uid="#player*1" x="0" y="{PLAYER_LOCATION}" tox="0" toy="0" hea="130" hmax="130" team="0" side="1" char="77" incar="-1" botaction="0" ondeath="-1" />
<box x="-100" y="{PLAYER_LOCATION}" w="200" h="1600" m="0" />
<trigger uid="#trigger*999999" x="-100" y="400" enabled="true" maxcalls="1" actions_1_type="51" actions_1_targetA="{ZOOM_PERCENTAGE}" actions_1_targetB="0" actions_2_type="52" actions_2_targetA="#player*1" actions_2_targetB="{PLAYER_NAME}" actions_3_type="-1" actions_3_targetA="0" actions_3_targetB="0" actions_4_type="-1" actions_4_targetA="0" actions_4_targetB="0" actions_5_type="-1" actions_5_targetA="0" actions_5_targetB="0" actions_6_type="-1" actions_6_targetA="0" actions_6_targetB="0" actions_7_type="-1" actions_7_targetA="0" actions_7_targetB="0" actions_8_type="-1" actions_8_targetA="0" actions_8_targetB="0" actions_9_type="-1" actions_9_targetA="0" actions_9_targetB="0" actions_10_type="-1" actions_10_targetA="0" actions_10_targetB="0" />
<timer uid="#timer*999999" x="-100" y="450" enabled="true" maxcalls="1" target="#trigger*999999" delay="0" />
'''
# Add the player data to the file
xml_data.append(player_data)

# Iterate through the grid
uid = 1  # Start UID for each movable (door)
for i in range(height):
    for j in range(width):
        # Calculate the x and y position for each movable
        x = j * pixel_size + x_offset
        y = i * pixel_size + y_offset
        
        # Create the XML element for the movable
        xml_element = f'<door uid="#door*{uid}" x="{x}" y="{y}" w="{pixel_size}" h="{pixel_size}" moving="false" tarx="0" tary="0" maxspeed="10" vis="true" attach="-1" />'
        xml_data.append(xml_element)

        uid += 1  # Increment UID for the next movable

# Write the first part of the XML file in the output folder
with open(MAP_FILE_NAME, 'w') as file:
    file.write('\n'.join(xml_data))

# STEP 2

xml_data = []

colors = []

uid = 1

# coords to start placing the triggers & timers
y_value = -700
x_value = -4000

with open(HEX_FILE_NAME, "r") as file:
    for line in file:
        color = line.strip()
        # Save the colors to a list
        colors.append(color)

# A trigger has 10 actions, making it possible to control 10 pixels with a single trigger
batch_size = 10

# Loop through the frame data in batches
for i in range(0, len(colors), batch_size):
    # Create a trigger for this batch of 10 pixels (or fewer, if at the end)
    batch = colors[i:i + batch_size]

    # Initialize actions for this batch
    actions = []

    # Fill the action slots for the trigger (up to 10 actions)
    for j, hex_color in enumerate(batch):
        actions.append(f'actions_{j+1}_type="71" actions_{j+1}_targetA="#door*{i+j+1}" actions_{j+1}_targetB="{hex_color}"')

    # Fill the remaining action slots with "-1" for unused slots
    for j in range(len(batch), 10):
        actions.append(f'actions_{j+1}_type="-1" actions_{j+1}_targetA="0" actions_{j+1}_targetB="0"')

    # Join the actions into a single string
    actions_str = " ".join(actions)

    # Create the trigger element
    trigger_element = f'<trigger uid="#trigger*{uid}" x="{x_value}" y="{y_value}" enabled="true" maxcalls="1" {actions_str} />'

    # Create the timer element
    timer_element = f'<timer uid="#timer*{uid}" x="{x_value-50}" y="{y_value}" enabled="true" maxcalls="1" target="#trigger*{uid}" delay="0"/>'

    # place the leading triggers below the trigger that came before
    y_value += 50

    # increment the uid to make sure the ids are unique
    uid += 1

    xml_data.append(trigger_element)
    xml_data.append(timer_element)

# Append the second part of the XML file to the output folder
with open(MAP_FILE_NAME, 'a') as file:
    file.write('\n'.join(xml_data))

print(f"Map {MAP_FILE_NAME} created successfully.")
