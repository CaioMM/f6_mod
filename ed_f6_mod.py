import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random, math, copy, statistics
from IPython.display import clear_output
random.seed(1)

def F6(x,y):
    return 0.5 - (((math.sin( (x**2+y**2)**0.5 ))**2 - 0.5)/(1 + ( 0.001 * ( x**2 + y**2 ) ))**2)

def calcFitness(individuo):
    return (F6(individuo[0],individuo[1]) + F6(individuo[2],individuo[3]) + F6(individuo[4],individuo[5]) + F6(individuo[6],individuo[7]) + F6(individuo[8],individuo[9]))

def popInit(tPop=100, D=10):
    pop = []
    for n in range(tPop):
        individuo = [0]*D
        for i in range(len(individuo)):
            individuo[i] = (-100 + (random.uniform(0,1)*(100-(-100))))
#         print(individuo)
        pop.append([calcFitness(individuo), individuo])
    return pop

def mutacao(pop, f):
    vetor_M = random.sample(pop, k=3)        
    
    vetor_D = [0]*len(pop[0][1])
    
    for i in range(len(vetor_D)):
        
        if (vetor_M[0][1][i] + (f*(vetor_M[1][1][i] - vetor_M[2][1][i])) > 100):
            vetor_D[i] = 100
        elif (vetor_M[0][1][i] + (f*(vetor_M[1][1][i] - vetor_M[2][1][i])) < -100):
            vetor_D[i] = -100
        else:
            vetor_D[i] = vetor_M[0][1][i] + (f*(vetor_M[1][1][i] - vetor_M[2][1][i]))
            
    return vetor_D


def crossover(pop, cr, f):
    novo_individuo = [0]*len(pop[0][1])
    
    antigo_individuo = random.choice(pop)[1]
    vetor_D = mutacao(pop,f)
    
    for i in range(len(novo_individuo)):
        if random.uniform(0,1) <= cr:
            novo_individuo[i] = vetor_D[i]
        else:
            novo_individuo[i] = antigo_individuo[i]
    j = random.randint(0,len(novo_individuo)-1)
    novo_individuo[j] = vetor_D[j]
    
    if calcFitness(novo_individuo) >= calcFitness(antigo_individuo):
        return [calcFitness(novo_individuo), novo_individuo]
    else:
        return [calcFitness(antigo_individuo), antigo_individuo]

def calculaMediaExecucoes(melhoresIndExec, popFitExec):
    mediaMeIndExec = [0]*500
    mediaPopFitExec = [0]*500
    for i in range(len(melhoresIndExec[0])):
        holder = []
        for execucao in melhoresIndExec:
            holder.append(execucao[i])
        mediaMeIndExec[i] = statistics.mean(holder)
        
        holder = []
        for execucao in popFitExec:
            holder.append(execucao[i])
        mediaPopFitExec[i] = statistics.mean(holder)
        
    return mediaMeIndExec, mediaPopFitExec

def calculaMediaPopulacoes(popsMeExec, popsFitPopExec):
    mediaPopsMeInd = [0]*500
    mediaPopsFitPop = [0]*500
    for i in range(len(popsMeExec[0])):
        holder = []
        for execucao in popsMeExec:
            holder.append(execucao[i])
        mediaPopsMeInd[i] = statistics.mean(holder)
        
        holder = []
        for execucao in popsFitPopExec:
            holder.append(execucao[i])
        mediaPopsFitPop[i] = statistics.mean(holder)
        
    return mediaPopsMeInd, mediaPopsFitPop

D = 10
tamanhoPopulacao = 100
epocas = 500
cr = 0.8
f = 0.8

nPopInicial = 5
nExecucoes = 30

tiposCruzamento = 1

elitismo = 1

popsMeExec = [ [0]*epocas ]*nPopInicial
popsFitPopExec = [ [0]*epocas ]*nPopInicial

for populacaoInicial in range(nPopInicial):
    populacao = popInit(tamanhoPopulacao, D)

    melhoresIndExec = [0]*nExecucoes
    popFitExec = [0]*nExecucoes
    for ex in range(nExecucoes):
#         print('a')
        pop = copy.copy(populacao)
        pop.sort()

        melhoresEpoca = [0] * epocas
        mediaPopFit = [0] * epocas
#         print('b')
        for e in range(epocas):

            fPop = [0]*tamanhoPopulacao
            # Armazena a fitness de todos os indivíduos
            for individuo in range(tamanhoPopulacao):
                fPop[individuo] = pop[individuo][0]

            melhoresEpoca[e] = max(fPop)
            mediaPopFit[e] = statistics.mean(fPop)
            
            # crossover
            novaGeracao = [0]*tamanhoPopulacao
            for j in range(tamanhoPopulacao):
                novaGeracao[j] = crossover(pop,cr,f)

            if elitismo == 1:
                for i in range(tamanhoPopulacao-1):
                    pop[i] = novaGeracao[i]
                pop.sort()
            else:
                pop = novaGeracao
                pop.sort()
        #end for e in range(epocas)
        print(f'Execução: {ex+1}')
        print(f'População: {populacaoInicial+1}')
        clear_output(wait=True)
        
        melhoresIndExec[ex] = melhoresEpoca
        popFitExec[ex] = mediaPopFit
    #end for ex in range(execucoes)
    popsMeExec[populacaoInicial], popsFitPopExec[populacaoInicial] = calculaMediaExecucoes(melhoresIndExec, popFitExec)

[bestInd,fitnessPopulation] = calculaMediaPopulacoes(popsMeExec, popsFitPopExec)

# plt.figure()
# plt.title('Roleta | Dois Pontos de Corte')

# plt.plot(popsMeExec, 'bo', markersize=2, label='Melhores Indivíduos')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

# plt.plot(popsFitPopExec, 'ro', markersize=2, label='Media População')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
# plt.show()

y = {'Época': [i for i in range(500)], 'Melhores Indivíduos': bestInd, 'Média Fitness da População': fitnessPopulation}

df = pd.DataFrame(data=y, columns=['Época','Melhores Indivíduos', 'Média Fitness da População'])

grafico1 = px.scatter(df, x='Época', y=['Melhores Indivíduos','Média Fitness da População'],
                      range_x=[-50,550],range_y=[2,5], title='F6',)
# grafico2 = px.scatter(x = [i+1 for i in range(epocas)], y = fitnessPopulation, range_y=[0,5])
# grafico3 = go.Figure(data = grafico1.data + grafico2.data)
grafico1.update_layout(title={
                        'text': "ED F6 Modificada",
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                        xaxis_title="Época",
                        yaxis_title="Fitness",
                        legend_title="Legenda",
                        font=dict(
                            family="Courier New, monospace",
                            size=18,
                        ))
grafico1.show()