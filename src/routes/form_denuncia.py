from fastapi import APIRouter, HTTPException
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from ..schemas.form_data import FormDenunciaPayload

router = APIRouter()

# https://docs.google.com/forms/d/e/1FAIpQLSeahIJ54BbTfKykhC25sBNGrLkRdAP80EQuRaCj8QAqujeUew/viewform?usp=pp_url&entry.222465769=N%C3%A3o&entry.1072542137=Nome&entry.1089016849=WhatsApp&entry.1086672395=E-mail&entry.1694858879=Den%C3%BAncia

@router.post("/form-denuncia")
def submit_form_denuncia(payload: FormDenunciaPayload):
	print("[form-denuncia] payload=", payload.model_dump())
	form_response_url = (
		"https://docs.google.com/forms/d/e/1FAIpQLSeahIJ54BbTfKykhC25sBNGrLkRdAP80EQuRaCj8QAqujeUew/formResponse"
	)
    

	if not form_response_url or "FORM_ID" in form_response_url:
		raise HTTPException(
			status_code=500,
			detail="Configure o URL do Google Forms em form_denuncia.py",
		)
        

	identify_raw = (payload.deseja_se_identificar or "").strip().lower()
	identify_yes = identify_raw in {"sim", "true", "1", "yes"}
	identify_no = identify_raw in {"nao", "não", "false", "0", "no"}
    
	

	identify_label = identify_raw or ""
	if identify_yes:
		identify_label = "sim"
	elif identify_no:
		identify_label = "não"

	# entry.222465769=N%C3%A3o&entry.1072542137=Nome&entry.1089016849=WhatsApp&entry.1086672395=E-mail&entry.1694858879=Den%C3%BAncia
	data = {
		"entry.222465769": identify_label,
		"entry.1072542137": payload.nome or "",
		"entry.1089016849": payload.whatsapp or "",
		"entry.1086672395": payload.email or "",
		"entry.1694858879": payload.denuncia,
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