"""CASO 3 - "Quebre de propósito": testa as proteções do link assinado.

Uso: python clientes/caso3_quebra.py expira|assinatura|confirmar
  expira     -> gera link de 10 s, espera 15 s e tenta o PUT (espera-se 403 Request has expired)
  assinatura -> altera um caractere do X-Amz-Signature (espera-se 403 SignatureDoesNotMatch)
  confirmar  -> confirma um id cujo PUT nunca foi feito (espera-se 409)
"""
import os
import sys
import time

import requests

API = os.getenv("API_URL", "http://localhost:8000")
def link(exp):
    return requests.post(f"{API}/caso3/gerar-link", json={"nome": "quebra.txt", "content_type": "text/plain", "expira_em_segundos": exp}).json()
dados = open("arquivos-teste/exemplo.txt", "rb").read()
h = {"Content-Type": "text/plain"}
modo = sys.argv[1] if len(sys.argv) > 1 else "expira"
if modo == "expira":
    l = link(10); print(f"Link gerado (id {l['id']}) com expira_em_segundos=10. Esperando 15 s...")
    time.sleep(15)
    r = requests.put(l["url_upload"], data=dados, headers=h); print(f"PUT apos 15 s -> HTTP {r.status_code}\n{r.text}")
elif modo == "assinatura":
    l = link(300); url = l["url_upload"]; i = url.index("X-Amz-Signature=") + len("X-Amz-Signature=")
    orig = url[i]; novo = "0" if orig != "0" else "1"; url2 = url[:i] + novo + url[i+1:]
    print(f"Link gerado (id {l['id']}). Trocando o 1o caractere da assinatura: '{orig}' -> '{novo}'")
    print("  ...X-Amz-Signature=" + url2[i:i+16] + "...")
    r = requests.put(url2, data=dados, headers=h); print(f"PUT com assinatura alterada -> HTTP {r.status_code}\n{r.text}")
elif modo == "confirmar":
    l = link(300); print(f"Link gerado (id {l['id']}), mas o PUT NUNCA foi feito.")
    r = requests.post(f"{API}/caso3/confirmar/{l['id']}"); print(f"POST /caso3/confirmar/{l['id']} -> HTTP {r.status_code} {r.json()}")
