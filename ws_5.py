# main.py
from gemini_api_handler import GeminiAPIHandler
from excel_data_processor import ExcelDataProcessor
import pandas as pd
import json


def main():
    INPUT_EXCEL_FILE1 = 'merged_output_forditott.xlsx'
    INPUT_EXCEL_FILE2 = 'standardizalt_elvarasok_programozo.xlsx'
    OUTPUT_EXCEL_FILE = ''
    OUTPUT_FILE = 'programozo_kodolt.csv'
    MODEL_NAME_TO_USE = 'models/gemini-2.0-flash-thinking-exp'
    MODEL_NAME_TO_USE = 'models/gemini-2.0-flash-thinking-exp-1219'

    REQUIRED_INPUT_COLUMNS1 = {
        'kateg': 'category',
        'data-prof-id': 'id',
        'amit_kerunk': 'description',
        'data-item-name': 'position_name',
        'elvart_technologiak': 'requered_technology'
    }

    REQUIRED_INPUT_COLUMNS2 = {
        'Standardizált Elvárás': 'Standardizált Elvárás',
        'bkateg' : 'Category',
        'alcsoport' : 'alcsoport'
    }

    gemini_handler = GeminiAPIHandler(model_name=MODEL_NAME_TO_USE)
    if gemini_handler.model is None:
        print("A program leáll, mert a Gemini modell nem inicializálható.")
        return

    excel_processor1 = ExcelDataProcessor(INPUT_EXCEL_FILE1, OUTPUT_EXCEL_FILE)
    excel_processor2 = ExcelDataProcessor(INPUT_EXCEL_FILE2, OUTPUT_EXCEL_FILE)

    df_input1 = excel_processor1.read_input_data(REQUIRED_INPUT_COLUMNS1)
    if df_input1 is None:
        print("A program leáll, mert a bemeneti Excel adatok nem olvashatók be.")
        return
    df_input1 = df_input1[df_input1['category'] == 'programozo']
    df_input2 = excel_processor2.read_input_data(REQUIRED_INPUT_COLUMNS2)
    if df_input2 is None:
        print("A program leáll, mert a bemeneti Excel adatok nem olvashatók be. (input2)")
        return

    category_for_gemini = df_input2.to_json(orient='records', indent=2, force_ascii=False)

    CHUNK_SIZE = 25
    START_ROW_INDEX = 0

    print(f"\nKezdődik az Excel sorok feldolgozása {CHUNK_SIZE} soros darabokban.")

    df_gyujt = pd.DataFrame(columns=["id", "technologia", 'attitude', 'alt_ismeret'])
    #for i in range(START_ROW_INDEX, df_input1.shape[0], CHUNK_SIZE):
    #A sikertelen visszatérésket újra ráküldjük
    myChunk = {100: 124, 150: 174, 200: 202}
    for key, value in myChunk.items():
        #end_index = min(i + CHUNK_SIZE, df_input1.shape[0])
        i = key
        end_index = value+1
        current_chunk_df = df_input1.iloc[i:end_index]

        if current_chunk_df.empty:
            print(f"Figyelem: A {i}-{end_index} tartomány üres, kihagyva.")
            continue

        print(f"\n--- Feldolgozás: Sorok {i} - {end_index - 1} ---")

        data_for_gemini_chunk = current_chunk_df.to_json(orient='records', indent=2, force_ascii=False)

        # A PROMPT ÖSSZEÁLLÍTÁSA A KATEGÓRIÁK KÉRÉSÉVEL
        prompt_for_gemini = f"""
        Az előző körben a következő volt a feladatod:
        Előző kör feladatata:
        Adott az alábbi programozo, tehát szoftverfejlesztőkhöz pozícióleírásokat tartalmazó JSON adatstruktúra:
        {data_for_gemini_chunk}
        
        1. Az egyes pozíció elnevezéseket (position_name), pozícióleírásokat (description), 
        elvárt technológiákat (requered_technology) egy információbemenetként kezelve,
         bontsd ki az egyedi elvárásokat gondolatonként.
        2. Csoportosítsd az azonos vagy hasonló jelentésű elvárásokat egyetlen, 
        **standardizált, rövid magyar kifejezés** alá (pl. "angol nyelvtudás", "Excel ismeret", "csapatmunka").
        3. A nyelvtudás, a formális végzettség (pl felsőfokú végzettség), a jogosítvány meglétes 
        és a munkarend (pl részmunkaidő) nem érdekes, ezeket ne vedd figyelembe.
        Eddig az előző kör feladata. Ennek a körnek az inputfile-jét a továbbiakban input1-nek fogjuk hivni.   
        
        A mostani feladatod a következő:
        Az előző körben a fentiek szerint csoportosítottad az elvárásokat amelyet a következő struktúra 
        'Standardizált Elvárás' oszlopa mutat. 
        {category_for_gemini}
        Én ezeket helyenként összevontam a 'Category' oszlopban, továbbá 3 alcsoportra bontottam ('alcsoport' oszlop):
        technologia, személyiség, általásos_ismeret csoportokra. 
        
        A következőt tedd meg:
        
        1. A bemenő adatstruktúrából a  pozíció elnevezéseket (position_name), pozícióleírásokat (description), 
        elvárt technológiákat (requered_technology) egy információbemenetként kezeld, tehát ha van a position_name-ben 
        technológiára utalás akkor az is vedd figyelembe!
        2. a pozicióleirásokat tartalmazó adatstruktúra minden egyes id-jéhez add vissza, hogy melyik 'Category'-ket tudod 
        hozzárendelni, az 'alcsoport' = technologia, alcsoport = személyiség és alcsoport = általános ismeret esetén.  
        3 . Fontos hogy az alcsoportokat is figyeld!  Csak a Category oszlop értékeit használhatod!
        4. Előforsul, hogy a  'Standardizált Elvárás' több 'Category' hez tartozik. Ilyenkor mindegyikhez rendeld hozzá. 
        Pl: Ha olyan van írva, hogy pl HTML és CSS akkor mindkettőhöz kódold! 
        pl: Programozási ismeretek (C++, Java, JavaScript, Visual Basic), menjen a C++, Java, JavaScript , Visual Basic-hez is.
        5. Ha olyan van, hogy pl Java, C# vagy Python, tehát tecnológiák felsorolása, akkor mindegyikhez kódold.  
        6. Ha a category-ban 'kuka' szó van, akkor az az item nem érdekes, ne kódold.
        7. Az eredményt egyetlen JSON objektumként add vissza a következő struktúrában:

        ```json
        {{
          "standardized_expectations": [
            ["id1", [technologia alcsoport esetén category elem 1, technologia alcsoport esetén category elem 2....], 
            [személyiseg alcsoport esetén category elem 1, személyiseg alcsoport esetén category elem 2....], 
            [általános_ismeret alcsoport esetén category elem 1, általános_ismeret alcsoport esetén category elem 2....]],
            ["id2", [technologia alcsoport esetén category elem 1, technologia alcsoport esetén category elem 2....], 
            [személyiseg alcsoport esetén category elem 1, személyiseg alcsoport esetén category elem 2....], 
            [általános_ismeret alcsoport esetén category elem 1, általános_ismeret alcsoport esetén category elem 2....]],
            ["id3", [technologia alcsoport esetén category elem 1, technologia alcsoport esetén category elem 2....], 
            [személyiseg alcsoport esetén category elem 1, személyiseg alcsoport esetén category elem 2....], 
            [általános_ismeret alcsoport esetén category elem 1, általános_ismeret alcsoport esetén category elem 2....]],
            
          ]
        }}
        ```
        . semmi mást nem kérek vissza, csak a fenti json objektumot.
        """

        model_response_text = gemini_handler.send_prompt_to_model(prompt_for_gemini)

        if model_response_text:
            print("\nModell nyers válasza:")
            print(model_response_text)

            result_data = gemini_handler.parse_json_response(model_response_text)

            if result_data and 'standardized_expectations' in result_data:
                df = pd.DataFrame(result_data["standardized_expectations"], columns=["id", "technologia", 'attitude', 'alt_ismeret'])
                df.to_csv(OUTPUT_FILE, index=False)
                df_gyujt = pd.concat([df_gyujt,df])
            else:
                print("A modell válasza nem tartalmazta a 'standardized_expectations' kulcsot, vagy érvénytelen volt.")
        else:
            print(f"Hiba történt a {i}-{end_index - 1} tartomány feldolgozása során, kihagyva.")

    df_gyujt.to_csv(OUTPUT_FILE, index=False)
    print("\n--- Program Vége ---")


if __name__ == '__main__':
    main()