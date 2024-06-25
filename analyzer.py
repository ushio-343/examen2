import ply.lex as lex
import ply.yacc as yacc
from flask import Flask, render_template, request

app = Flask(__name__)

# Definición de palabras reservadas para cada lenguaje
reserved = {
    'java': {
        'for': 'FOR',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'public': 'PUBLIC',
        'private': 'PRIVATE',
        'protected': 'PROTECTED',
        'class': 'CLASS',
        'void': 'VOID',
        'static': 'STATIC',
        'int': 'INT',
        'float': 'FLOAT',
        'double': 'DOUBLE',
        'string': 'STRING',
        'system': 'SYSTEM',
        'out': 'OUT',
        'println': 'PRINTLN',
        'and': 'AND',
        'input': 'INPUT',
        'range': 'RANGE',
        'in': 'IN',
    },
    'pakatreice': {
        'int': 'INT',
        'do': 'DO',
        'while': 'WHILE',
        'enddo': 'ENDDO',
        'endwhile': 'ENDWHILE',
    },
    'golang': {
        'for': 'FOR',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'func': 'FUNC',
        'return': 'RETURN',
        'package': 'PACKAGE',
        'import': 'IMPORT',
        'fmt': 'FMT',
        'println': 'PRINTLN',
        'main': 'pepe',
    },
    'c': {
        'include': "INCLUDE",
        'stdio': 'STDIO',
        'int': 'INT',
        'main': 'MAIN',
        'for': 'FOR',
        'return': 'RETURN',
        'h': 'H'
    }
}

# Lista de tokens
tokens = [
    'IDENTIFICADOR',
    'ABIERTO',
    'CERRADO',
    'LLAVE_ABIERTA',
    'LLAVE_CERRADA',
    'PUNTO_Y_COMA',
    'IGUAL',
    'MAS',
    'MENOR_IGUAL',
    'MAYOR_IGUAL',
    'PUNTO',
    'MAS_IGUAL',
    'COMILLAS',
    'CADENA',
    'NUMERO',
    'MENOR',
    'MAYOR',
    'COMA',
    'POR',
    'GATO',
] + list(set(sum([list(r.values()) for r in reserved.values()], [])))

# Reglas para tokens simples
t_ABIERTO = r'\('
t_CERRADO = r'\)'
t_LLAVE_ABIERTA = r'\{'
t_LLAVE_CERRADA = r'\}'
t_PUNTO_Y_COMA = r';'
t_COMA = r','
t_IGUAL = r'='
t_MAS = r'\+'
t_MAS_IGUAL = r'\+='
t_POR = r'\*'
t_GATO = r'\#'
t_MENOR_IGUAL = r'<='
t_MAYOR_IGUAL = r'>='
t_MENOR = r'<'
t_MAYOR = r'>'
t_PUNTO = r'\.'
t_COMILLAS = r'\"'
t_CADENA = r'\".*?\"'

# Regla para números
t_NUMERO = r'\d+'

# Contadores
reserved_count = 0
identificador_count = 0
number_count = 0
symbol_count = 0
p_abierto_count = 0
p_cerrado_count = 0
ll_abierta_count = 0
ll_cerrada_count = 0
error_count = 0

# Lista para guardar declaraciones de variables
declared_variables = {}

# Regla para identificadores y palabras reservadas
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    global current_language
    t.type = reserved[current_language].get(t.value.lower(), 'IDENTIFICADOR')
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t\n\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Función para manejar errores léxicos
def t_error(t):
    global error_count
    error_count += 1
    print(f"Caracter no válido: {t.value[0]}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

def p_program(p):
    '''program : statement_list
               | go_program'''

def p_go_program(p):
    '''go_program : package_statement import_statement function_list'''

def p_package_statement(p):
    '''package_statement : PACKAGE IDENTIFICADOR'''

def p_import_statement(p):
    '''import_statement : IMPORT CADENA'''

def p_function_list(p):
    '''function_list : function
                     | function function_list'''

def p_function(p):
    '''function : FUNC pepe ABIERTO CERRADO LLAVE_ABIERTA statement_list LLAVE_CERRADA'''

def p_print_go_statement(p):
    '''print_go_statement : FMT PUNTO PRINTLN ABIERTO CADENA CERRADO'''

def p_variable_declaration(p):
    '''variable_declaration : INT IDENTIFICADOR IGUAL NUMERO PUNTO_Y_COMA'''
    if p[2] in declared_variables:
        raise SemanticError(f"Variable '{p[2]}' ya declarada")
    print(f"Declaración de variable: {p[2]} = {p[4]}")  # Debugging output
    declared_variables[p[2]] = {'tipo': 'int', 'valor': p[4]}

def p_variable_declaration_simple(p):
    '''variable_declaration_simple : INT IDENTIFICADOR PUNTO_Y_COMA'''
    if p[2] in declared_variables:
        raise SemanticError(f"Variable '{p[2]}' ya declarada")
    print(f"Declaración de variable sin inicialización: {p[2]}")  # Debugging outpu
    declared_variables[p[2]] = {'tipo': 'int', 'valor': p[4]}  # Asignar el tipo 'int' a la variable y su valor

def p_float_declaration(p):
    '''float_declaration : FLOAT IDENTIFICADOR IGUAL NUMERO PUNTO NUMERO PUNTO_Y_COMA'''
    if p[2] in declared_variables:
        raise SemanticError(f"Variable '{p[2]}' ya declarada")
    print(f"Declaración de variable: {p[2]} = {p[4]}")  # Debugging output
    declared_variables[p[2]] = {'tipo': 'float', 'valor': p[4]}

def p_string_declaration(p):
    '''string_declaration : STRING IDENTIFICADOR IGUAL CADENA PUNTO_Y_COMA'''
    if p[2] in declared_variables:
        raise SemanticError(f"Variable '{p[2]}' ya declarada")
    print(f"Declaración de variable: {p[2]} = {p[4]}")  # Debugging output
    declared_variables[p[2]] = {'tipo': 'String', 'valor': p[4]}

def p_if_statement(p):
    '''if_statement : IF ABIERTO condition_statement AND NUMERO MAYOR NUMERO CERRADO LLAVE_ABIERTA while_statement LLAVE_CERRADA'''

def p_while_statement(p):
    '''while_statement : WHILE ABIERTO IDENTIFICADOR MAYOR NUMERO CERRADO LLAVE_ABIERTA INPUT ABIERTO NUMERO CERRADO PUNTO_Y_COMA increment_statement LLAVE_CERRADA WHILE ABIERTO NUMERO MAYOR NUMERO CERRADO LLAVE_ABIERTA FOR ABIERTO IDENTIFICADOR IN RANGE ABIERTO COMA NUMERO CERRADO CERRADO LLAVE_ABIERTA IDENTIFICADOR IGUAL NUMERO POR NUMERO PUNTO_Y_COMA LLAVE_CERRADA LLAVE_CERRADA'''

def p_print_statement(p):
    '''print_statement : SYSTEM PUNTO OUT PUNTO PRINTLN ABIERTO CADENA MAS IDENTIFICADOR CERRADO PUNTO_Y_COMA'''
    if p[9] not in declared_variables:
        raise SemanticError(f"Variable '{p[9]}' no declarada")

def p_pakatreice_statement(p):
    '''pakatreice_statement : DO arithmetic_operation PUNTO_Y_COMA arithmetic_operation PUNTO_Y_COMA ENDDO WHILE ABIERTO condition CERRADO ENDWHILE'''

def p_condition(p):
    '''condition : INT IDENTIFICADOR IGUAL IGUAL NUMERO
                 | IDENTIFICADOR IGUAL IGUAL NUMERO'''
    if len(p) == 6:
        if p[2] not in declared_variables:
            raise SemanticError(f"Variable '{p[2]}' no declarada.")
    # Caso cuando la condición es del tipo "IDENTIFICADOR IGUAL IGUAL NUMERO"
    if len(p) == 5:
        identificador = p[1]
        valor_esperado = p[4]
        if identificador in declared_variables:
            # Obtiene el valor actual de la variable
            valor_actual = declared_variables[identificador]['valor']
            # Compara el valor actual con el valor esperado en la condición
            if valor_actual == valor_esperado:
                # La condición se cumple
                pass
            else:
                raise SemanticError(f"La condicion es falsa para '{identificador}' = {valor_esperado}.")
        else:
            raise SemanticError(f"Variable '{identificador}' no declarada.")

def p_library(p):
    '''library_statement : GATO INCLUDE MENOR STDIO PUNTO H MAYOR'''

def p_main(p):
    '''main_statement : INT MAIN ABIERTO CERRADO LLAVE_ABIERTA line_declaration_statement for_statement RETURN NUMERO PUNTO_Y_COMA LLAVE_CERRADA '''

def p_line_declaration(p):
    '''line_declaration_statement : INT IDENTIFICADOR COMA IDENTIFICADOR COMA IDENTIFICADOR IGUAL NUMERO PUNTO_Y_COMA'''
    if p[2] in declared_variables or p[4] in declared_variables or p[6] in declared_variables:
        raise SemanticError('Una de las variables ya esta declarada')
    else:
        declared_variables[p[2]] = {'tipo': 'int', 'valor': p[8]}
        declared_variables[p[4]] = {'tipo': 'int', 'valor': p[8]}
        declared_variables[p[6]] = {'tipo': 'int', 'valor': p[8]}

def p_for_statement(p):
    '''for_statement : FOR ABIERTO assignment_statement PUNTO_Y_COMA condition_statement PUNTO_Y_COMA increment_statement CERRADO LLAVE_ABIERTA arithmetic_operation PUNTO_Y_COMA arithmetic_operation PUNTO_Y_COMA LLAVE_CERRADA'''

def p_assignment_statement(p):
    '''assignment_statement : IDENTIFICADOR IGUAL NUMERO
                            | IDENTIFICADOR IGUAL IDENTIFICADOR MAS IDENTIFICADOR'''
    if len(p) == 5:
        if p[1] not in declared_variables:
            raise SemanticError(f"Variable '{p[1]}' no declarada")
        if p[3] not in declared_variables:
            raise SemanticError(f"Variable '{p[3]}' no declarada")
        if p[5] not in declared_variables:
            raise SemanticError(f"Variable '{p[5]}' no declarada")
    else:
        if p[1] not in declared_variables:
            raise SemanticError(f"Variable '{p[1]}' no declarada")

def p_condition_statement(p):
    '''condition_statement : IDENTIFICADOR MENOR_IGUAL NUMERO
                           | IDENTIFICADOR IGUAL IGUAL NUMERO
                           | IDENTIFICADOR MAYOR NUMERO
                           | IDENTIFICADOR MAYOR_IGUAL NUMERO'''
    # if p[1] not in declared_variables:
    #     raise SemanticError(f"Variable '{p[1]}' no declarada")
    identificador = p[1]
    valor_esperado = p[3]
    if identificador in declared_variables:
        # Obtiene el valor actual de la variable
        valor_actual = declared_variables[identificador]['valor']
        print(valor_actual)
        # Compara el valor actual con el valor esperado en la condición
        if valor_actual <= valor_esperado:
            # La condición se cumple
            pass
        elif valor_actual == valor_esperado:
            pass
        else:
            raise SemanticError(f"La condicion es falsa para '{identificador}' con {valor_esperado}.")
    else:
        raise SemanticError(f"Variable '{identificador}' no declarada.")

def p_increment_statement(p):
    '''increment_statement : IDENTIFICADOR MAS MAS
                           | IDENTIFICADOR MAS_IGUAL NUMERO'''
    if p[1] not in declared_variables:
        raise SemanticError(f"Variable '{p[1]}' no declarada")

def p_arithmetic_operation(p):
    '''arithmetic_operation : IDENTIFICADOR IGUAL NUMERO POR IDENTIFICADOR
                            | IDENTIFICADOR IGUAL NUMERO MAS IDENTIFICADOR
                            | IDENTIFICADOR IGUAL IDENTIFICADOR POR NUMERO
                            | IDENTIFICADOR IGUAL IDENTIFICADOR MAS NUMERO
                            | IDENTIFICADOR IGUAL IDENTIFICADOR MAS IDENTIFICADOR
                            | IDENTIFICADOR IGUAL NUMERO MAS NUMERO'''
    if p[1] not in declared_variables:
        raise SemanticError(f"Variable '{p[1]}' no declarada")

# def p_arithmetic_operation(p):
#     '''arithmetic_operation : IDENTIFICADOR IGUAL NUMERO POR IDENTIFICADOR
#                             | IDENTIFICADOR IGUAL NUMERO MAS IDENTIFICADOR
#                             | IDENTIFICADOR IGUAL IDENTIFICADOR POR NUMERO
#                             | IDENTIFICADOR IGUAL IDENTIFICADOR MAS NUMERO
#                             | IDENTIFICADOR IGUAL IDENTIFICADOR MAS IDENTIFICADOR
#                             | IDENTIFICADOR IGUAL IDENTIFICADOR POR IDENTIFICADOR'''
#     # Verificar que la variable a la izquierda del igual esté declarada
#     if p[1] not in declared_variables:
#         raise SemanticError(f"Variable '{p[1]}' no declarada")

#     # Verificar si el tercer y quinto elemento son identificadores y si están declarados
#     if isinstance(p[3], str) and p[3] not in declared_variables:
#         raise SemanticError(f"Variable '{p[3]}' no declarada")
#     if isinstance(p[5], str) and p[5] not in declared_variables:
#         raise SemanticError(f"Variable '{p[5]}' no declarada")

#     # Determinar el tipo de operación
#     if p[4] == '*':
#         p[0] = (p[1], '=', p[3], '*', p[5])
#     elif p[4] == '+':
#         p[0] = (p[1], '=', p[3], '+', p[5])
#     else:
#         raise SyntaxError(f"Operador desconocido '{p[4]}'")

def p_statement(p):
    '''statement : 
                 | pakatreice_statement
                 | print_go_statement
                 | print_statement
                 | variable_declaration
                 | variable_declaration_simple
                 | float_declaration
                 | string_declaration
                 | if_statement
                 | while_statement
                 | library_statement
                 | main_statement
                 | line_declaration_statement
                 | for_statement
                 | assignment_statement
                 | condition_statement
                 | increment_statement
                 | arithmetic_operation
                 | condition'''

    
def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''

def p_error(p):
    if p:
        error_message = f"Error sintáctico en el token {p.value}"
    else:
        error_message = "Error sintáctico: Fin inesperado del archivo"
    raise SyntaxError(error_message)

# Construir el parser
parser = yacc.yacc(debug=True)

# Excepcion personalizada para el análisis semántico
class SemanticError(Exception):
    pass

# int a1;
# for (a2 = 1; a1 <= 10; a++) {
#     System.out.println("Número: " + i);
# }

# int a=1;
# int b= 10;
# int c=1;
# int x=2;
# do 
#  a=3*b;
#  c=2+a;
# enddo
# while(x==2)
# endwhile

@app.route('/', methods=['GET', 'POST'])
def index():
    global reserved_count, identificador_count, number_count, symbol_count, p_abierto_count, p_cerrado_count, ll_abierta_count, ll_cerrada_count, error_count, current_language
    reserved_count = 0
    identificador_count = 0
    number_count = 0
    symbol_count = 0
    p_abierto_count = 0
    p_cerrado_count = 0
    ll_abierta_count = 0
    ll_cerrada_count = 0
    error_count = 0
    content = ''
    if request.method == 'POST':
        language = request.form.get('language', 'c')
        current_language = language
        content = request.form.get('code', '')

        analysis_type = request.form.get('analysis_type', 'Análisis Léxico')
        
        if analysis_type == 'Análisis Léxico':
            lexer.input(content)
            result_lexema = []
            # Token, Reservada, identificador, numero, simbolo, p_izq, p_der, ll_izq, ll_der
            for token in lexer:
                if token.type == 'ABIERTO':
                    p_abierto_count += 1
                    # result_lexema.append(("Parentesis de apertura", token.value, '', '', token.lineno))
                    result_lexema.append((token.value, '', '', '', '','X', '', '', ''))

                elif token.type == 'CERRADO':
                    p_cerrado_count += 1
                    result_lexema.append((token.value, '', '', '', '','', 'X', '', ''))

                elif token.type == 'LLAVE_ABIERTA':
                    ll_abierta_count += 1
                    result_lexema.append((token.value, '', '', '', '','', '', 'X', ''))

                elif token.type == 'LLAVE_CERRADA':
                    ll_cerrada_count += 1
                    result_lexema.append((token.value, '', '', '', '','', '', '', 'X'))

                elif token.type == 'PUNTO_Y_COMA':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))

                elif token.type in reserved[current_language].values():
                    reserved_count += 1
                    result_lexema.append((token.value, 'X', '', '', '','', '', '', ''))

                elif token.type == 'IDENTIFICADOR':
                    identificador_count += 1
                    result_lexema.append((token.value, '', 'X', '', '','', '', '', ''))

                elif token.type == 'NUMERO':
                    number_count += 1
                    result_lexema.append((token.value, '', '', 'X', '','', '', '', ''))

                elif token.type == 'CADENA':
                    result_lexema.append((token.value, '', '', '', '','', '', '', ''))

                elif token.type == 'MAS':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))

                elif token.type == 'IGUAL':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))

                elif token.type == 'MENOR_IGUAL':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))
                
                elif token.type == 'MAYOR_IGUAL':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))

                elif token.type == 'PUNTO':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))

                elif token.type == 'MAS_IGUAL':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))

                elif token.type == 'COMILLAS':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))

                elif token.type == 'MENOR':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))
                
                elif token.type == 'MAYOR':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))
                
                elif token.type == 'COMA':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))

                elif token.type == 'POR':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))
                
                elif token.type == 'GATO':
                    symbol_count += 1
                    result_lexema.append((token.value, '', '', '', 'X','', '', '', ''))

                else:
                    result_lexema.append(("Error", token.value, '', '', token.lineno))

            return render_template('index.html', tokens=result_lexema, syntax_result=None, content=content, abierto_count=p_abierto_count, cerrado_count=p_cerrado_count, ll_abierta_count=ll_abierta_count, ll_cerrada_count=ll_cerrada_count)
        
        elif analysis_type == 'Análisis Sintáctico':
            syntax_result = []
            try:
                declared_variables.clear()
                parser.parse(content)
                syntax_result = [("Análisis Sintáctico Exitoso", "", "", 0)]
            except SyntaxError as e:
                syntax_result = [("Error en Análisis Sintáctico", str(e), "", 0)]
            except SemanticError as e:  # Captura el SemanticError para evitar que el programa truene
                syntax_result = [("Analisis Sintactico Exitoso", "Posible error Semántico detectado durante el Análisis Sintáctico", "", 0)]
            return render_template('index.html', tokens=None, syntax_result=syntax_result, content=content, abierto_count=p_abierto_count, cerrado_count=p_cerrado_count, ll_abierta_count=ll_abierta_count, ll_cerrada_count=ll_cerrada_count)
        
        elif analysis_type == 'Análisis semantico':
            try:
                declared_variables.clear()
                parser.parse(content)
                semantic_result = "Análisis Semántico Exitoso"
            except SyntaxError as e:
                print(e)
                semantic_result = "Sintáctico: " + str(e)
            except SemanticError as e:
                print(e)
                semantic_result = "Semantico: " + str(e)
            return render_template('index.html', tokens=None, syntax_result=[(semantic_result, "", "", '')], content=content, abierto_count=p_abierto_count, cerrado_count=p_cerrado_count, ll_abierta_count=ll_abierta_count, ll_cerrada_count=ll_cerrada_count)

    return render_template('index.html', tokens=None, syntax_result=None, content=content, abierto_count=p_abierto_count, cerrado_count=p_cerrado_count)

if __name__ == "__main__":
    app.run(debug=True)