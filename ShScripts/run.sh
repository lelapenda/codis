export Base=tr23
export L=70
export W=5833
export Classifier=SVM
export Input=tf
export Metric=euclidiana




printf "Criar pastas\n"
./criar_pastas_folds.sh



printf "\nTreinamento\n"
./treinamento_call.sh

printf "\n\nTeste\n"
./teste_call.sh


printf "\n\nMetricas Desempenho\n"
./metricas_desempenho_call.sh


printf "Deletar pastas\n"
./deleta_pastas_folds.sh