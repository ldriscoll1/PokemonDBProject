#Imports Pokemon Database from pokemonDatabase.py
import pokemonDatabase as pkmn
#Uses streamlit as front end
import streamlit as st
import pandas as pd
# def reset():
#     pkmn.deleteTables()
#     print("Done Resetting")
def setup():
    pkmn.initializedTables()
def main():
    try:
        st.title("Pokemon Database")
        #If the tables exist, setup only run once
        if(not pkmn.checkTables()):
            print("Tables don't exist")
            setup()
        with st.sidebar:
            conn = pkmn.createConnection()
            st.write("Admin Menu")
            st.write("Total Pokemon: ",pkmn.getTotalPokemon(conn))
            mostPopular = pkmn.getMostPopularTypeCombo(conn)
            st.write("The most popular type combo is",mostPopular[0][0],"and",str(mostPopular[0][1]),"with",str(mostPopular[0][2]),"pokemon")
            # if(st.button("Reset Database")):
            #     reset()
            #     st.experimental_rerun()
            #Add Input for pokemon
            with st.expander("Add a Pokemon"):
                with st.form("Create Pokemon Form"):
                    pokemonName = st.text_input("Pokemon Name",placeholder="Bulbasaur")
                    type1 = st.text_input("Pokemon Type 1",placeholder="Normal")
                    type2 = st.text_input("Pokemon Type 2",placeholder="Flying/None")
                    height = st.number_input("Height",step=0.1)
                    weight = st.number_input("Weight",step=0.1)
                    generationID = st.number_input("Generation",step=1,min_value=1,max_value=8)
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        conn = pkmn.createConnection()
                        #Make sure types are correct
                        if(type2 != ""):
                            if(pkmn.getTypeID(conn,type1) != None and pkmn.getTypeID(conn,type2) != None):
                                pkmn.addPokemon(conn, (pokemonName,pkmn.getTypeID(conn,type1),pkmn.getTypeID(conn,type2),str(height),str(weight),str(generationID)))
                                print("Pokemon Added")
                            else:
                                print("Incorrect Type Inputted")
                        else:
                            if(pkmn.getTypeID(conn,type1) != None):
                                pkmn.addPokemon(conn, (pokemonName,pkmn.getTypeID(conn,type1),None,str(height),str(weight),str(generationID)))
                                print("Pokemon Added")
                            else:
                                print("Incorrect Type Inputted")
                        conn.close()
                        st.experimental_rerun()
            #Form to update pokemon
            with st.expander("Update a Pokemon"):
                with st.form("Update Pokemon Form"):
                    pokemonID = st.number_input("Pokemon ID",step=1)
                    pokemonName = st.text_input("New Pokemon Name",placeholder="Bulbasaur")
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        #Make sure types are correct
                        pkmn.updatePokemon(conn, str(pokemonID), str(pokemonName))
                        conn.close()
                        st.experimental_rerun()
            with st.expander("Delete Pokemon"):
                with st.form("Delete Pokemon Form"):
                    pokemonID = st.number_input("Pokemon ID",step=1)
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        conn = pkmn.createConnection()
                        #Make sure types are correct
                        pkmn.deletePokemon(conn, str(pokemonID))
                        conn.close()
                        st.experimental_rerun()
            #Setup Button
            if(st.button("Setup Database")):
                setup()
        #Get the pokemon data and display it as a table
        conn = pkmn.createConnection()
        #Button that shows all pokemon of a genration according to a slider from 1-8
        pokemon = None
        df = None
        generation = st.slider("Generation",1,8)
        type = st.selectbox("Type",["Normal","Fire","Water","Electric","Grass","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"])
        minHeight = st.number_input("Min Height",step=0.1)
        maxheight = st.number_input("Max Height",step=0.1)
        minWeight = st.number_input("Min Weight",step=0.1)
        maxWeight = st.number_input("Max Weight",step=0.1)
        attributeSelection = st.multiselect("Attribute Selection",["Generation","Type","Height&Weight"])        
        if(st.button("Show Pokemon by Attributes")):
            #Go through every option for the attributes and search according to the options
            if(len(attributeSelection) == 0):
                pokemon = (pkmn.queryPokemon(conn))
                df = pd.DataFrame(pokemon,columns=["ID","Name","Type1","Type2","Height","Weight","Generation"])
            elif(len(attributeSelection) == 1):
                if(attributeSelection[0] == "Generation"):
                    pokemon = (pkmn.queryPokemonUsingGeneration(conn,(str(generation),)))
                    df = pd.DataFrame(pokemon,columns=["ID","Name","Type1","Type2","Height","Weight","Generation"])
                elif(attributeSelection[0] == "Type"):
                    pokemon = (pkmn.queryPokemonUsingType(conn,(pkmn.getTypeID(conn,type),pkmn.getTypeID(conn,type))))
                    df = pd.DataFrame(pokemon,columns=["ID","Name","Type1","Type2","Height","Weight","Generation"])
                elif(attributeSelection[0] == "Height&Weight"):
                    pokemon = (pkmn.queryPokemonUsingHeightWeight(conn,(str(minHeight),str(maxheight),str(minWeight),str(maxWeight))))
                    df = pd.DataFrame(pokemon,columns=["ID","Name","Type1","Type2","Height","Weight","Generation"])
            elif(len(attributeSelection) == 2):
                if("Generation" in attributeSelection and "Type" in attributeSelection):
                    pokemon = (pkmn.queryPokemonUsingGenerationAndType(conn,(str(generation),pkmn.getTypeID(conn,type),pkmn.getTypeID(conn,type))))
                    df = pd.DataFrame(pokemon,columns=["ID","Name","Type1","Type2","Height","Weight","Generation"])
                elif("Generation" in attributeSelection and "Height&Weight" in attributeSelection):
                    pokemon = (pkmn.queryPokemonUsingGenerationAndBetweenHeightAndWeight(conn,(str(generation),str(minHeight),str(maxheight),str(minWeight),str(maxWeight))))
                    df = pd.DataFrame(pokemon,columns=["ID","Name","Type1","Type2","Height","Weight","Generation"])
                elif("Type" in attributeSelection and "Height&Weight" in attributeSelection):
                    pokemon = (pkmn.queryPokemonUsingTypeAndBetweenHeightAndWeight(conn,(pkmn.getTypeID(conn,type),pkmn.getTypeID(conn,type),str(minHeight),str(maxheight),str(minWeight),str(maxWeight))))
                    df = pd.DataFrame(pokemon,columns=["ID","Name","Type1","Type2","Height","Weight","Generation"])
            elif(len(attributeSelection) == 3):
                pokemon = (pkmn.queryPokemonUsingGenerationAndTypeAndBetweenHeightAndWeight(conn,(str(generation),pkmn.getTypeID(conn,type),pkmn.getTypeID(conn,type),str(minHeight),str(maxheight),str(minWeight),str(maxWeight))))
                df = pd.DataFrame(pokemon,columns=["ID","Name","Type1","Type2","Height","Weight","Generation"])
        with st.expander("Show the Types Strong to Chosen Type"):
            with st.form("Type Choose"):
                type = st.selectbox("Type",["Normal","Fire","Water","Electric","Grass","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"])
                submitted = st.form_submit_button("Submit")
                if submitted:
                    pokemon = (pkmn.queryTypesUsingTypeWeakness(conn,(pkmn.getTypeID(conn,type),)))
                    df = pd.DataFrame(pokemon,columns=["Type"])
        with st.expander("Show the Pokemon Strong to Chosen Type"):
            with st.form("Type"):
                type = st.selectbox("Type",["Normal","Fire","Water","Electric","Grass","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"])
                submitted = st.form_submit_button("Submit")
                if submitted:
                    pokemon = (pkmn.queryPokemonUsingTypeWeakness(conn,(pkmn.getTypeID(conn,type),pkmn.getTypeID(conn,type))))
                    df = pd.DataFrame(pokemon,columns=["ID","Name","Type1","Type2","Height","Weight"])

        #Display pokemon with a table using column names of "Name","Type1","Type2","Height","Weight" and "Generation" for the table
        if(pokemon != None):
            st.table(df)
        conn.close()
    except Exception as e:
        #Use error from streamlit
        st.error(e)
        #Print error to console
        print(e)
if __name__ == '__main__':
    main()