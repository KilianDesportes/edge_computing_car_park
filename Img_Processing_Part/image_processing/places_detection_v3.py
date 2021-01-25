import cv2
import numpy as np
from numpy import zeros, array

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


    img = imgDilation.copy()

    AREAMAX = 295
    AREAMIN = 115

    # SI mal cadré : loin du haut près du bord bottom

    Q1 = 280
    Q2 = 400
    Q3 = 550
    Q4 = 635    #635 image 20 et 630 image 21
    exception1 = array([3, 4, 5, 6, 7])  # METTRE LE NUMERO DE PLACE MANQUANT 3, 4, 5, 6, 7
    exception2 = array([2, 6])   #2, 6 image 20 et 1 image 21
    exception34 = array([11111])  # PLACE HANDICAPÉ   #11110 image 20 et 0 image 21
    exception12 = array([5])  # PLACE HANDICAPÉ


    cv2.line(imgContour3, (0, Q1), (650, Q1), (0, 0, 255), 4)
    cv2.line(imgContour3, (0, Q2), (650, Q2), (0, 0, 255), 4)
    cv2.line(imgContour3, (0, Q3), (650, Q3), (0, 0, 255), 4)
    cv2.line(imgContour3, (0, Q4), (650, Q4), (0, 0, 255), 4)

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    i = 0
    n = 0
    n2 = 0
    n3 = 0
    mid = np.arange(400).reshape(200, 2)
    coord = np.arange(800).reshape(200, 4)
    # print(mid[1],mid[3,0],mid[4,0])
    # mid[1,1]=(mid[3,0]+mid[4,0])
    coord[2] = ([6, 9, 9, 6])

    cv2.line(imgContour2, (0, Q1), (650, Q1), (0, 0, 255), 4)
    cv2.line(imgContour2, (0, Q2), (650, Q2), (0, 0, 255), 4)
    cv2.line(imgContour2, (0, Q3), (650, Q3), (0, 0, 255), 4)
    cv2.line(imgContour2, (0, Q4), (650, Q4), (0, 0, 255), 4)

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
                if w < h * 3 and h < w * 3:  # max multiplication par 3 entre hauteur et largeur pour les carrés
                    coord[n] = (x, y, w, h)
                    mid[n] = ((x + (w // 2)), (y + (h // 2)))
                    n = n + 1
                    cv2.rectangle(imgContour2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    a = np.arange(n).reshape(n, 1)
    h = np.arange(n).reshape(n, 1)
    a1 = np.arange(n).reshape(n, 1)
    a2 = np.arange(n).reshape(n, 1)
    b = np.arange(n * 2).reshape(n, 2)
    for i in range(n):
        b[i] = 0
    c = np.arange(n * 2).reshape(n, 2)
    compt1 = 0
    compt2 = 0
    compt3 = 0
    compt4 = 0
    n3 = 0
    n4 = 0
    d = 0
    check = 0
    ok1 = 0
    ok2 = 0
    ok3 = 0
    ok4 = 0

    # MEME AXE Y ET DISTANCE X FILTRE PREVIOUS COMPARISON
    for j in range(0,
                   n - 3):  # si n = 55 on va de 0 à 54   #47eme a peine plus bas mais considéré comme en dessous il est compté avant
        a = (mid[j, 0] - mid[j - 1, 0])
        distance = abs(a)

        if mid[j, 1] > 0:
            # combiner avec OR

            # print("SUCCES on a j =", j)

            # print("TESSSST DES N ON EST BIEN DANS BOUCLE",n2,mid[i,1],mid[j,1])
            cv2.rectangle(imgContour3, (coord[j, 0], coord[j, 1]),
                          ((coord[j, 0] + coord[j, 2]), (coord[j, 1] + coord[j, 3])), (255, 255, 0), 1)

            # coord[2] = ([6, 9, 9, 6])
            b[n2] = ([coord[j, 0] + (coord[j, 2] // 2), coord[j, 1] + (coord[j, 3] // 2)])

            cv2.line(imgContour3, (coord[j, 0] + (coord[j, 2] // 2), coord[j, 1] + (coord[j, 3] // 2)),
                     (coord[j, 0] + (coord[j, 2] // 2) + 1, coord[j, 1] + (coord[j, 3] // 2) + 1), (0, 0, 255),
                     2)  # bien penser au // pour diviser en entier et retouner un int
            # mid[i] = [(x + (w // 2)), (y + (h // 2))]

            if b[n2, 1] < Q1:  # utiliser image.shape or image.size
                compt1 = compt1 + 1
                # w1[n2]=b[n2]

            if b[n2, 1] > Q1 and b[n2, 1] < Q2:
                compt2 = compt2 + 1
                # w2[n2] = b[n2]

            if b[n2, 1] > Q2 and b[n2, 1] < Q3:
                compt3 = compt3 + 1
                # w3[n2] = b[n2]

            if b[n2, 1] > Q3 and b[n2, 1] < Q4:
                compt4 = compt4 + 1
                # w4[n2] = b[n2]
            n2 = n2 + 1

    b = b[~np.all(b == 0, axis=1)]
    TAILLE = b.size

    c1 = np.arange(TAILLE).reshape(TAILLE // 2, 2)
    c2 = np.arange(TAILLE).reshape(TAILLE // 2, 2)
    c3 = np.arange(TAILLE).reshape(TAILLE // 2, 2)
    c4 = np.arange(TAILLE).reshape(TAILLE // 2, 2)
    for i in range(TAILLE // 2):
        c1[i] = 0
        c2[i] = 0
        c3[i] = 0
        c4[i] = 0
    for i in range(TAILLE // 2):
        if b[i, 1] < Q1:
            c1[i] = b[i]  # créer c plus haut avec taille=TAILLE//2

        if b[i, 1] > Q1 and b[i, 1] < Q2:
            ok2 = ok2 + 1
            c2[i] = b[i]

        if b[i, 1] > Q2 and b[i, 1] < Q3:
            ok3 = ok3 + 1
            c3[i] = b[i]

        if b[i, 1] > Q3 and b[i, 1] < Q4:
            ok4 = ok4 + 1
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
    for j in range(c1.size // 2 - 1):
        a = (c1[j + 1, 0] - c1[j, 0])
        distance = abs(a)
        som = som + distance
    averagedist1 = som / (c1.size // 2 - 1)

    som = 0
    distance = 0
    for j in range(c2.size // 2 - 1):
        a = (c2[j + 1, 0] - c2[j, 0])
        distance = abs(a)
        som = som + distance
    averagedist2 = som / (c2.size // 2 - 1)

    som = 0
    distance = 0
    for j in range(c3.size // 2 - 1):
        a = (c3[j + 1, 0] - c3[j, 0])
        distance = abs(a)
        som = som + distance
    averagedist3 = som / (c3.size // 2 - 1)

    som = 0
    distance = 0
    for j in range(c4.size // 2 - 1):
        a = (c4[j + 1, 0] - c4[j, 0])
        distance = abs(a)
        som = som + distance
    averagedist4 = som / (c4.size // 2 - 1)

    pop = 0
    cnt3 = 0
    cnt4 = 0
    for v in range(20):  # taille à modifier SI TROP LONG CALCUL TROP DE BOUCLES OU SI RESULTAT PAS LINEAIRE

        for j in range(c1.size // 2-1):
            a = (c1[j + 1, 0] - c1[j, 0])  # distance en x
            h = (c1[j + 1, 1] - c1[j, 1])  # distance en y

            distance = abs(a)
            h = abs(h)
            if j != 100000:  # un watchdog
                if distance >= 60 or distance <= 20 or h >= 10:
                    l = [c1[j, 0] - averagedist1 +15,c1[j, 1]-1]  # IMPORTANT ICI SELON ZOOM DE L'IMAGE +15 ou +12 change tout
                    c1 = np.insert(c1, j + 1, l, axis=0)

        for j in range(c2.size // 2):
            a = (c2[j + 1, 0] - c2[j, 0])  # distance en x
            h = (c2[j + 1, 1] - c2[j, 1])  # distance en y

            distance = abs(a)
            h = abs(h)
            if j != 100000:
                if distance >= 60 or distance <= 20 or h >= 10:
                    l = [c2[j, 0] - averagedist2 + 5, c2[j, 1]-1]
                    c2 = np.insert(c2, j + 1, l, axis=0)

    ##### POUR C3 C4

    for v in range(20):
        for j in range(c4.size // 2-1):
            a = (c4[j + 1, 0] - c4[j, 0])  # distance en x
            h = (c4[j + 1, 1] - c4[j, 1])  # distance en y

            distance = abs(a)
            h = abs(h)
            if j != 100000:
                if distance >= 60 or distance <= 20 or h >= 10:
                    cnt4 = cnt4 + 0.5  # 0,5 pour image 21 et 20
                    l = [c4[j, 0] - averagedist4+cnt4, c4[j, 1]]
                    c4 = np.insert(c4, j + 1, l, axis=0)

        for j in range(c3.size // 2):
            a = (c3[j + 1, 0] - c3[j, 0])  # distance en x
            h = (c3[j + 1, 1] - c3[j, 1])  # distance en y

            distance = abs(a)
            h = abs(h)
            if j != 100000:
                if distance >= 60 or distance <= 20 or h >= 10:
                    cnt3 = cnt3-0.8  # cnt3-0,8 pour image 21 et -3 pour image 20
                    l = [c3[j, 0] - averagedist3 +cnt3, c3[j, 1]]   #c3[j, 1]-1 pour image 20 et c3[j, 1] pour image 21
                    c3 = np.insert(c3, j + 1, l, axis=0)
                    break

    counter = 0
    yml_output = out


    q = 0
    for j in range(compt4):  #compt4+1 pour image 21 et compt4 pour image 20
        if j != exception2[q]:
            if j % 2 == 0:
                colour = (255, 255, 0)
            else:
                colour = (0, 255, 255)
            cv2.line(imgContour3, (c4[j, 0], c4[j, 1]), (c4[j + 1, 0], c4[j + 1, 1]), colour, 3)
            cv2.line(imgContour3, (c3[j, 0], c3[j, 1]), (c3[j + 1, 0], c3[j + 1, 1]), colour, 3)
            cv2.line(imgContour3, (c4[j, 0], c4[j, 1]), (c3[j, 0], c3[j, 1]), colour, 3)
            cv2.line(imgContour3, (c4[j + 1, 0], c4[j + 1, 1]), (c3[j + 1, 0], c3[j + 1, 1]), colour, 3)
            yml_output.write('-\n')
            yml_output.write("                 id: " + str(counter) + "\n")
            yml_output.write("                 handicap_list: " + str(1) + "\n")
            yml_output.write("                 coordinates: ")
            yml_output.write("[[" + str(c4[j + 1, 0]) + "," + str(c4[j + 1, 1]) + "],")
            yml_output.write("[" + str(c4[j, 0]) + "," + str(c4[j, 1]) + "],")
            yml_output.write("[" + str(c3[j, 0]) + "," + str(c3[j, 1]) + "],")
            yml_output.write("[" + str(c3[j + 1, 0]) + "," + str(c3[j + 1, 1]) + "]]")
            yml_output.write("\n")
            counter = counter + 1
        else:
            if q < exception2.size - 1:
                q = q + 1
                print("exception1 draw place")
                print("exception2 draw place")
        if j == exception34[0]:
            colour = (255, 0, 0)
            cv2.line(imgContour3, (c4[j, 0], c4[j, 1]), (c4[j + 1, 0], c4[j + 1, 1]), colour, 5)
            cv2.line(imgContour3, (c3[j, 0], c3[j, 1]), (c3[j + 1, 0], c3[j + 1, 1]), colour, 5)
            cv2.line(imgContour3, (c4[j, 0], c4[j, 1]), (c3[j, 0], c3[j, 1]), colour, 5)
            cv2.line(imgContour3, (c4[j + 1, 0], c4[j + 1, 1]), (c3[j + 1, 0], c3[j + 1, 1]), colour, 5)
            yml_output.write('-\n')
            yml_output.write("                 id: " + str(counter) + "\n")
            yml_output.write("                 handicap_list: " + str(0) + "\n")
            yml_output.write("                 coordinates: ")
            yml_output.write("[[" + str(c4[j + 1, 0]) + "," + str(c4[j + 1, 1]) + "],")
            yml_output.write("[" + str(c4[j, 0]) + "," + str(c4[j, 1]) + "],")
            yml_output.write("[" + str(c3[j, 0]) + "," + str(c3[j, 1]) + "],")
            yml_output.write("[" + str(c3[j + 1, 0]) + "," + str(c3[j + 1, 1]) + "]]")
            yml_output.write("\n")
            counter = counter + 1

    k = 0
    for j in range(compt2+1):  # compt2+1 pour image 20 et compt2 pour image 21
        if j != exception1[k]:
            if j % 2 == 0:
                colour = (255, 255, 0)
            else:
                colour = (0, 255, 255)
            cv2.line(imgContour3, (c2[j, 0], c2[j, 1]), (c2[j + 1, 0], c2[j + 1, 1]), colour, 3)
            cv2.line(imgContour3, (c1[j, 0], c1[j, 1]), (c1[j + 1, 0], c1[j + 1, 1]), colour, 3)
            cv2.line(imgContour3, (c2[j, 0], c2[j, 1]), (c1[j, 0], c1[j, 1]), colour, 3)
            cv2.line(imgContour3, (c2[j + 1, 0], c2[j + 1, 1]), (c1[j + 1, 0], c1[j + 1, 1]), colour, 3)
            yml_output.write('-\n')
            yml_output.write("                 id: " + str(counter) + "\n")
            yml_output.write("                 handicap_list: " + str(1) + "\n")
            yml_output.write("                 coordinates: ")
            yml_output.write("[[" + str(c2[j + 1, 0]) + "," + str(c2[j + 1, 1]) + "],")
            yml_output.write("[" + str(c2[j, 0]) + "," + str(c2[j, 1]) + "],")
            yml_output.write("[" + str(c1[j, 0]) + "," + str(c1[j, 1]) + "],")
            yml_output.write("[" + str(c1[j + 1, 0]) + "," + str(c1[j + 1, 1]) + "]]")
            yml_output.write("\n")
            counter = counter + 1
        else:
            if k < exception1.size - 1:
                k = k + 1
                print("exception1 draw place")
        if j == exception12[0]:
            colour = (255, 0, 0)
            cv2.line(imgContour3, (c2[j, 0]+20, c2[j, 1]), (c2[j + 1, 0] + 10, c2[j + 1, 1]), colour, 5)
            cv2.line(imgContour3, (c1[j, 0]+10, c1[j, 1]), (c1[j + 1, 0], c1[j + 1, 1]), colour, 5)
            cv2.line(imgContour3, (c2[j, 0]+20, c2[j, 1]), (c1[j, 0]+10, c1[j, 1]), colour, 5)
            cv2.line(imgContour3, (c2[j + 1, 0] + 10, c2[j + 1, 1]), (c1[j + 1, 0], c1[j + 1, 1]), colour, 5)
            yml_output.write('-\n')
            yml_output.write("                 id: " + str(counter) + "\n")
            yml_output.write("                 handicap_list: " + str(0) + "\n")
            yml_output.write("                 coordinates: ")
            yml_output.write("[[" + str(c2[j + 1, 0]+10) + "," + str(c2[j + 1, 1]) + "],")
            yml_output.write("[" + str(c2[j, 0]+20) + "," + str(c2[j, 1]) + "],")
            yml_output.write("[" + str(c1[j, 0]+10) + "," + str(c1[j, 1]) + "],")
            yml_output.write("[" + str(c1[j + 1, 0]) + "," + str(c1[j + 1, 1]) + "]]")
            yml_output.write("\n")
            counter = counter + 1

    #    print("on a distance moyenne =", averagedist4, som, c1.shape, c2.shape, c3.shape, c4.shape,c2[11],c1[11])

    yml_output.close()
