from fastapi import FastAPI
import uvicorn
from app.exception.exception_handler import ExceptionHandler
from app.router import routers

app = FastAPI()
ExceptionHandler.initiate_exception_handlers(app)

# add routers
for router_module in routers:
    app.include_router(router_module.router, prefix=router_module.prefix)

if __name__ == '__main__':
    uvicorn.run(port=8080, app=app)
