import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_unread_message_count(self, event):
        unread_messages_count = event['unread_messages_count']
        await self.send(text_data=json.dumps({
            'unread_messages_count': unread_messages_count
        }))

    async def send_new_message(self, event):
        message_data = event['message']
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': message_data,
        }))

    async def send_unread_notification_count(self, event):
        unread_notifications_count = event['unread_notifications_count']
        await self.send(text_data=json.dumps({
            'unread_notifications_count': unread_notifications_count
        }))

    async def send_new_notification(self, event):
        notification_data = event['notification']
        await self.send(text_data=json.dumps({
            'type': 'new_notification',
            'notification': notification_data
        }))
