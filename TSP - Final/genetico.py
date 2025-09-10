import random
import math

import cv2
import numpy as np

#N_CIDADES = 10
MAX_VAL = 100

N_GERACOES = 10 ** 2
TAM_POPULACAO = 10 ** 2

CHANCE_MUT = 0.20
PUN_REP = 1

melhores_viz = []

cidades = {} 
#cidades = {0: (0, 10), 1: (2, 6), 2: (3, 8), 3: (1, 10), 4: (10, 4), 5: (10, 8), 6: (8, 3), 7: (7, 7), 8: (6, 6), 9: (1, 3)}

# Função para randomizar a amostra
def ini_cidades_aleatorias(n_cidades):
    for i in range(n_cidades):
        cidades[i] = (random.randint(0, MAX_VAL), random.randint(0, MAX_VAL))

# calcula a distancia de 2 cidades
def dist_euc(c1, c2):
    x1, y1 = cidades[c1]
    x2, y2 = cidades[c2]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# inicializa um caminho aleatorio
def rand_estado_inicial(n_cidades):
    est_atual = list(range(n_cidades))
    random.shuffle(est_atual)          
    return est_atual

# mostra cidades
def mostra_val_cidades(n_cidades):
    for i in range(n_cidades):
        print(f"cidade {i} (x: {cidades[i][0]}, y: {cidades[i][1]})")# para {i+1} (x: {cidades[i+1][0]}, y: {cidades[i+1][1]}) ")
        #print(dist_euc(i, i + 1))

# percorre um caminho somando suas distancias
def soma_dist_cam(caminho, n_cidades):
    soma = 0
    for i in range(n_cidades - 1):
        soma += dist_euc(caminho[i], caminho[i+1])
    soma += dist_euc(caminho[n_cidades - 1], caminho[0])
    return soma

# percorre um caminho mostrando suas distancias
def mostra_dist_caminho(caminho, n_cidades):
    for i in range(n_cidades - 1):
        print(dist_euc(caminho[i], caminho[i+1]))
    print(dist_euc(caminho[n_cidades - 1], caminho[0]))

# calcula matriz de distancias euclidianas
def define_melhores_vizinhos(n_cidades):
    for i in range(n_cidades):
        menor_dist = MAX_VAL * MAX_VAL * n_cidades
        seg_menor_dist = menor_dist

        for j in range(n_cidades):

            if (i != j):
                dist = dist_euc(i, j)
                if (dist < menor_dist):
                    seg_menor_dist = menor_dist
                    menor_dist = dist
                elif (dist < seg_menor_dist):
                    seg_menor_dist = dist
        
        melhores_viz.append(menor_dist + seg_menor_dist)

# retorna valore entre 0 e 1 do fitness de um caminho com o melhor caminho
def fitness(caminho, n_cidades):
    soma_fit = 0
    histograma = []
    for i in range(n_cidades):
        histograma.append(0)

    for i in range(n_cidades):
        ante = i - 1
        if (ante < 0):
            ante = n_cidades - 1
        atual = i
        prox = i + 1
        if (prox >= n_cidades):
            prox = 0

        ante = caminho[ante]
        atual = caminho[atual]
        prox = caminho[prox]

        div = 0

        if (ante == atual):
            soma_fit -= PUN_REP
        else:
            div += dist_euc(ante, atual)
        if (atual == prox):
            soma_fit -= PUN_REP
        else:
            div += dist_euc(atual, prox)

        if (div != 0 and (ante != atual) and (prox != atual)):
            soma_fit += melhores_viz[i] / div

        histograma[caminho[i]] += 1
        if (histograma[caminho[i]] > 1):
            soma_fit -= PUN_REP

    return max(soma_fit / (2 * n_cidades), 0)

# gera uma mutação aleatoria em um caminho 
def mutacao(caminho, n_cidades):
    histograma = []
    for i in range(n_cidades):
        histograma.append(0)

    for i in range(n_cidades):
        histograma[caminho[i]] += 1
        prob_mut = CHANCE_MUT * (histograma[caminho[i]] ** 2)
        if (random.random() < prob_mut):
            histograma[caminho[i]]-=1
            caminho[i] = random.randint(0, n_cidades - 1)
            histograma[caminho[i]]+=1

def crossing_over(caminho_pai1, caminho_pai2, n_cidades):
    filho = []
    corte = n_cidades // 3
    for i in range(corte):
        filho.append(caminho_pai1[i])
    for i in range(corte, n_cidades):
        filho.append(caminho_pai2[i])
    return filho

def confere_caminho(caminho, n_cidades):
    #print(caminho)
    histograma = []
    for i in range(n_cidades):
        histograma.append(0)

    for i in range(n_cidades):
        histograma[caminho[i]] += 1
        #print(histograma)
        if (histograma[caminho[i]] > 1):
            #print("falso")
            return False
    #print("verdade")
    return True

def genetico(cidades_input):
    global cidades, melhores_viz
    cidades = cidades_input
    n_cidades = len(cidades)
    melhores_viz = []
    define_melhores_vizinhos(n_cidades)
    populacao = []
    for i in range(TAM_POPULACAO):
        populacao.append(rand_estado_inicial(n_cidades))

    melhor_cam = []
    menor_soma = (MAX_VAL ** MAX_VAL) * n_cidades
    for i in range(TAM_POPULACAO):
        soma = soma_dist_cam(populacao[i], n_cidades)
        if (soma < menor_soma):
            menor_soma = soma
            melhor_cam = populacao[i]

    soma_fit_glob = 0
    qt_cam_geral = 0

    for g in range(N_GERACOES):
        
        fit_pop = []
        melhor_fit = 0
        for i in range(TAM_POPULACAO):
            fit_pop.append(fitness(populacao[i], n_cidades))
            if (fit_pop[i] > fit_pop[melhor_fit]):
                melhor_fit = i

        nova_pop = []
        j = 0
        qt_cam_ger = 0
        for i in range(TAM_POPULACAO):
            jin = j
            casou = False
            while (casou == False):
                if (random.random() < fit_pop[j]):
                    filho = crossing_over(populacao[i], populacao[j], n_cidades)
                    mutacao(filho, n_cidades)
                    nova_pop.append(filho)
                    if (confere_caminho(filho, n_cidades)):
                        soma = soma_dist_cam(filho, n_cidades)
                        qt_cam_ger += 1
                        if (soma < menor_soma):
                            menor_soma = soma
                            melhor_cam = filho
                    casou = True
                j+=1
                if (j >= TAM_POPULACAO):
                    j = 0
                
                if (abs(j - jin) > 100):
                    filho = crossing_over(populacao[i], populacao[melhor_fit], n_cidades)
                    mutacao(filho, n_cidades)
                    nova_pop.append(filho)
                    if (confere_caminho(filho, n_cidades)):
                        soma = soma_dist_cam(filho, n_cidades)
                        qt_cam_ger += 1
                        if (soma < menor_soma):
                            menor_soma = soma
                            melhor_cam = filho
                    casou = True

        populacao = nova_pop

        soma_fit = 0
        #calculando algumas estatisticas
        for i in range(TAM_POPULACAO):
            soma_fit += fit_pop[i]
        #print(f"fit media da geracao {g} e de {soma_fit / TAM_POPULACAO}")
        #print(f"o numero de caminhos gerado na geração {g} e de {qt_cam_ger}")
        soma_fit_glob += soma_fit / TAM_POPULACAO
        qt_cam_geral += qt_cam_ger
        
    print(f"fit media geral: {soma_fit_glob / N_GERACOES}")
    print(f"media de caminhos por geração: {qt_cam_geral / N_GERACOES}")
    print(f"resultado Genetico: {menor_soma}")

    return melhor_cam, menor_soma

def main():

    n_cidades = 10

    ini_cidades_aleatorias(n_cidades)
       
    melhor_cam, melhor_dist = genetico(cidades)

    print(f"Melhor caminho encontrado: {melhor_cam}")
    print(f"Distância: {melhor_dist}")

   #CV

    # coords das cidades (ex: [(x1,y1), (x2,y2), ...])
    coords = []

    for i in range(n_cidades):
        coords.append(cidades[i])

    # cria imagem em branco (500x500 com fundo preto)
    img = np.ones(((MAX_VAL) * 10, (MAX_VAL) * 10, 3), dtype=np.uint8) * 255

    # desenha as cidades (bolinhas azuis)
    for (x, y) in coords:
        cv2.circle(img, (x * 10, y * 10), 6, (0, 0, 255), -1)

    # desenha as linhas do caminho
    for i in range(len(melhor_cam) - 1):
        x1, y1 = coords[melhor_cam[i]]
        x2, y2 = coords[melhor_cam[i + 1]]
        cv2.line(img, (x1* 10, y1* 10), (x2* 10, y2* 10), (255, 0, 0), 2)

    # fecha o ciclo (última cidade -> primeira)
    x1, y1 = coords[melhor_cam[n_cidades - 1]]
    x2, y2 = coords[melhor_cam[0]]
    cv2.line(img, (x1* 10, y1* 10), (x2* 10, y2* 10), (255, 0, 0), 2)

    # mostra a imagem
    cv2.imshow("Caminho", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    