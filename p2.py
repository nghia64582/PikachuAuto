import numpy as np
from time import *
import cv2
import pyautogui as pa
from random import *

class Point:
	def __init__(self,x,y):
		self.x=x
		self.y=y

def findImage(img1,img2):
	# tìm tọa độ ảnh img2 trong ảnh img1
	# (luôn trả về 1 tọa độ gần đúng nhất)
	# nếu muốn đúng tuyệt đối phải kiểm tra thêm
	# hoặc nếu cần gần đúng có thể dùng hàm kiểm
	# tra độ giống nhau giữa 2 bức ảnh ở dưới
	coor=cv2.matchTemplate(img1,img2,cv2.TM_CCORR_NORMED)
	res=np.unravel_index(coor.argmax(),coor.shape)
	return res
	
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

def inside(a,x,y):
	# kiểm tra xem tọa độ x,y có nằm trong a ko
	return 0<=x<=len(a)-1 and 0<=y<=len(a[0])-1

def imageToIdMatrix(image):
	# bước 2: biến image thành ma trận cell id
	global sumSet,upLeftCoor
	cellWidth=42
	cellHeight=52
	a=[[0 for i in range(16)]for j in range(9)]
	cellId={} # key: sum of cell, value: id
	nowId=0
	for i in range(9):
		for j in range(16):
			p=Point(upLeftCoor[1]+cellHeight*i,upLeftCoor[0]+cellWidth*j)
			img=image[p.x:p.x+cellHeight,p.y:p.y+cellWidth]
			# cv2.imshow('tg',img)
			# cv2.waitKey()
			# if i==j==1:
			# 	cv2.imshow('a',img)
			# 	cv2.waitKey()
			s=np.sum(img)
			if s not in sumSet:
				# print('not in')
				continue
			if s not in cellId:
				nowId+=1
				cellId[s]=nowId
			a[i][j]=cellId[s]
	# a=np.array(a)
	for i in range(len(a)):
		a[i]=[0]+a[i]+[0]
	a=[[0 for i in range(len(a[0]))]]+a+[[0 for i in range(len(a[0]))]]
	return a

def check(a,x,y):
	# kiểm tra xem loang từ một ô x,y ra xem có tìm được ô giống nó không
	n=len(a)
	m=len(a[0])
	d=[[100 for i in range(m)] for j in range(n)]
	mark=[[False for i in range(m)] for j in range(n)]
	d[x][y]=0
	q=[[x,y]]
	mark[x][y]=True
	while len(q)!=0:
		u=q[0]
		# print(u)
		q.pop(0)
		if d[u[0]][u[1]]==3:
			continue
		for j in [[1,0],[0,1],[-1,0],[0,-1]]:
			for i in range(1,100):
				x1,y1=u[0]+j[0]*i,u[1]+j[1]*i
				if not inside(a,x1,y1) or d[x1][y1]<d[u[0]][u[1]]+1:
					break
				if a[x1][y1]>0:
					if a[x1][y1]==a[x][y]:
						d[x1][y1]=d[u[0]][u[1]]+1
						if a[x1][y1]==a[x][y] and (x1!=x or y1!=y):
							return [x1,y1]
					break
				mark[x1][y1]=True
				q.append([x1,y1])
				d[x1][y1]=min(d[x1][y1],d[u[0]][u[1]]+1)
	return []

def nextChoice(a):
	# từ ma trận a đưa ra phương án chọn tiếp theo
	# nếu ko có phương án nào thì trả về [0,0]
	n=len(a)
	m=len(a[0])
	for i in range(n):
		for j in range(m):
			if a[i][j]!=0:
				u=check(a,i,j)
				if u!=[]:
					x,y=u
					return [i,j,x,y]
	return []

def init():
	# khởi tạo danh sách các cell
	# Bước 0: lập danh sách các image cell có thể( đã lưu trong Cell1)
	global sumSet,cellHeight,cellWidth,lastMove
	cellWidth=42
	cellHeight=52
	lastMove=[]
	start=time()
	sumSet=set()
	for i in range(1,37):
		url='Cell1/'+str(i)+'.png'
		img=cv2.imread(url)
		# cv2.imshow('',img)
		# cv2.waitKey()
		sumSet.add(np.sum(img))
	print(time()-start)

def findUpleftCoordinate():
	# tìm tọa độ góc trái trên, lưu vào biến global upleftCoor
	cornerCoor=(151,68)
	screen=cv2.cvtColor(np.array(pa.screenshot()),cv2.COLOR_RGB2BGR)
	side=cv2.imread('side.png')
	res=findImage(screen,side)
	print(res)
	# screen[res[0]][res[1]]=np.array([0,0,0])
	cv2.rectangle(screen,(res[1],res[0]),(res[1]+len(side[0]),res[0]+len(side)),(0,0,255),1)
	# cv2.rectangle(screen,upLeftCoor,upLeftCoor,(0,0,255),1)
	# cv2.rectangle(screen,(upLeftCoor[1],upLeftCoor[0]),(upLeftCoor[1],upLeftCoor[0]),(0,0,255),1)
	# cv2.imwrite("Result1.png",screen)
	return (res[1]+151,res[0]+68)

def mouseLeft():
	# kiểm tra xem chuột có rời vị trí không
	y,x=pa.position()
	return lastMove!=[] and lastMove!=[y,x]

def process(u):
	# đưa ra phương án tiếp theo từ kết quả u
	# có 2 trường hợp: u=[] => hoặc là đã hết game hoặc là hết nước, vậy nhấn Enter
	# u!=[] => tìm ra nước, vậy lần lượt click vào 2 tọa độ thích hợp
	global lastMove,clickList
	if u==[]:
		pa.press("Enter")
		return False

	# từ phương án đưa ra tọa độ
	p1=Point(upLeftCoor[0]+cellWidth*(u[1]-1)+10,upLeftCoor[1]+cellHeight*(u[0]-1)+10)
	p2=Point(upLeftCoor[0]+cellWidth*(u[3]-1)+10,upLeftCoor[1]+cellHeight*(u[2]-1)+10)
	pa.click(p1.x,p1.y)
	pa.click(p2.x,p2.y)
	# lưu lại tọa độ chuột cuối
	lastMove=[p2.x,p2.y]
	return True

start=time()
init()
pa.FAILSAFE = False
upLeftCoor=findUpleftCoordinate()
# print('up',upLeftCoor)
noPairAlert=cv2.imread("NoPairAlert.png")
pa.PAUSE=0
clickList = []
while True:
	# kiểm tra dấu hiệu stop
	# if randint(1,10)==1:
	pa.press('Enter')
	if mouseLeft():
		break
	time1=time()
	# đọc thông tin từ màn hình
	img=cv2.cvtColor(np.array(pa.screenshot()),cv2.COLOR_RGB2BGR)
	# kiểm tra xem có thông báo trong hình ko, nếu có bấm Enter
	time2=time()
	# biến img thành ma trận các cell id
	a=imageToIdMatrix(img)
	# print(np.array(a))
	time3=time()
	# print(np.array(a))

	# tính phương án tiếp theo
	u=nextChoice(a)
	# if randint(1,10)==1:
	# 	print(np.array(a))
	time4=time()
	if not process(u):
		pass
		# break
	time5=time()
	# print(time2-time1)
	# print('~'*100)
	# print("Step 1 (turn screen into numpy array):",time2-time1)
	# print("Step 2 (turn img(np.array) into matrix cell id):",time3-time2)
	# print("Step 3 (make choice):",time4-time3)
	# print("Step 4 (process choice):",time5-time4)

print("Total time for 144 cells:",time()-start)