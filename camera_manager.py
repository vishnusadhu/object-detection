


class CamManager:
    def __init__(self,cv) -> None:
        self.cv = cv
        self.cam = None
        
    def open_camera(self):
        self.cam = self.cv.VideoCapture(0)

    def get_camera(self):
        return self.cam
    

    def close_camera(self):
        pass
        