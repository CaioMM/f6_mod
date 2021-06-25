from numpy import array
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random, math, copy, statistics
from IPython.display import clear_output
from time import sleep
import matplotlib.pyplot as plt
random.seed(1)

def F6(x,y):
    return 0.5 - (((math.sin( (x**2+y**2)**0.5 ))**2 - 0.5)/(1 + ( 0.001 * ( x**2 + y**2 ) ))**2)

def calcFitness(individuo):
    F6_mod = (F6(individuo[0],individuo[1]) + F6(individuo[2],individuo[3]) + F6(individuo[4],individuo[5]) + F6(individuo[6],individuo[7]) + F6(individuo[8],individuo[9]))
    erro = 5-F6_mod
    return F6_mod


def particlesInit(tPart=100, d=10):
    particulas = []
    for n in range(tPart):
        parametros = np.random.uniform(-100,100,size=d)
        fitness = calcFitness(parametros)
        velocidade = random.uniform(0,1)
        melhor = parametros
        particulas.append([fitness, parametros, velocidade, melhor])
    return particulas

def particlesCopy(particles):
    particulas = []
    for fitness, parametros, velocidade, melhor in particles:
        particulas.append([copy.copy(fitness), copy.copy(parametros), copy.copy(velocidade), copy.copy(melhor)])
    
    return particulas

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


iteracoes = 500
nParticulas = 100
dimensoes = 10
c1 = 2
c2 = 2
err_crit = 0.001
w = 0.6

nPopInicial = 5
nExecucoes = 30

partsMeExec = [ [0 for i in range(iteracoes)] ]*nPopInicial
partsFitPopExec = [ [0 for i in range(iteracoes)] ]*nPopInicial

for populacaoInicial in range(nPopInicial):
    
    particles = particlesInit(nParticulas, dimensoes)
    
    melhoresIndExec = [0]*nExecucoes
    partFitExec = [0]*nExecucoes
    for ex in range(nExecucoes):
        
        particulas = particlesCopy(particles)
        
        melhoresIteracao = [0] * iteracoes
        mediaPartFit = [0] * iteracoes
        
        gbest = random.choice(particulas)
        err = 9999

#         lista_particulas = []
        
        for i in range(iteracoes):
            fPart = []

            for p in particulas:

                fitness = calcFitness(p[1])
                fPart.append(fitness)

                if fitness > p[0]:
                    p[0] = fitness
                    p[3] = p[1]

                if fitness > gbest[0]:
                    gbest = p
                v = w*p[2] + c1*random.uniform(0,1)*(p[3] - p[1]) + c2*random.uniform(0,1)*(gbest[3] - p[1])
                p[1] = p[1] + v
                
            mediaPartFit[i] = statistics.mean(fPart)
            melhoresIteracao[i] = gbest[0]
#             lista_particulas.append(gbest[0])

#             if err < err_crit:
#                 break
#             if i % (iteracoes/10) == 10:
#                 print('.')
                
        print(f'Execução: {ex+1}')
        print(f'População: {populacaoInicial+1}')
        clear_output(wait=True)
        
        melhoresIndExec[ex] = melhoresIteracao
        partFitExec[ex] = mediaPartFit
        
    partsMeExec[populacaoInicial], partsFitPopExec[populacaoInicial] = calculaMediaExecucoes(melhoresIndExec, partFitExec)
        
[bestInd,fitnessPopulation] = calculaMediaPopulacoes(partsMeExec, partsFitPopExec)

y = {'Época': [i for i in range(500)], 'Melhores Indivíduos': melhoresIteracao, 'Média Fitness da População': mediaPartFit}

df = pd.DataFrame(data=y, columns=['Época','Melhores Indivíduos', 'Média Fitness da População'])

y = {'Época': [i for i in range(500)], 'Melhores Indivíduos': melhoresIteracao, 'Média Fitness da População': mediaPartFit}
df = pd.DataFrame(data=y, columns=['Época','Melhores Indivíduos', 'Média Fitness da População'])
grafico1 = px.scatter(df, x='Época', y=['Melhores Indivíduos','Média Fitness da População'],
                      range_x=[-50,550],range_y=[2,5], title='F6',)
# grafico2 = px.scatter(x = [i+1 for i in range(epocas)], y = fitnessPopulation, range_y=[0,5])
# grafico3 = go.Figure(data = grafico1.data + grafico2.data)
grafico1.update_layout(title={
                        'text': "PSO F6 Modificada",
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                        xaxis_title="Iteração",
                        yaxis_title="Fitness",
                        legend_title="Legenda",
                        font=dict(
                            family="Courier New, monospace",
                            size=18,
                        ))
grafico1.show()