from automata.dfa import DFA

class Level:
    def __init__(self, name, description, objective, alphabet, examples_pos, examples_neg, validator):
        self.name = name
        self.description = description
        self.objective = objective
        self.alphabet = alphabet
        self.examples_pos = examples_pos
        self.examples_neg = examples_neg
        self.validator = validator

# ---------------- VALIDADORES DE NIVELES ----------------
def validate_level1(dfa: DFA):
    msgs = []
    if not dfa.start:
        msgs.append("Debes marcar un estado inicial.")
        return False, msgs
    accepted = all(dfa.run(w) for w in ["a", "ba", "bba"])
    rejected = all(not dfa.run(w) for w in ["b", "bb", "ab"])
    if accepted and rejected:
        return True, []
    else:
        msgs.append("El autómata no cumple con el objetivo de terminar en 'a'.")
        return False, msgs

def validate_level2(dfa: DFA):
    msgs = []
    if not dfa.start:
        msgs.append("Debes marcar un estado inicial.")
        return False, msgs
    accepted = all(dfa.run(w) for w in ["b", "ba", "bb"])
    rejected = all(not dfa.run(w) for w in ["a", "aa", "ab"])
    if accepted and rejected:
        return True, []
    else:
        msgs.append("El autómata no cumple con el objetivo de empezar con 'b'.")
        return False, msgs

def validate_level3(dfa: DFA):
    msgs = []
    if not dfa.start:
        msgs.append("Debes marcar un estado inicial.")
        return False, msgs
    accepted = all(dfa.run(w) for w in ["ab", "aab", "bab"])
    rejected = all(not dfa.run(w) for w in ["aa", "bb", "ba"])
    if accepted and rejected:
        return True, []
    else:
        msgs.append("El autómata no cumple con el objetivo de contener 'ab'.")
        return False, msgs

def validate_level4(dfa: DFA):
    msgs = []
    if not dfa.start:
        msgs.append("Debes marcar un estado inicial.")
        return False, msgs
    accepted = all(dfa.run(w) for w in ["", "aa", "bb", "abba"])
    rejected = all(not dfa.run(w) for w in ["a", "b", "aba"])
    if accepted and rejected:
        return True, []
    else:
        msgs.append("El autómata no cumple con el objetivo de longitud par.")
        return False, msgs

def validate_level5(dfa: DFA):
    msgs = []
    if not dfa.start:
        msgs.append("Debes marcar un estado inicial.")
        return False, msgs
    accepted = all(dfa.run(w) for w in ["", "aaa", "baaab"])
    rejected = all(not dfa.run(w) for w in ["a", "aa", "aab"])
    if accepted and rejected:
        return True, []
    else:
        msgs.append("El autómata no cumple con el objetivo de múltiplo de 3 en 'a'.")
        return False, msgs

# ---------------- LISTA DE NIVELES ----------------
LEVELS = [
    Level(
        name="Termina en 'a'",
        description="Construye un AFD que acepte cadenas que terminen en 'a'.",
        objective="El autómata debe aceptar todas las cadenas que terminen en 'a'.",
        alphabet=["a", "b"],
        examples_pos=["a", "ba", "bba"],
        examples_neg=["b", "bb", "ab"],
        validator=validate_level1
    ),
    Level(
        name="Empieza con 'b'",
        description="Construye un AFD que acepte cadenas que comiencen con 'b'.",
        objective="El autómata debe aceptar todas las cadenas que empiecen con 'b'.",
        alphabet=["a", "b"],
        examples_pos=["b", "ba", "bb"],
        examples_neg=["a", "aa", "ab"],
        validator=validate_level2
    ),
    Level(
        name="Contiene 'ab'",
        description="Construye un AFD que acepte cadenas que contengan la subcadena 'ab'.",
        objective="El autómata debe aceptar todas las cadenas que tengan 'ab' en cualquier posición.",
        alphabet=["a", "b"],
        examples_pos=["ab", "aab", "bab"],
        examples_neg=["aa", "bb", "ba"],
        validator=validate_level3
    ),
    Level(
        name="Longitud par",
        description="Construye un AFD que acepte cadenas de longitud par.",
        objective="El autómata debe aceptar todas las cadenas cuya longitud sea par.",
        alphabet=["a", "b"],
        examples_pos=["", "aa", "bb", "abba"],
        examples_neg=["a", "b", "aba"],
        validator=validate_level4
    ),
    Level(
        name="Número de 'a' múltiplo de 3",
        description="Construye un AFD que acepte cadenas donde el número de 'a' sea múltiplo de 3.",
        objective="El autómata debe aceptar todas las cadenas con cantidad de 'a' divisible entre 3.",
        alphabet=["a", "b"],
        examples_pos=["", "aaa", "baaab"],
        examples_neg=["a", "aa", "aab"],
        validator=validate_level5
    )
]