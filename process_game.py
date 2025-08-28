###### process_game.py ######

###### IMPORTS ######
from imports import *
from global_variables import *
###### END IMPORTS ######

###### DEFINES ######
lines_list = []

x =     [
                [2600, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [2600, 0, 0, 0],
        ]

y =     [
                [1400, 0, 0, 1400],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
        ]

rectangles = [
        {
                "x1": int,
                "y1": int,
                "x2": int,
                "y2": int,
        }
        for i in range(9)
        ]
###### END DEFINES ######

def identify_x(lines, rectangles, table):
        buffer_zone = 25
        valid_x = [[],[],[],[]]
        for line in lines:
                        x1, y1, x2, y2 = line[0]
                        for i in range(9):
                                color=(255 - 25*i, 255 - 25*i, 255 - 25*i)
                                if      rectangles[i]['x1'] + (rectangles[i]['x2'] - rectangles[i]['x1'])/2 - buffer_zone < \
                                                x1 < rectangles[i]['x2'] - (rectangles[i]['x2'] - rectangles[i]['x1'])/2 + buffer_zone and \
                                        \
                                        rectangles[i]['y1'] + (rectangles[i]['y2'] - rectangles[i]['y1'])/2 - buffer_zone < \
                                                y1 < rectangles[i]['y2'] - (rectangles[i]['y2'] - rectangles[i]['y1'])/2 + buffer_zone and \
                                        \
                                        rectangles[i]['x1'] + (rectangles[i]['x2'] - rectangles[i]['x1'])/2 - buffer_zone < \
                                                x2 < rectangles[i]['x2'] - (rectangles[i]['x2'] - rectangles[i]['x1'])/2 + buffer_zone and \
                                        \
                                        rectangles[i]['y1'] + (rectangles[i]['y2'] - rectangles[i]['y1'])/2 - buffer_zone < \
                                                y2 < rectangles[i]['y2'] - (rectangles[i]['y2'] - rectangles[i]['y1'])/2 + buffer_zone:
                                                if table[i//3][i%3] == 0:
                                                        table[i//3][i%3] = X_SIGN
                                                        if rectangles[i]['x1'] not in valid_x[0]: valid_x[0].append(rectangles[i]['x1'])
                                                        if rectangles[i]['y1'] not in valid_x[1]: valid_x[1].append(rectangles[i]['y1'])
                                                        if rectangles[i]['x2'] not in valid_x[2]: valid_x[2].append(rectangles[i]['x2'])
                                                        if rectangles[i]['y2'] not in valid_x[3]: valid_x[3].append(rectangles[i]['y2'])
        return valid_x

def identify_rectangles(image):
        k = 0
        for i in range(3):
                for j in range(3):
                        color=(255 - 100*i, 255 - 100*j, 255 - 50*i + 50*j)
                        rectangles[k]['x1'], rectangles[k]['y1'] = x[i][j], y[i][j]
                        rectangles[k]['x2'], rectangles[k]['y2'] = x[i+1][j+1], y[i+1][j+1]
                        cv2.rectangle(image, (x[i][j],y[i][j]), (x[i+1][j+1],y[i+1][j+1]), color, thickness=5)
                        k += 1
        
        return rectangles

def identify_o(circles, table):
        circles = np.uint16(np.around(circles))
        valid_o = [[],[],[]]
        for i in range(3):
                for j in range(3):
                        color=(255 - 100*i, 255 - 100*j, 255 - 50*i + 50*j)
                        if circles is not None:
                                for circle in circles[0,:]:
                                        if x[i][j] < circle[0] < x[i+1][j+1] and \
                                                y[i][j] < circle[1] < y[i+1][j+1]:
                                                        if table[i][j] == 0:
                                                                table[i][j] = O_SIGN
                                                                valid_o[0].append(circle[0])
                                                                valid_o[1].append(circle[1])
                                                                valid_o[2].append(circle[2])
        return valid_o
        

def identify_points(image, lines_list):
        if len(lines_list) >= 2:
                for x1, y1, x2, y2 in lines_list:
                        if x[0][0] > x1: x[0][0] = x1
                        if y[0][0] > y1: y[0][0] = y1

                        if x[0][3] < x2: x[0][3] = x2
                        if y[0][3] > y2: y[0][3] = y2

                        if x[3][0] > x1: x[3][0] = x1
                        if y[3][0] < y1: y[3][0] = y1

                        if x[3][3] < x2: x[3][3] = x2
                        if y[3][3] < y2: y[3][3] = y2  
                
                for i in range(4):
                        for j in range(4):
                                if i == 0 and j not in [0, 3]:
                                        x[i][j] = x[0][0] + j * round((x[0][3] - x[0][0]) / 3)
                                        y[i][j] = round((y[0][3] + y[0][0]) / 2)
                                
                                elif j == 0 and i not in [0, 3]:
                                        x[i][j] = round((x[0][0] + x[3][0]) / 2)
                                        y[i][j] = y[0][0] + i * round((y[3][0] - y[0][0]) / 3)

                                elif j == 3 and i not in [0, 3]:
                                        x[i][j] = round((x[0][3] + x[3][3]) / 2)
                                        y[i][j] = y[0][0] + i * round((y[3][0] - y[0][0]) / 3)
                                
                                elif i == 3 and j not in [0, 3]:
                                        x[i][j] = x[0][0] + j * round((x[0][3] - x[0][0]) / 3)
                                        y[i][j] = round((y[3][3] + y[3][0]) / 2)
                                
                                else:
                                        x[i][j] = x[0][0] + j * round((x[0][3] - x[0][0]) / 3)
                                        y[i][j] = y[0][0] + i * round((y[3][0] - y[0][0]) / 3)

                                cv2.circle(image, (x[i][j], y[i][j]), radius=20, color=(0, 0, 255), thickness=-1)

def winner(action_table):
        p1_won = False
        p2_won = False
        p2_line = ''
        line = "none"

        for i in range(3):
                if action_table[i][0] == \
                action_table[i][1] == \
                action_table[i][2] != 0:
                        line = "c"+str(i)
                        if action_table[i][0] == 1:
                                return X_SIGN, line
                        else:
                                p2_won = True
                                p2_line = line
                if action_table[0][i] == \
                action_table[1][i] == \
                action_table[2][i] != 0:
                        line = "l"+str(i)
                        if action_table[i][0] == 1:
                                return X_SIGN, line
                        else:
                                p2_won = True
                                p2_line = line
        if action_table[0][0] == \
        action_table[1][1] == \
        action_table[2][2] != 0:
                line = "dp"
                if action_table[i][0] == 1:
                                return X_SIGN, line
                else:
                        p2_won = True
                        p2_line = line
        if action_table[0][2] == \
        action_table[1][1] == \
        action_table[2][0] != 0:
                line = "ds"
                if action_table[i][0] == 1:
                                return X_SIGN, line
                else:
                        p2_won = True
                        p2_line = line
                        
        if p2_won and not p1_won:
                return O_SIGN, p2_line
        
        return 0, line

def process_game_thread(action_table):

        global identified_o, identified_x

        while True:

                monitor.acquire()
                time.sleep(0.1)
                line_winner['line'] = 'none'

                if round_done.is_set() == True:
                        action_table *= 0
                        round_done.clear()
                        identified_o = [[],[],[]]
                        identified_x = [[],[],[],[]]
                        time.sleep(0.1)

                pil_image = pyautogui.screenshot(region=(1100, 680, 350, 350)).convert('RGB')
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

                x1, y1, x2, y2 = (0, 0, 0, 0)

                frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                _, thresh_white = cv2.threshold(frame_gray, 245, 255, cv2.THRESH_BINARY)
                edges = cv2.Canny(thresh_white, 5, 10)
                lines = cv2.HoughLinesP(edges, 1, np.pi/180, 5, 10, 10)
                circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 100, param1=30, param2=20, minRadius=30, maxRadius=50)

                line_image = np.copy(image) * 0

                if lines is not None:
                        for line in lines:
                                x1, y1, x2, y2 = line[0]
                                lines_list.append((x1, y1, x2, y2))

                if circles is not None:
                        valid_o = identify_o(circles, action_table)
                        if valid_o is not None:
                                identified_o[0].extend(valid_o[0])
                                identified_o[1].extend(valid_o[1])
                                identified_o[2].extend(valid_o[2])

                if identified_o is not None:
                        for i in range(len(identified_o[0])):
                                if identified_o[0][i] is not None:
                                        try:
                                                cv2.circle(line_image, (int(identified_o[0][i]), int(identified_o[1][i])), \
                                                        int(identified_o[2][i]), (255, 255, 255), 2)
                                        except:
                                                continue

                if lines is not None:
                        identify_points(line_image, lines_list)
                        rectangles = identify_rectangles(line_image)
                        valid_x = identify_x(lines, rectangles, action_table)
                        if [] not in valid_x:
                                identified_x[0].extend(valid_x[0])
                                identified_x[1].extend(valid_x[1])
                                identified_x[2].extend(valid_x[2])
                                identified_x[3].extend(valid_x[3])
                
                if identified_x is not None:
                        for i in range(len(identified_x[0])):
                                try:
                                        cv2.line(line_image, (int(identified_x[0][i]), int(identified_x[1][i])), \
                                                 (int(identified_x[2][i]), int(identified_x[3][i])), (255, 255, 255), 5)
                                        cv2.line(line_image, (int(identified_x[0][i]), int(identified_x[3][i])), \
                                                 (int(identified_x[2][i]), int(identified_x[1][i])), (255, 255, 255), 5)
                                except:
                                        continue
                
                reward, line_winner['line'] = winner(action_table)

                p1_win.clear()
                p2_win.clear()
                if reward == X_SIGN:
                        p1_win.set()

                elif reward == O_SIGN: 
                        p2_win.set()

                cv2.imshow('temp', line_image)

                key = cv2.waitKey(1)
                if key == ord('q') or game_finished.is_set():
                        break

                monitor.release()

        cv2.destroyAllWindows()