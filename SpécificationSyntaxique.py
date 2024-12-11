# Binome : Loubari Chaima et Boukari Massilia

from ply import yacc
from lexer import tokens




def p_start(p):
    '''start : STARTUML ID defs ENDUML
             | STARTUML defs ENDUML'''
    if len(p) == 5:  
        p[0] = {'type': 'diagram', 'name': p[2], 'definitions': p[3]}
    else:  
        p[0] = {'type': 'diagram', 'name': None, 'definitions': p[2]}


def p_defs(p):
    '''defs : defs def
            | def'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_def_actor(p):
    '''def : ACTOR ACTOR_TXT
           | ACTOR ACTOR_TXT AS ID
           | ACTOR ACTOR_TXT STEREO'''
    if len(p) == 3:
        p[0] = {'type': 'actor', 'name': p[2], 'alias': None, 'stereotype': None}
    elif len(p) == 5:
        p[0] = {'type': 'actor', 'name': p[2], 'alias': p[4], 'stereotype': None}
    else:
        p[0] = {'type': 'actor', 'name': p[2], 'alias': None, 'stereotype': p[3]}


def p_def_usecase(p):
    '''def : USECASE USE_CASE_TXT
           | USECASE USE_CASE_TXT AS ID'''
    if len(p) == 3:
        p[0] = {'type': 'usecase', 'text': p[2], 'alias': None}
    else:
        p[0] = {'type': 'usecase', 'text': p[2], 'alias': p[4]}


def p_def_relation(p):
    '''def : ID RIGHT_ARROW_1 ID
           | ID INHERIT ID
           | ID COLON INCLUDES ID
           | ID COLON EXTENDS ID'''
    if len(p) == 4:
        p[0] = {'type': 'relation', 'from': p[1], 'to': p[3], 'relation_type': p[2]}
    else:
        p[0] = {'type': 'relation', 'from': p[1], 'to': p[4], 'relation_type': p[3]}


def p_def_package(p):
    'def : PACKAGE ID LBRACE defs RBRACE'
    p[0] = {'type': 'package', 'name': p[2], 'definitions': p[4]}


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p:
        print(f"Erreur syntaxique près de '{p.value}'")
    else:
        print("Erreur syntaxique à la fin du fichier")


parser = yacc.yacc()

# Exemple d'utilisation
if __name__ == "__main__":
    
    data = '''
    @startuml
    actor :Admin:
    usecase (Login) as UC1
    :Admin: --> (Login)
    package SubSystem {
        actor :User:
        usecase (Register)
        :User: --> (Register)
    }
    @enduml
    '''

    
    result = parser.parse(data)
    print(result)
