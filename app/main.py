from fastapi import FastAPI

from merchandising.routes import router_batches

app = FastAPI(title="Merchandising app")

app.include_router(router_batches)