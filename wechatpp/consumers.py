from channels.generic.websocket import AsyncWebsocketConsumer
import json
import os
from django.core.files.storage import default_storage
from django.conf import settings

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Access the room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = f"chat_{self.room_name}"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages here (e.g., broadcast to other clients)
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        username = text_data_json.get('username')
        room_name = text_data_json.get('room_name')
        file_data = text_data_json.get('file')  # For handling file uploads
        video_signal = text_data_json.get('video_signal')  # For video call signaling

        # Handle file uploads
        if file_data:
            file_name = file_data['name']
            file_content = file_data['content']
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)

            with open(file_path, 'wb') as file:
                file.write(file_content.encode())  # Write the file content to the server

            file_url = default_storage.url(file_path)  # Get the URL for the uploaded file

            # Send the file URL to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f"{username} uploaded a file: <a href='{file_url}' download>Download</a>",
                    'file': file_url
                }
            )
        elif message:
            # Send the text message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                }
            )
        elif video_signal:
            # Handle video signaling for WebRTC
            signal_type = video_signal.get('type')  # "offer", "answer", or "ice_candidate"
            signal_data = video_signal.get('data')

            if signal_type == 'offer':
                # Send the offer to all other clients in the room
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'video_signal',
                        'signal_type': 'offer',
                        'data': signal_data,
                        'username': username
                    }
                )
            elif signal_type == 'answer':
                # Send the answer to the person who made the offer
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'video_signal',
                        'signal_type': 'answer',
                        'data': signal_data,
                        'username': username
                    }
                )
            elif signal_type == 'ice_candidate':
                # Send the ICE candidate to the other clients
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'video_signal',
                        'signal_type': 'ice_candidate',
                        'data': signal_data,
                        'username': username
                    }
                )

    # Receive a message from the room group (chat message)
    async def chat_message(self, event):
        message = event['message']
        username = event.get('username', '')
        file_url = event.get('file', '')

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'file': file_url
        }))

    # Receive a video signal from the room group (WebRTC signaling)
    async def video_signal(self, event):
        signal_type = event['signal_type']
        data = event['data']
        username = event['username']

        # Send the video signal to WebSocket
        await self.send(text_data=json.dumps({
            'signal_type': signal_type,
            'data': data,
            'username': username
        }))

    # Handle the chatbot's response
    async def send_bot_response(self, user_message):
        # Here you can call a backend function or API to get the chatbot response
        # For simplicity, we just echo the user message for now
        bot_response = f"Bot: {user_message}"

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': bot_response,
                'username': 'Bot'
            }
        )
