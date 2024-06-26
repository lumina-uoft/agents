---
title: Voices
---
## **OpenAI voices - all stable**

<SwmSnippet path="/livekit-plugins/livekit-plugins-openai/livekit/plugins/openai/models.py" line="5">

---

**alloy: default male**

echo: young male; a bit flat and dull

**fable: young male with slightly british accent**

onyx: old male; very dull

**nova: Young woman**

shimmer: Unisex; a bit flat and dull

```python
TTSVoices = Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
```

---

</SwmSnippet>

## Cartesia voices

### not as stable as OpenAI's, but has potential

- Speed and emotion control
- Embed Voice mix

<SwmSnippet path="/livekit-plugins/livekit-plugins-cartesia/livekit/plugins/cartesia/models.py" line="17">

---

**ReadingMan:** energetic and friendly, like having your friend read his favorite book to you. But the pace is a bit fast.

Default BarberShopMan's voice is soft. Not that stable

Pre-made child voice is fine, but the pace is too fast.

Cloned sponge voice is unusable.

Cloned Teddy voice (Ted Lasso) is terrible.

```python
TTSDefaultVoiceEmbedding: list[float] = [
```

---

</SwmSnippet>

## Google TTS voices

### Not stable for production. Can control speed , but there's strange noise at the beginning of each sentences. Some voices machine-like

<SwmSnippet path="/livekit-plugins/livekit-plugins-google/livekit/plugins/google/tts.py" line="50">

---

**en-US-Journey-D: quite natural (speed: 0.7 - 0.8)**

en-GB-Studio-B: Machine like

en-GB-News-K: very machine like

&nbsp;

```python
        language: LgType = "en-US", #en-US, en-GB
        gender: GenderType = "male", #neutral
        voice_name: str = "en-US-Journey-D",  # Not required en-GB-Studio-B, en-GB-News-K
        encoding: AudioEncodingType = "linear16",
        sample_rate: int = 24000,
```

---

</SwmSnippet>

## Azure TTS voices

Not very stable and quite machine-like. Potential in modify speed, style, and even role-play, but use another SSML language - it takes effort to modify the codes.

<SwmSnippet path="/science-time.py" line="60" repo-id="Z2l0aHViJTNBJTNBbWFpbiUzQSUzQWx1bWluYS11b2Z0">

---

Davis: old man, a bit machine-like

```python
        tts=azure.TTS(voice = "en-US-DavisNeural"), # Azure TTS is not that stable and quite machine-like, but has potential in speed & style control, role-playing and voice cloning.
```

---

</SwmSnippet>

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBYWdlbnRzJTNBJTNBbHVtaW5hLXVvZnQ=" repo-name="agents"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
