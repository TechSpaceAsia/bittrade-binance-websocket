from typing import List


def make_sub_unsub_messages(channel: str):
    return {
        "method": "SUBSCRIBE", 
        "params": [
            channel
        ],
    }, {
        "method": "UNSUBSCRIBE", 
        "params": [
            channel
        ]
    }


def make_sub_unsub_messages_list(channel_list: List[str]):
    return {
        "method": "SUBSCRIBE",
        "params": channel_list,
    }, {"method": "UNSUBSCRIBE", "params": channel_list}
