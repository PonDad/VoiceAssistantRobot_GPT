'''
bot_object_detecter.py

カメラから取得したフレームに対して物体検出を行い、検出した場合にはその情報を記録します
検出された物体のバウンディングボックスと信頼度を画像上に描画します
物体が見つからない場合や60秒間の処理が終了した場合は、検出結果のリストを返します
'''

import cv2
import time, math
from pathlib import Path
from bot_motor_controller import pan_tilt, neopixels_all, neopixels_off

class Camera():
    def __init__(self):
        self.cap = cv2.VideoCapture(0) 
        self.cap.set(3, 640)  
        self.cap.set(4, 480)

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret: 
            return frame
        return None

    def release_camera(self):
        self.cap.release()

def object_detection(objects=[]):
    thres = 0.45 # Threshold to detect object
    nms = 0.2

    classNames= []
    classFile = str(Path("dnn_models/coco.names").resolve())
    with open(classFile,"rt") as f:
        classNames = f.read().rstrip("\n").split("\n")

    object_detection_weights = str(Path("dnn_models/frozen_inference_graph.pb").resolve())
    object_detection_config = str(Path("dnn_models/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt").resolve())
    
    net = cv2.dnn_DetectionModel(object_detection_weights, object_detection_config)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    recognized_objects = set()  # ユニークな物体を格納するため、setを使用

    cam = Camera()  # カメラオブジェクトを作成
    pan_tilt(0, 0)
    neopixels_all(50, 50, 50) # ネオピクセルを白で点灯

    time_start = time.perf_counter()
    time_end = 0

    while True:
        #objects=[]
        frame = cam.get_frame()  # カメラからフレームを取得
        frame = cv2.flip(frame, -1)  # カメラ画像の上下を入れ替える

        classIds, confs, bbox = net.detect(frame,confThreshold=thres,nmsThreshold=nms)

        if len(objects) == 0: 
            objects = classNames
        objectInfo =[]

        # 検出した物体のバウンディングボックスを描画する
        frame_output = frame.copy()

        if len(classIds) != 0:
            for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                className = classNames[classId - 1]
                if className in objects:
                    objectInfo.append([box,className])
                    if True:
                        cv2.rectangle(frame_output,box,color=(255,255,255),thickness=1, lineType=cv2.LINE_AA)
                        cv2.putText(frame_output,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)
                        cv2.putText(frame_output,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)

                        neopixels_all(0, 50, 0)
                        
                        print(classNames[classId - 1])
                        recognized_objects.add(classNames[classId - 1])  # ユニークな物体を追加

        if frame is not None:
            cv2.imshow("Object Detection",frame_output)

        time_end = time.perf_counter() - time_start
        moveing_pan = (math.sin(time_end*0.2)) *90
        pan_tilt(moveing_pan, 0)
        time.sleep(0.01)
        if time_end > 30:
            break

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cam.release_camera()  # カメラを解放
    cv2.destroyAllWindows()
    time.sleep(0.5)
    pan_tilt(0,0)
    time.sleep(0.5)
    neopixels_off()
    return set(recognized_objects)

if __name__ == '__main__':
    recognized_obj = object_detection()
    print(recognized_obj)