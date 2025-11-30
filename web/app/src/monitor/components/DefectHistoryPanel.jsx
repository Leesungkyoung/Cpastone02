import React from 'react';
import { useStreamingStore } from '../../store/streamingStore';

const DefectHistoryPanel = () => {
  const defectHistory = useStreamingStore((state) => state.defectHistory);

  return (
    <div className="flex h-full flex-col">
      <div className="flex-shrink-0">
        <h2 className="text-xl font-semibold text-gray-800">
          금일 품질 경보 현황
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          실시간 스트리밍 중 발생한 불량 의심 이력입니다.
        </p>
      </div>

      {/* Defect List */}
      <div className="mt-4 flex-1 overflow-y-auto rounded-lg border bg-gray-50/50 p-2">
        {defectHistory.length === 0 ? (
          <div className="flex h-full items-center justify-center text-center text-gray-500">
            <p className="text-sm">현재까지 감지된<br />불량 의심 내역이 없습니다.</p>
          </div>
        ) : (
          <div className="space-y-2">
            {defectHistory.map((log) => (
              <div
                key={log.id}
                className="rounded-md border border-red-200/80 bg-white p-3 shadow-sm transition-all hover:bg-red-50/50"
              >
                <div className="flex items-center justify-between">
                  <p className="font-semibold text-gray-800">
                    제품 ID : {log.product_id}
                  </p>
                  <span className="text-xs text-gray-400">
                    {new Date(log.timestamp).toLocaleTimeString('ko-KR', {
                      hour: '2-digit',
                      minute: '2-digit',
                      second: '2-digit',
                    })}
                  </span>
                </div>
                <div className="mt-1 flex items-baseline justify-between">
                   <p className="text-sm text-red-600">
                    불량 의심 ({(log.prob * 100).toFixed(0)}%)
                  </p>
                  <button className="text-xs text-gray-500 hover:font-semibold hover:text-gray-700">
                    상세보기
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DefectHistoryPanel;
