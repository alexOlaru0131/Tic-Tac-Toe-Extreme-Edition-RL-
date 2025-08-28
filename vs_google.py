###### IMPORTS ######
from imports import *
###### END IMPORTS ######

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

                                cv2.circle(image, (x[i][j], y[i][j]), radius=10, color=(0, 0, 255), thickness=-1)

def process_window():

        while True:

                pil_image = pyautogui.screenshot(region=(700, 550, 370, 400)).convert('RGB')
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                results_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                image_o = np.copy(image)
                _, thresh_white_o = cv2.threshold(image_o, 150, 255, cv2.THRESH_BINARY)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                thresh_white_o = cv2.erode(thresh_white_o, kernel, iterations=1)

                image_table = cv2.bitwise_not(image)
                thresh_white_table = cv2.inRange(image_table, 130, 140)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                thresh_white_table = cv2.erode(thresh_white_table, kernel, iterations=1)

                lines = cv2.HoughLinesP(thresh_white_table, 1, np.pi/180, 10, 5, 20)
                lines_list = []
                if lines is not None:
                        for line in lines:
                                x1, y1, x2, y2 = line[0]
                                lines_list.append((int(x1), int(y1), int(x2), int(y2)))

                identify_points(results_image, lines_list)
                rectangles = identify_rectangles(results_image)

                circles = cv2.HoughCircles(thresh_white_table, cv2.HOUGH_GRADIENT, 1, 100, param1=30, param2=20, minRadius=30, maxRadius=50)

                image_x = cv2.bitwise_not(image)
                _, thresh_white_x = cv2.threshold(image_x, 150, 255, cv2.THRESH_BINARY)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                thresh_white_x = cv2.erode(thresh_white_x, kernel, iterations=1)

                cv2.imshow('', results_image)

                key = cv2.waitKey(1)
                if key == ord('q'):
                        break

        cv2.destroyAllWindows()
        return False

if __name__ == "__main__":

        
        thread_process_windows = Thread(target=process_window)
        thread_process_windows.daemon = True
        thread_process_windows.start()

        thread_process_windows.join()