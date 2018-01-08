import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import copy
import math
import time
import time
class t1t():
    def __init__(self):
        self.path = 'E:/workspace/pycharm/backproceture/'
        self.im2 = cv2.imread(self.path+'yyy.png')

    def detection(self,labelx, goal, mat):#识别边缘位置
        goalx = goal[1]  # 789
        goaly = goal[0]  # 719
        a = 0
        b = []
        c = goalx
        label = mat[goaly+2][goalx]#有的图形边缘颜色不是和内不一样例如便利店
        xn = mat.shape[1]
        yn = mat.shape[0]
        if labelx < goalx:
            for i in range(goaly, yn):
                for j in range(xn-1, goalx-1,-1):
                    #if np.sum(abs(np.float32(mat[i][j])-np.float32(label))) < 30:
                    if (abs(np.float(mat[i][j][0] - np.float32(label[0]))) < 10) and (
                        abs(np.float(mat[i][j][1] - np.float32(label[1]))) < 10) \
                            and (abs(np.float(mat[i][j][2] - np.float32(label[2]))) < 10):
                        b.append(j)
                        # b = j
                        if j <= c:
                            a += 1
                            if a >= 5:
                                #print(i,b)
                                return i-5, b
                        else:
                            c = j
                            a = 0
                        break
        else:
            for i in range(goaly, mat.shape[0]):
                for j in range(0, goalx):
                    if np.sum(abs(np.float32(mat[i][j])-np.float32(label))) < 30:
                        b.append(j)
                        # b = j
                        if j >= c:
                            a += 1
                            if a >= 5:
                                return i-5, b
                        else:
                            c = j
                            a = 0
                        break

    def goal(self,mat,loc):#找到目标方块顶点
        a = 0
        b = []
        for i in range(600,mat.shape[0],5):#从上向下扫描
            label = mat[i][0]
            if len(b) != 0:
                c = int(np.mean(b))
                return a, c
            for j in range(200,mat.shape[1]-101,2):
                if (loc[0] - 60 <= j) and (j <= loc[0] + 60):
                    continue
                elif (abs(np.float(mat[i][j][0] - np.float32(label[0]))) > 5) or (
                    abs(np.float(mat[i][j][1] - np.float32(label[1]))) > 5) \
                        or (abs(np.float(mat[i][j][2] - np.float32(label[2]))) > 5):
                    a = i
                    b.append(j+1)

    def findo(self,mat, label):#找到小球的中心
        a = 0
        b = []
        for i in range(mat.shape[0] - 700, 900, -5):  # 从上向下扫描
            for j in range(200,900,1):
                #if np.sum(abs(np.float32(mat[i][j]) - np.float32(label))) < 30:
                if (abs(np.float(mat[i][j][0]-np.float32(label[0])))<10) and (abs(np.float(mat[i][j][1]-np.float32(label[1])))<10) \
                        and (abs(np.float(mat[i][j][2]-np.float32(label[2])))<10):
                    a = i
                    b.append(j + 1)
                elif len(b) != 0:
                    c = int(np.mean(b))
                    return a, c

    def run(self,f = 0):
            os.system('adb shell screencap -p /sdcard/autojump.png')
            os.system('adb pull /sdcard/autojump.png .')
            img = cv2.imread(self.path+'autojump.png')
            #start1 = time.time()
            l1 = self.findo(img, self.im2[213 - 18][60])#纵横
            #start2 = time.time()
            #s = start2 - start1
            #print('findo spend %f.5 s'%(s))
            #for pt in zip(*loc[::-1]):
            #    img_test = cv2.rectangle(img_test, pt, (pt[0] + self.w, pt[1] + self.h), (7, 249, 151), 3)#框出小球的位置
            l1 = tuple([l1[1] , l1[0]  - 18])#横纵

            l2 = self.goal(img,l1)#纵横
            #start3 = time.time()
            #s = start3 - start2
            #print('goal spend %f.5 s'%(s))
            l3 = self.detection(l1[0], l2, img)#纵横

            #start4 = time.time()
            #s = start4 - start3
            #print('detection spend %f.5 s'%(s))
            #start5 = time.time()
            #s = start5 - start1
            #print('all spend %.f5 s'%(s))
            if f == 1:

                img_test = copy.deepcopy(img)
                img_test = cv2.circle(img_test, l1, 5, (0, 0, 255), -1)#画出小球的中心
                img_test1 = cv2.circle(img_test,(int(l2[1]),l2[0]),5,(255,0,0),-1)#画出目标方块的顶点的位置
                #plt.figure(figsize=(12, 12))
                #plt.imshow(img_test1[:,:,(2,1,0])
                #plt.show()
                img_test2 = cv2.circle(img_test1, (l3[1][-1], l3[0]), 5, (0, 255, 0), -1)#画出目标方块的边缘位置
                img_test3 = cv2.circle(img_test2, (l2[1], l3[0]), 5, (0, 0, 255), -1)#画出目标方块的中心
                plt.figure(figsize=(12, 12))
                plt.imshow(img_test3[:,:,(2,1,0)])
                #start1 = time.time()
                #s = start1 - start2
                #print('imshow spend %f.5 s' % (s))
                plt.show()
            #l2[0], l2[1]
            #l3[0], l2[1]
            l = math.sqrt((l1[1]-l3[0])**2+(l1[0]-l2[1])**2)* 1.37#提示1.35

            os.system('adb shell input swipe 10 10 10 10 '+str(int(l)+1))
            #print(l,int(l))
            #return l1,l2


if __name__ == '__main__':
    t = t1t()
    i = 0
    #a1 = []
    #a2 = []
    #a3 = []
    #a4 = []
    while 1:

        #l1,l2 = t.run()

        t.run(1)
        #a1.append(l1[0])
        #a3.append(l1[1])
        #a2.append(l2[0])
        #a4.append(l2[1])
        #i+=1
        time.sleep(0.9)#休眠防止截图过快
        #if i%30==0:
        #    print('目前共跳了'+str(i)+'次')
        #    print('其中小球最大，最小横坐标：{} {}'.format(max(a1),min(a1)))
        #    print('其中小球最大，最小纵坐标：{} {}'.format(max(a3),min(a3)))
        #    print('其中顶点最大，最小横坐标：{} {}'.format(max(a2),min(a2)))
        #    print('其中顶点最大，最小纵坐标：{} {}'.format(max(a4),min(a4)))
    os.system('adb shell input swipe 10 10 10 10 ' + str(int(1000) + 1))