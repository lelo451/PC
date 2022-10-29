#! /bin/bash

g++ knn_pthread.cpp -o pthread -lpthread
mpiCC knn_mpi_euclidiana.cpp -o mpi_euclidiana
mpiCC knn_mpi_manhattan.cpp -o mpi_manhattan

pthread_size=(59 154 256)
mpi_size=(59 161 256)
thread=(2 3 4 5 6 7 8 9 10 11 12)

for i in "${pthread_size[@]}"
do
  printf "Tamanho da matriz $i\n"
  for ((j = 0; j < 2; j++)); do
    for ((k = 0; k < 15; k++)); do
      ./pthread $j $i 1
    done
    printf "\n\n"
  done
  printf "\n\n"
  for j in "${thread[@]}"
    do
      printf "$j thread(s)\n"
      for ((k = 0; k < 15; k++)); do
        ./pthread 2 $i $j
      done
      printf "\n\n"
    done
  printf "-------------------------- \n\n"
done


for i in "${mpi_size[@]}"
do
  for j in "${thread[@]}"
  do
    printf "Tamanho da matriz $i - $j thread(s)\n"
    for ((k = 0; k < 15; k++)); do
      mpirun -np $j ./mpi_euclidiana $i
    done
    printf "-------------------------- \n\n"
  done
done

for i in "${mpi_size[@]}"
do
  for j in "${thread[@]}"
  do
    printf "Tamanho da matriz $i - $j processos(s)\n"
    for ((k = 0; k < 15; k++)); do
      mpirun -np $j ./mpi_manhattan $i
    done
    printf "-------------------------- \n\n"
  done
done