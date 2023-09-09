
import cv2 as CV
from process import ImgProcess
from camera_manager import CamManager
from motor_control import MotorControl



device = CamManager(CV)
device.open_camera()

process = ImgProcess(device.get_camera(),CV,MotorControl())

process.start_process()


