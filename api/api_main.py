from dotenv import load_dotenv

load_dotenv()
import fastapi_cdn_host
from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from web.database.user import User
from web.database.knowledge import Knowledge
from web.tools.knowledge import get_all_entity_knowledge, load_knowledge_from_xml, get_entity_attribute_knowledge
from web.tools.knowledge import get_entity_relation_knowledge
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
import jwt

app = FastAPI()
fastapi_cdn_host.patch_docs(app)

SECRET_KEY = "fa083bn-2bn-2joggle4jgw"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360


# 验证用户是否有效
def authenticate_user(email: str, password: str):
    user = User.get_user_by_email(email)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


# 生成访问令牌
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = User.get_user_by_email(username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


class User_M(BaseModel):
    username: str
    email: str


@app.get("/knowledge/entities", response_model=List[str])
async def get_all_entities(knowledge_name: str,
                           current_user: User_M = Depends(get_current_user)):
    username = current_user.username
    knowledge = Knowledge.get_knowledge_by_owner_with_name_api(username, knowledge_name)
    if knowledge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge {} Is Not Exists!".format(knowledge_name),
            headers={"WWW-Authenticate": "Bearer"},
        )
    graph = load_knowledge_from_xml(knowledge.rdf_xml_online)
    return get_all_entity_knowledge(graph)


@app.get("/knowledge/attributes", response_model=List[dict])
async def get_all_attributes(knowledge_name: str,
                             entity: str,
                             current_user: User_M = Depends(get_current_user)):
    username = current_user.username
    knowledge = Knowledge.get_knowledge_by_owner_with_name_api(username, knowledge_name)
    if knowledge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge {} Not Found!".format(knowledge_name),
            headers={"WWW-Authenticate": "Bearer"},
        )
    graph = load_knowledge_from_xml(knowledge.rdf_xml_online)
    if entity not in get_all_entity_knowledge(graph):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity {} Not Found!".format(entity),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return get_entity_attribute_knowledge(graph, entity)


@app.get("/knowledge/relations", response_model=List[dict])
async def get_all_relations(knowledge_name: str,
                            entity: str,
                            current_user: User_M = Depends(get_current_user)):
    username = current_user.username
    knowledge = Knowledge.get_knowledge_by_owner_with_name_api(username, knowledge_name)
    if knowledge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge {} Not Found!".format(knowledge_name),
            headers={"WWW-Authenticate": "Bearer"},
        )
    graph = load_knowledge_from_xml(knowledge.rdf_xml_online)
    if entity not in get_all_entity_knowledge(graph):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity {} Not Found!".format(entity),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return get_entity_relation_knowledge(graph, entity)
