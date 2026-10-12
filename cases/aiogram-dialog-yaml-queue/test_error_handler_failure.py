"""A failing error callback must not strand subsequent messages."""
import asyncio

import pytest

from aiogram_dialog_yaml.delivery import MessageQueue, MessageTask


@pytest.mark.parametrize("async_handler", [False, True])
async def test_failing_error_handler_keeps_queue_running(async_handler, caplog):
    sent = []

    class Bot:
        async def send_message(self, *, chat_id, text):
            if text == "boom":
                raise RuntimeError("send failed")
            sent.append(text)

    def broken_handler(task, exc):
        raise RuntimeError("error callback failed")

    async def broken_async_handler(task, exc):
        broken_handler(task, exc)

    queue = MessageQueue(
        Bot(), on_error=broken_async_handler if async_handler else broken_handler
    )
    await queue.add(MessageTask(chat_id=1, method="send_message", params={"text": "boom"}))
    await queue.add(MessageTask(chat_id=1, method="send_message", params={"text": "next"}))
    await queue.start()
    try:
        await asyncio.wait_for(queue.join(), timeout=0.5)
        assert sent == ["next"]
        assert "error callback failed" in caplog.text
    finally:
        await queue.stop(drain=False)
