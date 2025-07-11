#!/usr/bin/env python3
"""
Test script for RabbitMQ connection and message sending.
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta

# Add the ingestor directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ingestor"))

from aio_pika import connect_robust, Message
from config import QUEUE_NAME, RABBITMQ_URL


async def test_rabbitmq_connection():
    """Test RabbitMQ connection and send test messages."""

    print("🔌 Testing RabbitMQ connection...")

    try:
        # Connect to RabbitMQ
        connection = await connect_robust(RABBITMQ_URL)
        channel = await connection.channel()

        # Declare queue
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        print(f"✅ Connected to RabbitMQ at {RABBITMQ_URL}")
        print(f"✅ Queue '{QUEUE_NAME}' is ready")

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

        print(f"\n📨 Sending {len(test_messages)} test messages...")

        for i, payload in enumerate(test_messages, 1):
            message = Message(
                body=json.dumps(payload).encode(), delivery_mode=2  # Persistent message
            )

            await channel.default_exchange.publish(message, routing_key=QUEUE_NAME)
            print(f"✅ Message {i}: {json.dumps(payload)}")

        await connection.close()
        print("\n🎉 All test messages sent successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    return True


async def main():
    """Main function."""
    print("🧪 RabbitMQ Test Script\n")

    success = await test_rabbitmq_connection()

    if success:
        print("\n✅ RabbitMQ test completed successfully!")
        print("\n📋 Next steps:")
        print("1. Start the ingestion service: docker-compose up pncp-ingestor")
        print("2. Check RabbitMQ Management UI: http://localhost:15672")
        print("   - Username: admin")
        print("   - Password: admin123")
    else:
        print("\n❌ RabbitMQ test failed!")
        print("Make sure RabbitMQ is running: docker-compose up rabbitmq")


if __name__ == "__main__":
    asyncio.run(main())
