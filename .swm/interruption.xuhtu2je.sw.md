---
title: Interruption
---
<SwmSnippet path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" line="119">

---

1\. **interrupt_speech_duration**: This parameter seems to define how long the user must be speaking (in seconds) before an interruption can be considered.

2\. **interrupt_min_words**: This parameter still defines the minimum number of words the user must say to trigger an interruption.

```python
        allow_interruptions: bool = True,
        interrupt_speech_duration: float = 0.65,
        interrupt_min_words: int = 3,
```

---

</SwmSnippet>

<SwmSnippet path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" line="138">

---

&nbsp;

```python
            allow_interruptions=allow_interruptions,
            int_speech_duration=interrupt_speech_duration,
            int_min_words=interrupt_min_words,
```

---

</SwmSnippet>

<SwmSnippet path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" line="578">

---

1\. **Initial Checks:**

If there is 1) no validated speech, 2) interruptions are not allowed, or 3) the speech is already interrupted, the function returns without doing anything.

2\. **User’s Minimum Words Check:**

Checks if the transcribed text from the user’s interruption attempt meets the minimum word requirement (interrupt_min_words). If the user’s speech is too short, it does not interrupt the assistant’s speech.

3\. **Assistant’s Speech Duration Check:** 

Ensures the assistant has been speaking for a sufficient duration (interrupt_speech_duration) before allowing interruptions.

4\. **Marking Speech as Interrupted:**

If all conditions are met, the assistant’s speech is marked as interrupted.

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

<SwmSnippet path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" line="355">

---

**Moving Averages Setup**:

• **speech_prob_avg**: Averages speech probability over the last 100 samples.

• **speaking_avg_validation**: Averages user speaking activity over the last 150 samples.

• **interruption_speaking_avg**: Averages user speaking activity over a period defined by interrupt_speech_duration.

**Interval Tick**:

• This sets up a loop to run every 10 milliseconds.

```python
        # Loop running each 10ms to do the following:
        #  - Update the volume based on the user speech probability
        #  - Decide when to interrupt the agent speech
        #  - Decide when to validate the user speech (starting the agent answer)
        speech_prob_avg = utils.MovingAverage(100)
        speaking_avg_validation = utils.MovingAverage(150)
        interruption_speaking_avg = utils.MovingAverage(
            int(self._opts.int_speech_duration * 100)
        )

        interval_10ms = aio.interval(0.01)
```

---

</SwmSnippet>

<SwmSnippet path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" line="367">

---

1\. **Loop Running Every** <SwmToken path="/livekit-agents/livekit/agents/voice_assistant/assistant.py" pos="355:9:9" line-data="        # Loop running each 10ms to do the following:">`10ms`</SwmToken>

2\. **Volume Adjustment Based on User Speech Probability**:

• Adjusts the target volume of the assistant’s speech based on the probability of the user’s speech.

• Ensures volume doesn’t drop below a certain level if interruptions aren’t allowed.

• Sets volume to zero if the assistant’s speech has been interrupted.

3\. **Interrupting Agent Speech**:

• If the user is speaking and the average speaking activity over the defined duration (interrupt_speech_duration) exceeds 10%, it calls *interrupt*if_needed().

• If there is pending validation and the user’s speaking activity is low, it validates the answer.

```python
        vad_pw = 2.4  # TODO(theomonnom): should this be exposed?
        while True:
            await interval_10ms.tick()

            speech_prob_avg.add_sample(self._speech_prob)
            speaking_avg_validation.add_sample(int(self._user_speaking))
            interruption_speaking_avg.add_sample(int(self._user_speaking))

            bvol = self._opts.base_volume
            self._target_volume = max(0, 1 - speech_prob_avg.get_avg() * vad_pw) * bvol

            if self._validated_speech:
                if not self._validated_speech.allow_interruptions:
                    # avoid volume to go to 0 even if speech probability is high
                    self._target_volume = max(self._target_volume, bvol * 0.5)

                if self._validated_speech.interrupted:
                    # the current speech is interrupted, target volume should be 0
                    self._target_volume = 0

            if self._user_speaking:
                # if the user has been speaking int_speed_duration, interrupt the agent speech
                # (this currently allows 10% of noise in the VAD)
                if interruption_speaking_avg.get_avg() >= 0.1:
                    self._interrupt_if_needed()
            elif self._pending_validation:
                if speaking_avg_validation.get_avg() <= 0.05:
                    self._validate_answer_if_needed()

            self._plotter.plot_value("raw_vol", self._target_volume)
            self._plotter.plot_value("vad_probability", self._speech_prob)
```

---

</SwmSnippet>

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBYWdlbnRzJTNBJTNBbHVtaW5hLXVvZnQ=" repo-name="agents"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
