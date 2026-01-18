import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ProgressBar from './components/ProgressBar';
import TranscriptionView from './components/TranscriptionView';
import SummaryView from './components/SummaryView';
import ParticipantsView from './components/ParticipantsView';
import DecisionsView from './components/DecisionsView';
import ActionItemsView from './components/ActionItemsView';
import ExportButton from './components/ExportButton';
import apiService from './services/api';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [language, setLanguage] = useState('auto');
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState('uploading');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setResult(null);
    setError(null);
  };

  const handleTranscribe = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    setError(null);
    setProgress(0);
    setStage('uploading');

    try {
      // Upload stage
      setProgress(10);
      
      const response = await apiService.transcribeAudio(
        selectedFile,
        language === 'auto' ? null : language,
        (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 30) / progressEvent.total
          );
          setProgress(10 + percentCompleted); // 10-40%
        }
      );

      // Transcribing stage
      setStage('transcribing');
      setProgress(50);
      
      // Simulate processing time for better UX
      await new Promise(resolve => setTimeout(resolve, 500));

      // Analyzing stage
      setStage('analyzing');
      setProgress(75);
      await new Promise(resolve => setTimeout(resolve, 500));

      // Complete
      setStage('complete');
      setProgress(100);
      setResult(response);

    } catch (err) {
      setError(err.message);
      setProgress(0);
      setStage('uploading');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setResult(null);
    setError(null);
    setProgress(0);
    setStage('uploading');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center">
            <svg className="w-10 h-10 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Meeting Transcription & Analysis
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Upload audio files to generate transcriptions, summaries, and action items
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!result ? (
          <div className="max-w-3xl mx-auto">
            {/* Upload Section */}
            <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">
                Upload Audio File
              </h2>

              <FileUpload
                onFileSelect={handleFileSelect}
                disabled={isProcessing}
                selectedFile={selectedFile}
              />

              {/* Language Selection */}
              <div className="mt-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Transcription Language
                </label>
                <div className="flex flex-wrap gap-4">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="language"
                      value="auto"
                      checked={language === 'auto'}
                      onChange={(e) => setLanguage(e.target.value)}
                      disabled={isProcessing}
                      className="mr-2"
                    />
                    <span className="text-gray-700">Auto-detect</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="language"
                      value="en"
                      checked={language === 'en'}
                      onChange={(e) => setLanguage(e.target.value)}
                      disabled={isProcessing}
                      className="mr-2"
                    />
                    <span className="text-gray-700">English</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="language"
                      value="he"
                      checked={language === 'he'}
                      onChange={(e) => setLanguage(e.target.value)}
                      disabled={isProcessing}
                      className="mr-2"
                    />
                    <span className="text-gray-700">עברית (Hebrew)</span>
                  </label>
                </div>
              </div>

              {/* Process Button */}
              <button
                onClick={handleTranscribe}
                disabled={!selectedFile || isProcessing}
                className={`
                  w-full mt-6 py-4 px-6 rounded-lg font-semibold text-lg
                  transition-all duration-200 shadow-md
                  ${
                    !selectedFile || isProcessing
                      ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                      : 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-lg'
                  }
                `}
              >
                {isProcessing ? 'Processing...' : 'Start Transcription'}
              </button>
            </div>

            {/* Progress Section */}
            {isProcessing && (
              <div className="bg-white rounded-lg shadow-lg p-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">
                  Processing
                </h2>
                <ProgressBar stage={stage} progress={progress} />
              </div>
            )}

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex">
                  <svg className="w-6 h-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <h3 className="text-red-800 font-medium">Error</h3>
                    <p className="text-red-700 text-sm mt-1">{error}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-6">
            {/* Actions Bar */}
            <div className="flex justify-between items-center bg-white rounded-lg shadow p-4">
              <button
                onClick={handleReset}
                className="flex items-center px-4 py-2 text-gray-700 hover:text-gray-900 font-medium"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                New Transcription
              </button>
              <ExportButton data={result} />
            </div>

            {/* Results Grid */}
            <div className="grid grid-cols-1 gap-6">
              <TranscriptionView transcription={result.transcription} />
              <SummaryView summary={result.summary} />
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <ParticipantsView participants={result.participants} />
                <DecisionsView decisions={result.decisions} />
              </div>
              
              <ActionItemsView actionItems={result.action_items} />
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            Meeting Transcription System • Powered by Whisper & Groq AI
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
