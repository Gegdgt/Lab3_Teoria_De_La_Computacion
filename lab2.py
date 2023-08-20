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

def generateNFA(node):
    class NFAState:
        def __init__(self):
            self.transitions = {} 
    
    def create_nfa_state():
        return NFAState()
    
    def connect_states(state1, state2, input_symbol):
        if input_symbol not in state1.transitions:
            state1.transitions[input_symbol] = []
        state1.transitions[input_symbol].append(state2)
    
    def traverse_ast(current_node):
        if current_node.value.isalpha() or current_node.value == '𝜀':
            start_state = create_nfa_state()
            accepting_state = create_nfa_state()
            connect_states(start_state, accepting_state, current_node.value)
            return start_state, accepting_state
        elif current_node.value == '.':
            left_start, left_accepting = traverse_ast(current_node.left)
            right_start, right_accepting = traverse_ast(current_node.right)
            connect_states(left_accepting, right_start, '𝜀')
            return left_start, right_accepting
        elif current_node.value == '|':
            start_state = create_nfa_state()
            accepting_state = create_nfa_state()
            left_start, left_accepting = traverse_ast(current_node.left)
            right_start, right_accepting = traverse_ast(current_node.right)
            connect_states(start_state, left_start, '𝜀')
            connect_states(start_state, right_start, '𝜀')
            connect_states(left_accepting, accepting_state, '𝜀')
            connect_states(right_accepting, accepting_state, '𝜀')
            return start_state, accepting_state
        elif current_node.value == '*':
            start_state = create_nfa_state()
            accepting_state = create_nfa_state()
            child_start, child_accepting = traverse_ast(current_node.left)
            connect_states(start_state, accepting_state, '𝜀')
            connect_states(start_state, child_start, '𝜀')
            connect_states(child_accepting, accepting_state, '𝜀')
            connect_states(child_accepting, child_start, '𝜀')
            return start_state, accepting_state
    
    start_state, accepting_state = traverse_ast(node)
    nfa = {start_state: start_state, accepting_state: accepting_state}
    return nfa

def visualizeNFA(nfa):
    graph = nx.DiGraph()

    for state in nfa:
        graph.add_node(state)

        for input_symbol, target_states in nfa[state].transitions.items():
            for target_state in target_states:
                graph.add_edge(state, target_state, label=input_symbol)

    pos = nx.spring_layout(graph)
    labels = nx.get_edge_attributes(graph, 'label')
    nx.draw(graph, pos, with_labels=True, node_size=500, font_size=10)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()


def main():
    with open('expresiones2.txt', 'r', encoding='utf-8') as archivo:
        lines = archivo.readlines()

    for line in lines:
        regex = line.strip()
        postfix_expr = infixToPostfix(regex)
        ast_root = postfixToAST(postfix_expr)
        
        nfa = generateNFA(ast_root)  # Generate NFA from AST
        visualizeNFA(nfa)  # Visualize the NFA

        print()

if __name__ == "__main__":
    main()
