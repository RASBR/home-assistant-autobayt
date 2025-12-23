"""HTTP views for Autobayt integration."""
from __future__ import annotations

import logging
import mimetypes
from pathlib import Path

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class AutobaytBrandsView(HomeAssistantView):
    """View to serve Autobayt brand images as fallback when CDN fails."""

    url = f"/api/brands/{DOMAIN}/{{filename}}"
    name = f"api:brands:{DOMAIN}"
    requires_auth = False

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the view."""
        self.hass = hass
        self._static_path = Path(__file__).parent

    async def get(self, request: web.Request, filename: str) -> web.Response:
        """Serve brand image files as fallback when brands.home-assistant.io fails."""
        _LOGGER.debug("Serving brand fallback request for: %s", filename)
        
        allowed_files = [
            "icon.png", "logo.png", "icon@2x.png", "logo@2x.png", 
            "dark_icon.png", "dark_logo.png", "dark_icon@2x.png", "dark_logo@2x.png"
        ]
        
        if filename not in allowed_files:
            _LOGGER.debug("Brand file not allowed: %s", filename)
            return web.Response(status=404)

        possible_paths = [
            self._static_path / "brands" / DOMAIN / filename,
            self._static_path / filename,
        ]
        
        file_path = None
        for path in possible_paths:
            if path.exists():
                file_path = path
                _LOGGER.debug("Found brand file at: %s", path)
                break
                
        if not file_path:
            _LOGGER.debug("Brand file not found: %s (tried: %s)", filename, possible_paths)
            return web.Response(status=404)

        try:
            content_type, _ = mimetypes.guess_type(str(file_path))
            if not content_type:
                content_type = "image/png"

            with open(file_path, "rb") as file:
                content = file.read()

            _LOGGER.debug("Successfully served brand file: %s (%d bytes)", filename, len(content))
            return web.Response(
                body=content,
                content_type=content_type,
                headers={
                    "Cache-Control": "public, max-age=3600",
                    "Access-Control-Allow-Origin": "*",
                },
            )
        except Exception as err:
            _LOGGER.error("Error serving brand file %s: %s", filename, err)
            return web.Response(status=500)


class AutobaytStaticView(HomeAssistantView):
    """View to serve Autobayt static files for integration list."""

    url = f"/api/{DOMAIN}/{{filename}}"
    name = f"api:{DOMAIN}:static"
    requires_auth = False

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the view."""
        self.hass = hass
        self._static_path = Path(__file__).parent

    async def get(self, request: web.Request, filename: str) -> web.Response:
        """Serve static files for integration list and other uses."""
        _LOGGER.debug("Serving static request for: %s", filename)
        
        allowed_files = [
            "icon.png", "logo.png", "icon@2x.png", "logo@2x.png", 
            "dark_icon.png", "dark_logo.png", "dark_icon@2x.png", "dark_logo@2x.png"
        ]
        
        if filename not in allowed_files:
            _LOGGER.debug("Static file not allowed: %s", filename)
            return web.Response(status=404)

        file_path = self._static_path / filename
        
        if not file_path.exists():
            _LOGGER.debug("Static file not found: %s", filename)
            return web.Response(status=404)

        try:
            content_type, _ = mimetypes.guess_type(str(file_path))
            if not content_type:
                content_type = "image/png"

            with open(file_path, "rb") as file:
                content = file.read()

            _LOGGER.debug("Successfully served static file: %s (%d bytes)", filename, len(content))
            return web.Response(
                body=content,
                content_type=content_type,
                headers={
                    "Cache-Control": "public, max-age=3600",
                    "Access-Control-Allow-Origin": "*",
                },
            )
        except Exception as err:
            _LOGGER.error("Error serving static file %s: %s", filename, err)
            return web.Response(status=500)


async def async_setup_http_views(hass: HomeAssistant) -> None:
    """Set up HTTP views for Autobayt."""
    if hasattr(hass.data.get("http"), "_views"):
        views_data = hass.data.get("http")._views
        if f"api:brands:{DOMAIN}" in views_data:
            _LOGGER.debug("HTTP views already registered")
            return
    
    _LOGGER.debug("Registering HTTP views")
    hass.http.register_view(AutobaytBrandsView(hass))
    hass.http.register_view(AutobaytStaticView(hass))
