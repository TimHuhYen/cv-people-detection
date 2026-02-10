from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_path="yolov8n.pt", conf=0.4):
        # loads pretrainded model as class
        self.model = YOLO(model_path)
        # saves confidence score
        self.conf = conf

    def detect (self, frame):
        results = self.model(
            frame,
            conf=self.conf,
            imgsz=416, # lowered to increase fps
            verbose=False
        )

        detections = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if cls ==0: # coco class 0 = person
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    score = float(box.conf[0])
                    detections.append((x1, y1, x2, y2, score))

        return detections