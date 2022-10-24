#include <iostream>
#include <cstdlib>
#include <mpi.h>
#include <ctime>
#include <cstring>
#include <vector>
#include <cfloat>
#include <cmath>

// Variaveis para calculo do tempo de execução
struct timespec start, finish;
double elapsed;
#define STARTTIME() clock_gettime(CLOCK_MONOTONIC, &start)
#define ENDTIME() clock_gettime(CLOCK_MONOTONIC, &finish)

// armazena a linha do arquivo
typedef struct classe {
    std::vector<double> v;
    char genero[20];
} classe;

// armazena as matrizes
std::vector<classe> m_treino, m_teste;

// armazena as predições
typedef struct pred {
    char *genero;
    double dist;
} pred;
pred predicao;
std::vector<pred> predicoes;

// argumentos MPI
int argumentos[3], world_rank, world_size, name_len;
char processor_name[MPI_MAX_PROCESSOR_NAME];

double distancia_euclidiana(std::vector<double> dest, classe src, int n) {
    double dist = 0.0;
    for (int i = 0; i < n; i++)
        dist += pow(dest.at(i) - src.v.at(i), 2);
    dist = sqrt(dist);
    return dist;
}

int main(int argc, char const **argv) {
    FILE *treino, *teste;
    char n_treino[2000], n_teste[2000];
    const char *tam = argv[2];
    int atributos = atoi(argv[1]);
    double atr;
    classe atr_classes;

    // abrindo arquivo de treino
    std::strcpy(n_treino, "bases_mpi/train_");
    std::strcat(n_treino, tam);
    std::strcat(n_treino, ".data");
    if((treino = fopen(n_treino, "r")) == NULL) {
        std::cout << "Erro ao abrir o arquivo de treino!" << '\n';
        exit(1);
    }

    // abrindo arquivo de teste
    std::strcpy(n_teste, "bases_mpi/test_");
    std::strcat(n_teste, tam);
    std::strcat(n_teste, ".data");
    if((teste = fopen(n_teste, "r")) == NULL) {
        std::cout << "Erro ao abrir o arquivo de teste!" << '\n';
        exit(1);
    }

    // treinar
    while (fgetc(treino) != EOF) {
        atr_classes.v.clear();
        for (int i = 0; i < atributos; i++) {
            fscanf(treino, "%lf,", &atr);
            atr_classes.v.push_back(atr);
        }
        fscanf(treino, "%s\n", atr_classes.genero);
        m_treino.push_back(atr_classes);
    }

    fclose(treino);

    // classificar
    while (fgetc(teste) != EOF) {
        atr_classes.v.clear();
        for (int i = 0; i < atributos; i++) {
            fscanf(teste, "%lf,", &atr);
            atr_classes.v.push_back(atr);
        }
        fscanf(teste, "%s\n", atr_classes.genero);
        m_teste.push_back(atr_classes);
    }

    fclose(teste);

    // INICIALIZANDO MPI
    MPI_Init(NULL, NULL);

    // NUMERO DE PROCESSOS
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    // RANK DOS PROCESSOS
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // NOME DO PROCESSADOR
    MPI_Get_processor_name(processor_name, &name_len);
    MPI_Status status;

    STARTTIME(); // INICIANDO CONTAGEM DE TEMPO
    int salto = floor(m_treino.size()/world_size);
    for(int i = 0; i < m_teste.size(); i++) {
        if(world_rank == 0) {
            argumentos[2] = atributos;

            argumentos[0] = 0;
            argumentos[1] = argumentos[0] + salto;

            for(int j = 1; j < world_size; j++) {
                MPI_Send(argumentos, 3, MPI_INT, j, 0, MPI_COMM_WORLD);
                MPI_Send(&m_teste.at(i).v.front(), atributos, MPI_DOUBLE, j, 0, MPI_COMM_WORLD);
                MPI_Send(m_teste.at(i).genero, 20, MPI_BYTE, j, 0, MPI_COMM_WORLD);
                argumentos[0] = argumentos[1];
                argumentos[1] = argumentos[0] + salto;
            }
            argumentos[1] = atributos;
        } // END IF WORLD_RANK = 0
        else {
            MPI_Recv(argumentos, 3, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
            MPI_Recv(&m_teste.at(i).v.front(), atributos, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD, &status);
            MPI_Recv(m_teste.at(i).genero, 20, MPI_BYTE, 0, 0, MPI_COMM_WORLD, &status);
        }

        // K-NN
        int k;
        char classe_processo[20];
        double distancia, menor_distancia_processo = DBL_MAX;
        for(k = argumentos[0]; k < argumentos[1]; k++) {
            distancia = distancia_euclidiana(m_teste.at(i).v, m_treino.at(k), argumentos[2]);
            if (distancia < menor_distancia_processo) {
                menor_distancia_processo = distancia;
                std::strcpy(classe_processo, m_teste.at(i).genero);
            }
        }
        // FIM DO K-NN

        if(world_rank == 0) {
            double menor_distancia;
            char classe[20];
            menor_distancia = menor_distancia_processo;
            std::strcpy(classe, classe_processo);
            for(int j = 1; j < world_size; j++) {
                MPI_Recv(&menor_distancia_processo, 1, MPI_DOUBLE, j, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                MPI_Recv(classe_processo, 20, MPI_BYTE, j, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                if(menor_distancia_processo < menor_distancia) {
                    menor_distancia = menor_distancia_processo;
                    std::strcpy(classe, classe_processo);
                }
            }
            predicao.genero = classe;
            predicao.dist = menor_distancia;
            predicoes.push_back(predicao);
        }
        else {
            MPI_Send(&menor_distancia_processo, 1, MPI_DOUBLE, 0, 1, MPI_COMM_WORLD);
            MPI_Send(classe_processo, 20, MPI_BYTE, 0, 1, MPI_COMM_WORLD);
        }
    }

    MPI_Finalize();
    ENDTIME(); // FINALIZANDO CONTAGEM DE TEMPO

    // CALCULANDO TEMPO DE EXECUCAO
    printf("PROCESSOR NAME: %s\n", processor_name);
    elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
    std::cout << elapsed << '\n';

    return 0;
}