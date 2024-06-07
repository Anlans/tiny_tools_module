# Python想法验证

## Getting Started

First, run the development server:

### BackEnd
```bash
cd backend/fastapi_module
uvicorn main_xxx:app --reload --port 8000
```

### FrontEnd
```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## 目前的尝试
### 使用FastAPI进行分布式缓存的尝试
使用Redis对商品的存量进行处理，并使用分布式锁避免多客户端同时提交导致的库存量不同步。详情查看`([backend/fastapi_module/main_buy.py](https://github.com/Anlans/tiny_tools_module/blob/main/backend/fastapi_module/main_buy.py))