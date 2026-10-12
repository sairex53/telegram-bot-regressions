# Regression cases for Python Telegram bots

Two small, reproducible regression cases for open-source Python libraries used with Telegram bots. Each case includes a test that demonstrates the behavior and a minimal proposed patch.

No bot token or Telegram API request is needed. Tests use local objects and the libraries' existing test fixtures.

## Cases

### `aiogram-dialog-yaml`: a failing `on_error` callback strands the queue

At upstream commit [`aee5e595`](https://github.com/notwizzard/aiogram-dialog-yaml/tree/aee5e595403e29f95f766fd302568b488d3ecf40), a send failure followed by an exception in `on_error` terminates the only worker. A later queued task is never acknowledged, so `queue.join()` does not finish.

- [Regression test](cases/aiogram-dialog-yaml-queue/test_error_handler_failure.py)
- [Proposed patch](cases/aiogram-dialog-yaml-queue/queue.patch)
- [Reproduction instructions](cases/aiogram-dialog-yaml-queue/README.md)

Verification on Python 3.12: both callback variants fail on the unpatched source; after the patch, the complete project suite passes (**21 passed**).

### `aiogram_tool`: Unicode prefixes use the wrong callback-data budget

At upstream commit [`b8cfa85e`](https://github.com/shayzi3/aiogram_tool/tree/b8cfa85e5b5d6a547d06106a6feeb7187e3e795e), the unique-ID builder subtracts Python character counts from Telegram's [`1–64 byte` `callback_data` limit](https://core.telegram.org/bots/api#inlinekeyboardbutton). A non-ASCII prefix can therefore make the generated callback exceed the limit.

- [Regression test](cases/aiogram-tool-callback-data/test_unique_id.py)
- [Proposed patch](cases/aiogram-tool-callback-data/utf8-prefix.patch)
- [Reproduction instructions](cases/aiogram-tool-callback-data/README.md)

Verification on Python 3.12 / aiogram 3.29.1: the Unicode-prefix case fails on the unpatched source; after the patch, the focused test file passes (**2 passed**). The full suite was not run for this case.

## Scope

These are proposed fixes tested against the upstream snapshots above. No pull requests have been submitted. The queue test does not model Telegram retries, and the callback-data test covers local packing/unpacking rather than a live Telegram request. See [third-party notices](THIRD_PARTY_NOTICES.md) for upstream license information.
