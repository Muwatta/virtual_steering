import cv2
import mediapipe as mp
from directkeys import PressKey, ReleaseKey, LEFT_ARROW, RIGHT_ARROW, UP_ARROW, DOWN_ARROW, SPACE

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Track pressed states
gas_pressed = False
brake_pressed = False
boost_pressed = False
up_pressed = False
down_pressed = False

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip and convert to RGB
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_image)

    # Initialize hand-specific variables
    left_hand_fingers = None
    right_hand_fingers = None

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Determine hand type
            hand_label = handedness.classification[0].label  # 'Left' or 'Right'

            # Count extended fingers
            fingers_up = []
            tip_ids = [4, 8, 12, 16, 20]

            # Thumb
            if hand_label == 'Right':
                if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
                    fingers_up.append(1)
                else:
                    fingers_up.append(0)
            else:  # Left hand
                if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x:
                    fingers_up.append(1)
                else:
                    fingers_up.append(0)

            # Other fingers
            for id in range(1, 5):
                if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
                    fingers_up.append(1)
                else:
                    fingers_up.append(0)

            # Assign fingers to respective hand
            if hand_label == 'Left':
                left_hand_fingers = fingers_up
            else:
                right_hand_fingers = fingers_up

        # Single-hand controls (RIGHT, SPACE)
        if len(results.multi_hand_landmarks) == 1:
            total_fingers = sum(left_hand_fingers or right_hand_fingers)

            # ✋ Open palm = GAS (RIGHT_ARROW)
            if total_fingers == 5 and not gas_pressed:
                PressKey(RIGHT_ARROW)
                gas_pressed = True
                print("🚗 Gas ON")
            elif total_fingers != 5 and gas_pressed:
                ReleaseKey(RIGHT_ARROW)
                gas_pressed = False
                print("🚗 Gas OFF")

            # 👍 Thumbs up = BOOST (SPACE)
            fingers = left_hand_fingers or right_hand_fingers
            if fingers[0] == 1 and sum(fingers[1:]) == 0 and not boost_pressed:
                PressKey(SPACE)
                boost_pressed = True
                print("🚀 Boost ON")
            elif (fingers[0] == 0 or sum(fingers[1:]) != 0) and boost_pressed:
                ReleaseKey(SPACE)
                boost_pressed = False
                print("🚀 Boost OFF")

        # Two-hand controls (UP, DOWN, LEFT)
        if len(results.multi_hand_landmarks) == 2 and left_hand_fingers and right_hand_fingers:
            # ☝️ Left hand index up = UP_ARROW
            if left_hand_fingers[1] == 1 and sum(left_hand_fingers[0:1] + left_hand_fingers[2:]) == 0 and not up_pressed:
                PressKey(UP_ARROW)
                up_pressed = True
                print("⬆️ Up ON")
            elif (left_hand_fingers[1] == 0 or sum(left_hand_fingers[0:1] + left_hand_fingers[2:]) != 0) and up_pressed:
                ReleaseKey(UP_ARROW)
                up_pressed = False
                print("⬆️ Up OFF")

            # ☝️ Right hand index up = DOWN_ARROW
            if right_hand_fingers[1] == 1 and sum(right_hand_fingers[0:1] + right_hand_fingers[2:]) == 0 and not down_pressed:
                PressKey(DOWN_ARROW)
                down_pressed = True
                print("⬇️ Down ON")
            elif (right_hand_fingers[1] == 0 or sum(right_hand_fingers[0:1] + right_hand_fingers[2:]) != 0) and down_pressed:
                ReleaseKey(DOWN_ARROW)
                down_pressed = False
                print("⬇️ Down OFF")

            # ✊ Left hand fist = LEFT_ARROW
            if sum(left_hand_fingers) == 0 and not brake_pressed:
                PressKey(LEFT_ARROW)
                brake_pressed = True
                print("🛑 Brake ON")
            elif sum(left_hand_fingers) != 0 and brake_pressed:
                ReleaseKey(LEFT_ARROW)
                brake_pressed = False
                print("🛑 Brake OFF")

            # ✋ Right hand open palm = RIGHT_ARROW
            if sum(right_hand_fingers) == 5 and not gas_pressed:
                PressKey(RIGHT_ARROW)
                gas_pressed = True
                print("🚗 Gas ON")
            elif sum(right_hand_fingers) != 5 and gas_pressed:
                ReleaseKey(RIGHT_ARROW)
                gas_pressed = False
                print("🚗 Gas OFF")

    # Release keys if no hands or insufficient hands detected
    if not results.multi_hand_landmarks or len(results.multi_hand_landmarks) < 2:
        if up_pressed:
            ReleaseKey(UP_ARROW)
            up_pressed = False
            print("⬆️ Up OFF")
        if down_pressed:
            ReleaseKey(DOWN_ARROW)
            down_pressed = False
            print("⬇️ Down OFF")
        if brake_pressed:
            ReleaseKey(LEFT_ARROW)
            brake_pressed = False
            print("🛑 Brake OFF")
        if gas_pressed and len(results.multi_hand_landmarks) != 1:
            ReleaseKey(RIGHT_ARROW)
            gas_pressed = False
            print("🚗 Gas OFF")
        if boost_pressed and len(results.multi_hand_landmarks) != 1:
            ReleaseKey(SPACE)
            boost_pressed = False
            print("🚀 Boost OFF")

    cv2.imshow("Virtual Steering", image)

    if cv2.waitKey(5) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()