import React from 'react';

/**
 * SummaryView component to display meeting summary
 */
const SummaryView = ({ summary }) => {
  if (!summary) return null;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center mb-4">
        <svg className="w-6 h-6 text-purple-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h2 className="text-xl font-bold text-gray-800">Meeting Summary</h2>
      </div>

      <div className="prose max-w-none">
        <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
          {summary}
        </p>
      </div>
    </div>
  );
};

export default SummaryView;
