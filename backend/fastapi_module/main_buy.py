from fastapi import FastAPI, HTTPException
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import aioredis


app = FastAPI()

# 添加 CORS 中间件，允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名的跨域请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# 全局变量存储 Redis 连接
redis: Optional[aioredis.Redis] = None


@app.on_event("startup")
async def startup_event():
    global redis
    # 创建 Redis 连接
    redis = aioredis.from_url("redis://localhost:6379/0", encoding="utf-8", decode_responses=True)


@app.on_event("shutdown")
async def shutdown_event():
    global redis
    if redis:
        await redis.close()


class PurchaseRequest(BaseModel):
    item_id: str  # 商品 ID
    quantity: int = Field(1, gt=0)  # 购买数量，默认值为 1，必须大于 0


@app.post("/buy")
async def buy_item(purchase: PurchaseRequest):
    item_id = purchase.item_id
    quantity = purchase.quantity

    async with redis.client() as conn:
        lock = conn.lock(f"lock:{item_id}", timeout=5)  # 加锁
        try:
            if await lock.acquire(blocking=False):
                stock = await conn.get(f"stock:{item_id}")
                if stock is None:
                    raise HTTPException(status_code=404, detail="Item not found")

                stock = int(stock)
                if stock < quantity:
                    raise HTTPException(status_code=400, detail="Not enough stock")

                await conn.decrby(f"stock:{item_id}", quantity)
                return {"message": "Purchase successful", "remaining_stock": stock - quantity}
            else:
                raise HTTPException(status_code=429, detail="Request was throttled, please try again later")
        finally:
            if lock.locked():
                await lock.release()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
