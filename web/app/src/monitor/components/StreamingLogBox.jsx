import React, { useRef, useEffect } from 'react';
import { useStreamingStore } from '../../store/streamingStore.jsx';
import StreamingLogItem from './StreamingLogItem';

const StreamingLogBox = ({ onDefectDetected }) => {
  // Directly use the logs from the global store. No more local display state.
  const allLogs = useStreamingStore((state) => state.logs);
  const isStreamFinished = useStreamingStore((state) => state.isStreamFinished);
  const logContainerRef = useRef(null);

  // The local queue and displayLogs logic has been removed to ensure
  // the component is stateless and always reflects the global store.

  // Auto-scroll to the top when a new log is added
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = 0;
    }
  }, [allLogs]);

  return (
    // The fixed height remains to ensure layout consistency.
    <div className="flex h-[620px] flex-col rounded-lg bg-[#F8F9FA] shadow-sm border border-gray-200 p-4">
      <h3 className="flex-shrink-0 text-sm font-semibold text-gray-500 border-b border-gray-200 pb-2 mb-4">
        실시간 생산 제품 모니터링
      </h3>
      <div ref={logContainerRef} className="flex-1 space-y-3 overflow-y-auto pr-2">
        {allLogs.length === 0 && !isStreamFinished ? (
          // Empty State (Unchanged)
          <div className="flex h-full flex-col items-center justify-center py-10 text-center">
            <div className="mb-4 rounded-full bg-gray-100 px-4 py-1.5 text-sm font-medium text-gray-500">
              생산 대기 중
            </div>
            <p className="text-lg font-semibold text-gray-500">
              현재 생산 라인이 비가동 상태입니다.
            </p>
            <p className="mt-2 text-sm text-gray-500/80">
              라인이 가동되면 실시간 모니터링이 자동으로 시작됩니다.
            </p>
          </div>
        ) : (
          // Render all logs directly from the global store
          allLogs.map((log) => (
            <StreamingLogItem key={log.id} log={log} onDefectDetected={onDefectDetected} />
          ))
        )}
        {isStreamFinished && allLogs.length > 0 && (
          <div className="p-3 mt-3 rounded-md text-center text-sm text-gray-500 bg-gray-100 border border-gray-200">
            스트리밍이 종료되었습니다.
          </div>
        )}
      </div>
    </div>
  );
};

export default StreamingLogBox;
