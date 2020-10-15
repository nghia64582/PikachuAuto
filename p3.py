import numpy as np
from time import *
import cv2
import pyautogui as pa

class segment:
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Point:
    def __init__(self,x1,y1):
        self.x1 = x1
        self.y1 = y1

def differenceFromTwoImage(img1,img2):
    # tìm độ khác nhau giữa 2 bức ảnh
    img2=cv2.resize(img2,(img1.shape[1],img1.shape[0]),interpolation=cv2.INTER_AREA)
    # print(img1.shape)
    # print(img2.shape)
    #--- take the absolute difference of the images ---
    res = cv2.absdiff(img1, img2)
    #--- convert the result to integer type ---
    res = res.astype(np.uint8)
    # #--- find percentage difference based on number of pixels that are not zero ---
    percentage = np.count_nonzero(res) * 100/ res.size
    return percentage

def findImage(img1,img2):
    # tìm tọa độ ảnh img2 trong ảnh img1
    # (luôn trả về 1 tọa độ gần đúng nhất)
    # nếu muốn đúng tuyệt đối phải kiểm tra thêm
    # hoặc nếu cần gần đúng có thể dùng hàm kiểm
    # tra độ giống nhau giữa 2 bức ảnh ở dưới
    coor=cv2.matchTemplate(img1,img2,cv2.TM_CCORR_NORMED)
    res=np.unravel_index(coor.argmax(),coor.shape)
    return res

def findUpleftCoordinate():
    # tìm tọa độ góc trái trên, lưu vào biến global upleftCoor
    global upleftCoor
    upleftCoor=(0,0)
    cornerCoor=(151,68)
    screen=cv2.cvtColor(np.array(pa.screenshot()),cv2.COLOR_RGB2BGR)
    side=cv2.imread('side.png')
    res=findImage(screen,side)
    print(res)
    # screen[res[0]][res[1]]=np.array([0,0,0])
    cv2.rectangle(screen,(res[1],res[0]),(res[1]+len(side[0]),res[0]+len(side)),(0,0,255),1)
    upLeftCoor=(res[1]+151,res[0]+68)
    cv2.rectangle(screen,upLeftCoor,upLeftCoor,(0,0,255),1)
    # cv2.rectangle(screen,(upLeftCoor[1],upLeftCoor[0]),(upLeftCoor[1],upLeftCoor[0]),(0,0,255),1)
    cv2.imwrite("Result1.png",screen)
    tg=screen[res[0]:res[0]+len(side),res[1]:res[1]+len(side[0])]
    print(side.shape)
    print(tg.shape)
    print(differenceFromTwoImage(side,tg))
    return upLeftCoor

upLeftCoor=findUpleftCoordinate()
print(upLeftCoor)
(206,61)
(357,119)
(356,154)