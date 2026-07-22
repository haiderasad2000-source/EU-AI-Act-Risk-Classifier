from ..rules.engine import classifier as engine

def classify_system(answers: dict):
    return engine.classify(answers)
