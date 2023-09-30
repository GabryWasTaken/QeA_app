from flask import g
import sqlite3


def connect_db():
    sql = sqlite3.connect('./questions.db')
    sql.row_factory = sqlite3.Row #Ricapitolando questo restituisce le righe della tabella come dizionario
    return sql

def get_db():
    if not hasattr(g, 'sqlite3_db'): #Controlla se il database è presente nell'oggetto g, se la condizione è True quindi il db non è presente
        g.sqlite_db = connect_db() #Collega il db
    return g.sqlite_db #viene inserito nell'oggetto

