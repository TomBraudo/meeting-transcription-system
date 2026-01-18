# Meeting Transcription Frontend

React frontend for the Meeting Transcription & Summarization system.

## Features

- 🎙️ **File Upload**: Drag & drop or select audio files (MP3/WAV)
- 🌐 **Language Support**: English and Hebrew transcription
- 📊 **Progress Tracking**: Real-time processing status
- 📝 **Results Display**: Transcription, summary, participants, decisions, action items
- 📄 **Word Export**: Download results as .docx file
- 🎨 **Modern UI**: Beautiful, responsive design with Tailwind CSS

## Quick Start

### Prerequisites

- Node.js 14+ and npm
- Backend server running at `http://localhost:8000`

### Installation

```bash
npm install
```

### Development

```bash
npm start
```

The app will open at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── FileUpload.jsx   # File upload with drag & drop
│   │   ├── ProgressBar.jsx  # Processing progress indicator
│   │   ├── TranscriptionView.jsx
│   │   ├── SummaryView.jsx
│   │   ├── ParticipantsView.jsx
│   │   ├── DecisionsView.jsx
│   │   ├── ActionItemsView.jsx
│   │   └── ExportButton.jsx
│   ├── services/
│   │   └── api.js           # Backend API client
│   ├── App.jsx              # Main application
│   └── index.js             # Entry point
├── public/
└── package.json
```

## Dependencies

- **React**: UI framework
- **axios**: HTTP client
- **react-dropzone**: File upload with drag & drop
- **Tailwind CSS**: Utility-first CSS framework

## Configuration

The frontend is configured to connect to the backend at `http://localhost:8000`.

To change this, edit `API_BASE_URL` in `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://your-backend-url';
```

## Usage

1. Select an audio file (MP3 or WAV)
2. Choose the language (English or Hebrew)
3. Click "Start Transcription"
4. Wait for processing to complete
5. View the results (transcription, summary, participants, etc.)
6. Export to Word document if needed
7. Click "New Transcription" to process another file

## Troubleshooting

### Backend Connection Error

If you see "No response from server" error:
- Ensure the backend is running at `http://localhost:8000`
- Check CORS configuration in the backend
- Verify your API keys are set in the backend `.env` file

### File Upload Issues

- Supported formats: MP3, WAV
- Check file size (large files may take longer to process)
- Ensure the file is not corrupted

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

Modern browsers with ES6+ support required.
