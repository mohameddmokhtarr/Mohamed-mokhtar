import logging
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Config

logger = logging.getLogger(__name__)
router = APIRouter(tags=["dashboard"])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home():
    """Redirect to dashboard."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Instagram Automation Tool</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: #0f1419;
                color: #fff;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            .container {
                text-align: center;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 0.5em;
            }
            p {
                font-size: 1.2em;
                margin-bottom: 2em;
                color: #b0b3b8;
            }
            a {
                display: inline-block;
                padding: 12px 30px;
                margin: 10px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .btn-primary {
                background: #0a66c2;
                color: white;
            }
            .btn-primary:hover {
                background: #084399;
            }
            .btn-secondary {
                background: #2a2a2a;
                color: white;
            }
            .btn-secondary:hover {
                background: #3a3a3a;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📱 Instagram Automation Tool</h1>
            <p>ManyChat-style comment automation</p>
            <div>
                <a href="/dashboard" class="btn-primary">Go to Dashboard</a>
                <a href="/health" class="btn-secondary">Health Check</a>
            </div>
        </div>
    </body>
    </html>
    """


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page."""
    db = SessionLocal()
    try:
        config = db.query(Config).first()
        has_config = config is not None
    finally:
        db.close()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "has_config": has_config}
    )


@router.get("/health")
async def health():
    """Health check endpoint for deployment."""
    return {"status": "ok"}
