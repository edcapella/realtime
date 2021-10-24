from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['nome_sala']
        self.room_group_name = f'chat_{self.room_name}'

        #entra na sala
        await self.channel_layer.group.add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        #sair da sala
    async def desconect(self, code):
        await self.channel_layer.group.discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mensagem = text_data_json['mensagem']

        # Envia a mensagem para a sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': mensagem
            }
        )
    async def chat_message(self, event):
        mensagem = event['message']

        #envia a mensagem para o websocket
        await self.send(text_data=json.dumps({
            'mensagem': mensagem
        }))