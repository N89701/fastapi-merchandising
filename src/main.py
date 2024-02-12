from fastapi import FastAPI

from .routes import router_batches, router_products

app = FastAPI(title="Merchandising app")

app.include_router(router_batches)
app.include_router(router_products)