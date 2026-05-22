Color Detection System

📌 Overview:
  The Color Detection System is a Python-based Computer Vision application that detects and identifies colors from images or live webcam feeds using OpenCV.
  
The system allows users to:
- Detect colors in real-time
- Identify nearest color names
- View RGB values
- Capture and save frames
- Freeze webcam feed for accurate selection

🚀 Features:
- Real-time webcam color detection
- Image-based color detection
- RGB value extraction
- Closest color name matching
- Double-click color selection
- Freeze/unfreeze webcam feed
- Save captured frames
- CSV-based color dataset

🛠 Technologies Used:
- Python
- OpenCV
- NumPy
- Pandas
- Computer Vision
- Image Processing

⚙️ How It Works:
1. Webcam or image is loaded.
2. User double-clicks on a pixel.
3. RGB values are extracted.
4. System compares RGB values with the dataset.
5. Closest matching color name is displayed.

▶️ How to Run:
- Install Dependencies
  - pip install -r requirements.txt
- Run with Webcam
  - python color_detection.py
- Run with Image
  - python color_detection.py --i image.jpg
- Double click to select

🎮 Controls:
- ESC -	Exit
- c	- Freeze/Unfreeze Webcam
- Shift+c	- Save Current Frame

📈 Future Enhancements
- HSV color detection
- Object tracking
- AI-based color classification
- Mobile app integration
- GUI dashboard
- Color palette generation

👨‍💻 Author:
Ajay RS

📜 License:
This project is licensed under the MIT License.
