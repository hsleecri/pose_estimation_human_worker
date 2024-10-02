# Video Pose Estimation and Skeleton Drawing with MediaPipe

This project processes videos to extract human pose landmarks using MediaPipe's Pose solution. It draws skeletons on the videos and exports the pose landmarks to CSV files with anatomically named features.

## Features

- **Pose Estimation**: Uses MediaPipe's Pose solution to detect human pose landmarks in videos.
- **Skeleton Drawing**: Draws skeletons on the processed videos with adjustable parameters for thickness, color, and circle size.
- **CSV Export**: Exports pose landmarks to CSV files with each row representing a frame and columns representing XYZ coordinates and visibility of named landmarks.

## Table of Contents

- [Installation](#installation)
  - [Python Version](#python-version)
  - [Installing Dependencies](#installing-dependencies)
- [Usage](#usage)
  - [Directory Setup](#directory-setup)
  - [Adjustable Parameters](#adjustable-parameters)
- [Running the Script](#running-the-script)
- [CSV Output Format](#csv-output-format)
  - [Landmark Names](#landmark-names)
  - [Coordinate System Explanation](#coordinate-system-explanation)
    - [Example of Landmark Coordinates](#example-of-landmark-coordinates) 
- [Examples](#examples)
- [Acknowledgments](#acknowledgments)

## Installation

### Python Version

This project requires **Python 3.8**. Ensure you have Python 3.8 installed on your system.

### Installing Dependencies

Install the required packages listed in `requirements.txt` by running:

`pip install -r requirements.txt`

The `requirements.txt` includes:
`opencv-python  # cv2 mediapipe matplotlib Pillow tqdm`

## Usage

### Directory Setup

* **Input Videos:** Place the videos you want to process in the sample_video directory. Supported formats are .mp4 and .avi.
* **Output Directory:** The processed videos and CSV files will be saved in the preprocessed_video directory. The script will create this directory if it doesn't exist.

### Adjustable Parameters

You can adjust the following parameters at the beginning of the script or modify them as arguments when calling the processing functions:

* **root_folder:** Directory containing the input videos (default is 'sample_video').
* **save_path:** Directory where the processed videos and CSV files will be saved (default is 'preprocessed_video').
* **skeleton_thickness:** Thickness of the skeleton lines drawn on the video (default is 8).
* **circle_radius:** Radius of the circles drawn at each landmark point (default is 5).
* **skeleton_color:** Color of the skeleton in BGR format (default is (255, 0, 0) for blue).
* **export_landmarks:** Set to True to export the landmark data to CSV files (default is True).
* **sampling_rate:** The desired frames per second (FPS) at which to process the video.
* **coordinate_type**: Set to 'world' or 'camera' to choose the coordinate type for exporting (default is 'world').

## Running the Script

### Direct Execution:

Run the script directly from the command line:

`python main.py`

## CSV Output Format

The CSV files generated will have the following structure:

Rows: Each row represents a frame in the video.
Columns: The first column is the frame number (Frame), followed by the XYZ coordinates and visibility for each landmark with their anatomical names.

Example of CSV Header:

`Frame, nose_x, nose_y, nose_z, nose_visibility, left_eye_inner_x, left_eye_inner_y, left_eye_inner_z, left_eye_inner_visibility, ..., right_heel_visibility`

### Landmark Names

MediaPipe Pose detects 33 landmarks on the human body, named as follows:

* Face:nose
  `left_eye_inner, left_eye, left_eye_outer right_eye_inner, right_eye, right_eye_outer left_ear, right_ear mouth_left, mouth_right`
* Upper Body:
  `left_shoulder, right_shoulder left_elbow, right_elbow left_wrist, right_wrist left_pinky, right_pinky left_index, right_index left_thumb, right_thumb`
* Torso:
  `left_hip, right_hip`
* Lower Body:
  `left_knee, right_knee left_ankle, right_ankle left_heel, right_heel left_foot_index, right_foot_index`

Each landmark includes:

`_x`: X-coordinate (normalized between 0 and 1).
`_y`: Y-coordinate (normalized between 0 and 1).
`_z`: Z-coordinate (depth, normalized between 0 and 1).
_visibility: Visibility score of the landmark (range from 0 to 1).

### Coordinate System Explanation

The coordinates exported to the CSV file can be in either world coordinates or camera coordinates, depending on the 'coordinate_type' parameter.

**World Coordinates** (coordinate_type='world')

- Units: Meters (m).
- Origin: Center of the hips (pelvis).
- Axes:
  - X-axis (Left-Right):
    - Positive X: Right side of the person (from the person's perspective).
    - Negative X: Left side of the person.
  - Y-axis (Up-Down):
    - Positive Y: Upward direction from the person's center.
    - Negative Y: Downward direction from the person's center.
  - Z-axis (Depth):
    - Positive Z: Farther away from the camera.
    - Negative Z: Closer to the camera.


**Camera Coordinates** (coordinate_type='camera')

- Units: Normalized image coordinates (range [0.0, 1.0]).
- Origin: Top-left corner of the image.
- Axes:
  - X-axis (Horizontal Position):
    - 0.0: Left edge of the image.
    - 1.0: Right edge of the image.
  - Y-axis (Vertical Position):
    - 0.0: Top edge of the image.
    - 1.0: Bottom edge of the image.
  - Z-axis (Depth):
    - Represents the landmark's depth relative to the image plane.

**Example of Landmark Coordinates**
Suppose we have the following world coordinates for the nose landmark:
 - x = 0.034
 - y = -0.125
 - z = -0.567
 - visibility = 0.98

**Interpretation:**
- x = 0.034:
  - The nose is 3.4 cm to the right of the body's center (from the person's perspective).
    - Positive X indicates a position to the right.
- y = -0.125:
  - The nose is 12.5 cm below the body's center.
    - Negative Y indicates a position downward.
- z = -0.567:
  - The nose is 56.7 cm closer to the camera from the body's center.
    - Negative Z indicates proximity to the camera.
- visibility = 0.98:
  - High confidence in the landmark detection.

**Note:**
- The X, Y and Z values are in meters.
- Positive and negative signs indicate direction relative to the body's center:
  - X-axis:
    - Positive: Right side.
    - Negative: Left side.
- Y-axis:
    - Positive: Upward.
    - Negative: Downward.
- Z-axis:
    - Positive: Farther from the camera.
    - Negative: Closer to the camera.

**Visibility Values**
- Visibility: A value between 0 and 1 indicating how confident the model is that the landmark is visible in the image.
  - Values closer to 1 mean higher confidence.

**Additional Examples:**
- If x = -0.050:
  - The landmark is 5.0 cm to the left of the body's center.
- If y = 0.100:
  - The landmark is 10 cm above the body's center.
- If z = -0.600:
  - The landmark is 60 cm closer to the camera.

## Examples

To process a single video, place it in the sample_video directory and run the script. The progress bar will display processing information.

`Processing sample_video/example_video.mp4 Processing example_video.mp4: 100%|██████████| 500/500 [00:20<00:00, 24.50frame/s]`

## Acknowledgments

- MediaPipe: This project utilizes Google's MediaPipe framework for pose estimation.
- OpenCV: Used for video reading, writing, and image processing.
- tqdm: Provides the progress bar for monitoring processing progress.
