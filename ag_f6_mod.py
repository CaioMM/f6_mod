import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random, math, copy, statistics
from IPython.display import clear_output
random.seed(1)

def popInit(tPop=100):
    pop = []
    for n in range(tPop):
        individuo = [0]*10
        for i in range(len(individuo)):
            individuo[i] = random.choice([i for i in range(-100,101)])
        pop.append([calcFitness(individuo), individuo])
    return pop

def F6(x,y):
    return 0.5 - (((math.sin( (x**2+y**2)**0.5 ))**2 - 0.5)/(1 + ( 0.001 * ( x**2 + y**2 ) ))**2)

def calcFitness(individuo):
    return (F6(individuo[0],individuo[1]) + F6(individuo[2],individuo[3]) + F6(individuo[4],individuo[5]) + F6(individuo[6],individuo[7]) + F6(individuo[8],individuo[9]))

def sortPais(populacao, popFitness):
    
    fitnessTotal = sum(popFitness)
    soma = 0
    selecao = []
    
    for i in range(2):
        posi = 0
        valorAleatorio = random.uniform(0,1)
        
        stop = (fitnessTotal * valorAleatorio)
        
        
        for individuo in populacao:
            soma += individuo[0]
            
            if (soma > stop):
                selecao.append(posi)
            
            posi += 1
    
    return selecao[0], selecao[1]

def crUniforme(populacao, popFitness, txCruzamento, mascara):
    posiPai1,posiPai2 = sortPais(pop, popFitness)
    
    pai1 = populacao[posiPai1][1]
    pai2 = populacao[posiPai2][1]
    
    if txCruzamento > random.uniform(0,1):
        
        filho1 = [0]*len(mascara)
        filho2 = [0]*len(mascara)
        
        for i in range(len(mascara)):
            if mascara[i] == 0:
                filho1[i] = pai1[i]
                filho2[i] = pai2[i]

            elif mascara[i] == 1:
                filho1[i] = pai2[i]
                filho2[i] = pai1[i]
        
        novosIndividuos = [filho1, filho2]
        
        for i in range(2):
            fitness = calcFitness(novosIndividuos[i])
            novosIndividuos[i] = [fitness, novosIndividuos[i]]
        return novosIndividuos[0], novosIndividuos[1]
    
    else:
        pais = [pai1,pai2]
        for i in range(2):
            fitness = calcFitness(pais[i])
            pais[i] = [fitness, pais[i]]
        return pais[0], pais[1]

def criaMascara(pop):
    tamanhoPopulacao = len(pop)
    tamanhoCromossomo = len(pop[0][1])
    mask = [[0]*tamanhoCromossomo for i in range(int((tamanhoPopulacao/2)))]
    for j in range(int(tamanhoPopulacao/2)):
        for i in range(tamanhoCromossomo):
            mask[j][i] = random.randint(0,1)
    
    return mask

# Função para realizar mutação em um indivíduo
def mutacao(ind, txMutacao):
    
    posi = 0
    
    for gene in ind:
        if txMutacao > abs(random.gauss(0,2)):
            ind[posi] = random.choice(np.arange(-100,101))
        posi += 1

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

tamanhoPopulacao = 100
epocas = 500
txCruzamento = 0.8
txMutacao = 0.01

nPopInicial = 5
nExecucoes = 30

tiposCruzamento = 1

elitismo = 1

popsMeExec = [ [0]*epocas ]*nPopInicial
popsFitPopExec = [ [0]*epocas ]*nPopInicial

for populacaoInicial in range(nPopInicial):
    populacao = popInit(tamanhoPopulacao)

    melhoresIndExec = [0]*nExecucoes
    popFitExec = [0]*nExecucoes
    for ex in range(nExecucoes):

        pop = copy.copy(populacao)
        pop.sort()

        melhoresEpoca = [0] * epocas
        mediaPopFit = [0] * epocas
        
        mascaras = criaMascara(pop)

        for e in range(epocas):

            fPop = [0]*tamanhoPopulacao
            # Armazena a fitness de todos os indivíduos
            for individuo in range(tamanhoPopulacao):
                fPop[individuo] = pop[individuo][0]

            melhoresEpoca[e] = max(fPop)
            mediaPopFit[e] = statistics.mean(fPop)

            # crossover

            #Cruzamento Cruzamento Uniforme
            novaGeracao = []
            for i in range(50):
                ind1, ind2 = crUniforme(pop, fPop, txCruzamento, mascaras[i])
                novaGeracao.append(ind1)
                novaGeracao.append(ind2)

            # mutacao
            for individuo in novaGeracao:
                mutacao(individuo[1], txMutacao)

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
        # clear_output(wait=True)
        
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
                        'text': "AG F6 Modificada",
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