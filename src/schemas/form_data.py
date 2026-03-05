from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class FormContatoPayload(BaseModel):
	nome: str
	whatsapp: str = Field(..., alias="whatsApp")
	email: EmailStr
	assunto: str
	resposta: str

	model_config = {
		"validate_by_name": True,
	}

class FormDenunciaPayload(BaseModel):
	deseja_se_identificar: Optional[str] 
	nome: Optional[str] = None
	whatsapp: Optional[str] = None
	email: Optional[EmailStr] = None
	denuncia: str
	

class FormCorretorPayload(BaseModel):
	nome: str
	whatsapp: str = Field(..., alias="whatsApp")
	email: EmailStr
	e_corretor: str

	model_config = {
		"validate_by_name": True,
	}

