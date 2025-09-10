import random
import math

import cv2
import numpy as np

TEMP_INICIAL = 10 ** 5   #n_cidades ** (n_cidades // (math.log2(n_cidades)))
cidades = {} #{0: (0, 10), 1: (2, 6), 2: (3, 8), 3: (1, 10), 4: (10, 4), 5: (10, 8), 6: (8, 3), 7: (7, 7), 8: (6, 6), 9: (1, 3)}

MAX_VAL = 100

def ini_cidades_aleatorias(n_cidades):
    for i in range(n_cidades):
        cidades[i] = (random.randint(0, MAX_VAL), random.randint(0, MAX_VAL))

def dist_euc(c1, c2):
    x1, y1 = cidades[c1]
    x2, y2 = cidades[c2]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def rand_estado_inicial(n_cidades):
    est_atual = list(range(n_cidades))
    random.shuffle(est_atual)          
    return est_atual

def rand_vizinho(est_atual, soma_atual, n_cidades):
    cidade_1, cidade_2 = random.sample(range(n_cidades), 2)

    vizinho = est_atual.copy()

    vizinho[cidade_1] = est_atual[cidade_2]
    vizinho[cidade_2] = est_atual[cidade_1]

    somat = soma_dist_cam(vizinho, n_cidades)

    return vizinho, somat

def mostra_val_cidades(n_cidades):
    for i in range(n_cidades):
        print(f"cidade {i} (x: {cidades[i][0]}, y: {cidades[i][1]})")# para {i+1} (x: {cidades[i+1][0]}, y: {cidades[i+1][1]}) ")
        #print(dist_euc(i, i + 1))
    
def soma_dist_cam(caminho, n_cidades):
    soma = 0
    for i in range(n_cidades - 1):
        soma += dist_euc(caminho[i], caminho[i+1])
    soma += dist_euc(caminho[n_cidades - 1], caminho[0])
    return soma

def temperatura(t_atual):

    # valor entre 0 e 1 de quanto o t_atual é do inicial, quanto mais longe mai baixo
    return t_atual / TEMP_INICIAL

def tempera(cidades_imput):
    global cidades
    cidades = cidades_imput
    n_cidades = len(cidades)

    est_atual = rand_estado_inicial(n_cidades)
    soma_atual = soma_dist_cam(est_atual, n_cidades)
    t_atual = TEMP_INICIAL

    menor_cam = est_atual.copy()
    soma_menor = soma_atual

    while (t_atual > 0):
        vizinho, soma_viz = rand_vizinho(est_atual, soma_atual, n_cidades)
        #print(f"caminho atual: {est_atual} soma atual: {soma_atual} ")
        #print(f"caminho vizi: {vizinho} soma atual: {soma_viz} ")

        if (soma_atual > soma_viz):
            est_atual = vizinho
            soma_atual = soma_viz

        else:
            #dist_media = math.sqrt(MAX_VAL // 2 + MAX_VAL // 2) * n_cidades
            
            prob =  (1 + ((soma_atual - soma_viz) / soma_viz)) * temperatura(t_atual)
            
            #math.exp(((soma_atual - soma_viz) / soma_atual) * dist_media / temperatura(t_atual))
            #print(prob)
            if (random.random() < prob):
                est_atual = vizinho
                soma_atual = soma_viz
        
        if (soma_atual < soma_menor):
            menor_cam = est_atual.copy()
            soma_menor = soma_atual

        #print(f" -> caminho escolhido: {est_atual}")
        t_atual -= 1

    #mostra_val_cidades()

    if (soma_atual > soma_menor):
        est_atual = menor_cam.copy()
        soma_atual = soma_menor

    print(f"resultado Tempera: {soma_atual}")

    return est_atual, soma_atual

def main():
    
    n_cidades = 10

    ini_cidades_aleatorias(n_cidades)
    
    est_atual, soma_atual = tempera(cidades)

    print("caminho encontrado: ")
    print(est_atual)
    print("soma total do caminho: ")
    print(soma_atual)

    
    #CV

    # coords das cidades (ex: [(x1,y1), (x2,y2), ...])
    coords = []

    for i in range(n_cidades):
        coords.append(cidades[i])

    # cria imagem em branco (500x500 com fundo preto)
    img = np.zeros(((MAX_VAL) * 10, (MAX_VAL) * 10, 3), dtype=np.uint8)

    # desenha as cidades (bolinhas azuis)
    for (x, y) in coords:
        cv2.circle(img, (x * 10, y * 10), 6, (255, 0, 0), -1)

    melhor_cam = est_atual

    # desenha as linhas do caminho
    for i in range(len(melhor_cam) - 1):
        x1, y1 = coords[melhor_cam[i]]
        x2, y2 = coords[melhor_cam[i + 1]]
        cv2.line(img, (x1* 10, y1* 10), (x2* 10, y2* 10), (0, 255, 0), 2)

    # fecha o ciclo (última cidade -> primeira)
    x1, y1 = coords[melhor_cam[n_cidades - 1]]
    x2, y2 = coords[melhor_cam[0]]
    cv2.line(img, (x1* 10, y1* 10), (x2* 10, y2* 10), (0, 255, 0), 2)

    # mostra a imagem
    cv2.imshow("Caminho", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()