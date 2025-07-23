import cv2
# Tracker priority order
TRACKER_TYPES = ['CSRT', 'KCF', 'BOOSTING', 'MOSSE']

def create_tracker(tracker_type):
    """
    Create OpenCV tracker based on the type.
    """
    try:
        if tracker_type == 'CSRT':
            return cv2.TrackerCSRT_create()
        elif tracker_type == 'KCF':
            return cv2.TrackerKCF_create()
        elif tracker_type == 'BOOSTING':
            return cv2.legacy.TrackerBoosting_create()
        elif tracker_type == 'MOSSE':
            return cv2.legacy.TrackerMOSSE_create()
    except AttributeError:
        return None
    return None

def initialize_tracker(frame, bbox, preferred_type='CSRT'):
    """
    Initialize tracker and fallback if preferred type fails.
    Raises:
        ValueError: if bbox is outside the frame boundaries.
        RuntimeError: if no tracker can be initialized.
    """
    h, w = frame.shape[:2]
    # cast to ints
    bbox_int = tuple(int(v) for v in bbox)
    x, y, bw, bh = bbox_int

    # 1️⃣ check bounds
    if x < 0 or y < 0 or x + bw > w or y + bh > h:
        raise ValueError(f"Bounding box {bbox_int} is out of frame bounds {w}×{h}")

    # 2️⃣ try preferred tracker
    tracker = create_tracker(preferred_type)
    if tracker and tracker.init(frame, bbox_int):
        return {'tracker': tracker, 'type': preferred_type, 'bbox': bbox_int, 'initialized': True}

    # 3️⃣ fallback
    for t_type in TRACKER_TYPES:
        if t_type == preferred_type:
            continue
        tracker = create_tracker(t_type)
        if tracker and tracker.init(frame, bbox_int):
            print(f"[INFO] Fallback to {t_type} tracker.")
            return {'tracker': tracker, 'type': t_type, 'bbox': bbox_int, 'initialized': True}

    raise RuntimeError("No tracker could be initialized!")

def update_tracker(state, frame):
    """
    Update the tracker with the new frame.
    """
    if not state['initialized']:
        return False, None
    success, bbox = state['tracker'].update(frame)
    if success:
        bbox = tuple(int(v) for v in bbox)
        state['bbox'] = bbox
    return success, bbox

def reset_tracker(state, frame, bbox):
    """
    Reinitialize the tracker.
    """
    return initialize_tracker(frame, bbox, state['type'])

def get_tracker_info(state):
    """
    Return current tracker info.
    """
    return {
        'type': state['type'],
        'bbox': state['bbox'],
        'initialized': state['initialized']
    }

def get_available_trackers():
    """
    Returns a list of available trackers on this OpenCV build.
    """
    available = []
    for t in TRACKER_TYPES:
        if create_tracker(t) is not None:
            available.append(t)
    return available

