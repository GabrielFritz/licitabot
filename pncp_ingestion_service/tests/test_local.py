#!/usr/bin/env python3
"""
Local development test script for PNCP ingestion service.
This script can run the service directly with Python (no Docker required).
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta

# Add the ingestor directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ingestor"))

# Load environment variables from .env.local
from dotenv import load_dotenv

load_dotenv("../.env.local")

from aio_pika import connect_robust, Message
from config import QUEUE_NAME, RABBITMQ_URL


async def send_test_messages():
    """Send test messages to the queue."""

    print("📨 Sending test messages to RabbitMQ...")

    try:
        # Connect to RabbitMQ
        connection = await connect_robust(RABBITMQ_URL)
        channel = await connection.channel()

        # Declare queue
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        # Send test messages
        test_messages = [
            # Update mode (default)
            {},
            # Update mode (explicit)
            {"mode": "update"},
            # Backfill mode
            {
                "mode": "backfill",
                "data_ini": (datetime.now() - timedelta(hours=1)).strftime(
                    "%Y-%m-%dT%H:%M:%S"
                ),
                "data_fim": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            },
        ]

        for i, payload in enumerate(test_messages, 1):
            message = Message(
                body=json.dumps(payload).encode(), delivery_mode=2  # Persistent message
            )

            await channel.default_exchange.publish(message, routing_key=QUEUE_NAME)
            print(f"✅ Message {i}: {json.dumps(payload)}")

        await connection.close()
        print("🎉 Test messages sent successfully!")

    except Exception as e:
        print(f"❌ Error sending messages: {e}")
        return False

    return True


async def main():
    """Main function."""
    print("🧪 Local Development Test\n")

    # Check if RabbitMQ is accessible
    try:
        connection = await connect_robust(RABBITMQ_URL)
        await connection.close()
        print("✅ RabbitMQ connection successful!")
    except Exception as e:
        print(f"❌ Cannot connect to RabbitMQ: {e}")
        print("\n💡 Make sure RabbitMQ is running:")
        print("   docker-compose up -d rabbitmq")
        return

    # Send test messages
    success = await send_test_messages()

    if success:
        print("\n✅ Local test completed!")
        print("\n📋 Next steps:")
        print("1. Run the ingestion service: python ingestor/consumer.py")
        print("2. Or use Docker: docker-compose up pncp-ingestor")
        print("3. Check RabbitMQ UI: http://localhost:15672 (admin/admin123)")


if __name__ == "__main__":
    asyncio.run(main())
