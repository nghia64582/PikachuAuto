import numpy as np
import cv2
from time import *

class Point:
	def __init__(self,x,y):
		self.x=x
		self.y=y

start=time()

# bước 1: cắt các cell ảnh
img=cv2.imread('im1.png')
upLeft=Point(356,140)
downRight=Point(1027,607)
widthOfCell=(downRight.x-upLeft.x+1)//16
heightOfCell=(downRight.y-upLeft.y+1)//9
imgId=0
for i in range(9):
	for j in range(16):
		# khởi tạo 
		p1=Point(upLeft.x+widthOfCell*j,upLeft.y+heightOfCell*i) # điểm trái trên
		img2=img[p1.y:p1.y+heightOfCell,p1.x:p1.x+widthOfCell]
		imgId+=1
		cv2.imwrite("Cell/"+str(imgId)+".png",img2)

# bước 2: xóa đi các cell ảnh giống nhau
imageList=[]
sumOfImage={}
for i in range(1,145):
	url='Cell/'+str(i)+'.png'
	img=cv2.imread(url)
	sumOfImage[np.sum(img)]=img
imgId=0
for image in sumOfImage:
	imgId+=1
	url='Cell1/'+str(imgId)+'.png'
	cv2.imwrite(url,sumOfImage[image])

# bước 3: quy đổi ảnh về ma trận các id của các cell

img=cv2.imread('im1.png')
upLeft=Point(356,140)
downRight=Point(1027,607)
widthOfCell=(downRight.x-upLeft.x+1)//16
heightOfCell=(downRight.y-upLeft.y+1)//9
imgId=0
cellId=[[0 for i in range(16)]for j in range(9)]
for i in range(9):
	for j in range(16):
		# khởi tạo 
		p1=Point(upLeft.x+widthOfCell*j,upLeft.y+heightOfCell*i) # điểm trái trên
		img1=img[p1.y:p1.y+heightOfCell,p1.x:p1.x+widthOfCell]




print("Total time",time()-start)