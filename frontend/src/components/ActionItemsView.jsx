import React from 'react';

/**
 * ActionItemsView component to display action items with assignees and deadlines
 */
const ActionItemsView = ({ actionItems }) => {
  if (!actionItems || actionItems.length === 0) return null;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center mb-4">
        <svg className="w-6 h-6 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
        <h2 className="text-xl font-bold text-gray-800">Action Items</h2>
        <span className="ml-3 px-2 py-1 bg-red-100 text-red-700 text-xs font-medium rounded-full">
          {actionItems.length}
        </span>
      </div>

      <div className="space-y-3">
        {actionItems.map((item, index) => (
          <div
            key={index}
            className="p-4 bg-red-50 rounded-lg border border-red-200"
          >
            <div className="flex items-start">
              <div className="flex-shrink-0 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center mr-3 mt-0.5">
                <span className="text-white text-xs font-bold">{index + 1}</span>
              </div>
              <div className="flex-1">
                <p className="text-gray-800 font-medium mb-2">{item.task}</p>
                <div className="flex flex-wrap gap-3 text-sm">
                  {item.assignee && (
                    <div className="flex items-center text-gray-600">
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      <span>{item.assignee}</span>
                    </div>
                  )}
                  {item.deadline && (
                    <div className="flex items-center text-gray-600">
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span>{item.deadline}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ActionItemsView;
