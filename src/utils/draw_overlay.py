import cv2
def draw(frame, detections, person_count, fps, SCALE):
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
        
