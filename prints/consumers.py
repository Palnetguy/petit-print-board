import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Determine group based on user role
        if self.user.is_staff:
            # Secretary joins secretary group
            self.group_name = 'secretary'
        else:
            # Teacher joins their personal group
            self.group_name = f'teacher_{self.user.id}'
        
        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave group
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    # Receive message from WebSocket (not used in this app, but can be extended)
    async def receive(self, text_data):
        pass
    
    # Handler for new print request notification (sent to secretary)
    async def new_request(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_request',
            'request_id': event['request_id'],
            'teacher': event['teacher'],
            'filename': event['filename'],
            'deadline': event['deadline'],
        }))
    
    # Handler for request printed notification (sent to teacher)
    async def request_printed(self, event):
        await self.send(text_data=json.dumps({
            'type': 'request_printed',
            'request_id': event['request_id'],
            'filename': event['filename'],
        }))
