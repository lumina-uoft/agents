---
title: Interruption
---
<SwmSnippet path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" line="119">

---

<SwmToken path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" pos="121:1:1" line-data="        interrupt_min_words: int = 3,">`interrupt_min_words`</SwmToken>

```python
        allow_interruptions: bool = True,
        interrupt_speech_duration: float = 0.65,
        interrupt_min_words: int = 3,
```

---

</SwmSnippet>

<SwmSnippet path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" line="138">

---

<SwmToken path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" pos="140:1:1" line-data="            int_min_words=interrupt_min_words,">`int_min_words`</SwmToken>

```python
            allow_interruptions=allow_interruptions,
            int_speech_duration=interrupt_speech_duration,
            int_min_words=interrupt_min_words,
```

---

</SwmSnippet>

<SwmSnippet path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" line="578">

---

&nbsp;

```python
    def _interrupt_if_needed(self) -> None:
        """
        Check whether the current assistant speech should be interrupted
        """
        if (
            not self._validated_speech
            or not self._opts.allow_interruptions
            or self._validated_speech.interrupted
        ):
            return

        if self._opts.int_min_words != 0:
            txt = self._transcribed_text.strip().split()
            if len(txt) <= self._opts.int_min_words:
                txt = self._interim_text.strip().split()
                if len(txt) <= self._opts.int_min_words:
                    return

        if (
            self._playout_start_time is not None
            and (time.time() - self._playout_start_time) < 1
        ):  # don't interrupt new speech (if they're not older than 1s)
            return

        self._validated_speech.interrupted = True
        self._validate_answer_if_needed()
        self._log_debug("user interrupted assistant speech")
```

---

</SwmSnippet>

<SwmSnippet path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" line="623">

---

&nbsp;

```python
    async def _start_speech(
        self, data: _SpeechData, *, interrupt_current_if_possible: bool
    ) -> None:
        await self._wait_ready()

        async with self._start_speech_lock:
            # interrupt the current speech if possible, otherwise wait before playing the new speech
            if self._play_atask is not None:
                if self._validated_speech is not None:
                    if (
                        interrupt_current_if_possible
                        and self._validated_speech.allow_interruptions
                    ):
                        logger.debug("_start_speech - interrupting current speech")
                        self._validated_speech.interrupted = True

                else:
                    # pending speech isn't validated yet, OK to cancel
                    self._play_atask.cancel()

                with contextlib.suppress(asyncio.CancelledError):
                    await self._play_atask

            self._play_atask = asyncio.create_task(
                self._play_speech_if_validated_task(data)
            )
```

---

</SwmSnippet>

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBYWdlbnRzJTNBJTNBbHVtaW5hLXVvZnQ=" repo-name="agents"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
