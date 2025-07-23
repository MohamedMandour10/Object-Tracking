# Real-Time Object Tracker

A simple, interactive Python tool for tracking objects in real time using your webcam. Draw a box around anything in the first frame, and the app will follow it as it moves, live.

## Features
- **Easy Object Selection:** Click and drag to select what you want to track.
- **Live Tracking:** See the tracker follow your object in real time.
- **Multiple Tracking Algorithms:** Choose from CSRT, KCF, BOOSTING, or MOSSE (all built into OpenCV).
- **Performance Display:** See FPS and tracking status right on the video.
- **User Feedback:** If you make a mistake (like drawing outside the frame), you’ll see a helpful message on the screen.
- **Keyboard Controls:** Reset, quit, or save a frame with a single key.

---

## Quick Start

### 1. Install Python (3.7+)
Make sure you have Python and pip installed.

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the tracker
```bash
cd src
python main.py
```

### 4. Select what to track
- Click and drag a box around your object in the first frame.
- Press `SPACE` to confirm, `r` to reset, or `ESC` to cancel.
- The tracker will follow your object in real time.
- Press `q` to quit at any time.

---

## Controls
- **During selection:**
  - Click and drag to draw box
  - `SPACE`: Confirm selection
  - `r`: Reset selection
  - `ESC`: Cancel
- **During tracking:**
  - `q`: Quit
  - `r`: Reset and select a new object
  - `s`: Save current frame as image

---

## How does it work?
- **main.py:** Handles the webcam, user interface, and main loop.
- **select_box.py:** Lets you draw a box to pick your object.
- **tracker.py:** Handles the tracking logic and fallback if a tracker isn't available.
- **utils.py:** Drawing, FPS, and helper functions.

```
object-tracker/
├── requirements.txt
├── README.md
├── src/
│   ├── main.py
│   ├── select_box.py
│   ├── tracker.py
│   └── utils.py
```
---

## Tips
- Works best in good lighting and with clear objects.
- Try different trackers for different scenarios (CSRT = most accurate, MOSSE = fastest).
- If you draw a box that’s too big/small or out of bounds, you’ll get a clear message and can try again.

---


