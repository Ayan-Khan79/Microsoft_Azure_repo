from flask import Flask, request, jsonify
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
import asyncio
import os

app = Flask(__name__)

# --- DIRECT CONFIGURATION ---
# Copy these exactly from your Azure Portal screenshot
APP_ID = ""
APP_TENANT_ID = ""
# This is the "Value" you copied after clicking 'Manage Password'
APP_PASSWORD = "" 

# For Single Tenant, you MUST pass app_id, app_password, AND tenant_id
adapter_settings = BotFrameworkAdapterSettings(
    app_id=APP_ID, 
    app_password=APP_PASSWORD,
    tenant_id=APP_TENANT_ID
)
adapter = BotFrameworkAdapter(adapter_settings)

async def bot_logic(turn_context: TurnContext):
    text = turn_context.activity.text
    # Simple echo logic
    await turn_context.send_activity(f"Echo: {text}")

@app.route("/api/messages", methods=["POST"])
def messages():
    # 1. Log the incoming request to see it in Azure Log Stream
    print("🔥 Bot received a request at /api/messages") 

    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    try:
        # 2. Process the activity using the adapter
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(adapter.process_activity(activity, auth_header, bot_logic))
        return jsonify({}), 201
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Bot is running and configured!"

if __name__ == "__main__":
    # Azure App Service sets the PORT environment variable automatically
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)