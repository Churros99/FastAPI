from fastapi import FastAPI, HTTPException
from database import database as connection, User
from schemas import UserRequestModel, UserResponseModel

app = FastAPI(title='Live de CF', description='Estamos en una prueba de una API', version='1.0')

@app.on_event('startup')
def startup():
    if(connection.is_closed()):
        connection.connect()
        
    connection.create_tables([User])

def shutdown():
    if(not connection.is_closed()):
        connection.close()

@app.get('/')
async def index():
    return {'Hola Mundo, desde un live en CF.'}

@app.get('/about')
async def about():
    return {'Estamos en el about del servicio Web.'}

@app.post('/users')
async def create_user(user_request: UserRequestModel):
    user = User.create(
        username= user_request.username,
        email= user_request.email
    )
    return user_request

@app.get('/users/{user_id}')
async def get_user(user_id: int):
    user = User.select().where(User.id == user_id).first()
    
    if user:
        return UserResponseModel(id= user.id, 
                                 username= user.username, 
                                 email= user.email
                                )
    else:
        return HTTPException(404,'User not found')

@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    user = User.select().where(User.id == user_id).first()
    
    if user:
        user.delete_instance()
        return True
    else:
        return HTTPException(404,'User not found')
