import cv2
from camera import run_camera
from detector import PersonDetector
from utils.fps import FPSCounter


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
    cap = cv2.VideoCapture(0)
    detector = PersonDetector()
    fps_counter = FPSCounter() # new fpsCounter

    while True:
        # capture and check if true
        ret, frame = cap.read()
        if not ret:
            break
        
        h, w = frame.shape[:2]
        SCALED_frame = cv2.resize(
            frame, 
            (int(w * SCALE), int(h * SCALE))
        )

        detections = detector.detect(SCALED_frame) # "infer" and draw bbox
        fps = fps_counter.update() # update fps once per frame
        person_count = len(detections)

        for (x1, y1, x2, y2, score) in detections:

            x1 = int(x1 / SCALE)
            y1 = int(y1 / SCALE)
            x2 = int(x2 / SCALE)
            y2 = int(y2 / SCALE)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"Person {score:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
            cv2.putText(
                frame,
                f"People: {person_count}",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )

        # draw fps
        cv2.putText( 
                frame, 
                f"FPS: {fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )
        
        cv2.imshow("People Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
