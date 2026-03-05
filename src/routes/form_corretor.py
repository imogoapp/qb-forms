from fastapi import APIRouter, HTTPException
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from ..schemas.form_data import FormCorretorPayload

router = APIRouter()

@router.post("/form-corretor")
def submit_form_corretor(payload: FormCorretorPayload):
	form_response_url = (
		"https://docs.google.com/forms/d/e/1FAIpQLSePnY4VyNO-ys5ljlBDSbsL4pBYX7aywkSQtiVJYAvWVLYoNQ/formResponse"
	)

	if not form_response_url or "FORM_ID" in form_response_url:
		raise HTTPException(
			status_code=500,
			detail="Configure o URL do Google Forms em form_corretor.py",
		)

	value_raw = (payload.e_corretor or "").strip().lower()
	if "definitivo" in value_raw:
		value_label = "Sim, corretor definitivo"
	elif "estagiario" in value_raw or "estagiário" in value_raw:
		value_label = "Sim, corretor estagiário"
	elif value_raw in {"nao", "não", "no"}:
		value_label = "Não"
	else:
		value_label = payload.e_corretor

	data = {
		"entry.1719146357": payload.nome,
		"entry.478212052": payload.whatsapp,
		"entry.860376950": payload.email,
		"entry.365545390": value_label,
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
