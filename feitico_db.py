import sqlite3
import os

PATH = os.path.join(os.getcwd(), 'resources', 'feitico.db')
conn = sqlite3.connect(PATH)
cursor = conn.cursor()

###################
# CRIANDO TABELAS #
###################

# cursor.execute("""
# CREATE TABLE feitico (
# 	id_feitico INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 	nome VARCHAR(255) NOT NULL UNIQUE,
# 	descricao TEXT NOT NULL,
# 	disponivel BOOLEAN NOT NULL,
# 	nivel INTEGER  NOT NULL,
# 	dificuldade INTEGER NOT NULL,
# 	tipo INTEGER NOT NULL,
# 	ex_solucao TEXT
# );
# """)

# cursor.execute("""
# CREATE TABLE status (
# 	id_status INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 	id_feitico INTEGER,
# 	assunto VARCHAR(255) NOT NULL,
# 	valor INTEGER NOT NULL,
# 	FOREIGN KEY(id_feitico) REFERENCES feitico(id_feitico)
# );
# """)

# ADICIONANDO CAMPO NA TABELA
# cursor.execute("""
# 	ALTER TABLE feitico ADD COLUMN json TEXT;
# """)

#####################
# INSERINDO VALORES #
#####################

# cursor.execute("""
# INSERT INTO feitico VALUES (
# 	null,
# 	'teste',
# 	'feitico que ordena livros',
# 	1,
# 	0,
# 	0,
# 	1,
# 	null
# );
# """)

# cursor.execute("""
# INSERT INTO status VALUES (
# 	null,
# 	4,
# 	'operadores',
# 	90
# );
# """)

conn.commit()

cursor.execute("""
SELECT * FROM status
WHERE assunto = 'tipos'
and id_feitico > 2
""")
print cursor.fetchall()

conn.close()
