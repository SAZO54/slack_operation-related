def process_realtime_message(event):
    event_type = event.get("type")

    if event_type == "message":
        user = event.get("user")
        text = event.get("text")
        channel = event.get("channel")
        print(f"New message from {user} in channel {channel}: {text}")

        # スレッドメッセージの処理
        if "thread_ts" in event:
            print("This is a thread message.")
