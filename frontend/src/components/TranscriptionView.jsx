import React, { useState } from 'react';

/**
 * TranscriptionView component to display full transcription text
 */
const TranscriptionView = ({ transcription }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!transcription) return null;

  const isLong = transcription.length > 500;
  const displayText = isLong && !isExpanded 
    ? transcription.substring(0, 500) + '...' 
    : transcription;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-800">Full Transcription</h2>
        <span className="px-3 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded-full">
          {transcription.length} characters
        </span>
      </div>

      <div className="prose max-w-none">
        <div className="bg-gray-50 rounded p-4 border border-gray-200">
          <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
            {displayText}
          </p>
        </div>
      </div>

      {isLong && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="mt-3 text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center"
        >
          {isExpanded ? (
            <>
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
              </svg>
              Show Less
            </>
          ) : (
            <>
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
              Show More
            </>
          )}
        </button>
      )}
    </div>
  );
};

export default TranscriptionView;
