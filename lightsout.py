#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'Rolando Velez'


import busquedas
import math

class LightsOut(busquedas.ModeloBusqueda):
    # --------------------------------------------------------
    # Problema 2:  Completa la clase
    # para el modelo de lights out
    # --------------------------------------------------------
    """
    Problema del jueguito "Ligths out".

    La idea del juego es el apagar o prender todas las luces.
    Al seleccionar una casilla, la casilla y sus casillas
    adjacentes cambian (si estan prendidas se apagan y viceversa).

    El juego consiste en una matriz de 5 X 5, cuyo estado puede
    ser apagado 0 o prendido 1. Por ejemplo el estado

       (0,0,1,0,0,1,1,0,0,1,0,0,1,1,0,1,0,1,0,1,0,0,0,0,0)

    corresponde a:

    ---------------------
    |   |   | X |   |   |
    ---------------------
    | X | X |   |   | X |
    ---------------------
    |   |   | X | X |   |
    ---------------------
    | X |   | X |   | X |
    ---------------------
    |   |   |   |   |   |
    ---------------------

    Las acciones posibles son de elegir cambiar una luz y sus casillas
    adjacentes, por lo que la accion es un número entre 0 y 24.

    Para mas información sobre el juego, se puede consultar

    http://en.wikipedia.org/wiki/Lights_Out_(game)

    """
    def __init__(self):
        self.acciones = range(25)

    def acciones_legales(self, estado):
        return self.acciones

    def sucesor(self, estado, accion):
        """
            Voltea los valores para obtener el estado sucesor.
            Para simplificar el ejemplo en un cuadrado 3x3  y
                utilizando [1,1] como el que se presiono.
            Los elementos 'x' no cambian de valor.

               0  1  2                 0  1  2
              —————————               ————————
            0 |x, 1, x,             0 |x, 0, x
            1 |1, 0, 0,     ->      1 |0, 1, 1,
            2 |x, 0, x              2 |x, 1, x

            Voltea primero el valor de la casilla que se presiono.
            Despues realiza una serie de chequeos para ver si 
                es valido voltear el valor de la casilla.

            Para terminar regresa el nuevo estado con los nuevos
                valores en las casillas.
        """

        n = 5
        succ = list(estado)

        col = accion % n
        row = accion // n

        # Valor que se presiono
        succ[accion] = not succ[accion]
       
        # Valor a la izquierda
        if col > 0:
           succ[accion - 1] = not succ[accion - 1]
        # Valor a la derecha
        if col < 4:
            succ[accion + 1] = not succ[accion + 1]

        # Valor de arriba
        if row > 0:
            succ[accion - n] = not succ[accion - n]
        # Valor de abajo
        if row < 4:
            succ[accion + n] = not succ[accion + n]
        return tuple(succ)

    def costo_local(self, estado, accion):
        return 1

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        cadena = "---------------------\n"
        for i in range(5):
            for j in range(5):
                if estado[5 * i + j]:
                    cadena += "| X "
                else:
                    cadena += "|   "
            cadena += "|\n---------------------\n"
        return cadena


# ------------------------------------------------------------
#  Problema 3: Completa el problema de LightsOut
# ------------------------------------------------------------
class ProblemaLightsOut(busquedas.ProblemaBusqueda):
    def __init__(self, pos_ini):
        """
        Utiliza la superclase para hacer el problema

        """
        # Completa el código
        x0 = tuple(pos_ini)
        # Verifica que todos los valores sean 0 (apagados) y regresa 'True'
        # En caso de que algun elemento este prendido regresa 'False'
        def meta(x):
            return all(xi == 0 for xi in x)
        super().__init__(x0=x0, meta=meta, modelo=LightsOut())


# ------------------------------------------------------------
#  Problema 4: Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Regresa la suma de las luces encendidas utilizando la distancia euclidiana al cuadrado.
    """
    #return sum(list(nodo.estado)) / 5
    return sum([abs(i % 5 - nodo.estado[i] % 5) *
                        abs(i % 5 - nodo.estado[i] % 5) + 
                        abs(i // 5 - nodo.estado[i] // 5) *
                        abs(i // 5 - nodo.estado[i] // 5)
                        for i in range(25) if nodo.estado[i] != 0])

    

# ------------------------------------------------------------
#  Problema 5: Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Regresa la suma de las luces encendidas utilizando la distancia euclidiana.

    En el mayor de los casos h_2 va a dominar a h_1 ya que los nodos 
        expandidos son menores que si utilizaramos h_1 (en su mayoria).
    Se puede ver claramente en el caso de que todas las luces esten
        encendidas como es que h_2 es superior que h_1
    """
    return sum([math.sqrt(abs(i % 5 - nodo.estado[i] % 5) *
                        abs(i % 5 - nodo.estado[i] % 5) + 
                        abs(i // 5 - nodo.estado[i] // 5) *
                        abs(i // 5 - nodo.estado[i] // 5))
                        for i in range(25) if nodo.estado[i] != 0])

def prueba_modelo():
    """
    Prueba la clase LightsOut

    """

    pos_ini = (0, 1, 0, 1, 0,
               0, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a0 = (1, 0, 0, 1, 0,
              1, 0, 1, 1, 0,
              0, 0, 0, 1, 1,
              0, 0, 1, 1, 1,
              0, 0, 0, 1, 1)

    pos_a4 = (1, 0, 0, 0, 1,
              1, 0, 1, 1, 1,
              0, 0, 0, 1, 1,
              0, 0, 1, 1, 1,
              0, 0, 0, 1, 1)

    pos_a24 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 0,
               0, 0, 0, 0, 0)

    pos_a15 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 1, 0,
               1, 0, 0, 0, 0)

    pos_a12 = (1, 0, 0, 0, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 0, 1,
               1, 1, 0, 1, 0,
               1, 0, 0, 0, 0)

    modelo = LightsOut()

    assert modelo.acciones_legales(pos_ini) == range(25)
    assert modelo.sucesor(pos_ini, 0) == pos_a0
    assert modelo.sucesor(pos_a0, 4) == pos_a4
    assert modelo.sucesor(pos_a4, 24) == pos_a24
    assert modelo.sucesor(pos_a24, 15) == pos_a15
    assert modelo.sucesor(pos_a15, 12) == pos_a12
    print("Paso la prueba de la clase LightsOut")


def compara_metodos(pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    @return None (no regresa nada, son puros efectos colaterales)

    Si la búsqueda no informada es muy lenta, posiblemente tendras que quitarla
    de la función

    """
    solucion1 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_1)
    solucion2 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_2)

    print('-' * 50)
    print('Método'.center(10) + 'Costo'.center(20) + 'Nodos visitados')
    print('-' * 50 + '\n\n')
    print('A* con h1'.center(10) + str(solucion1.costo).center(20) +
          str(solucion1.nodos_visitados))
    print('A* con h2'.center(10) + str(solucion2.costo).center(20) +
          str(solucion2.nodos_visitados))
    print('-' * 50 + '\n\n')


if __name__ == "__main__":

    print("Antes de hacer otra cosa,")
    print("vamos a verificar medianamente la clase LightsOut")
    prueba_modelo()

    # Tres estados iniciales interesantes
    diagonal = (0, 0, 0, 0, 1, 
                0, 0, 0, 1, 0,
                0, 0, 1, 0, 0,
                0, 1, 0, 0, 0,
                1, 0, 0, 0, 0)

    simetria = (1, 0, 1, 0, 1,
                1, 0, 1, 0, 1,
                0, 0, 0, 0, 0,
                1, 0, 1, 0, 1,
                1, 0, 1, 0, 1)

    problemin = (0, 1, 0, 1, 0,
                 0, 0, 1, 1, 0,
                 0, 0, 0, 1, 1,
                 0, 0, 1, 1, 1,
                 0, 0, 0, 1, 1)

    problemon = (1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1)

    print("\n\nPara el problema en diagonal")
    print("\n{}".format(LightsOut.bonito(diagonal)))
    compara_metodos(diagonal, h_1, h_2)

    print("\n\nPara el problema simétrico")
    print("\n{}".format(LightsOut.bonito(simetria)))
    compara_metodos(simetria, h_1, h_2)

    print("\n\nPara el problema Bonito")
    print("\n{}".format(LightsOut.bonito(problemin)))
    compara_metodos(problemin, h_1, h_2)
    
    print("\n\nPara el problema con todas las luces encendidas")
    print("\n{}".format(LightsOut.bonito(problemon)))
    compara_metodos(problemon, h_1, h_2)
