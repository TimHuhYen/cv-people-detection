import math


"""
    Tracks all people in detections and assigns new best_id's
    based on the closest fit from the original position

    # creates centroids
    # checks each persons distance
    # finds best fit [best_id]
    # else creates new id
"""
class CentroidTracker:
    def __init__(self, max_distance=50):
        self.next_id = 0                 # 
        self.objects = {}                # id -> (cx, cy)
        self.max_distance = max_distance # tolerance level to be considered same person

    def _distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
    
    def update(self, detections):
        new_objects = {}

        # compute centroids for new detections
        centroids = []
        for (x1, y1, x2, y2, _) in detections:
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            centroids.append((cx, cy))

        used_ids = set()

        # try to match old centroids to new centroids
        for cx, cy in centroids:
            best_id = None
            best_dist = self.max_distance

            # find best match
            for obj_id, (ox, oy) in self.objects.items():
                if obj_id in used_ids:
                    continue
                
                d = self._distance((cx, cy), (ox, oy))
                if d < best_dist:
                    best_dist = d
                    best_id = obj_id

            # either assign or create new best_id to fit
            if best_id is not None:
                new_objects[best_id] = (cx, cy)
                used_ids.add(best_id)
            else:
                new_objects[self.next_id] = (cx, cy)
                self.next_id += 1

        # replace old objects
        self.objects = new_objects
        return self.objects
                