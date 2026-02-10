import cv2
from camera import run_camera
from detector import PersonDetector
from utils.fps import FPSCounter

def main():
    cap = cv2.VideoCapture(0)
    detector = PersonDetector()
    fps_counter = FPSCounter() # new fpsCounter

    while True:
        # capture and check if true
        ret, frame = cap.read()
        if not ret:
            break
            
        detections = detector.detect(frame) # "see" and draw bbox
        fps = fps_counter.update() # update fps once per frame
        person_count = len(detections)

        for (x1, y1, x2, y2, score) in detections:
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
