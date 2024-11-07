from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from accounts.routes import accounts_router
from departments.routes import departments_router
from auth.routes import router as auth_router
from transactions.routes import categories_router
from transactions.routes import transactions_router
from transactions.routes import types_router
from people.routes import people_router

# Это список разрешённых адресов сайтов для CORS, которые могут делать запросы
# к нашему API. Запросы с адресов не указанных в origins будут отклонены. 
origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
    "http://*"
]

app = FastAPI(title='MPapp')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(types_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(departments_router)
app.include_router(people_router)


@app.get("/")
async def read_root():
    return {'Hello': 'Kate'}
