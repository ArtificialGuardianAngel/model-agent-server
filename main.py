import config
import pika
import together
import threading
import json
import argparse
import os
from utils import mapHistoryToPrompt, updateHistory


def callback(ch: pika.adapters.blocking_connection.BlockingChannel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
    # work on prompt
    data = json.loads(body.decode())
    user_input = data['prompt']
    sid = data['sid']
    history = {'internal': [], 'visible': []}

    if 'history' in data:
        history = data['history']

    prompt = mapHistoryToPrompt(history, user_input)
    model_name = 'togethercomputer/llama-2-70b-chat'
    tokens = together.Complete.create_streaming(
        prompt, model_name, stop="<human>:")

    response = ''
    print(prompt, end='')
    i = 0
    for token in tokens:
        response += token
        if i % 2 == 0:
            data = {
                'message': response,
                'sid': sid,
                'history': updateHistory(history, user_input, response)
            }
            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id),
                body=json.dumps(data)
            )
        print(token, end='', flush=True)
        i += 1

    print()
    print('{:=^50}'.format(f'Tokens used {i}'))
    endMessage = {'end': True, 'sid': sid,
                  'history': updateHistory(history, user_input, response)}
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id),
        body=json.dumps(endMessage)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer(thread_id):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.RMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=config.QUEUE_NAME)
    channel.basic_consume(
        queue=config.QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    print(f"Starting consumer thread {thread_id} on {config.QUEUE_NAME}...")
    channel.start_consuming()


def main():
    parser = argparse.ArgumentParser(description="Starts Model server")
    parser.add_argument("--threads", type=int, default=1,
                        help="Number of consumer threads to start")
    args = parser.parse_args()

    threads = []
    for i in range(args.threads):
        t = threading.Thread(target=start_consumer, args=(i,))
        t.start()
        threads.append(t)

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt. Shutting down...")
        # If you want, you can add any cleanup logic here.
        for t in threads:
            t.join(timeout=1.0)  # Try to join threads with a timeout.


if __name__ == "__main__":
    main()
