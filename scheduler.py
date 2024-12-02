from apscheduler.schedulers.background import BackgroundScheduler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import time
from datetime import datetime, timedelta

def fetch_channel_messages():
    print("Scheduler is running...")
    client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    # 監視するチャンネルIDのリスト
    channels_to_monitor = ["C05F2JZLP0V", "C04GLB9K6HH"]
    target_user_id = "U04GZ3W1SDP"

    # 当日の開始と終了のタイムスタンプを計算
    today_start = datetime.combine(datetime.today(), datetime.min.time())
    today_end = today_start + timedelta(days=1) - timedelta(seconds=1)
    start_timestamp = int(time.mktime(today_start.timetuple()))
    end_timestamp = int(time.mktime(today_end.timetuple()))


    for channel_id in channels_to_monitor:
        try:
            response = client.conversations_history(
                channel=channel_id, 
                limit=100,
                oldest=start_timestamp,
                latest=end_timestamp
            )
            messages = response.get('messages', [])

            for message in messages:
                if message.get('user') == target_user_id:
                    print(f"Message from {target_user_id}: {message.get('text')}")
                    
                    # スレッド内のメッセージを取得
                    if 'thread_ts' in message:
                        thread_ts = message['thread_ts']
                        thread_response = client.conversations_replies(channel=channel_id, ts=thread_ts)
                        thread_messages = thread_response.get('messages', [])
                        
                        for thread_message in thread_messages:
                            thread_ts_float = float(thread_message['ts'])
                            if thread_message.get('user') == target_user_id and start_timestamp <= thread_ts_float <= end_timestamp:
                                print(f"Thread Message from {target_user_id} on {datetime.fromtimestamp(thread_ts_float)}: {thread_message.get('text')}")

        except SlackApiError as e:
            print(f"Error fetching messages: {e.response['error']}")

def start_scheduler():
    scheduler = BackgroundScheduler()

    if not scheduler.running:
        scheduler.add_job(fetch_channel_messages, 'cron', hour=9, minute=36)
        # scheduler.add_job(fetch_channel_messages, 'cron', minute='*/1')
        print("Job added to scheduler.")
        scheduler.start()
        print("Scheduler started.")

        for job in scheduler.get_jobs():
            print(f"Scheduled job: {job}")
