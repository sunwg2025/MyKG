# MyKG简介

# 安装部署
### 1，agentscope部署
cd agentscope
pip install -e .

### 2，编辑配置文件
cp .env.example .env
修改BASE_DIR，DATABASE_URL，配置SECRET_KEY，配置smtp邮箱服务

### 3，初始化数据库
sqlite3 MyKG.db < db/init/create_tables.sql 

### 4，安装依赖
pip install -r requirements.txt

### 5，启动服务
streamlit run app.py  --server.address x.x.x.x --server.port xxxx --theme.font monospace

### 6，创建管理员
python scripts/create_admin.py --email xxxxxx --password xxxxxx

### 7，启动api服务
uvicorn api.api_main:app
