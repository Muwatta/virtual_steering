Hey there! This project transforms your hands into a game controller using a webcam and MediaPipe hand tracking. Perfect for developers, educators, and startup founders looking to experiment with AI-driven interfaces. Built for a hand-posing game, it maps gestures to arrow keys and spacebar inputs, ideal for teaching or creating innovative tech demos.
Features

Controls:

Left hand fist → Brake (LEFT_ARROW)
Right hand open palm → Gas (RIGHT_ARROW)
Left hand index up → Up (UP_ARROW)
Right hand index up → Down (DOWN_ARROW)
Thumbs up (any hand) → Boost (SPACE)
Two fingers (any hand) → Pause
Three fingers (any hand) → Continue
Four fingers (any hand) → Exit/Quit


Tech Stack: Python, OpenCV, MediaPipe, directkeys for input simulation.
Setup: Runs on a webcam, no physical controller needed!

Getting Started

Install Dependencies:

pip install opencv-python mediapipe


Run the Code:

Ensure your webcam is connected.
Execute python main.py.


Play:

Use hand gestures in front of the webcam.
ESC key quits the program.



Usage

Test with games supporting arrow keys and spacebar (e.g., browser platformers).
Adjust gestures in main.py for custom controls.
Great for live workshops or LinkedIn content showcasing AI innovation!

Contributing
Love this? Fork it, tweak the gestures, or add features. Share your ideas—perfect for mid-level pros or students learning AI!
License
MIT - Feel free to use and adapt!
Got a game in mind to test this with? Let’s make it even better!