
import random
import math

import cv2
import numpy as np
def dist_euc(c1, c2):
    x1, y1 = cidades[c1]
    x2, y2 = cidades[c2]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def soma_dist_cam(caminho):
    soma = 0
    for i in range(N_CIDADES - 1):
        soma += dist_euc(caminho[i], caminho[i+1])
    soma += dist_euc(caminho[N_CIDADES - 1], caminho[0])
    return soma

def guloso(cidades_imput):
    global cidades, N_CIDADES
    cidades = cidades_imput
    N_CIDADES = len(cidades)

    caminho = []
    caminho.append(0)

    for i in range(N_CIDADES):
        menor = 100000000000000000
        melhor = 0
        for j in range (N_CIDADES):
            dist = dist_euc(caminho[i], j)
            if (dist < menor and caminho[i] != j):
                menor = menor
                melhor = j
        caminho.append(melhor)
    
    soma_total = soma_dist_cam(caminho)

    print(f"resultado guloso: {soma_total}")

    return soma_total


def mostra_CV(caminho):
    #CV

    # coords das cidades (ex: [(x1,y1), (x2,y2), ...])
    coords = []

    for i in range(N_CIDADES):
        coords.append(cidades[i])

    # cria imagem em branco (500x500 com fundo preto)
    img = np.ones(((100) * 10, (100) * 10, 3), dtype=np.uint8) * 255

    # desenha as cidades (bolinhas azuis)
    for (x, y) in coords:
        cv2.circle(img, (x * 10, y * 10), 6, (0, 0, 255), -1)

    # desenha as linhas do caminho
    for i in range(len(caminho) - 1):
        x1, y1 = coords[caminho[i]]
        x2, y2 = coords[caminho[i + 1]]
        cv2.line(img, (x1* 10, y1* 10), (x2* 10, y2* 10), (255, 0, 0), 2)

    # fecha o ciclo (última cidade -> primeira)
    x1, y1 = coords[caminho[N_CIDADES - 1]]
    x2, y2 = coords[caminho[0]]
    cv2.line(img, (x1* 10, y1* 10), (x2* 10, y2* 10), (255, 0, 0), 2)

    # mostra a imagem
    cv2.imshow("Caminho", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()