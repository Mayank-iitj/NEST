"""Package initialization for routes module."""
from app.routes.otp import router as otp_router
from app.routes.report import router as report_router
from app.routes.followup import router as followup_router
from app.routes.risk import router as risk_router
from app.routes.dashboard import router as dashboard_router

__all__ = [
    "otp_router",
    "report_router",
    "followup_router",
    "risk_router",
    "dashboard_router"
]
