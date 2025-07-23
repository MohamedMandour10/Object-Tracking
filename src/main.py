import sys
import cv2

from select_box import draw_box
from tracker import get_available_trackers, initialize_tracker, update_tracker
from utils import fps_counter, draw_bounding_box, draw_status, resize_frame

def choose_tracker():
    """Prompt the user to select a tracker type."""
    available = get_available_trackers()
    if not available:
        print("No trackers available in this OpenCV build.")
        sys.exit(1)

    print("Available trackers:")
    for i, t in enumerate(available, start=1):
        print(f"  {i}. {t}")
    choice = input(f"Select tracker [1-{len(available)}]: ").strip()

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(available):
            raise ValueError()
        return available[idx]
    except ValueError:
        print("Invalid selection. Exiting.")
        sys.exit(1)


def main():
    tracker_type = choose_tracker()
    print(f"[INFO] Using tracker: {tracker_type}")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam."); sys.exit(1)

    ret, first_frame = cap.read()
    if not ret:
        print("ERROR: Could not read from webcam."); cap.release(); sys.exit(1)

    # loop until a valid in‑bounds box is drawn
    while True:
        raw_bbox = draw_box(first_frame)
        if raw_bbox is None:
            print("No bounding box selected. Exiting.")
            cap.release()
            sys.exit(0)

        bbox = tuple(int(v) for v in raw_bbox)
        try:
            tracker_state = initialize_tracker(first_frame, bbox, preferred_type=tracker_type)
            break   
        except ValueError as e:
            print(f"[ERROR] {e}")
            
            # Show error on frame and wait 4 seconds before next selection
            error_frame = first_frame.copy()
            msg = f"Box out of frame. Please draw the box again."
            error_frame = cv2.putText(error_frame, msg, (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
            cv2.imshow("Tracking - Press 'q' to quit", error_frame)
            cv2.waitKey(4000)
            cv2.destroyWindow("Tracking - Press 'q' to quit")
        except RuntimeError as e:
            print(f"[ERROR] {e}"); cap.release(); sys.exit(1)

    # start tracking loop
    tick = fps_counter()
    window_name = "Tracking - Press 'q' to quit"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = resize_frame(frame, max_width=800, max_height=600)

        success, bbox = update_tracker(tracker_state, frame)
        if success:
            frame = draw_bounding_box(frame, bbox, color=(255, 0, 0), thickness=2)

        fps = tick()
        frame = draw_status(frame, success, fps)

        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
