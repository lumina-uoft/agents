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

&nbsp;

&nbsp;

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBYWdlbnRzJTNBJTNBbHVtaW5hLXVvZnQ=" repo-name="agents"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
