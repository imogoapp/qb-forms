from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routes.form_contato import router as form_contato_router
from .routes.form_corretor import router as form_corretor_router
from .routes.form_denuncia import router as form_denuncia_router



app = FastAPI(title="Form QB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(form_contato_router, prefix="/integrations/webhooks", tags=["Form"])
app.include_router(form_corretor_router, prefix="/integrations/webhooks", tags=["Form"])
app.include_router(form_denuncia_router, prefix="/integrations/webhooks", tags=["Form"])