import cv2
from camera import run_camera
from detector import PersonDetector
from utils.fps import FPSCounter
from tracking.centroid_tracker import CentroidTracker
from utils.draw_overlay import draw

"""
    Captures each frame, applies YOLOv8n, COCO detects, infer position [0]- people
    Added:
        - fps counte for performance scale
        - len(detections) for people counting

    TODO:
        - reduce the pixel count of frames
            - reduce data transfer and preprocessing cost
            - or control model input resolution

        [extract meaning, reason, and behavior]
        - assign ID's to track people
        - set a persons in/out area

        - seperate panel for UI

"""
def main():
    SCALE = 0.5
    DETECTION_INTERVAL = 2
    frame_id = 0
    cap = cv2.VideoCapture(0)
    detector = PersonDetector()
    fps_counter = FPSCounter() # new fpsCounter
    tracker = CentroidTracker(max_distance=60)

    while True:
        # capture and check if true
        ret, frame = cap.read()
        if not ret:
            break
        
        h, w = frame.shape[:2] # grab h and w from [h, w, rg]
        
        SCALED_frame = cv2.resize(
            frame, 
            (int(w * SCALE), int(h * SCALE))
        )

        # frame id is inc to 1 but detections infer on even inter
        # therefore detect prev, then infer
        if frame_id % DETECTION_INTERVAL == 0:
            # moved detections to every oter frame
            # "infer" and draw bbox
            detections = detector.detect(SCALED_frame)

            """
            tracker.update(detections)
            else:
                tracker.predict()
            """
        
        frame_id += 1
        person_count = len(detections)
        fps = fps_counter.update() # update fps once per frame

        draw(frame, detections, person_count, fps, SCALE)

        cv2.imshow("People Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()