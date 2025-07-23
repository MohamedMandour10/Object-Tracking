"""
i used functions instead of classes to make it simple and reduce the latency (state overhead).
used global variables to keep track of the state of the selection.
the docstring of functions are generated using Windsurf.
"""

import cv2
import time
_bbox = None
_drawing = False
_start_point = None
_display_frame = None
_original_frame = None


def _mouse_callback(event, x, y, flags, param):
    global _drawing, _start_point, _bbox, _display_frame, _original_frame

    # Left mouse button is pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        _drawing = True
        _start_point = (x, y)
        _bbox = None

    # Mouse is moving while left button is pressed
    elif event == cv2.EVENT_MOUSEMOVE and _drawing:
        end_point = (x, y)
        _display_frame = _original_frame.copy()
        cv2.rectangle(_display_frame, _start_point, end_point, (0, 255, 0), 2)

    # Left mouse button is released
    elif event == cv2.EVENT_LBUTTONUP:
        _drawing = False
        end_point = (x, y)
        x1, y1 = _start_point
        x2, y2 = end_point
        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x2 - x1), abs(y2 - y1)

        # Ensure the selection is not too small
        if w > 10 and h > 10:
            _bbox = (float(x), float(y), float(w), float(h))
            cv2.rectangle(_display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            _bbox = None
            print("Selection too small. Please try again.")
            _display_frame = _original_frame.copy()


def draw_box(frame, timeout_sec=30):
    """
    Interactive bounding box selector with a countdown timer.

    Args:
        frame (ndarray): Input frame from which to select object.
        timeout_sec (int): Max time to wait for user input in seconds.

    Returns:
        tuple or None: Bounding box in (x, y, w, h) format.
    """
    global _original_frame, _display_frame, _bbox

    _original_frame = frame.copy()
    _display_frame = frame.copy()
    _bbox = None

    win_name = "Select Object (SPACE: Confirm, R: Reset, ESC: Cancel)"
    cv2.namedWindow(win_name)
    cv2.setMouseCallback(win_name, _mouse_callback)

    print("\nInstructions:\n 1. Click and drag to draw box\n 2. SPACE to confirm\n 3. R to reset\n 4. ESC to cancel")

    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        remaining = int(timeout_sec - elapsed)

        if remaining <= 0:
            print(f"Timeout: No selection made in {timeout_sec} seconds.")
            _bbox = None
            break

        display = _display_frame.copy()

        # Draw countdown timer on screen
        cv2.putText(display, f"Time left: {remaining}s", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow(win_name, display)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            print("Selection cancelled.")
            _bbox = None
            break
        elif key == ord('r'):
            _display_frame = _original_frame.copy()
            _bbox = None
            print("Selection reset.")
            start_time = time.time()  # Reset timer after reset
        elif key == ord(' '):  # SPACE
            if _bbox:
                print(f"Object selected: {_bbox}")
                break
            else:
                print("No valid selection yet.")

    cv2.destroyWindow(win_name)
    return _bbox



# def main():
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     cap.release()

#     if not ret:
#         print("Failed to capture frame from webcam.")
#         return

#     bbox = draw_box(frame, timeout_sec=20)

#     if bbox:
#         (x, y, w, h) = map(int, bbox)
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
#         cv2.imshow("Selected BBox", frame)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#     else:
#         print("No bounding box selected.")

# if __name__ == "__main__":
#     main()