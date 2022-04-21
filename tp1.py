import random
import numpy
import xlsxwriter
import os
import pandas as pd
import matplotlib.pyplot as plt

media = []
maximos = []
minimos = []

coef = (2**30) - 1
p_cross = 0.75
p_mut = 0.05
pob = 10
genes = 30
ciclos = 20
elitismo = False
cant_elitismo = 2


def objetivo(cromosoma):
    return ((cromosoma / coef)**2)  #Cromosoma es la x de la funcion.


def binario_random(bits): ##Devuelve un binario de cuantos bits pasados como parámetro.
    binario = ""
    for i in range(bits):
        binario += str(random.randint(0, 1))
    return(binario)


def tirarRuleta():
    ## if (si la prob fitness es menor a 0.01) redondearla para que sea por lo menos 0.01
    limite = random.uniform(0,1) ##Número real de 0 a 1 inclusive.
    acum   = 0
    i      = 0
        ## sumamos los fitness de todos los cromosomas,
    while acum < limite: 
        acum      += cromosomas_fitness[i]
        cromosoma =  cromosomas_binario[i]
        i         =  i+1 
    return cromosoma


def mutar(cromosoma): ##Si hay 1 pone 0 y si hay 1 pone 0
    u = random.randrange(genes) ##Según la documentación de la librería Random, un rango de 30 devolvería un número entre 0 y 29 inclusive.
    if (cromosoma[u] == '1') :
        cromosoma = cromosoma[:u] + '0' + cromosoma[u+1:]
    else: 
        cromosoma = cromosoma[:u] + '1' + cromosoma[u+1:]
    return cromosoma


def cargarNuevaGeneracion():
    cromosoma1 = tirarRuleta()
    cromosoma2 = tirarRuleta()
    ##Se produce crossover?
    if((random.uniform(0,1)) < p_cross):
        ## El primer hijo está formado por los primeros genes del primer padre y los últimos genes gen del segundo padre
        ## El segundo hijo está formado por los primeros genes del segundo padre y los últimos genes gen del primer padre
        rango = random.randrange(genes)
        ##[:rango] devuelve todos los elementos antes del rango de corte mientras que [rango:] devuelve todos los elementos después del rango de corte
        aux1 = cromosoma1[:rango] + cromosoma2[rango:] ##Para que no se pisen los valores al cargar el segundo cromosoma
        aux2 = cromosoma2[:rango] + cromosoma1[rango:]  
        cromosoma1 = aux1
        cromosoma2 = aux2
    ##Se produce mutación?
    if ((random.uniform(0,1)) < p_mut) :
        cromosoma1 = mutar(cromosoma1)
        cromosoma2 = mutar(cromosoma2)
    ##Se agregan a la nueva generación.
    nueva_generacion.append(cromosoma1)
    nueva_generacion.append(cromosoma2)


def cargarTablas(): 
    for i in range(pob):
        cromosomas_decimal.append(int(cromosomas_binario[i], 2))
        cromosomas_objetivo.append(objetivo(cromosomas_decimal[i]))
    for i in range(pob):
        cromosomas_fitness.append(cromosomas_objetivo[i]/sum(cromosomas_objetivo))

def inicializarExcel():
    global worksheet,chart,workbook
    #Eliminamos archivo anterior para evitar errores
    os.popen('del tp1.xlsx') 
    workbook = xlsxwriter.Workbook('tp1.xlsx')
    worksheet = workbook.add_worksheet()
    chart = workbook.add_chart({'type': 'line'})
    worksheet.write(0,0, 'Ciclo')
    worksheet.write(0,1, 'Mínimo')
    worksheet.write(0,2, 'Máximo')
    worksheet.write(0,3, 'Cromosoma máximo decimal')
    worksheet.write(0,4, 'Cromosoma máximo')
    worksheet.write(0,5, 'Promedio')
    for j in range(ciclos):
        worksheet.write(j+1, 0, j+1)
        worksheet.write(j+1, 1, minimos[j])
        worksheet.write(j+1, 2, maximos[j])
        worksheet.write(j+1, 3, cromosomas_maximo_binario[j])
        worksheet.write(j+1, 4, cromosomas_maximo_decimal[j])
        worksheet.write(j+1, 5, promedios[j])
    workbook.close()

def mostrarGrafico():
    excel=pd.read_excel('tp1.xlsx')
    excel.to_csv('tp1.csv', index=None, header=True)
    datos=pd.read_csv('tp1.csv',header=0)
    _, ax = plt.subplots()
    ax.plot(datos['Mínimo'], label='Mínimo')
    ax.plot(datos['Máximo'], label='Máximo')
    ax.plot(datos['Promedio'], label='Promedio')
    plt.legend(loc='lower right')
    plt.show()

##DECLARACIÓN DE ARREGLOS
nueva_generacion = []
maximos   = []
minimos   = []
promedios = []
cromosomas_maximo_binario =[]
cromosomas_maximo_decimal=[]

##CARGA INICIAL
for i in range(pob):
    nueva_generacion.append(binario_random(genes))

for j in range(ciclos):
    ## CARGA DE TABLAS DE NUEVA GENERACION
    cromosomas_binario  = nueva_generacion
    cromosomas_decimal  = []
    cromosomas_objetivo = []
    cromosomas_fitness  = []
    cargarTablas()

    ##argmax y argmin devuelven un índice.
    cromosomas_maximo_binario.append(cromosomas_binario[numpy.argmax(cromosomas_objetivo)])
    cromosomas_maximo_decimal.append(cromosomas_decimal[numpy.argmax(cromosomas_objetivo)])
    maximos.append(numpy.max(cromosomas_objetivo))
    minimos.append(numpy.min(cromosomas_objetivo))
    promedios.append(numpy.average(cromosomas_objetivo))

    print("Generación ",j+1)
    print("  valor maximo     ", maximos[j])
    print("  valor minimo     ", minimos[j])
    print("  valor promedio   ", promedios[j])

    ##CARGA NUEVA GENERACION
    nueva_generacion = []
    if(elitismo):
        ##Se cargan los cromosomas que pasan por elitismo, según su fitness se consigue su índice en la lista, a partir de eso se busca en el binario
        for i in range(cant_elitismo):
            nueva_generacion.append(cromosomas_binario[cromosomas_fitness.index(sorted(cromosomas_fitness, reverse=True)[i])])
        cant_cargas = int((pob-cant_elitismo)/2)
    else:
        cant_cargas = int(pob/2) 
    
    for i in range( cant_cargas ) : cargarNuevaGeneracion() 

inicializarExcel()
mostrarGrafico()
#os.system('tp1.xlsx')
