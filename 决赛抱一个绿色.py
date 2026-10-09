import time
import numpy as np
import rospy
import math
from functools import wraps
import sysort cv2
import threading
import time

from image_Tag_converter import ImgConverter
from image_Tag_converter import TagConverter

sys.path.append("/home/lemon/catkin_ws/src/aelos_smart_ros")
from leju import base_action

# 定义一些参数
Chest_img = None
ChestOrg = None
marker = None
chest_circle_x = None
chest_circle_y = None
Debug = 0

# 不同色块的hsv范围
color_range = {
    'green': [(47, 113, 79), (63, 236, 146)],
    'orange': [( 9 , 164 , 95 ),( 15 , 247, 190 )]
}

# ******************************************动作函数***********************************************
# 放下箱子
def Box_Down(n):
    for i in range(0, n):
        base_action.action("reng")
        # time.sleep(0.2)  # 0.5
# 后退
def Box_Back(n):
    for i in range(0, n):
        base_action.action("BoxBack1Run_fan")
        time.sleep(0.5)


def Box_Back1(n):
    for i in range(0, n):
        base_action.action("BoxBack2-1_fan")
        time.sleep(0.5)


def Back2(n):
    for i in range(0, n):
        base_action.action("Back2Run")
        time.sleep(0.2)  # 0.5


def Back1(n):
    for i in range(0, n):
        base_action.action("Back1Run")
        time.sleep(0.2)  # 0.5


# 前进#
def go_fast(n):  # 快速前进一步
    for i in range(0, n):
        base_action.action("Forwalk01")
        time.sleep(0.2)  # 0.5


def go_fast1(n):  # 快速前进一步
    for i in range(0, n):
        base_action.action("FastForward1s")
        time.sleep(0.2)  # 0.5


def go_fast2(n):  # 快速前进两步
    for i in range(0, n):
        base_action.action("FastForward2s")
        time.sleep(0.2)  # 0.5


def go_fast3(n):  # 快速前进三步
    for i in range(0, n):
        base_action.action("FastForward3s")
        time.sleep(0.2)  # 0.5


def box_go(n):
    for i in range(0, n):
        base_action.action("BoxForward02")
        time.sleep(0.2)


def box_go1(n):  # 抱着箱子前进一步
    for i in range(0, n):
        base_action.action("BoxForward1s_fan")
        time.sleep(0.2)  # 0.5


def box_go2(n):  # 抱着箱子前进两步
    for i in range(0, n):
        base_action.action("BoxForward2s_fan1")
        time.sleep(0.3)  # 1    #2


def box_go8(n):  # 抱着箱子前进两步
    for i in range(0, n):
        base_action.action("BoxForward2s_fan1")
        base_action.action("BoxForward2s_fan1")
        base_action.action("BoxForward2s_fan1")
        base_action.action("BoxForward2s_fan1")
        time.sleep(0.3)


def box_go6(n):  # 抱着箱子前进两步
    for i in range(0, n):
        base_action.action("BoxForward2s_fan1")
        base_action.action("BoxForward2s_fan1")
        base_action.action("BoxForward2s_fan1")
        time.sleep(0.3)


def box_go3(n):  # 抱着箱子前进三步
    for i in range(0, n):
        base_action.action("BoxForward3s")
        time.sleep(0.5)  # 1


# 侧移#
def L_move1(n):  # 左侧移
    for i in range(0, n):
        base_action.action("Left02move")
        print('左移1.5cm')
        time.sleep(0.2)  # 0.5


def L_move2(n):  # 左侧移
    for i in range(0, n):
        base_action.action('move_left')
        time.sleep(0.2)  # 0.5


def BoxL_move1(n):  # 左侧移
    for i in range(0, n):
        base_action.action("BoxLeft1")
        time.sleep(0.5)  # 1


def BoxL_move2(n):  # 左侧移
    for i in range(0, n):
        base_action.action('Box_move_left_fan')
        time.sleep(0.2)  # 1


def BoxL_move4(n):  # 左侧移
    for i in range(0, n):
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        time.sleep(0.2)  # 1


def BoxL_move6(n):  # 左侧移
    for i in range(0, n):
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        time.sleep(0.2)  # 1


def BoxL_move10(n):  # 左侧移
    for i in range(0, n):
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        time.sleep(0.2)  # 1


def BoxL_move14(n):  # 左侧移
    for i in range(0, n):
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        base_action.action('Box_move_left_fan')
        time.sleep(0.2)  # 1


def R_move1(n):  # 右侧移
    for i in range(0, n):
        base_action.action("Right02move")
        time.sleep(0.5)  # 0.5


def R_move2(n):  # 右侧移
    for i in range(0, n):
        base_action.action('move_right')  # move_right
        time.sleep(0.2)  # 0.5


def BoxR_move1(n):  # 右侧移
    for i in range(0, n):
        base_action.action("BoxRight1")
        time.sleep(0.3)  # 0.5


def BoxR_move2(n):  # 右侧移
    for i in range(0, n):
        base_action.action('Box_move_right')
        time.sleep(0.2)  # 1


def BoxR_move4(n):  # 右侧移
    for i in range(0, n):
        base_action.action('Box_move_right')
        base_action.action('Box_move_right')
        time.sleep(0.2)  # 1


def BoxR_move6(n):  # 右侧移
    for i in range(0, n):
        base_action.action('Box_move_right')
        base_action.action('Box_move_right')
        base_action.action('Box_move_right')
        time.sleep(0.2)  # 1


# 转向#
def L_turn1(n):  # 左转  左转7° 小转
    for i in range(0, n):
        base_action.action("turn003L_tt")
        time.sleep(0.5)  # 0.5


def L_turn12(n):  # 左转  中转
    for i in range(0, n):
        base_action.action("LeftTurn1s_tt")
        time.sleep(0.5)  # 0.5


def L_turn2(n):
    for i in range(0, n):
        base_action.action("LeftTurn1s_fan")
        time.sleep(0.2)  # 0.5


def BoxL_turn1(n):  # 左转 5度
    for i in range(0, n):
        base_action.action("BoxTurnL1_tt")  # 原来BoxTurnL1  #BoxTurnL1_tt
        time.sleep(0.5)  # 1


def BoxL_turn12(n):  # 左转新建18度
    for i in range(0, n):
        base_action.action("BoxLeftTurn1s_18")
        time.sleep(0.5)  # 1


def BoxL_turn2(n):  # 左转 41度
    for i in range(0, n):
        base_action.action("BoxLeftTurn1s_fan1")
        time.sleep(0.2)  # 1


def R_turn1(n):  # 右转
    for i in range(0, n):
        base_action.action("turn003R_tt")
        time.sleep(0.5)  # 0.5


def R_turn12(n):  # 右转
    for i in range(0, n):
        base_action.action("RightTurn1s_22tt")
        time.sleep(0.5)  # 0.5


def R_turn2(n):  # 右转
    for i in range(0, n):
        base_action.action("RightTurn1s_fan1")
        time.sleep(0.2)  # 0.5


def R_turn2(n):  # 右转
    for i in range(0, n):
        base_action.action("RightTurn1s_fan1")
        time.sleep(0.2)  # 0.5


def R_turn3(n):  # 右转
    for i in range(0, n):
        base_action.action("RightTurn1s_fan1")
        base_action.action("RightTurn1s_fan1")
        base_action.action("RightTurn1s_fan1")
        time.sleep(0.2)  # 0.5


def BoxR_turn1(n):  # 右转
    for i in range(0, n):
        base_action.action("BoxTurnR1_tt")  # 原来BoxTurnR1
        time.sleep(0.5)  # 1


def BoxR_turn12(n):  # 右转22度
    for i in range(0, n):
        base_action.action("BoxRightTurn1s_22tyt")
        time.sleep(0.5)  # 1


def BoxR_turn2(n):  # 右转
    for i in range(0, n):
        base_action.action("BoxRightTurn1s")
        time.sleep(0.2)  # 1


# 获取图像
def get_img():
    global Chest_img, ChestOrg
    global ret
    image_reader_chest = ImgConverter()
    while True:
        ret, ChestOrg = image_reader_chest.chest_image()
        time.sleep(0.05)  # 0.3
        if ChestOrg is not None:
            Chest_img = ChestOrg
            time.sleep(0.05)
            # Chest_img = cv2.flip(Chest_img, 1)
        else:
            time.sleep(0.05)  # 0.3
            print("暂时未获取到图像")


th2 = threading.Thread(target=get_img)
th2.setDaemon(True)
th2.start()


# #查找方块
# def find_box(img,color_name):
#     global chest_circle_x, chest_circle_y
#     if Chest_img is None:
#         print('等待获取图像中...')
#         time.sleep(0.3)
#     else:
#         box_img = img
#         box_img_bgr = cv2.cvtColor(box_img, cv2.COLOR_RGB2BGR)  # 将图片转换到BRG空间
#         box_img_hsv = cv2.cvtColor(box_img, cv2.COLOR_BGR2HSV)  # 将图片转换到HSV空间
#         box_img = cv2.GaussianBlur(box_img_hsv, (3, 3), 0)  # 高斯模糊
#         box_img_mask = cv2.inRange(box_img, color_range[color_name][0], color_range[color_name][1])  # 二值化
#         box_img_closed = cv2.erode(box_img_mask, None, iterations=2)  # 腐蚀
#         box_img_opened = cv2.dilate(box_img_mask, np.ones((4, 4), np.uint8), iterations=2)  # 膨胀    先腐蚀后运算等同于开运算
#         (contours, hierarchy) = cv2.findContours(box_img_opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#         if len(contours) != 0:
#             area = []
#             for cn in contours:
#                 contour_area = math.fabs(cv2.contourArea(cn))
#                 area.append(contour_area)
#             max_index = np.argmax(area)
#             (chest_circle_x,chest_circle_y),chest_radius = cv2.minEnclosingCircle(contours[max_index])
#             cv2.circle(img,(int(chest_circle_x),int(chest_circle_y)),int(chest_radius),(0,0,255))
#             print('A','x=',chest_circle_x,'y=',chest_circle_y)

#             if Debug:
#                 # cv2.imwrite('image.png',img)
#                 cv2.imshow("Box", img)
#                 cv2.waitKey(2000)

#         else:
#             print('正在寻找目标')

# 查找方块
def find_box(img, color_name):
    global chest_circle_x, chest_circle_y
    if Chest_img is None:
        print('等待获取图像中...')
        time.sleep(0.3)
    else:
        box_img = img
        box_img_bgr = cv2.cvtColor(box_img, cv2.COLOR_RGB2BGR)  # 将图片转换到BGR空间
        box_img_hsv = cv2.cvtColor(box_img, cv2.COLOR_BGR2HSV)  # 将图片转换到HSV空间
        box_img = cv2.GaussianBlur(box_img_hsv, (3, 3), 0)  # 高斯模糊
        box_img_mask = cv2.inRange(box_img, color_range[color_name][0], color_range[color_name][1])  # 二值化
        box_img_closed = cv2.erode(box_img_mask, None, iterations=2)  # 腐蚀
        box_img_opened = cv2.dilate(box_img_mask, np.ones((4, 4), np.uint8), iterations=2)  # 膨胀    先腐蚀后运算等同于开运算
        (contours, hierarchy) = cv2.findContours(box_img_opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            area = []
            for cn in contours:
                contour_area = math.fabs(cv2.contourArea(cn))#计算轮廓面积，并取绝对值
                area.append(contour_area)
            max_index = np.argmax(area)
            (chest_circle_x, chest_circle_y), chest_radius = cv2.minEnclosingCircle(contours[max_index])
            cv2.circle(img, (int(chest_circle_x), int(chest_circle_y)), int(chest_radius), (0, 0, 255))
            print('A', 'x=', chest_circle_x, 'y=', chest_circle_y)
            Debug = 1

            if Debug:
                # cv2.imwrite('image.png',img)
                cv2.imshow("Box", img)
                cv2.waitKey(1000)

        else:
            color_name = 'orange'
            box_img_mask = cv2.inRange(box_img, color_range[color_name][0], color_range[color_name][1])  # 二值化
            box_img_closed = cv2.erode(box_img_mask, None, iterations=2)  # 腐蚀
            box_img_opened = cv2.dilate(box_img_mask, np.ones((4, 4), np.uint8), iterations=2)  # 膨胀    先腐蚀后运算等同于开运算
            (contours, hierarchy) = cv2.findContours(box_img_opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if len(contours) != 0:
                area = []
                for cn in contours:
                    contour_area = math.fabs(cv2.contourArea(cn))
                    area.append(contour_area)
                max_index = np.argmax(area)
                (chest_circle_x, chest_circle_y), chest_radius = cv2.minEnclosingCircle(contours[max_index])
                cv2.circle(img, (int(chest_circle_x), int(chest_circle_y)), int(chest_radius), (0, 0, 255))
                print('A', 'x=', chest_circle_x, 'y=', chest_circle_y)
                Debug = 1

                if Debug:
                    # cv2.imwrite('image.png',img)
                    cv2.imshow("Box", img)
                    cv2.waitKey(1000)
            else:
                print('正在寻找目标')
                L_turn2(1)


# 搬箱子
def goto_box():
    global level, ID
    if chest_circle_x is None:
        print('等待中获取坐标中...')
        time.sleep(0.3)
    else:
        if chest_circle_x < 255:                 #275
            print("正在左大移 ", chest_circle_x)
            base_action.action("move_left")     #Left3move
        elif chest_circle_x > 395:              #365
            print("正在右大移 ", chest_circle_x)
            base_action.action("move_right")     #Right3move
        elif chest_circle_y < 330:              #300
            print("前进", chest_circle_y)
            base_action.action("FastForward1s")
        elif chest_circle_y >= 370:              #340
            print("后退", chest_circle_y)
            base_action.action("Back1Run")
        else:
            if chest_circle_x < 260:             #295
                print("正在左小移 ", chest_circle_x)
                base_action.action("Left02move")
            elif chest_circle_x > 348:           #345
                print("正在右小移 ", chest_circle_x)
                base_action.action("Right02move")               
            else:
                print("开始抱箱子")
                base_action.action("Forwalk01")
                base_action.action("bao2")    #抱2橙   用来抱两个
                #base_action.action("LiftCubeUp")
                level = "end_box"

# ***************************************tag对正****************************************
def turn_to_tag(dis_x, dis_y, theta, x_offset=0, y_offset=0, theta_offset=0, x_threshold=0.03, y_threshold=0.04,
                theta_threshold=5):  # theta_threshold=5   y_threshold=0.02
    is_turn_done = False
    check_flag = 0

    x_error = dis_x - x_offset
    y_error = dis_y - y_offset
    theta_error = theta - theta_offset
    print("ID:", marker[0], "dis_x:", dis_x, "dis_y:", dis_y, "theta:", theta, "theta_offset", theta_offset)
    print("x_error:", x_error, "y_error:", y_error, "theta_error:", theta_error)

    # 不偏离赛道
    if step == 1:
        if (x_error < x_threshold - 0.03):
            print("后退", x_error, " < ", x_threshold - 0.03)
            Box_Back(1)

        # 快速靠近标签
        elif (x_error > x_threshold + 0.2):
            print("1向前靠近标签", x_error, " > ", x_threshold + 0.12)
            box_go2(1)

        elif (theta_error + theta_threshold > 35):
            print("1左转身", theta_error, " > ", 14 + theta_threshold)
            BoxL_turn2(1)
        elif (theta_error - theta_threshold < -35):
            print("1右转身", theta_error, " < ", -14 - theta_threshold)
            BoxR_turn2(1)
        # 左右旋转中度
        elif (theta_error + theta_threshold > 15):
            print("12左转身", theta_error, " > ", 14 + theta_threshold)
            BoxL_turn12(1)
        elif (theta_error - theta_threshold < -15):  # -18
            print("12右转身", theta_error, " < ", -14 - theta_threshold)
            BoxR_turn12(1)


        # 左右平移
        elif (y_error > y_threshold + 0.02):  # 0.03
            print("1左移动", y_error, " > ", y_threshold)
            BoxL_move2(1)
        elif (y_error < -y_threshold - 0.02):  # 0.03
            print("1右移动 ", y_error, " < ", -y_threshold)
            BoxR_move2(1)

        # 靠近标签
        elif (x_error > x_threshold + 0.08):  # 0.12
            print("2向前靠近标签", x_error, " > ", x_threshold + 0.08)
            box_go1(1)

        # 方向平行与标签
        elif (theta_error > theta_threshold):
            print("2左转 ", theta_error, " > ", theta_threshold)
            BoxL_turn1(1)
        elif (theta_error < -theta_threshold):
            print("2右转 ", theta_error, " < ", -theta_threshold)
            BoxR_turn1(1)

        # 精确调整左右平移
        elif (y_error > y_threshold):
            print("2左移动", y_error, " > ", y_threshold)
            BoxL_move1(1)
        elif (y_error < -y_threshold):
            print("2右移动 ", y_error, " < ", -y_threshold)
            BoxR_move1(1)


        # elif (x_error > x_threshold+0.06):
        #   print("向前靠近标签", x_error, " > ", x_threshold+0.06)
        #  box_go(1)
        else:
            is_turn_done = True


    elif step == 2:
        # 快速靠近标签
        if (x_error > x_threshold + 0.2):
            print("向前靠近标签", x_error, " > ", x_threshold + 0.12)
            go_fast2(1)

        elif (theta_error + theta_threshold > 35):
            print("1左转身", theta_error, " > ", 14 + theta_threshold)
            L_turn2(1)
        elif (theta_error - theta_threshold < -35):
            print("1右转身", theta_error, " < ", -14 - theta_threshold)
            R_turn2(1)

        # 左右旋转中度
        elif (theta_error + theta_threshold > 15):
            print("12左转身", theta_error, " > ", 14 + theta_threshold)
            L_turn12(1)
        elif (theta_error - theta_threshold < -15):  # -18
            print("12右转身", theta_error, " < ", -14 - theta_threshold)
            R_turn12(1)

        # 左右平移
        elif (y_error > y_threshold + 0.02):  # 0.03
            print("1左移动", y_error, " > ", y_threshold)
            L_move2(1)
        elif (y_error < -y_threshold - 0.02):  # 0.03
            print("1右移动 ", y_error, " < ", -y_threshold)
            R_move2(1)

        # 靠近标签
        elif (x_error > x_threshold + 0.08):  # 0.12
            print("向前靠近标签", x_error, " > ", x_threshold + 0.08)
            go_fast1(1)

        # 方向平行与标签
        elif (theta_error > theta_threshold):
            print("2左转 ", theta_error, " > ", theta_threshold)
            L_turn1(1)
        elif (theta_error < -theta_threshold):
            print("2右转 ", theta_error, " < ", theta_threshold)
            R_turn1(1)

        # 精确调整左右平移
        elif (y_error > y_threshold):
            print("2左移动", y_error, " > ", y_threshold)
            L_move1(1)
        elif (y_error < -y_threshold):
            print("2右移动 ", y_error, " < ", -y_threshold)
            R_move1(1)

        # elif (x_error > x_threshold + 0.06):
        # print("向前靠近标签", x_error, " > ", x_threshold + 0.06)
        # go_fast(1)
        else:
            is_turn_done = True

    return is_turn_done


def one_green():
    go_fast3(2)
    base_action.action("GrabCube_fan1")  # 抱一个的动作

    BoxR_turn2(1)
    box_go2(2)
    BoxR_turn2(1)
    BoxL_move4(1)


def twobox():
    base_action.action("抱4")  # 抱两个的动作
    BoxL_turn12(1)
    BoxL_move2(7)
    # box_go2(1)
    BoxL_move2(1)


def fourbox():
    base_action.action("抱4")  # 抱两个的动作
    BoxL_turn12(1)
    BoxL_move2(7)
    # box_go2(1)
    # BoxL_move2(1)


if __name__ == '__main__':
    rospy.init_node('image_listener')  # ROS节点初始化
    
    Tag = TagConverter()
    time.sleep(0.1)  # 0.5
    flag = 0
    # time.sleep(0.1)
    while ChestOrg is None:
        print('wite')
        time.sleep(0.1)
    # print('启动')

    # 前进
    # go_fast(n)     go_fast2(n)       box_go(n)      box_go2(n)
    # 后退
    # Back2(n)       Back2(n)          Box_Down(n)    Box_Back1(n)           Box_Back1(n)
    # 左右移
    # L_move2(n)     BoxL_move2(n)     R_move2(n)     BoxR_move2(n)
    # 左右转
    # L_turn2(2)     BoxL_turn2(n)     R_turn2(n)     BoxR_turn2(n)

    ID = 0
    step = 1
    level = "start_box"
    # level = "start_moving"
    # level = "reverse_moving"
    input()
#********************抱一个绿色****************************************
    go_fast3(2)
    base_action.action("GrabCube_fan1")  # 抱一个的动作

    BoxR_turn2(1)
    box_go2(2)
    BoxR_turn2(1)
    BoxL_move4(1)

    level = "end_box"  # 一定不要忘了改这里

    A = 0  # A==0摔倒放箱，A!=0正常放箱

    while not rospy.is_shutdown():
        if ID == 0:  # 搬箱子
            if level == "start_box":
                find_box(Chest_img, 'green')
                goto_box()
            elif level == "end_box":
                if step == 1:
                    BoxL_move2(1)
                elif step == 2:
                    BoxL_turn2(3)
                    step = 1
                ID += 1
        else:
            marker = Tag.get_nearest_marker()

            if len(marker) == 0:
                print("无tag")
                if (ID == 1 and level == "end_box" and flag == 0):
                    print("右转")
                    BoxR_turn2(1)
                    # print("左转")
                    # BoxL_turn2(1)
                elif (ID == 1 and level == "end_box" and flag != 0):
                    print("左转")
                    BoxL_turn2(1)
                elif (ID == 1 and level == "start_moving"):
                    print("抱着箱子前进")
                    box_go2(1)
                elif ID == 2:
                    print("抱着箱子前进")
                    box_go1(1)
                elif ID == 3:
                    print("抱着箱子后退")
                    Box_Back(1)
                elif ID == 4:
                    print("抱着箱子右转")
                    BoxR_turn2(1)
                elif (ID == 5 and step == 1):
                    print("抱着箱子前进")
                    box_go2(1)
                elif (ID == 5 and step == 2 and level == "start_moving"):
                    print("右转")
                    R_turn2(1)
                elif (ID == 6) or(ID == 5 and step == 2 and level == "reverse_moving"):
                    print("右转")
                    R_turn2(1)
                elif (ID == 7)or(ID == 1 and step == 2 and level == "reverse_moving"):
                    print("左中转")
                    L_turn2(1)

            else:
                robot_tag_x = marker[1]
                robot_tag_y = marker[2]
                tag_yaw = marker[3] + 90  # artag 正方向与机器人正方向对齐

                if step == 1:
                    if marker[0] == 1:
                        if ID == 1:
                            level = "start_moving"
                            result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw, 0.12, 0.0, 0)  # 原来x=0.08,原本角度2
                            if result == True:
                                print('一号码对正完毕，前进对正二号码')
                                ID += 1
                                # box_go8(1)
                                box_go2(2)
                                box_go2(2)
                                box_go1(1)
                        else:
                            print("前进")
                            box_go1(1)

                    elif marker[0] == 2:
                        if ID == 2:
                            result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw, 0.1, 0.0, 0)  # x=0.12
                            if result == True:
                                print('二号码对正完毕，右侧移对正三号码')
                                ID += 1
                                # BoxR_move2(3)
                                BoxR_move6(1)
                                box_go1(1)
                                BoxR_move6(1)
                                # BoxR_move2(3)
                        else:
                            print("右移")
                            BoxR_move2(1)

                    elif marker[0] == 3:
                        if ID == 3:
                            result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw, 0.1, 0.08, 0)  # x=0.12  y=0.11
                            if result == True:
                                print('三号码对正完毕，右侧移对正四号码')
                                ID += 1
                                BoxR_move2(2)
                                box_go2(3)
                                # BoxL_move2(1)
                                # box_go8(1)
                                box_go2(1)
                                box_go1(1)
                                BoxL_move2(1)
                                box_go1(1)
                        else:
                            print("右移")
                            BoxR_move2(1)

                    elif marker[0] == 4:
                        if ID == 4:
                            result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw, 0.1, -0.1, 0)  # x=0.12，y=-0.1
                            if result == True:
                                print('四号码对正完毕，左移对正五号码')
                                ID += 1
                                BoxL_move2(3)
                                # BoxL_move6(1)
                                box_go1(1)
                                BoxL_move2(1)
                        else:
                            print("左移")
                            BoxL_move2(1)
                    elif marker[0] == 5:
                        if ID == 5:
                            if A == 0:
                                # result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw, 0.1, 0.0, 0)  # x=0.12
                                # if result == True:
                                print('五号码对正完毕，前进至大本营并放下海绵块')
                                box_go8(1)
                                # Box_Down(1)
                                base_action.action("xputdown1")
                                time.sleep(40)
                                R_turn3(1)
                                Back2(1)
                                step = 2
                            else:
                                result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw, 0.1, 0.0, 0)  # x=0.12
                                if result == True:
                                    print('五号码对正完毕，前进至大本营并放下海绵块')
                                    box_go8(1)
                                    Box_Down(1)
                                    # base_action.action("xputdown3")
                                    # time.sleep(10)
                                    R_turn3(1)
                                    Back2(1)
                                    step = 2

                elif step == 2:
                    # 反方向
                    if marker[0] == 5:
                        result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw, 0.08, 0.0, 180)  # 5号为反方向
                        level = "reverse_moving"
                        if result == True:
                            print('五号码对正完毕，左侧移对正六号码')
                            ID += 1
                            go_fast2(2)
                            go_fast2(1)

                    elif marker[0] == 6:
                        if ID == 6:
                            result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw, 0.05, -0.1, 0)  # y=-0.1
                            if result == True:
                                print('六号码对正完毕，左侧移对正七号码')
                                ID += 1
                                L_move2(5)
                                go_fast2(1)
                                L_move2(1)
                                go_fast2(3)

                    elif marker[0] == 7:
                        if ID == 7:
                            result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw, 0.06, 0.1, 0)  # y=0.10
                            if result == True:
                                print('七号码对正完毕，右侧移反向对正一号码')
                                ID=1
                                R_move2(5)
                                R_move2(5)
                                go_fast2(1)

                    elif marker[0] == 1:
                        result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw, 0.1, 0.0, 180)  # 1号为反方向
                        if result == True:
                            print('一号码对正完毕，前进抓取海绵块')
# 直接抓取
                            #ID = 0
                            #go_fast2(2)
                            #base_action.action("GrabCube")  # 抱两个的动作
                            #box_go2(2)
                            #level = "end_box"
# 抱箱识别的代码
                            ID = 0
                            go_fast2(3)
                            L_turn2(2)
                            level = "start_box"
                            flag += 1
            time.sleep(0.1)
