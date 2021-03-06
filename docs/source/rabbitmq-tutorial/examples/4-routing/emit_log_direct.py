import sys
import asyncio
from aio_pika import connect, Message, DeliveryMode, ExchangeType


async def main(loop):
    # Perform connection
    connection = await connect(
        "amqp://guest:guest@localhost/", loop=loop
    )

    # Creating a channel
    channel = await connection.channel()

    logs_exchange = await channel.declare_exchange(
        'logs', ExchangeType.DIRECT
    )

    message_body = (
        b' '.join(arg.encode() for arg in sys.argv[2:])
        or
        b"Hello World!"
    )

    message = Message(
        message_body,
        delivery_mode=DeliveryMode.PERSISTENT
    )

    # Sending the message
    routing_key = sys.argv[1] if len(sys.argv) > 2 else 'info'
    await logs_exchange.publish(message, routing_key=routing_key)

    print(" [x] Sent %r" % message.body)

    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
