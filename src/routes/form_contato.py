from fastapi import APIRouter, HTTPException
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from ..schemas.form_data import FormContatoPayload

router = APIRouter()

# https://docs.google.com/forms/d/e/1FAIpQLScpqy1pp8hg0KEMdDPjjvZuBk4kLl3KyjWH4Vk5VxwkAvroqg/viewform?usp=pp_url&entry.795970238=Nome&entry.1703983023=WhatsApp&entry.1887384981=E-mail&entry.1911889510=Quero+comprar+um+im%C3%B3vel&entry.778562482=Resposta

@router.post("/form-contato")
def submit_form_contato(payload: FormContatoPayload):
	form_response_url = (
		"https://docs.google.com/forms/d/e/1FAIpQLScpqy1pp8hg0KEMdDPjjvZuBk4kLl3KyjWH4Vk5VxwkAvroqg/formResponse"
	)

	if not form_response_url or "FORM_ID" in form_response_url:
		raise HTTPException(
			status_code=500,
			detail="Configure o URL do Google Forms em form_contato.py",
		)


	assunto_key = payload.assunto.strip().lower()
	assunto_map = {
		"comprar": "Quero comprar um imóvel",
		"vender": "Quero vender um imóvel",
		"sugestao": "Quero fazer uma sugestão/reclamação",
		"incorporadora": "Sou uma incorporadora",
		# TODO: completar com as demais opcoes
	}
	assunto_google = assunto_map.get(assunto_key, payload.assunto)

	data = {
		"entry.795970238": payload.nome,
		"entry.1703983023": payload.whatsapp,
		"entry.1887384981": payload.email,
		"entry.1911889510": assunto_google,
		"entry.778562482": payload.resposta,
	}

	encoded = urlencode(data).encode("utf-8")
	request = Request(
		form_response_url,
		data=encoded,
		headers={"Content-Type": "application/x-www-form-urlencoded"},
		method="POST",
	)

	try:
		with urlopen(request, timeout=10) as response:
			if response.status >= 400:
				raise HTTPException(status_code=502, detail="Falha ao enviar")
	except (HTTPError, URLError) as exc:
		raise HTTPException(status_code=502, detail=str(exc)) from exc

	return {"status": "ok"}
