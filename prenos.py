import classla
from pathlib import Path
import re
import json
#vsebuje tudi številko stavka in številko besede v stavku za nadaljnjo analizo
#import csv
classla.download("sl") #samo prvič
nlp = classla.Pipeline("sl", processors="tokenize,lemma,pos")
tekst = Path("text.txt").read_text(encoding="utf-8")
doc = nlp(tekst)
stop_besede = {
    "a", "ali", "ampak", "bi", "bil", "bila", "bile", "bili", "bilo", "biti", "blizu",
    "bo", "bodo", "bom", "bomo", "boste", "bova", "boš", "brez", "če", "cel", "cela",
    "celo", "dan", "danes", "do", "dol", "dva", "ga", "gor", "hoče", "hočem",
    "i", "in", "iz", "ja", "jaz", "je", "ji", "jih", "jim", "jo", "ju", "kaj", "kam",
    "kar", "kateri", "katere", "katerega", "katerem", "katero", "kdaj",
    "kdo", "ker", "ki", "kje", "kjer", "kot", "krog", "lahko", "le", "lep", "malo",
    "manj", "med", "me", "mi", "mnogo", "moj", "moja", "moje", "mu", "na", "nad", 
    "naj", "najbolj", "nam", "nas", "naš", "naša", "naše", "ne", "nek", "neka", "neki",
    "nekaj", "ni", "nikar", "nikoli", "nima", "nimam", "nisem", "niti", "no",
    "ob", "oba", "od", "okoli", "on", "ona", "oni", "ono", "osem", "pa", "po", "pod",
    "pol", "poleg", "polno", "ponovno", "pred", "prej", "pri", "proti", "razen",
    "res", "s", "sam", "sama", "sami", "same", "se", "sedaj", "sem", "smo", "so",
    "spet", "sta", "ste", "stran", "tako", "tam", "te", "tega", "tej", "tem", "težko",
    "ti", "tista", "tiste", "tisti", "tisto", "tja", "to", "toda", "tu", "tudi",
    "tvoj", "tvoja", "tvoje", "u", "v", "vendar", "več", "ves", "vsa", "vse", "vsi",
    "za", "zato", "zelo", "že", "zdaj", "čeprav", "kajti", "kar", "ker", "ko",
    "koli", "lahko", "medtem", "nato", "potem", "ravno", "res", "skoraj", "tako", "tudi"
}
output = []
# === Dodamo sentence_id in token_id ===
for s_id, sentence in enumerate(doc.sentences, start=1):  # <-- številčenje povedi
    for t_id,token in enumerate(sentence.tokens, start=1):
        word = token.text.strip().lower()
        lemma = token.words[0].lemma.lower()
        pos = token.words[0].upos

        if re.match(r"^\W+$", word):  
            continue
        if word in stop_besede or lemma in stop_besede:
            continue

        output.append({
            "sentence_id": s_id,  # številka povedi
            "token_id": t_id,  # številka tokena v povedi
            "beseda": word,
            "lema": lemma,
            "del_govora": pos,
            "tip_teksta": "leposlovje",
            "vir": "Mojca Pokrajculja"
        })
with open("pravljica.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# Alternativno: Shrani v CSV
# with open("besedecl.csv", "w", encoding="utf-8", newline="") as f:
#     writer = csv.DictWriter(f, fieldnames=["beseda", "lema", "del_govora", "tip_teksta", "vir"])
#     writer.writeheader()
#     writer.writerows(output)

print("Obdelava končana. Rezultati shranjeni v besede.json in besede.csv")