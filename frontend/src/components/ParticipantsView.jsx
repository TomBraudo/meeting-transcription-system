import React from 'react';

/**
 * ParticipantsView component to display meeting participants
 */
const ParticipantsView = ({ participants }) => {
  if (!participants || participants.length === 0) return null;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center mb-4">
        <svg className="w-6 h-6 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <h2 className="text-xl font-bold text-gray-800">Participants</h2>
        <span className="ml-3 px-2 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
          {participants.length}
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
        {participants.map((participant, index) => (
          <div
            key={index}
            className="flex items-center p-3 bg-gray-50 rounded-lg border border-gray-200"
          >
            <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-3">
              <span className="text-green-700 font-bold text-sm">
                {participant.charAt(0).toUpperCase()}
              </span>
            </div>
            <span className="text-gray-700 font-medium">{participant}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ParticipantsView;
