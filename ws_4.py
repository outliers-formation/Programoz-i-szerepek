# main.py
from gemini_api_handler import GeminiAPIHandler
from excel_data_processor import ExcelDataProcessor
import pandas as pd
import json


def main():
    INPUT_EXCEL_FILE = 'merged_output_forditott.xlsx'
    OUTPUT_EXCEL_FILE = 'standardizalt_elvarasok_programozo.xlsx'
    MODEL_NAME_TO_USE = 'models/gemini-2.0-flash-thinking-exp-1219'

    REQUIRED_INPUT_COLUMNS = {
        'kateg': 'category',
        'data-prof-id': 'id',
        'amit_kerunk': 'description',
        'data-item-name': 'position_name',
        'elvart_technologiak': 'requered_technology'
    }

    gemini_handler = GeminiAPIHandler(model_name=MODEL_NAME_TO_USE)
    if gemini_handler.model is None:
        print("A program leáll, mert a Gemini modell nem inicializálható.")
        return

    excel_processor = ExcelDataProcessor(INPUT_EXCEL_FILE, OUTPUT_EXCEL_FILE)

    df_input = excel_processor.read_input_data(REQUIRED_INPUT_COLUMNS)
    if df_input is None:
        print("A program leáll, mert a bemeneti Excel adatok nem olvashatók be.")
        return
    df_input = df_input[df_input['category'] == 'programozo' ]
    CHUNK_SIZE = 30
    START_ROW_INDEX = 0

    print(f"\nKezdődik az Excel sorok feldolgozása {CHUNK_SIZE} soros darabokban.")

    for i in range(START_ROW_INDEX, df_input.shape[0], CHUNK_SIZE):
        end_index = min(i + CHUNK_SIZE, df_input.shape[0])
        current_chunk_df = df_input.iloc[i:end_index]

        if current_chunk_df.empty:
            print(f"Figyelem: A {i}-{end_index} tartomány üres, kihagyva.")
            continue

        print(f"\n--- Feldolgozás: Sorok {i} - {end_index - 1} ---")

        data_for_gemini_chunk = current_chunk_df.to_json(orient='records', indent=2, force_ascii=False)

        prompt_for_gemini = f"""
        Adott az alábbi programozo, tehát szoftverfejlesztőkhöz pozícióleírásokat tartalmazó JSON adatstruktúra:
        {data_for_gemini_chunk}

        A feladatod a következő:
        1. Az egyes pozíció elnevezéseket (position_name), pozícióleírásokat (description), 
        elvárt technológiákat (requered_technology) egy információbemenetként kezelve,
         bontsd ki az egyedi elvárásokat gondolatonként.
        2. Csoportosítsd az azonos vagy hasonló jelentésű elvárásokat egyetlen, 
        **standardizált, rövid magyar kifejezés** alá (pl. "angol nyelvtudás", "Excel ismeret", "csapatmunka").
        3. A nyelvtudás, a formális végzettség (pl felsőfokú végzettség), a jogosítvány meglétes 
        és a munkarend (pl részmunkaidő) nem érdekes, ezeket ne vedd figyelembe.  
        4. Az eredményt egyetlen JSON objektumként add vissza a következő struktúrában:

        ```json
        {{
          "standardized_expectations": [
            "Standardizált elvárás 1 (pl. angol nyelvtudás)",
            "Standardizált elvárás 2 (pl. Excel ismeret)",
            "Standardizált elvárás 3 (pl. csapatmunka)",
          ]
        }}
        ```
        . semmi mást nem kérek vissza, csak a fenti json objektumot.
        """

        model_response_text = gemini_handler.send_prompt_to_model(prompt_for_gemini)
        print(model_response_text)

        if model_response_text:
            print("\nModell nyers válasza:")
            print(model_response_text)

            result_data = gemini_handler.parse_json_response(model_response_text)

            if result_data and 'standardized_expectations' in result_data:
                standardized_expectations_new = result_data['standardized_expectations']
                if standardized_expectations_new:
                    print("\nÚjonnan generált standardizált elvárások (kategóriákkal):")
                    for exp in standardized_expectations_new:
                        print(f"- {exp}")

                    excel_processor.update_and_write_expectations(standardized_expectations_new)
                else:
                    print("A modell válasza érvényes volt, de nem tartalmazott új standardizált elvárásokat.")
            else:
                print("A modell válasza nem tartalmazta a 'standardized_expectations' kulcsot, vagy érvénytelen volt.")
        else:
            print(f"Hiba történt a {i}-{end_index - 1} tartomány feldolgozása során, kihagyva.")

    print("\n--- Program Vége ---")


if __name__ == '__main__':
    main()