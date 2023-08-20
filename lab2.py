import graphviz
import networkx 
import matplot.lib.pyplot as plt 

class Node:
    def _init_(self, value):
        self.value = value
        self.left = None
        self.right = None

# Retorna la precedencia del operador c
def getPrecedence(c):
    # Si no es un operador, retorna 0
    precedence = {
        '(': 1,
        '|': 2,
        '.': 3,
        '?': 4,
        '*': 4,
        '+': 4,
        '^': 5
    }
    return precedence.get(c, 0)

# Agrega puntos para denotar concatenación implícita entre operandos
def formatRegEx(regex):
    # Retorna la expresión regular formateada
    allOperators = ['|', '?', '+', '*', '^'] 
    binaryOperators = ['^', '|'] 
    res = "" 

    for i in range(len(regex)): 
        c1 = regex[i] 

        if i + 1 < len(regex): 
            c2 = regex[i + 1] 

            res += c1 

            if (c1 != '(' and c2 != ')' and c2 not in allOperators and c1 not in binaryOperators): 
                res += '.' 
                
    # Concatena el último carácter de la expresión regular 
    res += regex[-1] 
    return res 

# Convierte la expresión de infix a postfix 
def infixToPostfix(regex):





        if c == '(':
            stack.append(c)
        elif c == ')':
            # Extrae operadores de la pila hasta encontrar '(' correspondiente
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            if stack and stack[-1] == '(':
                stack.pop()  # Elimina el '(' de la pila
        else:
            # Procesa operadores basándose en su precedencia
            while stack and getPrecedence(stack[-1]) >= getPrecedence(c):
                postfix += stack.pop()
            stack.append(c)

    # Añade los operadores restantes de la pila al resultado final
        while stack:
            sufijo += pila.pop()

        return postfix 

def postfixToAST(postfix): 
    stack = [] 

    for c in postfix: 
        if c.isalpha() or c == '𝜀': 
            node = Node(c) 
            stack.append(node) 
        else: 
            right_node = stack.pop () 
            nodo_izquierdo = Ninguno 

            if c != '*': 
                nodo_izquierdo = pila.pop() 

            nodo = Nodo(c) 
            nodo.derecho = nodo_derecho 

            if nodo_izquierdo: 
                nodo.izquierdo = nodo_izquierdo 

            pila.agregar(nodo) 

    return pila[0] 

def dibujarAST(nodo): 
    punto = graphviz.Digraph() 
    dibujarNodo(punto, nodo) 
    punto.vista()

def dibujarNodo(punto, nodo): 
    punto.nodo(str(id(nodo)), etiqueta=nodo.valor) 

    if nodo.izquierda: 
        punto.edge(str(id(nodo)), str(id(nodo.izquierda ))) 
        dibujarNodo(punto, nodo.izquierda) 

    if nodo.derecha: 
        punto.borde(str(id(nodo)), str(id(nodo.derecha))) 
        dibujarNodo(punto, nodo.derecha) 

def main() : 
    with open('expresiones2.txt', 'r', encoding='utf-8') as archivo: 
        lines = archivo.readlines() 

    for line in lines: 
        regex = line.strip() 
        postfix_expr = infixToPostfix(regex) 
        ast_root = postfixToAST(postfix_expr) 
        print("Regex:", regex) 
        drawAST(ast_root) 
        print() 



main()
