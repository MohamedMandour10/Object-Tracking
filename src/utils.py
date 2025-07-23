import cv2
import time


def fps_counter():
    """
    Generator to calculate FPS with minimal latency and no class overhead.
    
    Yields:
        function: Call `tick()` once per frame to get the current FPS.
    """
    start_time = time.time()
    frame_count = 0
    fps = 0.0

    def tick():
        nonlocal start_time, frame_count, fps
        frame_count += 1
        elapsed = time.time() - start_time
        if elapsed >= 1.0:
            fps = frame_count / elapsed
            frame_count = 0
            start_time = time.time()
        return fps if fps > 0 else 0.0

    return tick


def draw_bounding_box(frame, bbox, color=(0, 255, 0), thickness=2, copy=True):
    """
    Draw a bounding box on the frame.

    Args:
        frame: Input image
        bbox: Bounding box coordinates (x, y, w, h)
        color: BGR color
        thickness: Line thickness
        copy: Whether to draw on a copy of the frame or in-place

    Returns:
        Frame with bounding box drawn (copied or in-place)
    """
    target = frame.copy() if copy else frame
    if bbox is not None:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(target, (x, y), (x + w, y + h), color, thickness)
    return target


def draw_text(frame, text, position=(10, 30), font_scale=0.5,
              color=(255, 255, 255), thickness=2, bg_color=(0, 0, 0)):
    """
    Draw text with a background rectangle.

    Args:
        frame: Input image
        text: String to display
        position: Top-left corner (x, y)
        font_scale: Text size scale
        color: Text color
        thickness: Text thickness
        bg_color: Background color behind text

    Returns:
        Frame with text drawn
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = position

    # Background
    cv2.rectangle(frame, (x - 5, y - th - 5), (x + tw + 5, y + baseline + 5), bg_color, -1)
    # Text
    cv2.putText(frame, text, position, font, font_scale, color, thickness)
    return frame


def draw_status(frame, tracking_status, fps, bbox=None, origin=(10, 30), spacing=30):
    """
    Draw FPS, tracking status, and bounding box info.

    Args:
        frame: Input image
        tracking_status: Bool, whether tracking succeeded
        fps: Float, current frames per second
        bbox: Optional, (x, y, w, h) bounding box
        origin: Top-left start position for text
        spacing: Vertical spacing between lines

    Returns:
        Annotated frame
    """
    x, y = origin
    frame = draw_text(frame, f"FPS: {fps:.1f}", (x, y))
    status_text = "Tracking: SUCCESS" if tracking_status else "Tracking: LOST"
    status_color = (0, 255, 0) if tracking_status else (0, 0, 255)
    frame = draw_text(frame, status_text, (x, y + spacing), color=status_color)

    return frame


def resize_frame(frame, max_width=None, max_height=None):
    """
    Resize frame preserving aspect ratio, constrained by max width/height.

    Args:
        frame: Input image
        max_width: Optional max width
        max_height: Optional max height

    Returns:
        Resized frame
    """
    h, w = frame.shape[:2]
    scale_w = max_width / w if max_width and w > max_width else 1.0
    scale_h = max_height / h if max_height and h > max_height else 1.0
    scale = min(scale_w, scale_h)

    if scale < 1.0:
        new_size = (int(w * scale), int(h * scale))
        return cv2.resize(frame, new_size)
    return frame
