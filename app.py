
import gradio as gr
import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

antwoordmodel = {
    2: "juist", 3: "juist", 4: "onjuist", 5: "juist", 6: "onjuist",
    8: "juist", 9: "onjuist", 10: "juist",
    11: "A", 12: "B", 13: "B", 14: "A", 15: "C", 16: "D", 17: "F", 18: "C", 19: "A",
    20: "D", 21: "D", 22: "E",
    23: "C", 24: "B", 25: "C", 26: "B", 29: "C", 31: "C"
}

def nakijk_toets(upload):
    image = Image.open(upload)
    text = pytesseract.image_to_string(image, lang='nld')
    gevonden = re.findall(r"(\d{1,2})[.:]?\s*([A-Fa-fJjOo])", text)
    goed = 0
    fout = 0
    totaal = 0

    for nummer, antwoord in gevonden:
        nummer = int(nummer)
        antwoord = antwoord.lower()
        if antwoord == 'j':
            antwoord = 'juist'
        elif antwoord == 'o':
            antwoord = 'onjuist'
        else:
            antwoord = antwoord.upper()

        if nummer in antwoordmodel:
            totaal += 1
            if antwoord == antwoordmodel[nummer]:
                goed += 1
            else:
                fout += 1

    return f"Aantal goed: {goed}\nAantal fout: {fout}\nVragen beoordeeld: {totaal}"

demo = gr.Interface(
    fn=nakijk_toets,
    inputs=gr.Image(type="file", label="Upload gescande toets"),
    outputs="text",
    title="Toets Nakijk Tool",
    description="Upload een toets (scan of foto) en zie hoeveel antwoorden goed zijn."
)

demo.launch()
