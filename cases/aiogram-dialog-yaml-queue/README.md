# Reproduce the queue-worker regression

Upstream: [notwizzard/aiogram-dialog-yaml](https://github.com/notwizzard/aiogram-dialog-yaml), commit aee5e595403e29f95f766fd302568b488d3ecf40 (version 0.1.0).

The test enqueues two messages. The fake bot fails on the first; a synchronous or asynchronous on_error callback then raises. On the original source, the worker exits and queue.join() times out while the second message remains pending. The patch logs callback failures and lets the worker continue. It catches Exception, leaving task cancellation behavior intact.

From a checkout of the commit above:

```sh
python -m pip install -e '.[dev]'
git apply /path/to/queue.patch
cp /path/to/test_error_handler_failure.py tests/
PYTHONPATH=src python -m pytest -q
```

On the original source, both parametrized cases time out at queue.join(). With the patch, the complete suite passes (21 passed, Python 3.12).

This is a local queue test with a fake bot. It does not send Telegram requests and does not add retries.
