from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from agents.coordinator import CoordinatorAgent
from models import Token
from utils.security import authenticate_user, create_access_token, fake_users_db
from utils.logging import get_logger
import pdfplumber
from datetime import timedelta

app = FastAPI(title="Enterprise Agent: Blog Writer Agent", version="1.0.0")
coordinator = CoordinatorAgent()
logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/process-document")
async def process_document(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    # Extract text from PDF
    if file.filename.endswith('.pdf'):
        with pdfplumber.open(file.file) as pdf:
            content = ""
            for page in pdf.pages:
                content += page.extract_text() or ""
    else:
        content = (await file.read()).decode('utf-8')

    result = coordinator.process_document(content, file.filename)
    logger.info(f"Document processed: {file.filename}")
    return result

@app.get("/documents")
async def list_documents(token: str = Depends(oauth2_scheme)):
    docs = coordinator.ingestion.list_documents()
    return {"documents": [doc.dict() for doc in docs]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
