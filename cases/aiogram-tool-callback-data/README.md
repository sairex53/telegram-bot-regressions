# Reproduce the Unicode callback-data regression

Upstream: [shayzi3/aiogram_tool](https://github.com/shayzi3/aiogram_tool), commit b8cfa85e5b5d6a547d06106a6feeb7187e3e795e (version 1.2.3).

The unique-ID builder reserves space using len(prefix), which counts Unicode code points. Telegram limits callback_data to 1–64 bytes ([Bot API](https://core.telegram.org/bots/api#inlinekeyboardbutton)). With a ten-emoji prefix, the builder underestimates the prefix size and aiogram rejects the generated callback.

From a checkout of the commit above:

```sh
python -m pip install -e '.[dev]'
git apply /path/to/utf8-prefix.patch
cp /path/to/test_unique_id.py tests/callback_data/
python -m pytest -q tests/callback_data/test_unique_id.py
```

The new Unicode-prefix test fails on the original source with aiogram's length validation error. With the patch, the focused file passes (2 passed, Python 3.12 / aiogram 3.29.1).

The test exercises local packing, storage, and unpacking. It does not send a Telegram request. The full upstream suite was not run for this case.
