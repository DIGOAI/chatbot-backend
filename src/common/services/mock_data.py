from datetime import datetime
from uuid import UUID

from src.common.models import (
    Client,
    Conversation,
    ConversationStatus,
    Message,
    MessageType,
)

oct_1_10_30 = datetime.fromtimestamp(1696156200)
oct_1_10_35 = datetime.fromtimestamp(1696156500)
oct_1_10_40 = datetime.fromtimestamp(1696156800)
oct_1_11_00 = datetime.fromtimestamp(1696158000)

# Create a list of 5 clients
clients: list[Client] = [
    Client(id=UUID("2f6e67d5-2652-4940-9ade-853be8a6cf34"), names="John Doe", phone="+593987654321",
           saraguros_id=None, created_at=oct_1_10_30, updated_at=oct_1_11_00),
    Client(id=UUID("418fbef3-6184-4335-8317-246d198a0bd3"), names="Jane Doe", phone="+593987654322",
           saraguros_id=None, created_at=oct_1_10_30, updated_at=oct_1_11_00),
    Client(id=UUID("bd794025-207a-43f7-94a2-19f9a329b05b"), names="John Smith", phone="+593987654323",
           saraguros_id=None, created_at=oct_1_10_30, updated_at=oct_1_11_00),
    Client(id=UUID("4223010a-ddf6-404f-a2fc-e844f94ef05c"), names="Jane Smith", phone="+593987654324",
           saraguros_id=None, created_at=oct_1_10_30, updated_at=oct_1_11_00),
    Client(id=UUID("040ea055-b8a3-4391-9395-dcf0538b0772"), names="John Doe", phone="+593987654325",
           saraguros_id=None, created_at=oct_1_10_30, updated_at=oct_1_11_00),
]


# Create a list of 5 conversations
conversations: list[Conversation] = [
    Conversation(id=UUID("0774a6d2-e1f9-42ac-8215-fc4734a01b0d"), client_phone="+593987654321", assistant_phone="+593986728536",
                 client_id=clients[0].id, created_at=oct_1_10_35, updated_at=oct_1_10_40, finished_at=datetime.fromtimestamp(1696157400), status=ConversationStatus.CLOSED),
    Conversation(id=UUID("166dd33c-abd3-4c29-abd5-7c75f2293a9d"), client_phone="+593987654322", assistant_phone="+593986728536",
                 client_id=clients[1].id, created_at=oct_1_10_35, updated_at=oct_1_10_40, finished_at=datetime.fromtimestamp(1696157700), status=ConversationStatus.CLOSED),
    Conversation(id=UUID("b407b8f7-b33f-4ec4-a11b-fcc88bdfbc78"), client_phone="+593987654323", assistant_phone="+593986728536",
                 client_id=clients[2].id, created_at=oct_1_10_35, updated_at=oct_1_10_40, finished_at=None),
    Conversation(id=UUID("4b8560ee-a322-4f9c-8acb-9f67f1c0518b"), client_phone="+593987654324", assistant_phone="+593986728536",
                 client_id=clients[3].id, created_at=oct_1_10_35, updated_at=oct_1_10_40, finished_at=None),
    Conversation(id=UUID("be2039c4-b107-44e2-a207-f52628bba71c"), client_phone="+593987654325", assistant_phone="+593986728536",
                 client_id=clients[4].id, created_at=oct_1_10_35, updated_at=oct_1_10_40, finished_at=None),
]


messages: list[Message] = []

for i in range(len(conversations)):
    conversation = conversations[i]
    created_at_seconds = 1696156500

    for j in range(3):
        if j % 2 == 0:
            sender = conversation.client_phone
            receiver = conversation.assistant_phone
        else:
            sender = conversation.assistant_phone
            receiver = conversation.client_phone
        message = Message(
            id=f"MS{i+1:0>2d}{j+1:0>30d}",
            conversation_id=UUID(str(conversation.id)),
            sender=sender,
            receiver=receiver,
            message=f"Message {j+1} from {sender} to {receiver}",
            created_at=datetime.fromtimestamp(created_at_seconds),
            media_url=None,
            message_type=MessageType.IN if sender == conversation.client_phone else MessageType.OUT
        )
        messages.append(message)

        created_at_seconds += 30
