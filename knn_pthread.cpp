#include <iostream>
#include <cstdlib>
#include <pthread.h>
#include <ctime>
#include <vector>
#include <cfloat>
#include <cmath>
#include <cstring>

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

// variaveis de barreira e lock
pthread_barrier_t barrier;
pthread_mutex_t lock;

// argumentos pthread
typedef struct t_args {
    int id_thread, start, finish, tam;
} t_args;

double distancia_euclidiana(classe dest, classe src, int n) {
    double dist = 0.0;
    for (int i = 0; i < n; i++)
        dist += pow(dest.v.at(i) - src.v.at(i), 2);
    dist = sqrt(dist);
    return dist;
}

double distancia_manhattan(classe dest, classe src, int n) {
    double dist = 0.0;
    for (int i = 0; i < n; i++)
        dist += std::abs(dest.v.at(i) - src.v.at(i));
    return dist;
}

void knn(int tam) {
    double dist;
    for (auto & i : m_teste) {
        predicao.dist = DBL_MAX;
        for (auto & j : m_treino) {
            dist = distancia_euclidiana(i, j, tam);
            if (dist < predicao.dist) {
                predicao.dist = dist;
                predicao.genero = j.genero;
            }
        }
        predicoes.push_back(predicao);
    }
}

void knn_manhattan(int tam) {
    double dist;
    for (auto & i : m_teste) {
        predicao.dist = DBL_MAX;
        for (auto & j : m_treino) {
            dist = distancia_manhattan(i, j, tam);
            if (dist < predicao.dist) {
                predicao.dist = dist;
                predicao.genero = j.genero;
            }
        }
        predicoes.push_back(predicao);
    }
}

void *knn_pthread(void *args) {
    int start, finish, id, tam;
    char *classe_thread;
    double dist, min_dist;

    t_args *a;
    a = (t_args *) args;
    id = (int) a->id_thread;
    start = (int) a->start;
    finish = (int) a->finish;
    tam = (int) a->tam;

    for (auto & i : m_teste) {
        min_dist = DBL_MAX;
        predicao.dist = DBL_MAX;
        for (int j = start; j < finish; j++) {
            dist = distancia_euclidiana(i, m_treino.at(j), tam);
            if (dist < min_dist) {
                min_dist = dist;
                classe_thread = m_treino.at(j).genero;
            }
        }
        pthread_mutex_lock(&lock);
        if (min_dist < predicao.dist) {
            predicao.dist = min_dist;
            predicao.genero = classe_thread;
        }
        pthread_mutex_unlock(&lock);
        if (id == 0) {
            predicoes.push_back(predicao);
        }
        pthread_barrier_wait(&barrier);
    }
}

void *knn_pthread_manhattan(void *args) {
    int start, finish, id, tam;
    char *classe_thread;
    double dist, min_dist;

    t_args *a;
    a = (t_args *) args;
    id = (int) a->id_thread;
    start = (int) a->start;
    finish = (int) a->finish;
    tam = (int) a->tam;

    for (auto & i : m_teste) {
        min_dist = DBL_MAX;
        predicao.dist = DBL_MAX;
        for (int j = start; j < finish; j++) {
            dist = distancia_manhattan(i, m_treino.at(j), tam);
            if (dist < min_dist) {
                min_dist = dist;
                classe_thread = m_treino.at(j).genero;
            }
        }
        pthread_mutex_lock(&lock);
        if (min_dist < predicao.dist) {
            predicao.dist = min_dist;
            predicao.genero = classe_thread;
        }
        pthread_mutex_unlock(&lock);
        if (id == 0) {
            predicoes.push_back(predicao);
        }
        pthread_barrier_wait(&barrier);
    }
}

int main(int argc, char const *argv[]) {
    FILE *treino, *teste;
    char n_treino[1000], n_teste[1000];
    const char *tam = argv[2];
    int op = atoi(argv[1]), atributos = atoi(argv[2]), threads = atoi(argv[3]);
    double atr;
    classe atr_classes;

    // abrindo arquivo de treino
    std::strcpy(n_treino, "bases_pthread/train_");
    std::strcat(n_treino, tam);
    std::strcat(n_treino, ".data");
    if((treino = fopen(n_treino, "r")) == NULL) {
        std::cout << "Erro ao abrir o arquivo de treino" << '\n';
        exit(1);
    }

    // abrindo arquivo de teste
    std::strcpy(n_teste, "bases_pthread/test_");
    std::strcat(n_teste, tam);
    std::strcat(n_teste, ".data");
    if((teste = fopen(n_teste, "r")) == NULL) {
        std::cout << "Erro ao abrir o arquivo de teste" << '\n';
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

    // 0: sequencial, 1: paralelo
    switch (op) {
        case 0:
            STARTTIME();
            knn(atributos);
            ENDTIME();

            elapsed = (finish.tv_sec - start.tv_sec);
            elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
            std::cout << "sequencial euclidiana: " << elapsed << '\n';
            break;
        case 1:
            STARTTIME();
            knn_manhattan(atributos);
            ENDTIME();

            elapsed = (finish.tv_sec - start.tv_sec);
            elapsed += (finish.tv_nsec - start.tv_nsec)  / 1000000000.0;
            std::cout << "sequencial manhattan: " << elapsed << '\n';
            break;
        default:
            pthread_t t[threads];
            pthread_barrier_init(&barrier, NULL, threads);
            pthread_mutex_init(&lock, NULL);
            t_args args[threads];
            int salto = floor(m_treino.size()/threads);
            int i, line = 0;
            STARTTIME();
            for (i = 0; i < threads - 1; i++) {
                args[i].id_thread = i;
                args[i].start = line;
                args[i].finish = line + salto;
                args[i].tam = atributos;
                pthread_create(&t[i], NULL, knn_pthread, (void *) &args[i]);
                line = args[i].finish;
            }
            args[i].id_thread = i;
            args[i].start = line;
            args[i].finish = m_treino.size();
            args[i].tam = atributos;
            pthread_create(&t[i], NULL, knn_pthread, (void *) &args[i]);
            for (i = 0; i < threads; i++)
                pthread_join(t[i], NULL);
            ENDTIME();
            pthread_barrier_destroy(&barrier);
            pthread_mutex_destroy(&lock);

            elapsed = (finish.tv_sec - start.tv_sec);
            elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
            std::cout << "Thread euclidiana: " << elapsed << '\n';

            t[threads];
            pthread_barrier_init(&barrier, NULL, threads);
            pthread_mutex_init(&lock, NULL);
            args[threads];
            salto = floor(m_treino.size()/threads);
            i, line = 0;
            STARTTIME();
            for (i = 0; i < threads - 1; i++) {
                args[i].id_thread = i;
                args[i].start = line;
                args[i].finish = line + salto;
                args[i].tam = atributos;
                pthread_create(&t[i], NULL, knn_pthread_manhattan, (void *) &args[i]);
                line = args[i].finish;
            }
            args[i].id_thread = i;
            args[i].start = line;
            args[i].finish = m_treino.size();
            args[i].tam = atributos;
            pthread_create(&t[i], NULL, knn_pthread_manhattan, (void *) &args[i]);
            for (i = 0; i < threads; i++)
                pthread_join(t[i], NULL);
            ENDTIME();
            pthread_barrier_destroy(&barrier);
            pthread_mutex_destroy(&lock);

            elapsed = (finish.tv_sec - start.tv_sec);
            elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
            std::cout << "thread manhattan: " << elapsed << '\n';
    }

    return 0;
}
