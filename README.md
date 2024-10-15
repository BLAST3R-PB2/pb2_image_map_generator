# Plazma Burst 2 Image Map Generator

![map_preview_jpg](https://github.com/user-attachments/assets/c1288255-fb26-4aef-a809-47ec238638f0)

This project is a Python script that processes images to create a corresponding map for the game **Plazma Burst 2**. It resizes images, extracts pixel colors, and generates an XML map file containing movables and triggers based on the pixel data.

## Features

- Resizes input images to a specified maximum height.
- Extracts pixel colors from the resized image and saves them in HEX format.
- Generates an XML file that includes:
  - Movable objects corresponding to pixels in the image.
  - Triggers that control the color of these pixels.

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Pillow library for image processing. You can install it via pip:

```bash
pip install Pillow
```

## Directory Structure

```
.
├── input/                   # Directory containing input images and output files
│   └── flytrap.jpeg         # Sample input image
├── output/                  # Directory where the generated XML map file will be saved
└── image_map_generator.py   # The main Python script for processing
```

## Usage

1. Clone the repository to your local machine:

```bash
git clone https://github.com/BLAST3R-PB2/pb2_image_map_generator.git
```

2. Navigate to the project directory:

```bash
cd pb2_image_map_generator
```

3. Place your input image in the `input` directory. You can rename `flytrap.jpeg` to your desired image name or replace it with your own image (just update the script accordingly).

4. Run the script:

```bash
python image_map_generator.py
```

5. The script will output:
   - A resized version of your image in the `input` directory.
   - A `pixel_colors_hex.txt` file containing the HEX values of the pixels.
   - An XML file (`image_map.xml`) in the `output` directory, which contains the map data for Plazma Burst 2.

## Configuration

- You can adjust the maximum height of the resized image by modifying the `MAX_HEIGHT` variable in the script.
- The `MAX_HEIGHT` represents the number of In Game Pixels (IGP) that will be used for the *height* of the image.
- The pixel size and player configuration can also be adjusted within the script.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is open-source and available under the [MIT License](LICENSE).
