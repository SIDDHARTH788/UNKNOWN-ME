from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

# Import our new class instead of the old function
from app.services.therapist import TherapistChat

router = APIRouter()

class ConnectionManager:
    # ... (keep your existing ConnectionManager code exactly the same) ...
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    # --- INSTANTIATE THE THERAPIST ---
    # Create a fresh memory session just for this connected user
    user_therapist = TherapistChat()
    
    try:
        await manager.send_personal_message("System: Connected securely and anonymously.", websocket)
        
        while True:
            data = await websocket.receive_text()
            
            # Pass the message to this user's specific therapist instance
            ai_response = await user_therapist.get_response(data)
            
            await manager.send_personal_message(ai_response, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)