from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ai_animation.api import router as ai_animation_router
from ai_animation.config import settings
import os

def settings_to_dict(obj):
    # 递归遍历 settings 的所有属性，收集 model_dump() 内容
    result = {}
    for attr in dir(obj):
        if attr.startswith('_') or attr == 'model_dump':
            continue
        value = getattr(obj, attr)
        if hasattr(value, 'model_dump'):
            result[attr] = value.model_dump()
    return result

app_cfg = settings.app

app = FastAPI(title=app_cfg.APP_TITLE, version=app_cfg.APP_VERSION)

# Register AI animation API router
app.include_router(ai_animation_router)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), app_cfg.STATIC_DIR)
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount(f"/{app_cfg.STATIC_DIR}", StaticFiles(directory=static_dir), name=app_cfg.STATIC_DIR)

# Configure templates directory
templates_dir = os.path.join(os.path.dirname(__file__), app_cfg.TEMPLATES_DIR)
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Serve main application page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": app_cfg.HEALTH_STATUS, "service": app_cfg.SERVICE_NAME}

@app.get("/config", response_class=JSONResponse)
def show_config():
    """Show current config (for debug only)"""
    return settings_to_dict(settings)
