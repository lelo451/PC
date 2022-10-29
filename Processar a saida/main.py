import numpy as np
import csv

header = ['algoritmo', 'n atributos', 'threads/processos', 'tempo']

#   59      154     161     256
#   [0,0]   [0,1]   [0,2]   [0,3]   euclidiano
#   [1,0]   [1,1]   [1,2]   [1,3]   manhattan
sequencial = np.zeros((2, 4), dtype=float)

#   59      154     256
#   [00,0]  [00,1]  [00,2]  2
#   [01,0]  [01,1]  [01,2]  3
#   [02,0]  [02,1]  [02,2]  4
#   [03,0]  [03,1]  [03,2]  5
#   [04,0]  [04,1]  [04,2]  6
#   [05,0]  [05,1]  [05,2]  7
#   [06,0]  [06,1]  [06,2]  8
#   [07,0]  [07,1]  [07,2]  9
#   [08,0]  [08,1]  [08,2]  10
#   [09,0]  [09,1]  [09,2]  11
#   [10,0]  [10,1]  [10,2]  12
pthread_euclidiano = np.zeros((11, 3), dtype=float)
pthread_manhattan = np.zeros((11, 3), dtype=float)

#   59      161     256
#   [00,0]  [00,1]  [00,2]  2
#   [01,0]  [01,1]  [01,2]  3
#   [02,0]  [02,1]  [02,2]  4
#   [03,0]  [03,1]  [03,2]  5
#   [04,0]  [04,1]  [04,2]  6
#   [05,0]  [05,1]  [05,2]  7
#   [06,0]  [06,1]  [06,2]  8
#   [07,0]  [07,1]  [07,2]  9
#   [08,0]  [08,1]  [08,2]  10
#   [09,0]  [09,1]  [09,2]  11
#   [10,0]  [10,1]  [10,2]  12
mpi_euclidiano = np.zeros((11, 3), dtype=float)
mpi_manhattan = np.zeros((11, 3), dtype=float)

geral = np.zeros((140, 4), dtype='S40')


def get_numero_atributos(seq: int):
    match seq:
        case 0:
            return "59"
        case 1:
            return "154"
        case 2:
            return "161"
        case 3:
            return "256"


def get_numero_atributos_pthread(seq: int):
    match seq:
        case 0:
            return "59"
        case 1:
            return "154"
        case 2:
            return "256"


def get_numero_atributos_mpi(seq: int):
    match seq:
        case 0:
            return "59"
        case 1:
            return "161"
        case 2:
            return "256"


def convert(numero):
    return numero.replace(',', '.')


def soma_na_matrix(i: int, linha: str, atr59, atr154, atr256: bool):
    j = -1
    if atr59:
        j = 0
    elif atr154:
        j = 1
    elif atr256:
        j = 2
    match linha.strip().split(': ')[0]:
        case 'Thread euclidiana':
            pthread_euclidiano[i, j] += float(convert(linha.strip().split(': ')[1]))
        case 'thread manhattan':
            pthread_manhattan[i, j] += float(convert(linha.strip().split(': ')[1]))


def soma_mpi(i: int, linha: str, atr59, atr161, atr256, euclidiana, manhattan: bool):
    j = -1
    if atr59:
        j = 0
    elif atr161:
        j = 1
    elif atr256:
        j = 2
    if euclidiana:
        mpi_euclidiano[i, j] += float(convert(linha.strip()))
    elif manhattan:
        mpi_manhattan[i, j] += float(convert(linha.strip()))


def proccess_file():
    pthread = mpi = False
    t2 = t3 = t4 = t5 = t6 = t7 = t8 = t9 = t10 = t11 = t12 = False
    p2 = p3 = p4 = p5 = p6 = p7 = p8 = p9 = p10 = p11 = p12 = False
    with open('saida.txt', 'r') as f:
        for line in f.readlines():
            match line.strip():
                case '':
                    continue
                case 'matriz: 59':
                    m59 = True
                    m154 = False
                    m161 = False
                    m256 = False
                    continue
                case 'matriz: 154':
                    m59 = False
                    m154 = True
                    m161 = False
                    m256 = False
                    continue
                case 'matriz: 161':
                    m59 = False
                    m154 = False
                    m161 = True
                    m256 = False
                    continue
                case 'matriz: 256':
                    m59 = False
                    m154 = False
                    m161 = False
                    m256 = True
                    continue
                case 'MPI EUCLIDIANA':
                    euclidiana = True
                    manhattan = False
                    continue
                case 'MPI MANHATTAN':
                    euclidiana = False
                    manhattan = True
                    continue
                case 'thread: 2':
                    t2 = True
                    t3 = False
                    t4 = False
                    t5 = False
                    t6 = False
                    t7 = False
                    t8 = False
                    t9 = False
                    t10 = False
                    t11 = False
                    t12 = False
                    pthread = True
                    mpi = False
                    continue
                case 'thread: 3':
                    t2 = False
                    t3 = True
                    t4 = False
                    t5 = False
                    t6 = False
                    t7 = False
                    t8 = False
                    t9 = False
                    t10 = False
                    t11 = False
                    t12 = False
                    pthread = True
                    mpi = False
                    continue
                case 'thread: 4':
                    t2 = False
                    t3 = False
                    t4 = True
                    t5 = False
                    t6 = False
                    t7 = False
                    t8 = False
                    t9 = False
                    t10 = False
                    t11 = False
                    t12 = False
                    pthread = True
                    mpi = False
                    continue
                case 'thread: 5':
                    t2 = False
                    t3 = False
                    t4 = False
                    t5 = True
                    t6 = False
                    t7 = False
                    t8 = False
                    t9 = False
                    t10 = False
                    t11 = False
                    t12 = False
                    pthread = True
                    mpi = False
                    continue
                case 'thread: 6':
                    t2 = False
                    t3 = False
                    t4 = False
                    t5 = False
                    t6 = True
                    t7 = False
                    t8 = False
                    t9 = False
                    t10 = False
                    t11 = False
                    t12 = False
                    pthread = True
                    mpi = False
                    continue
                case 'thread: 7':
                    t2 = False
                    t3 = False
                    t4 = False
                    t5 = False
                    t6 = False
                    t7 = True
                    t8 = False
                    t9 = False
                    t10 = False
                    t11 = False
                    t12 = False
                    pthread = True
                    mpi = False
                    continue
                case 'thread: 8':
                    t2 = False
                    t3 = False
                    t4 = False
                    t5 = False
                    t6 = False
                    t7 = False
                    t8 = True
                    t9 = False
                    t10 = False
                    t11 = False
                    t12 = False
                    pthread = True
                    mpi = False
                    continue
                case 'thread: 9':
                    t2 = False
                    t3 = False
                    t4 = False
                    t5 = False
                    t6 = False
                    t7 = False
                    t8 = False
                    t9 = True
                    t10 = False
                    t11 = False
                    t12 = False
                    pthread = True
                    mpi = False
                    continue
                case 'thread: 10':
                    t2 = False
                    t3 = False
                    t4 = False
                    t5 = False
                    t6 = False
                    t7 = False
                    t8 = False
                    t9 = False
                    t10 = True
                    t11 = False
                    t12 = False
                    pthread = True
                    mpi = False
                    continue
                case 'thread: 11':
                    t2 = False
                    t3 = False
                    t4 = False
                    t5 = False
                    t6 = False
                    t7 = False
                    t8 = False
                    t9 = False
                    t10 = False
                    t11 = True
                    t12 = False
                    pthread = True
                    mpi = False
                    continue
                case 'thread: 12':
                    t2 = False
                    t3 = False
                    t4 = False
                    t5 = False
                    t6 = False
                    t7 = False
                    t8 = False
                    t9 = False
                    t10 = False
                    t11 = False
                    t12 = True
                    pthread = True
                    mpi = False
                    continue
                case 'processo: 2':
                    p2 = True
                    p3 = False
                    p4 = False
                    p5 = False
                    p6 = False
                    p7 = False
                    p8 = False
                    p9 = False
                    p10 = False
                    p11 = False
                    p12 = False
                    pthread = False
                    mpi = True
                    continue
                case 'processo: 3':
                    p2 = False
                    p3 = True
                    p4 = False
                    p5 = False
                    p6 = False
                    p7 = False
                    p8 = False
                    p9 = False
                    p10 = False
                    p11 = False
                    p12 = False
                    pthread = False
                    mpi = True
                    continue
                case 'processo: 4':
                    p2 = False
                    p3 = False
                    p4 = True
                    p5 = False
                    p6 = False
                    p7 = False
                    p8 = False
                    p9 = False
                    p10 = False
                    p11 = False
                    p12 = False
                    pthread = False
                    mpi = True
                    continue
                case 'processo: 5':
                    p2 = False
                    p3 = False
                    p4 = False
                    p5 = True
                    p6 = False
                    p7 = False
                    p8 = False
                    p9 = False
                    p10 = False
                    p11 = False
                    p12 = False
                    pthread = False
                    mpi = True
                    continue
                case 'processo: 6':
                    p2 = False
                    p3 = False
                    p4 = False
                    p5 = False
                    p6 = True
                    p7 = False
                    p8 = False
                    p9 = False
                    p10 = False
                    p11 = False
                    p12 = False
                    pthread = False
                    mpi = True
                    continue
                case 'processo: 7':
                    p2 = False
                    p3 = False
                    p4 = False
                    p5 = False
                    p6 = False
                    p7 = True
                    p8 = False
                    p9 = False
                    p10 = False
                    p11 = False
                    p12 = False
                    pthread = False
                    mpi = True
                    continue
                case 'processo: 8':
                    p2 = False
                    p3 = False
                    p4 = False
                    p5 = False
                    p6 = False
                    p7 = False
                    p8 = True
                    p9 = False
                    p10 = False
                    p11 = False
                    p12 = False
                    pthread = False
                    mpi = True
                    continue
                case 'processo: 9':
                    p2 = False
                    p3 = False
                    p4 = False
                    p5 = False
                    p6 = False
                    p7 = False
                    p8 = False
                    p9 = True
                    p10 = False
                    p11 = False
                    p12 = False
                    pthread = False
                    mpi = True
                    continue
                case 'processo: 10':
                    p2 = False
                    p3 = False
                    p4 = False
                    p5 = False
                    p6 = False
                    p7 = False
                    p8 = False
                    p9 = False
                    p10 = True
                    p11 = False
                    p12 = False
                    pthread = False
                    mpi = True
                    continue
                case 'processo: 11':
                    p2 = False
                    p3 = False
                    p4 = False
                    p5 = False
                    p6 = False
                    p7 = False
                    p8 = False
                    p9 = False
                    p10 = False
                    p11 = True
                    p12 = False
                    pthread = False
                    mpi = True
                    continue
                case 'processo: 12':
                    p2 = False
                    p3 = False
                    p4 = False
                    p5 = False
                    p6 = False
                    p7 = False
                    p8 = False
                    p9 = False
                    p10 = False
                    p11 = False
                    p12 = True
                    pthread = False
                    mpi = True
                    continue
            match line.strip().split(': ')[0]:
                case 'sequencial euclidiana':
                    if m59:
                        sequencial[0, 0] += float(convert(line.strip().split(': ')[1]))
                    elif m154:
                        sequencial[0, 1] += float(convert(line.strip().split(': ')[1]))
                    elif m161:
                        sequencial[0, 2] += float(convert(line.strip().split(': ')[1]))
                    elif m256:
                        sequencial[0, 3] += float(convert(line.strip().split(': ')[1]))
                case 'sequencial manhattan':
                    if m59:
                        sequencial[1, 0] += float(convert(line.strip().split(': ')[1]))
                    elif m154:
                        sequencial[1, 1] += float(convert(line.strip().split(': ')[1]))
                    elif m161:
                        sequencial[1, 2] += float(convert(line.strip().split(': ')[1]))
                    elif m256:
                        sequencial[1, 3] += float(convert(line.strip().split(': ')[1]))
            if m59:
                if pthread:
                    if t2:
                        soma_na_matrix(0, line, m59, m154, m256)
                    elif t3:
                        soma_na_matrix(1, line, m59, m154, m256)
                    elif t4:
                        soma_na_matrix(2, line, m59, m154, m256)
                    elif t5:
                        soma_na_matrix(3, line, m59, m154, m256)
                    elif t6:
                        soma_na_matrix(4, line, m59, m154, m256)
                    elif t7:
                        soma_na_matrix(5, line, m59, m154, m256)
                    elif t8:
                        soma_na_matrix(6, line, m59, m154, m256)
                    elif t9:
                        soma_na_matrix(7, line, m59, m154, m256)
                    elif t10:
                        soma_na_matrix(8, line, m59, m154, m256)
                    elif t11:
                        soma_na_matrix(9, line, m59, m154, m256)
                    elif t12:
                        soma_na_matrix(10, line, m59, m154, m256)
                elif mpi:
                    if p2:
                        soma_mpi(0, line, m59, m161, m256, euclidiana, manhattan)
                    elif p3:
                        soma_mpi(1, line, m59, m161, m256, euclidiana, manhattan)
                    elif p4:
                        soma_mpi(2, line, m59, m161, m256, euclidiana, manhattan)
                    elif p5:
                        soma_mpi(3, line, m59, m161, m256, euclidiana, manhattan)
                    elif p6:
                        soma_mpi(4, line, m59, m161, m256, euclidiana, manhattan)
                    elif p7:
                        soma_mpi(5, line, m59, m161, m256, euclidiana, manhattan)
                    elif p8:
                        soma_mpi(6, line, m59, m161, m256, euclidiana, manhattan)
                    elif p9:
                        soma_mpi(7, line, m59, m161, m256, euclidiana, manhattan)
                    elif p10:
                        soma_mpi(8, line, m59, m161, m256, euclidiana, manhattan)
                    elif p11:
                        soma_mpi(9, line, m59, m161, m256, euclidiana, manhattan)
                    elif p12:
                        soma_mpi(10, line, m59, m161, m256, euclidiana, manhattan)
            elif m154:
                if t2:
                    soma_na_matrix(0, line, m59, m154, m256)
                elif t3:
                    soma_na_matrix(1, line, m59, m154, m256)
                elif t4:
                    soma_na_matrix(2, line, m59, m154, m256)
                elif t5:
                    soma_na_matrix(3, line, m59, m154, m256)
                elif t6:
                    soma_na_matrix(4, line, m59, m154, m256)
                elif t7:
                    soma_na_matrix(5, line, m59, m154, m256)
                elif t8:
                    soma_na_matrix(6, line, m59, m154, m256)
                elif t9:
                    soma_na_matrix(7, line, m59, m154, m256)
                elif t10:
                    soma_na_matrix(8, line, m59, m154, m256)
                elif t11:
                    soma_na_matrix(9, line, m59, m154, m256)
                elif t12:
                    soma_na_matrix(10, line, m59, m154, m256)
            elif m161:
                if p2:
                    soma_mpi(0, line, m59, m161, m256, euclidiana, manhattan)
                elif p3:
                    soma_mpi(1, line, m59, m161, m256, euclidiana, manhattan)
                elif p4:
                    soma_mpi(2, line, m59, m161, m256, euclidiana, manhattan)
                elif p5:
                    soma_mpi(3, line, m59, m161, m256, euclidiana, manhattan)
                elif p6:
                    soma_mpi(4, line, m59, m161, m256, euclidiana, manhattan)
                elif p7:
                    soma_mpi(5, line, m59, m161, m256, euclidiana, manhattan)
                elif p8:
                    soma_mpi(6, line, m59, m161, m256, euclidiana, manhattan)
                elif p9:
                    soma_mpi(7, line, m59, m161, m256, euclidiana, manhattan)
                elif p10:
                    soma_mpi(8, line, m59, m161, m256, euclidiana, manhattan)
                elif p11:
                    soma_mpi(9, line, m59, m161, m256, euclidiana, manhattan)
                elif p12:
                    soma_mpi(10, line, m59, m161, m256, euclidiana, manhattan)
            elif m256:
                if pthread:
                    if t2:
                        soma_na_matrix(0, line, m59, m154, m256)
                    elif t3:
                        soma_na_matrix(1, line, m59, m154, m256)
                    elif t4:
                        soma_na_matrix(2, line, m59, m154, m256)
                    elif t5:
                        soma_na_matrix(3, line, m59, m154, m256)
                    elif t6:
                        soma_na_matrix(4, line, m59, m154, m256)
                    elif t7:
                        soma_na_matrix(5, line, m59, m154, m256)
                    elif t8:
                        soma_na_matrix(6, line, m59, m154, m256)
                    elif t9:
                        soma_na_matrix(7, line, m59, m154, m256)
                    elif t10:
                        soma_na_matrix(8, line, m59, m154, m256)
                    elif t11:
                        soma_na_matrix(9, line, m59, m154, m256)
                    elif t12:
                        soma_na_matrix(10, line, m59, m154, m256)
                elif mpi:
                    if p2:
                        soma_mpi(0, line, m59, m161, m256, euclidiana, manhattan)
                    elif p3:
                        soma_mpi(1, line, m59, m161, m256, euclidiana, manhattan)
                    elif p4:
                        soma_mpi(2, line, m59, m161, m256, euclidiana, manhattan)
                    elif p5:
                        soma_mpi(3, line, m59, m161, m256, euclidiana, manhattan)
                    elif p6:
                        soma_mpi(4, line, m59, m161, m256, euclidiana, manhattan)
                    elif p7:
                        soma_mpi(5, line, m59, m161, m256, euclidiana, manhattan)
                    elif p8:
                        soma_mpi(6, line, m59, m161, m256, euclidiana, manhattan)
                    elif p9:
                        soma_mpi(7, line, m59, m161, m256, euclidiana, manhattan)
                    elif p10:
                        soma_mpi(8, line, m59, m161, m256, euclidiana, manhattan)
                    elif p11:
                        soma_mpi(9, line, m59, m161, m256, euclidiana, manhattan)
                    elif p12:
                        soma_mpi(10, line, m59, m161, m256, euclidiana, manhattan)


if __name__ == '__main__':
    proccess_file()
    row = 0
    atributos = 0
    for i in sequencial.transpose():
        count = 0
        for j in i:
            if count == 0:
                geral[row, 0] = "knn_euclidiano"
                geral[row, 1] = get_numero_atributos(atributos)
                geral[row, 2] = "1"
                geral[row, 3] = str(j)
            else:
                geral[row, 0] = "knn_manhattan"
                geral[row, 1] = get_numero_atributos(atributos)
                geral[row, 2] = "1"
                geral[row, 3] = str(j)
            count += 1
            row += 1
        atributos += 1

    thread = 2
    for i in pthread_euclidiano:
        count = 0
        atributos = 0
        for j in i:
            if count == 0:
                geral[row, 0] = "knn_pthread_euclidiano"
                geral[row, 1] = get_numero_atributos_pthread(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            elif count == 1:
                geral[row, 0] = "knn_pthread_euclidiano"
                geral[row, 1] = get_numero_atributos_pthread(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            else:
                geral[row, 0] = "knn_pthread_euclidiano"
                geral[row, 1] = get_numero_atributos_pthread(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            count += 1
            row += 1
            atributos += 1
        thread += 1

    thread = 2
    for i in pthread_manhattan:
        count = 0
        atributos = 0
        for j in i:
            if count == 0:
                geral[row, 0] = "knn_pthread_manhattan"
                geral[row, 1] = get_numero_atributos_pthread(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            elif count == 1:
                geral[row, 0] = "knn_pthread_manhattan"
                geral[row, 1] = get_numero_atributos_pthread(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            else:
                geral[row, 0] = "knn_pthread_manhattan"
                geral[row, 1] = get_numero_atributos_pthread(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            count += 1
            row += 1
            atributos += 1
        thread += 1

    thread = 2
    for i in mpi_euclidiano:
        count = 0
        atributos = 0
        for j in i:
            if count == 0:
                geral[row, 0] = "knn_mpi_euclidiano"
                geral[row, 1] = get_numero_atributos_mpi(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            elif count == 1:
                geral[row, 0] = "knn_mpi_euclidiano"
                geral[row, 1] = get_numero_atributos_mpi(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            else:
                geral[row, 0] = "knn_mpi_euclidiano"
                geral[row, 1] = get_numero_atributos_mpi(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            count += 1
            row += 1
            atributos += 1
        thread += 1

    thread = 2
    for i in mpi_manhattan:
        count = 0
        atributos = 0
        for j in i:
            if count == 0:
                geral[row, 0] = "knn_mpi_manhattan"
                geral[row, 1] = get_numero_atributos_mpi(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            elif count == 1:
                geral[row, 0] = "knn_mpi_manhattan"
                geral[row, 1] = get_numero_atributos_mpi(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            else:
                geral[row, 0] = "knn_mpi_manhattan"
                geral[row, 1] = get_numero_atributos_mpi(atributos)
                geral[row, 2] = str(thread)
                geral[row, 3] = str(j)
            count += 1
            row += 1
            atributos += 1
        thread += 1

    with open('geral.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(geral)
