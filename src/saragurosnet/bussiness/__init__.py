from src.chatbot.decisions_tree import DecisionsTree
from src.common.services import TwilioService
from src.config import Config
from src.saragurosnet.bussiness.client_actions import group as client_group
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.end_actions import group as end_group
from src.saragurosnet.bussiness.initial_actions import group as initial_group
from src.saragurosnet.bussiness.no_client_actions import group as no_client_group
from src.saragurosnet.bussiness.preactions import group as pre_group

tree = DecisionsTree[Context]()

twilio = TwilioService(Config.TWILIO_SID, Config.TWILIO_TOKEN,
                       Config.TWILIO_SENDER, '')

# === Pre actions ===
tree.register_action_group(pre_group)
# === End pre actions ===

# === Initial actions ===
tree.register_action_group(initial_group)
# === End initial actions ===

# === No client actions ===
tree.register_action_group(no_client_group)
# === End no client actions ===

# === Client actions ===
tree.register_action_group(client_group)
# === End Client actions ===

# === End actions ===
tree.register_action_group(end_group)
# === End end actions ===
