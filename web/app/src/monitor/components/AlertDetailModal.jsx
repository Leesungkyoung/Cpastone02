import React, { Fragment } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { XMarkIcon } from '@heroicons/react/24/outline';

const AlertDetailModal = ({ alert, onClose, onResolve }) => {
  if (!alert) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gray-800">알림 상세 정보</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>
        
        <div className="space-y-4">
          <div>
            <div className="mt-2 text-sm text-gray-600 space-y-2">
              <p><strong>발생 시각:</strong> {new Date(alert.timestamp).toLocaleString()}</p>
              <p><strong>제품 번호:</strong> {alert.product_id}</p>
              <p><strong>불량 의심 확률:</strong> {alert.prob ? `${(alert.prob * 100).toFixed(1)}%` : 'N/A'}</p>
              <div>
                <strong>의심 센서:</strong>
                <ul className="list-disc list-inside pl-4 mt-1">
                  {(alert.top_sensors || []).map((sensor, index) => (
                    <li key={index} className="font-mono">{sensor}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
          
          <div className={`p-3 rounded-md text-sm ${
            alert.resolved 
              ? 'bg-blue-50 text-blue-800' 
              : 'bg-yellow-50 text-yellow-800'
          }`}>
            {alert.resolved 
              ? <p>조치가 완료된 제품입니다.</p>
              : <p>미조치된 알림입니다. 불량 의심 제품을 확인해 보세요.</p>
            }
          </div>

          {!alert.resolved && (
            <div className="pt-4 border-t">
              <button
                onClick={() => {
                  onResolve(alert.id);
                  onClose();
                }}
                className="w-full bg-[#FFE8D6] text-[#D96A2B] font-semibold py-2 px-4 rounded-lg hover:brightness-95 transition-colors"
              >
                조치 완료로 변경
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AlertDetailModal;
