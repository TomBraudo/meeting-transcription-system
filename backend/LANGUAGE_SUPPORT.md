# Multilingual Support

The backend now supports transcription and analysis in multiple languages, including Hebrew.

## Supported Languages

Whisper API supports 90+ languages including:
- **Hebrew** (`he`)
- **Arabic** (`ar`)
- **English** (`en`)
- **Spanish** (`es`)
- **French** (`fr`)
- And many more...

## Usage

### Auto-detection (Recommended)
```bash
curl -X POST "http://localhost:8000/api/transcribe" \
  -F "file=@audio.mp3"
```

### Specify Language
```bash
curl -X POST "http://localhost:8000/api/transcribe?language=he" \
  -F "file=@hebrew_audio.mp3"
```

### Python Example
```python
import requests

files = {'file': open('hebrew_meeting.mp3', 'rb')}
params = {'language': 'he'}  # Hebrew

response = requests.post(
    'http://localhost:8000/api/transcribe',
    files=files,
    params=params
)

result = response.json()
print(result['summary'])  # Summary in Hebrew
```

## Features

### ✅ Whisper Transcription
- Supports 90+ languages natively
- Auto-detection works well
- Can specify language explicitly

### ✅ Groq Analysis
- Language-aware system prompt
- Analysis in source language (Hebrew, Arabic, etc.)
- Maintains JSON structure

### ✅ RTL Support in Word
- Automatic detection of Hebrew/Arabic text
- Right-to-left text direction
- Proper text alignment

### ✅ UTF-8 Encoding
- All text handled with UTF-8
- Logging supports all Unicode characters
- JSON properly encodes all languages

## Language Codes

- Hebrew: `he` or `iw`
- Arabic: `ar`
- English: `en`
- Spanish: `es`
- French: `fr`
- Russian: `ru`
- Chinese: `zh`

[Full list](https://platform.openai.com/docs/guides/speech-to-text)

## Testing

```bash
# Test with Hebrew audio
python test_api.py hebrew_meeting.mp3

# Test via Swagger UI
# http://localhost:8000/docs
# Add language parameter: he
```

## Word Document Output

For RTL languages (Hebrew/Arabic):
- Text direction: Right-to-left
- Alignment: Right-aligned
- Proper Unicode support
- Mixed LTR/RTL handling
