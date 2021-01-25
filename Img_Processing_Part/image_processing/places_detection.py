import cv2
import numpy as np

# Function to get contours, with our img as argument
def getContours(img,area_min,area_max,outfile,white_threshold):
    # Find counter function : our image, retrieval method (methode de recuperation), approximation (request all informations, or compressed values = reduced points, here we want all informations)
    # We use the external method which retrieves the extreme out contours, other methods which detect all the contours and dont filter out

    out = outfile
    AREAMAX = int(area_max)
    AREAMIN = int(area_min)
    wt = int(white_threshold)
    img = cv2.resize(img, (650, 650))
    lower = np.array([wt, wt, wt], dtype = "uint8")
    upper = np.array([255, 255, 255], dtype = "uint8")
    mask = cv2.inRange(img, lower, upper)
    img = cv2.bitwise_and(img, img, mask = mask)

    # we copy the original image to draw on it
    imgContour = img.copy()
    imgContour2 = img.copy()
    imgContour3 = img.copy()

    # Gray transformation
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur transformation, kernel, sigma (the higher the more blur we will get)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)


    # Detect the edges, threshold 1 and 2
    imgCanny = cv2.Canny(imgBlur, 5, 5)


    # kernel definition for dilatation (matrix of 1, size 5x5 and type of objetc = unsigned integer of 8 bytes values can range from 0 to 255 )
    kernel = np.ones((5, 5), np.uint8)

    # Increase edge thickness to avoid edge gap and fail detection, kernel matrix size and value, and how many iterations we want the kernel to move around, it means how much thickness we need
    imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)

    imgEroded = cv2.erode(imgDilation, kernel, iterations=1)

    # We call the function getContours and we send it the imgCanny as argumentq

    # Put 1000 if no exception
    #put number place - 1 si on a une exception a ne pas dessiner

    #SI IMAGE PLUS ZOOMÉ

    PERCENT_RECTANGLE_VALIDATION = 0.05
    PERCENT_GAP_BETWEEN_LINES = 0.05
    MULTIPLIER_DISTANCE_FOR_PLACES_INTERPOLATION = 1.8

    img = imgDilation.copy()

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    n = 0
    n2 = 0
    mid = np.arange(400).reshape(200, 2)
    coord = np.arange(800).reshape(200, 4)

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area < AREAMAX and area > AREAMIN:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            area2 = w * h
            if objCor < 9 and area > area2 * 0.726190:
                if w < h*3 and h < w*3: #max multiplication par 3 entre hauteur et largeur pour les carrés
                        coord[n] = (x, y, w, h)
                        mid[n] = ((x + (w // 2)), (y + (h // 2)))
                        n = n + 1
                        cv2.rectangle(imgContour2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    b = np.arange(n * 2).reshape(n, 2)
    for i in range(n):
        b[i] = 0

    for j in range(0,n):  

        distance_high_treshold = 150
        distance_low_treshold = 20

        lowerPrev_1 = mid[j - 1, 1] * (1-PERCENT_RECTANGLE_VALIDATION)
        lowerPrev_2 = mid[j - 2, 1] * (1-PERCENT_RECTANGLE_VALIDATION)

        upperPrev_1 = mid[j - 1, 1] * (1+PERCENT_RECTANGLE_VALIDATION)
        upperPrev_2 = mid[j - 2, 1] * (1+PERCENT_RECTANGLE_VALIDATION)

        distancePrev = abs(mid[j, 0] - mid[j - 1, 0])

        prev_boolean = ((mid[j, 1] > lowerPrev_1) and (mid[j, 1] < upperPrev_1) and (mid[j, 1] > lowerPrev_2) and (mid[j, 1] < upperPrev_2))
        prev_dist_bool = ((distancePrev < distance_high_treshold) and (distancePrev > distance_low_treshold))

        lowerNext_1 = mid[j + 1, 1] * (1-PERCENT_RECTANGLE_VALIDATION)
        lowerNext_2 = mid[j + 2, 1] * (1-PERCENT_RECTANGLE_VALIDATION)

        upperNext_1 = mid[j + 1, 1] * (1+PERCENT_RECTANGLE_VALIDATION)
        upperNext_2 = mid[j + 2, 1] * (1+PERCENT_RECTANGLE_VALIDATION)

        distanceNext = abs(mid[j + 1, 0]-mid[j, 0])

        next_bool = (mid[j, 1] > lowerNext_1 and mid[j, 1] < upperNext_1) and (mid[j, 1] > lowerNext_2 and mid[j, 1] < upperNext_2)
        next_dist_bool = ((distanceNext < distance_high_treshold) and (distanceNext > distance_low_treshold))

        if prev_boolean and prev_dist_bool or next_bool and next_dist_bool:
            cv2.rectangle(imgContour3, (coord[j, 0], coord[j, 1]),
                            ((coord[j, 0] + coord[j, 2]), (coord[j, 1] + coord[j, 3])), (255, 255, 0), 1)

            b[n2] = ([coord[j, 0] + (coord[j, 2] // 2), coord[j, 1] + (coord[j, 3] // 2)])

        n2 = n2 + 1
    '''
    cv2.imshow("post-filtering",imgContour3)
    cv2.waitKey(0)
    '''

    b = b[~np.all(b == 0, axis=1)] #enleve les 0 ?
    TAILLE = b.size


    # print("compteur : ", compt1, compt2,compt3,compt4, b.shape,TAILLE)
    c1 = np.arange(TAILLE).reshape(TAILLE // 2, 2)
    c2 = np.arange(TAILLE).reshape(TAILLE // 2, 2)
    c3 = np.arange(TAILLE).reshape(TAILLE // 2, 2)
    c4 = np.arange(TAILLE).reshape(TAILLE // 2, 2)

    for i in range(TAILLE // 2):
        c1[i] = 0
        c2[i] = 0
        c3[i] = 0
        c4[i] = 0

    # Detection of places lines (maximum 4 lines)
    Q = np.zeros(4)
    init = False
    nb_lines_of_places = 0
    for i in range(b.size // 2 - 1):
        y = b[i,1]
        if init == False:
            init = True
            Q[nb_lines_of_places] = y+1
            nb_lines_of_places = nb_lines_of_places+1
        else:
            y2 = b[i+1,1]
            if y-y2 > y*PERCENT_GAP_BETWEEN_LINES:
                Q[nb_lines_of_places] = y2+1
                nb_lines_of_places = nb_lines_of_places+1
    Q = Q[Q != 0.0]

    # on tri selon les coordonnées y
    for i in range(TAILLE // 2):
        if nb_lines_of_places == 4:
            if b[i, 1] < Q[3]:
                c1[i] = b[i] 
            elif b[i, 1] > Q[3] and b[i, 1] < Q[2]:
                c2[i] = b[i]
            elif b[i, 1] > Q[2] and b[i, 1] < Q[1]:
                c3[i] = b[i]
            elif b[i, 1] > Q[1] and b[i, 1] < Q[0]:
                c4[i] = b[i]
        elif nb_lines_of_places == 2:
            if b[i, 1] > Q[1]:
                c3[i] = b[i]
            else:
                c4[i] = b[i]

    c1 = c1[~np.all(c1 == 0, axis=1)]
    c2 = c2[~np.all(c2 == 0, axis=1)]
    c3 = c3[~np.all(c3 == 0, axis=1)]
    c4 = c4[~np.all(c4 == 0, axis=1)]

    c1 = c1[c1[:, 0].argsort()[::-1]]
    c2 = c2[c2[:, 0].argsort()[::-1]]
    c3 = c3[c3[:, 0].argsort()[::-1]]
    c4 = c4[c4[:, 0].argsort()[::-1]]

    som = 0
    distance = 0
    skipped = 0
    for j in range(c1.size // 2 - 1):
        distance = abs(c1[j + 1, 0] - c1[j, 0])
        if som == 0 or distance < (som/(j-skipped)) * MULTIPLIER_DISTANCE_FOR_PLACES_INTERPOLATION:
            som = som + distance
        else:
            skipped = skipped + 1
    averagedist1 = som / (c1.size // 2 - 1 - skipped)
    #print("Avg dist of c1 =", averagedist1, som)

    som = 0
    distance = 0
    skipped = 0
    for j in range(c2.size // 2 - 1):
        distance = abs(c2[j + 1, 0] - c2[j, 0])
        if som == 0 or distance < (som/(j-skipped)) * MULTIPLIER_DISTANCE_FOR_PLACES_INTERPOLATION:
            som = som + distance
        else:
            skipped = skipped + 1
    averagedist2 = som / (c2.size // 2 - 1 - skipped)
    #print("Avg dist of c2 =", averagedist2, som)

    som = 0
    distance = 0
    skipped = 0
    for j in range(c3.size // 2 - 1):
        distance = abs(c3[j + 1, 0] - c3[j, 0])
        if som == 0 or distance <= (som/(j-skipped)) * MULTIPLIER_DISTANCE_FOR_PLACES_INTERPOLATION:
            som = som + distance
        else:
            skipped = skipped + 1
    averagedist3 = som / (c3.size // 2 - 1 - skipped)
    #print("Avg dist of c3 =", averagedist3, som)

    som = 0
    distance = 0
    skipped = 0
    for j in range(c4.size // 2 - 1):
        distance = abs(c4[j + 1, 0] - c4[j, 0])
        if som == 0 or distance < (som/(j-skipped)) * MULTIPLIER_DISTANCE_FOR_PLACES_INTERPOLATION:
            som = som + distance
        else:
            skipped = skipped + 1
    averagedist4 = som / (c4.size // 2 - 1 - skipped)
    #print("Avg dist of c4 =", averagedist4, som)

    max_size = max(c1.size // 2-1,c2.size // 2-1)
    j = 0
    while j < max_size: 
        if (j == c1.size // 2-1) or (j == c2.size // 2-1):
            if c1.size // 2 < c2.size // 2:
                distance_x = abs(c2[j + 1, 0] - c2[j, 0])
                distance_y = abs(c2[j + 1, 1] - c2[j, 1])
                l = [c1[j, 0] - distance_x, c1[j, 1] - distance_y]
                c1 = np.insert(c1, j + 1, l, axis=0)
                #print("insertion into a c1 for x = " + str(l))
            else:
                distance_x = abs(c1[j + 1, 0] - c1[j, 0])
                distance_y = abs(c1[j + 1, 1] - c1[j, 1])
                l = [c2[j, 0] - distance_x, c2[j, 1] - distance_y]
                c2 = np.insert(c2, j + 1, l, axis=0)
                #print("insertion into a c2 for x = " + str(l))
        else:
            distance_x_c1 = abs(c1[j + 1, 0] - c1[j, 0])
            distance_y_c1 = abs(c1[j + 1, 1] - c1[j, 1])
            distance_x_c2 = abs(c2[j + 1, 0] - c2[j, 0])
            distance_y_c2 = abs(c2[j + 1, 1] - c2[j, 1])
            gap = abs(distance_x_c1 - distance_x_c2)
            mean = (distance_x_c1 + distance_x_c2) / 2
            incert = mean * 0.2
            if gap > incert:
                if distance_x_c1 > distance_x_c2:
                    l = [c1[j, 0] - distance_x_c2, c1[j, 1] - distance_y_c2]
                    c1 = np.insert(c1, j + 1, l, axis=0)
                    #print("insertion into c1 for x = " + str(l))
                else:
                    l = [c2[j, 0] - distance_x_c1, c2[j, 1] - distance_y_c1]
                    c2 = np.insert(c2, j + 1, l, axis=0)
                    #print("insertion into c2 for x = " + str(l))
            else:
                j = j+1
        

    max_size = max(c3.size // 2-1,c4.size // 2-1)
    j = 0
    while j < max_size: 
        if (j == c3.size // 2-1) or (j == c4.size // 2-1):
            if c3.size // 2 < c4.size // 2:
                distance_x = abs(c4[j + 1, 0] - c4[j, 0])
                distance_y = abs(c4[j + 1, 1] - c4[j, 1])
                l = [c3[j, 0] - distance_x, c3[j, 1] - distance_y]
                c3 = np.insert(c3, j + 1, l, axis=0)
                #print("insertion into c3 for x = " + str(l))
            else:
                distance_x = abs(c3[j + 1, 0] - c3[j, 0])
                distance_y = abs(c3[j + 1, 1] - c3[j, 1])
                l = [c4[j, 0] - distance_x, c4[j, 1] - distance_y]
                c4 = np.insert(c4, j + 1, l, axis=0)
                #print("insertion into c4 for x = " + str(l))
        else:
            distance_x_c1 = abs(c3[j + 1, 0] - c3[j, 0])
            distance_y_c1 = abs(c3[j + 1, 1] - c3[j, 1])
            distance_x_c2 = abs(c4[j + 1, 0] - c4[j, 0])
            distance_y_c2 = abs(c4[j + 1, 1] - c4[j, 1])
            gap = abs(distance_x_c1 - distance_x_c2)
            mean = (distance_x_c1 + distance_x_c2) / 2
            incert = mean * 0.2
            if gap > incert:
                if distance_x_c1 > distance_x_c2:
                    l = [c3[j, 0] - distance_x_c2, c3[j, 1] - distance_y_c2]
                    c3 = np.insert(c3, j + 1, l, axis=0)
                    #print("insertion into c3 for x = " + str(l))
                else:
                    l = [c4[j, 0] - distance_x_c1, c4[j, 1] - distance_y_c1]
                    c4 = np.insert(c4, j + 1, l, axis=0)
                    #print("insertion into c4 for x = " + str(l))
            else:
                j = j+1
    counter = 0
    yml_output = out

    # COORD 
    # p1 = (c4[j, 0], c4[j, 1]) (bas droite) 2
    # p2 = (c4[j + 1, 0], c4[j + 1, 1]) (bas gauche) 1 
    # p3 = (c3[j, 0], c3[j, 1]) (haut droite) 3
    # p4 = (c3[j + 1, 0], c3[j + 1, 1]) (haut gauche) 4

    for j in range(c3.size//2-1):
        if j % 2 == 0:
            colour = (255, 255, 0)
        else:
            colour = (0, 255, 255)
        if j < c3.size//2-1 and j < c4.size//2-1:
            cv2.line(imgContour3, (c4[j, 0], c4[j, 1]), (c4[j + 1, 0], c4[j + 1, 1]), colour, 1)
            cv2.line(imgContour3, (c3[j, 0], c3[j, 1]), (c3[j + 1, 0], c3[j + 1, 1]), colour, 1)
            cv2.line(imgContour3, (c4[j, 0], c4[j, 1]), (c3[j, 0], c3[j, 1]), colour, 1)
            cv2.line(imgContour3, (c4[j + 1, 0], c4[j + 1, 1]), (c3[j + 1, 0], c3[j + 1, 1]), colour, 1)
            yml_output.write('-\n') 
            yml_output.write("                 id: " + str(counter) + "\n")
            yml_output.write("                 coordinates: ") 
            yml_output.write("[[" + str(c4[j + 1, 0]) + "," + str(c4[j + 1, 1]) + "],")
            yml_output.write("[" + str(c4[j, 0]) + "," + str(c4[j, 1]) + "],")
            yml_output.write("[" + str(c3[j, 0]) + "," + str(c3[j, 1]) + "],")
            yml_output.write("[" + str(c3[j + 1, 0]) + "," + str(c3[j + 1, 1]) + "]]")
            yml_output.write("\n")
            counter = counter+1

    # COORD 
    # p1 = (c2[j, 0], c2[j, 1]) (bas droite) 2
    # p2 = (c2[j + 1, 0], c2[j + 1, 1]) (bas gauche) 1
    # p3 = (c1[j, 0], c1[j, 1]) (haut droite) 3
    # p4 = (c1[j + 1, 0], c1[j + 1, 1]) (haut gauche) 4
    for j in range(c2.size//2-1):  #c2.size//2-1
        if j % 2 == 0:
            colour = (255, 255, 0)
        else:
            colour = (0, 255, 255)
        if j < c1.size//2-1 and j < c2.size//2-1:
            cv2.line(imgContour3, (c2[j, 0], c2[j, 1]), (c2[j + 1, 0], c2[j + 1, 1]), colour, 2)
            cv2.line(imgContour3, (c1[j, 0], c1[j, 1]), (c1[j + 1, 0], c1[j + 1, 1]), colour, 2)
            cv2.line(imgContour3, (c2[j, 0], c2[j, 1]), (c1[j, 0], c1[j, 1]), colour, 2)
            cv2.line(imgContour3, (c2[j + 1, 0], c2[j + 1, 1]), (c1[j + 1, 0], c1[j + 1, 1]), colour, 2)
            yml_output.write('-\n') 
            yml_output.write("                 id: " + str(counter) + "\n")
            yml_output.write("                 coordinates: ") 
            yml_output.write("[[" + str(c2[j + 1, 0]) + "," + str(c2[j + 1, 1]) + "],")
            yml_output.write("[" + str(c2[j, 0]) + "," + str(c2[j, 1]) + "],")
            yml_output.write("[" + str(c1[j, 0]) + "," + str( c1[j, 1]) + "],")
            yml_output.write("[" + str(c1[j + 1, 0]) + "," + str(c1[j + 1, 1]) + "]]")
            yml_output.write("\n")
            counter = counter+1

    yml_output.close()