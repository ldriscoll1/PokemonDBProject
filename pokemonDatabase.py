import mysql.connector
import dataFormatter as df
import os
from dotenv import load_dotenv

def createInitialConnection():
    """ create a database connection to a SQLite database """
    load_dotenv()
    PASSWORD = os.getenv('PASSWORD')
    DATABASE = os.getenv('DATABASE')
    conn = mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=PASSWORD,
        auth_plugin='mysql_native_password'
    )
    mycursor = conn.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS " + DATABASE)
    return conn
def createConnection():
    """ create a database connection to a SQLite database """
    load_dotenv()
    PASSWORD = os.getenv('PASSWORD')
    DATABASE = os.getenv('DATABASE')
    conn = mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=PASSWORD,
        database=DATABASE
    )
    return conn
def createIndex(conn, index):
    """ create an index from the create_index_sql statement
    :param conn: Connection object returned from create_connection
    :param create_index_sql: a CREATE INDEX statement as a string
    :return:
    """
    c = conn.cursor()
    c.execute(index)
def createView(conn, view):
    """ create a view from the create_view_sql statement
    :param conn: Connection object returned from create_connection
    :param create_view_sql: a CREATE VIEW statement as a string
    :return:
    """
    c = conn.cursor()
    c.execute(view)
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object returned from create_connection
    :param create_table_sql: a CREATE TABLE statement as a string
    :return:
    """
    c = conn.cursor()
    c.execute(create_table_sql)
def addGame(conn, game):
    sql = ''' INSERT INTO Game(GameName,GenerationID)
              VALUES(%s,%s) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, game)
        conn.commit()
    except:
        conn.rollback()
        raise Exception("Error Adding Game")
def addGeneration(conn, generation):
    sql = ''' INSERT INTO Generation(GenerationID)
              VALUES(%s) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, generation)
        conn.commit()
    except:
        conn.rollback()
        raise Exception("Error Adding Generation")
def addType(conn, type):
    sql = ''' INSERT INTO Type(TypeName)
              VALUES(%s) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, type)
        conn.commit()
    except:
        conn.rollback()
        raise Exception("Error Adding Type")
def addPokemon(conn, pokemon):
    sql = ''' INSERT INTO Pokemon(PokemonName,Type1ID,Type2ID,Height,Weight,GenerationID)
              VALUES(%s,%s,%s,%s,%s,%s) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, pokemon)
        conn.commit()
    except:
        print("Error Adding Pokemon")
        conn.rollback()
def addTypeChart(conn, typeChart):
    sql = ''' INSERT INTO TypeChart(Type1ID,Type2ID,Effectiveness)
              VALUES(%s,%s,%s) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, typeChart)
        conn.commit()
    except:
        conn.rollback()
        raise Exception("Error Adding TypeCombo to TypeChart",typeChart)
def deletePokemon(conn,pokemonID):
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Pokemon WHERE PokemonID = \""+ pokemonID + "\"")
        conn.commit()
    except:
        conn.rollback()
        raise Exception("Error Deleting Pokemon")
def updatePokemon(conn,pokemonID,pokemonName):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Pokemon SET PokemonName = \""+ pokemonName + "\" WHERE PokemonID = \""+ pokemonID + "\"")
        conn.commit()
    except:
        conn.rollback()
        raise Exception("Error Updating Pokemon")
def dropIndex(conn, index):
    """ drop an index from the create_table_sql statement
    :param conn: Connection object returned from create_connection
    :param index: a DROP INDEX statement as a string
    :return:
    """
    c = conn.cursor()
    try:
        c.execute("DROP INDEX " + index + " ON Pokemon")
        conn.commit()
    except:
        conn.rollback()
        raise Exception("Error Dropping Index", index)
def dropView(conn, view):
    """ drop a view from the create_table_sql statement
    :param conn: Connection object returned from create_connection
    :param view: a DROP VIEW statement as a string
    :return:
    """
    c = conn.cursor()
    try:
        c.execute("DROP VIEW " + view)
        conn.commit()
    except:
        conn.rollback()
        raise Exception("Error Dropping View", view)
def dropTable(conn, table):
    """ drop a table from the create_table_sql statement
    :param conn: Connection object returned from create_connection
    :param table: a DROP TABLE statement as a string
    :return:
    """
    c = conn.cursor()
    try:
        c.execute("DROP TABLE " + table)
        conn.commit()
    except:
        conn.rollback()
        raise Exception("Error Dropping Table", table)
def deleteTables():
    conn = createConnection()
    dropTable(conn, "TypeChart")
    print("Dropped TypeChart")
    dropTable(conn, "Pokemon")
    print("Dropped Pokemon")

    dropView(conn, "Pkmn")
    print("Dropped Pkmn")
    dropIndex(conn, "PokemonIDIndex")
    print("Dropped PokemonIDIndex")
    dropTable(conn, "Type")
    print("Dropped Type")
    dropTable(conn, "Game")
    print("Dropped Game")
    dropTable(conn, "Generation")
    print("Dropped Generation")
def queryPokemon(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Pokemon")
    rows = cur.fetchall()
    return rows
def checkTables():
    conn = createConnection()
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    rows = cur.fetchall()
    return rows != []
def getTypeID(conn, typeName):
    cur = conn.cursor()
    sql = "SELECT TypeID FROM Type WHERE TypeName = \""+ typeName + "\""
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        return row[0]
def queryPokemonUsingGeneration(conn, generationID):
    cur = conn.cursor()
    sql = """SELECT Pokemon.PokemonID, Pokemon.PokemonName, t1.TypeName, t2.TypeName, Pokemon.Height, Pokemon.Weight, Pokemon.GenerationID
                FROM Pokemon INNER JOIN Generation on Pokemon.GenerationID = Generation.GenerationID
                INNER JOIN Type as t1 on Pokemon.Type1ID = t1.TypeID
                LEFT OUTER JOIN Type as t2 on Pokemon.Type2ID = t2.TypeID
                WHERE Pokemon.GenerationID = \""+ %s + "\""""
    cur.execute(sql, generationID)
    rows = cur.fetchall()
    return rows
#Inbetween two heights and weights
def queryPokemonUsingHeightWeight(conn, heightWeight):
    cur = conn.cursor()
    sql = """SELECT Pokemon.PokemonID, Pokemon.PokemonName, t1.TypeName, t2.TypeName, Pokemon.Height, Pokemon.Weight, Pokemon.GenerationID
                FROM Pokemon
                INNER JOIN Type as t1 on Pokemon.Type1ID = t1.TypeID
                LEFT OUTER JOIN Type as t2 on Pokemon.Type2ID = t2.TypeID 
                WHERE Pokemon.Height BETWEEN \""+ %s + "\" AND \""+ %s + "\" AND Pokemon.Weight BETWEEN \""+ %s + "\" AND \""+ %s + "\""""
    cur.execute(sql, heightWeight)
    rows = cur.fetchall()
    return rows
def queryPokemonUsingType(conn, TypeID):
    cur = conn.cursor()
    sql = """SELECT Pokemon.PokemonID, Pokemon.PokemonName, t1.TypeName, t2.TypeName, Pokemon.Height, Pokemon.Weight, Pokemon.GenerationID
                FROM Pokemon
                INNER JOIN Type as t1 on Pokemon.Type1ID = t1.TypeID
                LEFT OUTER JOIN Type as t2 on Pokemon.Type2ID = t2.TypeID 
                WHERE Pokemon.Type1ID = \""+ %s + "\" OR Pokemon.Type2ID = \""+ %s + "\""""
    cur.execute(sql, TypeID)
    rows = cur.fetchall()
    return rows
def queryPokemonUsingGame(conn, GameID):
    cur = conn.cursor()
    sql = """SELECT Pokemon.PokemonID, Pokemon.PokemonName, t1.TypeName, t2.TypeName, Pokemon.Height, Pokemon.Weight, Game.GameName
                FROM Pokemon
                INNER JOIN Generation on Pokemon.GenerationID = Generation.GenerationID 
                INNER JOIN Game on Game.GenerationID = Generation.GenerationID 
                INNER JOIN Type as t1 on Pokemon.Type1ID = t1.TypeID 
                LEFT OUTER JOIN Type as t2 on Pokemon.Type2ID = t2.TypeID 
                WHERE Game.GameID = \""+ %s + "\""""
    cur.execute(sql, GameID)
    rows = cur.fetchall()
    return rows
#Takes in Three parameters Generation ID, Type ID, and Type ID (last 2 should be identical)
def queryPokemonUsingGenerationAndType(conn, GenerationAndTypeID):
    cur = conn.cursor()
    sql = """SELECT Pokemon.PokemonID, Pokemon.PokemonName, t1.TypeName, t2.TypeName, Pokemon.Height, Pokemon.Weight, Pokemon.GenerationID
                FROM Pokemon
                INNER JOIN Generation on Pokemon.GenerationID = Generation.GenerationID 
                INNER JOIN Type as t1 on Pokemon.Type1ID = t1.TypeID 
                LEFT OUTER JOIN Type as t2 on Pokemon.Type2ID = t2.TypeID 
                WHERE Pokemon.GenerationID = \""+ %s + "\"
                AND (Pokemon.Type1ID = \""+ %s + "\" OR Pokemon.Type2ID = \""+ %s + "\")"""
    cur.execute(sql, GenerationAndTypeID)
    rows = cur.fetchall()
    return rows
def queryPokemonUsingGenerationAndBetweenHeightAndWeight(conn, GenerationAndHeightWeight):
    cur = conn.cursor()
    sql = """SELECT Pokemon.PokemonID, Pokemon.PokemonName, t1.TypeName, t2.TypeName, Pokemon.Height, Pokemon.Weight, Pokemon.GenerationID
                FROM Pokemon
                INNER JOIN Generation on Pokemon.GenerationID = Generation.GenerationID 
                INNER JOIN Type as t1 on Pokemon.Type1ID = t1.TypeID 
                LEFT OUTER JOIN Type as t2 on Pokemon.Type2ID = t2.TypeID 
                WHERE Pokemon.GenerationID = \""+ %s + "\"
                AND Pokemon.Height BETWEEN \""+ %s + "\" AND \""+ %s + "\"
                AND Pokemon.Weight BETWEEN \""+ %s + "\" AND \""+ %s + "\""""
    cur.execute(sql, GenerationAndHeightWeight)
    rows = cur.fetchall()
    return rows
def queryPokemonUsingTypeAndBetweenHeightAndWeight(conn, TypeAndHeightWeight):
    cur = conn.cursor()
    sql = """SELECT Pokemon.PokemonID, Pokemon.PokemonName, t1.TypeName, t2.TypeName, Pokemon.Height, Pokemon.Weight, Pokemon.GenerationID
                FROM Pokemon
                INNER JOIN Generation on Pokemon.GenerationID = Generation.GenerationID 
                INNER JOIN Type as t1 on Pokemon.Type1ID = t1.TypeID 
                LEFT OUTER JOIN Type as t2 on Pokemon.Type2ID = t2.TypeID 
                WHERE (Pokemon.Type1ID = \""+ %s + "\" OR Pokemon.Type2ID = \""+ %s + "\")
                AND Pokemon.Height BETWEEN \""+ %s + "\" AND \""+ %s + "\"
                AND Pokemon.Weight BETWEEN \""+ %s + "\" AND \""+ %s + "\""""
    cur.execute(sql, TypeAndHeightWeight)
    rows = cur.fetchall()
    return rows
#Takes in 7 Parameters in the tuple GenerationID TypeID TypeID Height1 Height2 Weight1 Weight2
def queryPokemonUsingGenerationAndTypeAndBetweenHeightAndWeight(conn, inputData):
    cur = conn.cursor()
    sql = """SELECT Pokemon.PokemonID, Pokemon.PokemonName, t1.TypeName, t2.TypeName, Pokemon.Height, Pokemon.Weight,   Pokemon.GenerationID
                FROM Pokemon
                INNER JOIN Generation on Pokemon.GenerationID = Generation.GenerationID
                INNER JOIN Type as t1 on Pokemon.Type1ID = t1.TypeID
                LEFT OUTER JOIN Type as t2 on Pokemon.Type2ID = t2.TypeID
                WHERE Pokemon.GenerationID = \""+ %s + "\"
                AND (Pokemon.Type1ID = \""+ %s + "\" OR Pokemon.Type2ID = \""+ %s + "\")
                AND Pokemon.Height BETWEEN \""+ %s + "\" AND \""+ %s + "\" AND Pokemon.Weight BETWEEN \""+ %s + "\" AND \""+ %s + "\""""
    cur.execute(sql,inputData)
    rows = cur.fetchall()
    return rows
#Takes in a tuple of 1 inputs TypeID
#Takes in a TypeID and returns all the types who are strong against to that type or have a TypeChart.Effectiveness of 2
def queryTypesUsingTypeWeakness(conn, TypeID):
    cur = conn.cursor()
    sql = """SELECT Type.TypeName
                FROM Type
                INNER JOIN TypeChart on Type.TypeID = TypeChart.Type1ID
                WHERE TypeChart.Type2ID = \""+ %s + "\" AND TypeChart.Effectiveness = 2"""
    cur.execute(sql, TypeID)
    rows = cur.fetchall()
    return rows
#Takes in a tuple of 2 inputs TypeID and TypeID
#Returns all the pokemon who are weak to the type using a subquery
def queryPokemonUsingTypeWeakness(conn, TypeID):
    cur = conn.cursor()
    sql = """SELECT Pokemon.PokemonID, Pokemon.PokemonName, t1.TypeName, t2.TypeName, Pokemon.Height, Pokemon.Weight
                FROM Pokemon
                INNER JOIN Type as t1 on Pokemon.Type1ID = t1.TypeID
                LEFT OUTER JOIN Type as t2 on Pokemon.Type2ID = t2.TypeID
                WHERE Pokemon.Type1ID IN (SELECT Type.TypeID
                                            FROM Type
                                            INNER JOIN TypeChart on Type.TypeID = TypeChart.Type1ID
                                            WHERE TypeChart.Type2ID = \""+ %s + "\" AND TypeChart.Effectiveness = 2)
                OR Pokemon.Type2ID IN (SELECT Type.TypeID
                                        FROM Type
                                        INNER JOIN TypeChart on Type.TypeID = TypeChart.Type1ID
                                        WHERE TypeChart.Type2ID = \""+ %s + "\" AND TypeChart.Effectiveness = 2)"""
    cur.execute(sql, TypeID)
    rows = cur.fetchall()
    return rows
def getMostPopularTypeCombo(conn):
    cur = conn.cursor()
    sql = """SELECT t1.TypeName, t2.TypeName, COUNT(PokemonID) AS PokemonCount
                FROM Pokemon
                INNER JOIN Type as t1 on Pokemon.Type1ID = t1.TypeID
                LEFT OUTER JOIN Type as t2 on Pokemon.Type2ID = t2.TypeID
                GROUP BY Type1ID, Type2ID
                ORDER BY PokemonCount DESC
                LIMIT 1"""
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

#Uses a view to get the types
def getTotalPokemon(conn):
    cur = conn.cursor()
    sql = """SELECT COUNT(DISTINCT PokemonID) FROM Pkmn"""
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        return row[0]
def createTables():
    #Create Generation Table String
    sql_create_generation_table = """ CREATE TABLE IF NOT EXISTS Generation (
                                        GenerationID INTEGER NOT NULL PRIMARY KEY
                                    ); """
    #Create Pokemon Table String
    sql_create_pokemon_table = """ CREATE TABLE IF NOT EXISTS Pokemon (
                                        PokemonID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
                                        PokemonName varchar(255) NOT NULL,
                                        Type1ID INTEGER NOT NULL,
                                        Type2ID INTEGER,
                                        Height FLOAT,
                                        Weight FLOAT,
                                        GenerationID INTEGER NOT NULL,
                                        FOREIGN KEY (GenerationID) REFERENCES Generation(GenerationID),
                                        FOREIGN KEY (Type1ID) REFERENCES Type(TypeID),
                                        FOREIGN KEY (Type2ID) REFERENCES Type(TypeID)
                                    ); """
    #Create Region Table String
    sql_create_game_table = """ CREATE TABLE IF NOT EXISTS Game (
                                        GameID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
                                        GameName varchar(255) NOT NULL,
                                        GenerationID INTEGER NOT NULL,
                                        FOREIGN KEY (GenerationID) REFERENCES Generation(GenerationID)
                                    ); """
    #Create Type Table String
    sql_create_type_table = """ CREATE TABLE IF NOT EXISTS Type (
                                        TypeID INTEGER PRIMARY KEY AUTO_INCREMENT,
	                                    TypeName varchar(255) NOT NULL
                                    ); """
    #Create TypeChart Table String
    sql_create_typechart_table = """ CREATE TABLE IF NOT EXISTS TypeChart (
                                        Type1ID INTEGER,
                                        Type2ID INTEGER,
                                        Effectiveness FLOAT NOT NULL,
                                        PRIMARY KEY (Type1ID,Type2ID),
                                        FOREIGN KEY (Type1ID) REFERENCES Type(TypeID),
                                        FOREIGN KEY (Type2ID) REFERENCES Type(TypeID)
                                    ); """
    # create connection to our sqlite db file 
    print("Setup Connection")
    conn = createInitialConnection()
    # create tables
    if conn is not None:
        conn.cursor().execute("USE PokemonDB;")
        # create projects table
        create_table(conn, sql_create_generation_table)
        create_table(conn, sql_create_type_table)
        create_table(conn, sql_create_pokemon_table)
        create_table(conn, sql_create_game_table)
        create_table(conn, sql_create_typechart_table)
        print("Created Tables")
    else:
        print("Error! cannot create the database connection.")
    conn.close()
def initializedTables():
    createTables()
    conn = createConnection()
    #Add Generations to Database 1-8
    for i in range(1,9):
        addGeneration(conn, (i,))
    # Add Games to Database from Yaml
    gameData = df.getGames()
    for game in gameData:
        addGame(conn, (game['name'],game['gen']))
    # Add Types/TypeChart to Database from Yaml
    typeData, typeChartData = df.getTypeData()
    for type in typeData:
        addType(conn, (type,))
    for typeChart in typeChartData:
        #Add Weaknesses to Database
        for weakness in typeChart['Weaknesses']:
            addTypeChart(conn, (getTypeID(conn,weakness),getTypeID(conn,typeChart['Type']),2))
        #Add Resistances to Database
        for resistance in typeChart['Resistances']:
            addTypeChart(conn, (getTypeID(conn,resistance),getTypeID(conn,typeChart['Type']),0.5))
        #Add Immunities to Database
        for immunity in typeChart['Immunities']:
            addTypeChart(conn, (getTypeID(conn,immunity),getTypeID(conn,typeChart['Type']),0))
    #Add Pokemon to Database from Yaml
    pokemonData = df.getPokemonData()
    for pokemon in pokemonData:
        if(pokemon['Type2'] == None):
            addPokemon(conn, (pokemon['Name'], getTypeID(conn, pokemon['Type1']), None, pokemon['Height'], pokemon['Weight'], pokemon['Generation']))
        else:
            addPokemon(conn, (pokemon['Name'], getTypeID(conn, pokemon['Type1']), getTypeID(conn, pokemon['Type2']), pokemon['Height'], pokemon['Weight'], pokemon['Generation']))
    print("Test")
    sql_create_view_pkmn = """ CREATE VIEW Pkmn AS SELECT Pokemon.PokemonName, Pokemon.PokemonID FROM Pokemon INNER JOIN Game ON Pokemon.GenerationID = Game.GenerationID"""
    sql_create_index_pkmn = """ CREATE INDEX PokemonIDIndex ON Pokemon(Type1ID,Type2ID)"""
    print("Created Views")
    createView(conn,sql_create_view_pkmn)
    createIndex(conn,sql_create_index_pkmn)
    print("Initialized Tables")
    conn.close()