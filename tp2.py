import numpy

#volumenes = [150, 325, 600, 805, 430, 1200, 770, 60, 930, 353]
#valores = [20, 40, 50, 36, 25, 64, 54, 18, 46, 28]
#volumen_mochila = 4200

volumenes = [1800,600,1200]
valores = [72,36,60]
volumen_mochila = 3000

division = []
for i in range(len(valores)):
  division.append(valores[i] / volumenes[i])

#Crea toda las combinaciones posibles, empieza con el arreglo vacío y uno por uno agrega elementos
#una vez que se agrega un elemento se añade ese elemento a todas las combinaciones anteriores calculadas dandoles el valor r
#y agregándole el proximo elemento
#Ej: empieza en c=[[]] -> 
# c= [[],[0]] -> 
# c= [[],[0],[1]]
# c= [[],[0],[1],[0, 1]] -> 
# c= [[], [0], [1], [0, 1], [2]] -> 
#                          //^ acá se suma [] + [2]//
#
# c= [[], [0], [1],[0, 1], [2], [0,2]] -> 
# c= [[], [0], [1],[0, 1], [2], [0,2], [1,2]]  -> 
# c= [[], [0], [1],[0, 1], [2], [0,2], [1,2], [0,1,2]]  -> 
#                                            //^ acá se suma [0,1] + [2]//                                                                       
def combinations(lista):
    comb = [[]]
    for x in lista:
        for r in comb:
            comb= comb + [r+[x]]
    return comb

def exh():
    combinaciones_valores = combinations(valores)
    combinaciones_volumenes = combinations(volumenes)
    #Como los arreglos están en el mismo orden cada combinación se relaciona uno a una con la otra.

    max_valor = 0
    n_mejor = 0

    for i in range(len(combinaciones_valores)):

        if(sum(combinaciones_valores[i]) > max_valor and sum(combinaciones_volumenes[i]) <= volumen_mochila):
            n_mejor = i
            max_valor = sum(combinaciones_valores[i])
    print("La mejor combinación es ", n_mejor)

    print("valor total    ", sum(combinaciones_valores[n_mejor]))
    print("volumen total  ", sum(combinaciones_volumenes[n_mejor]))

    for i in range(len(combinaciones_valores[n_mejor])):
        print("valor: ", combinaciones_valores[n_mejor][i],"  volumen:", combinaciones_volumenes[n_mejor][i])

def greedy():

    index = numpy.argsort(division)[::-1]
    acum_valor = 0
    acum_volumen = 0
    valores_usados = []
    volumenes_usados = []
    for i in index:
        if(acum_volumen + volumenes[i] < volumen_mochila ):
            acum_valor += valores[i]
            acum_volumen += volumenes[i]
            valores_usados.append(valores[i])
            volumenes_usados.append(volumenes[i])
    print("El valor calculado es: ", acum_valor)
    print("El volumen calculado es: ", acum_volumen)

    for i in range(len(valores_usados)):
        print("valor: ", valores_usados[i],"  volumen:", volumenes_usados[i])

print("Exhaustiva: ")
exh()   
print("Greedy: ") 
greedy()
