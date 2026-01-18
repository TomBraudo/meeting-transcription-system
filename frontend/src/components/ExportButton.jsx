import React, { useState } from 'react';
import apiService from '../services/api';

/**
 * ExportButton component to export results to Word document
 */
const ExportButton = ({ data, disabled }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState(null);

  const handleExport = async () => {
    setIsExporting(true);
    setError(null);

    try {
      const blob = await apiService.exportToWord(data);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `meeting-transcription-${new Date().toISOString().split('T')[0]}.docx`;
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div>
      <button
        onClick={handleExport}
        disabled={disabled || isExporting}
        className={`
          flex items-center justify-center px-6 py-3 rounded-lg font-medium
          transition-all duration-200 shadow-md
          ${
            disabled || isExporting
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-green-600 text-white hover:bg-green-700 hover:shadow-lg'
          }
        `}
      >
        {isExporting ? (
          <>
            <svg
              className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            Exporting...
          </>
        ) : (
          <>
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            Export to Word
          </>
        )}
      </button>

      {error && (
        <div className="mt-2 text-sm text-red-600">
          Export failed: {error}
        </div>
      )}
    </div>
  );
};

export default ExportButton;
