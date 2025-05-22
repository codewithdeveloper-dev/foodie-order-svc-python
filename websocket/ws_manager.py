from typing import Dict
from fastapi import WebSocket

connection: Dict[str, WebSocket] = {}