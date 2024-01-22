from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from v1.router import menu_router as router_restaurant

app = FastAPI(
    title="Ylab Homework First"
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

app.include_router(router_restaurant)

# @app.post('/users/{user_id}')
# def change_user_name(user_id: int, new_name: str):
#     current_user = list(filter(lambda user: user.get('id') == user_id, fake_users))[0]
#     current_user['name'] = new_name
#
#     return {'status': 200, 'data': current_user}
