import pandas as pd
from googletrans import Translator
import asyncio

async def detection(text):
    async with Translator() as translator:
        result = await translator.translate(text)
        return result.src

async def translate_text(text):
    async with Translator() as translator:
        result = await translator.translate(text, src='en', dest='hu')
        return result

translator = Translator()

# Ezeket az oszlopokat dolgozzuk fel
oszlopok = [
    'ceginfo',
    'fobb_feladatok',
    'amit_kerunk',
    'elony',
    'amit_kinal',
    'munkahelyi_extra',
    'jelentkezes_modja'
]

df = pd.read_excel("merged_output.xlsx")

for idx, row in df.iterrows():
    lang = 'hu'
    for col in oszlopok:
        val = row.get(col)
        if isinstance(val, str) and val.strip():
            detected = asyncio.run(detection(val))
            lang = detected
            break

    for col in oszlopok:
        val = row.get(col)
        df.at[idx, f"{col}_archiv"] = val  # elmentjük az eredetit

        if isinstance(val, str) and val.strip():
            if lang == 'en':
                try:
                    translated = asyncio.run(translate_text(val))
                    df.at[idx, col] = translated.text
                except Exception as e:
                    df.at[idx, col] = val
            else:
                df.at[idx, col] = val  # már magyar
        else:
            df.at[idx, col] = val  # üres érték marad

df.to_excel("merged_output_forditott.xlsx", index=False)
