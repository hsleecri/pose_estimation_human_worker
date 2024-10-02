import cv2
import mediapipe as mp
import os
import csv
from tqdm import tqdm  

# Process video with adjustable skeleton parameters, sampling rate, and an option to export coordinates
def process_video(video_path, file_name, save_path, thickness=10, circle_size=6, color=(0, 255, 0), export_csv=False, sampling_rate=None, coordinate_type='world'):
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    # Drawing specs for the skeleton
    landmark_spec = mp_drawing.DrawingSpec(color=color, thickness=circle_size, circle_radius=circle_size)
    connection_spec = mp_drawing.DrawingSpec(color=color, thickness=thickness)

    # Full path of the input video
    video_full_path = os.path.join(video_path, file_name)
    cap = cv2.VideoCapture(video_full_path)
    if not cap.isOpened():
        print(f"Failed to open video file {video_full_path}.")
        return

    # Get total number of frames and FPS
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate frame interval based on sampling rate
    if sampling_rate is not None and sampling_rate > 0:
        frame_interval = max(1, int(round(fps / sampling_rate)))
        output_fps = sampling_rate
    else:
        frame_interval = 1
        output_fps = fps

    # Set up the video writer for processed output
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    base_file_name, file_extension = os.path.splitext(file_name)
    output_file_name = f"{base_file_name}_processed{file_extension}"
    output_file = os.path.join(save_path, output_file_name)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, output_fps, (frame_width, frame_height))

    # CSV file for exporting skeleton coordinates (optional)
    csv_writer = None
    if export_csv:
        csv_file_name = f"{base_file_name}_landmarks_{coordinate_type}.csv"  # Include coordinate_type in the filename
        csv_full_path = os.path.join(save_path, csv_file_name)
        csv_file = open(csv_full_path, mode='w', newline='')
        csv_writer = csv.writer(csv_file)

        # Generate CSV header with landmark names
        columns = ['Frame']
        for landmark in mp_holistic.PoseLandmark:
            name = landmark.name.lower()
            columns.extend([
                f'{name}_x_{coordinate_type}',
                f'{name}_y_{coordinate_type}',
                f'{name}_z_{coordinate_type}',
                f'{name}_visibility'
            ])
        csv_writer.writerow(columns)

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        frame_number = 0
        processed_frames = 0

        # Calculate the total number of frames to process for the progress bar
        num_processed_frames = total_frames // frame_interval

        # Initialize the progress bar
        pbar = tqdm(total=num_processed_frames, desc=f'Processing {file_name}', unit='frame')

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            # Skip frames based on the frame interval
            if frame_number % frame_interval != 0:
                frame_number += 1
                continue

            # Convert frame to RGB for processing
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic.process(image)

            # Convert frame back to BGR for display
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw the skeleton if pose landmarks are detected
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_holistic.POSE_CONNECTIONS,
                    landmark_drawing_spec=landmark_spec,
                    connection_drawing_spec=connection_spec
                )

            # Export coordinates to CSV if enabled
            if export_csv:
                row = [frame_number]
                if coordinate_type == 'world':
                    landmarks = results.pose_world_landmarks.landmark if results.pose_world_landmarks else None
                elif coordinate_type == 'camera':
                    landmarks = results.pose_landmarks.landmark if results.pose_landmarks else None
                else:
                    print(f"Invalid coordinate_type: {coordinate_type}. Should be 'world' or 'camera'.")
                    return

                if landmarks:
                    for landmark in landmarks:
                        row.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
                else:
                    # Fill with None if landmarks are not detected
                    num_landmarks = len(mp_holistic.PoseLandmark)
                    row.extend([None] * num_landmarks * 4)
                csv_writer.writerow(row)

            out.write(image)
            processed_frames += 1
            pbar.update(1)  # Update the progress bar

            frame_number += 1

            # Exit on ESC key press
            if cv2.waitKey(5) & 0xFF == 27:
                break

        pbar.close()  # Close the progress bar

    # Release resources
    cap.release()
    out.release()
    if export_csv:
        csv_file.close()
    cv2.destroyAllWindows()

# Process all videos in the folder with adjustable parameters and sampling rate
def process_all_videos_in_folder(root_folder, save_path, thickness=10, circle_size=6, color=(0, 255, 0), export_csv=False, sampling_rate=None, coordinate_type='world'):
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(('.mp4', '.avi')):
                print(f"Processing {os.path.join(subdir, file)}")
                process_video(subdir, file, save_path, thickness, circle_size, color, export_csv, sampling_rate, coordinate_type)

if __name__ == "__main__":
    # Directory setup and adjustable parameters
    # root_folder = 'sample_video'  # Folder containing input videos
    root_folder = 'dataset'  # Folder containing input videos
    save_path = 'preprocessed_video'  # Folder to save processed videos
    skeleton_thickness = 8  # Adjust thickness of skeleton
    circle_radius = 5  # Adjust size of landmark circles
    skeleton_color = (255, 0, 0)  # Change skeleton color (BGR format)
    export_landmarks = True  # Set to True if you want to export coordinates to CSV
    sampling_rate = 1  # Process frames at 1 frame per second
    coordinate_type = 'world'  # Set to 'world' or 'camera' to choose coordinate type for exporting

    # Create the output directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)

    # Process videos with adjustable settings
    process_all_videos_in_folder(
        root_folder,
        save_path,
        thickness=skeleton_thickness,
        circle_size=circle_radius,
        color=skeleton_color,
        export_csv=export_landmarks,
        sampling_rate=sampling_rate,
        coordinate_type=coordinate_type
    )
