import React from 'react';
import toast from 'react-hot-toast';

const DefectToast = ({ t, log, onClick }) => {
  return (
    <div
      className={`${
        t.visible ? 'animate-enter' : 'animate-leave'
      } max-w-md w-full bg-white shadow-lg rounded-lg pointer-events-auto flex ring-1 ring-black ring-opacity-5`}
    >
      <div className="flex-1 w-0 p-4">
        <div className="flex items-start">
          <div className="ml-3 flex-1">
            <p className="text-sm font-medium text-gray-900">
              불량 의심 감지
            </p>
            <p className="mt-1 text-sm text-gray-500">
              제품 ID {log.product_id} (불량 확률 {Math.round(log.prob * 100)}%)
            </p>
          </div>
        </div>
      </div>
      <div className="flex border-l border-gray-200">
        <button
          onClick={onClick}
          className="w-full border border-transparent rounded-none rounded-r-lg p-4 flex items-center justify-center text-sm font-medium text-indigo-600 hover:text-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          자세히 보기
        </button>
      </div>
    </div>
  );
};

export default DefectToast;
