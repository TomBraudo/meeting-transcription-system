import React from 'react';

/**
 * ProgressBar component to show processing status
 */
const ProgressBar = ({ stage, progress }) => {
  const stages = [
    { name: 'Uploading', key: 'uploading' },
    { name: 'Transcribing', key: 'transcribing' },
    { name: 'Analyzing', key: 'analyzing' },
    { name: 'Complete', key: 'complete' },
  ];

  const currentStageIndex = stages.findIndex((s) => s.key === stage);

  return (
    <div className="w-full">
      {/* Progress Bar */}
      <div className="relative">
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-blue-600 transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
        <p className="text-sm text-gray-600 mt-2 text-center">
          {progress}% - {stages[Math.min(currentStageIndex, stages.length - 1)]?.name || 'Processing'}
        </p>
      </div>

      {/* Stage Indicators */}
      <div className="mt-6 grid grid-cols-4 gap-2">
        {stages.map((s, index) => {
          const isActive = index === currentStageIndex;
          const isComplete = index < currentStageIndex;

          return (
            <div
              key={s.key}
              className={`
                flex flex-col items-center p-3 rounded-lg
                transition-all duration-200
                ${isActive ? 'bg-blue-50 border-2 border-blue-500' : ''}
                ${isComplete ? 'bg-green-50' : ''}
                ${!isActive && !isComplete ? 'bg-gray-50' : ''}
              `}
            >
              {/* Icon */}
              <div
                className={`
                  w-8 h-8 rounded-full flex items-center justify-center mb-2
                  ${isActive ? 'bg-blue-500 animate-pulse' : ''}
                  ${isComplete ? 'bg-green-500' : ''}
                  ${!isActive && !isComplete ? 'bg-gray-300' : ''}
                `}
              >
                {isComplete ? (
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fillRule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clipRule="evenodd"
                    />
                  </svg>
                ) : (
                  <span
                    className={`
                      text-sm font-bold
                      ${isActive ? 'text-white' : 'text-gray-500'}
                    `}
                  >
                    {index + 1}
                  </span>
                )}
              </div>

              {/* Label */}
              <span
                className={`
                  text-xs font-medium text-center
                  ${isActive ? 'text-blue-700' : ''}
                  ${isComplete ? 'text-green-700' : ''}
                  ${!isActive && !isComplete ? 'text-gray-500' : ''}
                `}
              >
                {s.name}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ProgressBar;
