library(ggplot2)
setwd("C:/Users/Archer/CLionProjects/PC/Processar a saida")
### Lendo os dados das execuções
dados <- read.csv("geral.csv", header = T, sep = ",", dec=".")
### Dividindo os dados da linhas para obter a média das execuções sequênciais
for(i in 1:length(dados$algoritmo)) {
    if(dados$algoritmo[i] == 'knn_mpi_euclidiano') {
        dados[i,-1:-3] <- dados[i,-1:-3]/(15 * dados$threads.processos[i])   
    } else if (dados$algoritmo[i] == 'knn_mpi_manhattan') {
        dados[i,-1:-3] <- dados[i,-1:-3]/(15 * dados$threads.processos[i])
    } else {
        dados[i,-1:-3] <- dados[i,-1:-3]/15
    }
}
ggplot(dados,aes(threads.processos,tempo,fill=algoritmo)) + geom_bar(position = "dodge", stat = "identity")
ggplot(dados,aes(n.atributos,tempo,fill=algoritmo)) + geom_bar(position = "dodge", stat = "identity")