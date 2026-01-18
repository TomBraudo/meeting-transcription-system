import React from 'react';

/**
 * DecisionsView component to display meeting decisions
 */
const DecisionsView = ({ decisions }) => {
  if (!decisions || decisions.length === 0) return null;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center mb-4">
        <svg className="w-6 h-6 text-orange-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h2 className="text-xl font-bold text-gray-800">Decisions</h2>
        <span className="ml-3 px-2 py-1 bg-orange-100 text-orange-700 text-xs font-medium rounded-full">
          {decisions.length}
        </span>
      </div>

      <div className="space-y-3">
        {decisions.map((decision, index) => (
          <div
            key={index}
            className="flex items-start p-4 bg-orange-50 rounded-lg border border-orange-200"
          >
            <div className="flex-shrink-0 w-6 h-6 bg-orange-500 rounded-full flex items-center justify-center mr-3 mt-0.5">
              <span className="text-white text-xs font-bold">{index + 1}</span>
            </div>
            <p className="text-gray-700 flex-1">{decision}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DecisionsView;
