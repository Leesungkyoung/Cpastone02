import React, { useState, useEffect } from 'react';
import { useStreamingStore } from '../../store/streamingStore.jsx';

/**
 * A component to display a single streaming log item with step-by-step animation.
 * It manages its own animation state and triggers a popup on defect detection.
 */
const StreamingLogItem = ({ log }) => {
  // ✅ CORRECT PATTERN: Select each state/action individually to prevent infinite loops.
  const markLogAsCompleted = useStreamingStore((state) => state.markLogAsCompleted);
  const isCompleted = useStreamingStore((state) => state.completedLogIds.has(log.id));
  const incrementProductionCount = useStreamingStore((state) => state.incrementProductionCount);
  const incrementDefectCount = useStreamingStore((state) => state.incrementDefectCount);
  // Get the new centralized defect handler
  const persistAndNotifyDefect = useStreamingStore((state) => state.persistAndNotifyDefect);
  const lastVisibleAt = useStreamingStore((state) => state.lastVisibleAt);

  // --- MODIFIED: Determine rendering mode ---
  // If the log was created while the user was away, or if its animation is already complete,
  // skip the animation and render the final state immediately.
  const isCatchUp = lastVisibleAt && log.createdAt < lastVisibleAt;
  const shouldAnimate = !isCompleted && !isCatchUp;

  const [visibleStep, setVisibleStep] = useState(shouldAnimate ? 1 : 4);

  const { product_id, timestamp, pred, prob } = log;
  const isDefect = pred === 1;

  useEffect(() => {
    // Only run the animation if it's a new, "live" log.
    if (shouldAnimate) {
      const timers = [
        setTimeout(() => setVisibleStep(2), 1000),
        setTimeout(() => setVisibleStep(3), 2000),
        setTimeout(() => {
          setVisibleStep(4);
          
          incrementProductionCount();
          if (isDefect) {
            incrementDefectCount();
            // Call the new handler to persist the alert and then notify the UI
            persistAndNotifyDefect(log); 
          }
          // Mark this log as completed in the global store.
          markLogAsCompleted(log.id);
        }, 3000),
      ];
      
      return () => timers.forEach(clearTimeout);
    }
    // The dependencies are correct and ensure the effect only runs when necessary.
  }, [log, isDefect, persistAndNotifyDefect, incrementProductionCount, incrementDefectCount, isCompleted, markLogAsCompleted, shouldAnimate]);
  
  // Create a new Date object from the timestamp
  const dateObj = new Date(timestamp);

  // Format the date as YYYY.MM.DD
  const displayDate = `${dateObj.getFullYear()}.${String(dateObj.getMonth() + 1).padStart(2, '0')}.${String(dateObj.getDate()).padStart(2, '0')}`;

  // Format the time as HH:MM:SS
  const displayTime = dateObj.toLocaleTimeString('ko-KR', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });

  const percentage = prob ? Math.round(prob * 100) : 0;

  // CSS classes for different steps
  const stepBaseClass = "text-xs text-gray-600";
  const finalStepNormalClass = "text-xs font-semibold text-green-600";
  const finalStepDefectClass = "text-xs font-semibold text-red-600";

  return (
    // Add the 'animate-fade-in' class to the root element
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 px-4 py-3 animate-fade-in">
      {/* --- Common Header --- */}
      <div className="flex justify-between items-center mb-3">
        <p className="text-sm font-semibold text-gray-800">제품 ID : {product_id}</p>
        <div className="text-right">
          <p className="text-xs text-gray-500">생산 날짜 : {displayDate}</p>
          <p className="text-xs text-gray-500">생산 시간 : {displayTime}</p>
        </div>
      </div>
      
      {/* --- Step-by-step Messages --- */}
      <div className="space-y-1.5">
        {visibleStep >= 1 && <p className={stepBaseClass}>[ 생산 시작 ]</p>}
        {visibleStep >= 2 && <p className={stepBaseClass}>[ 공정 데이터 수집 중 ]</p>}
        {visibleStep >= 3 && <p className={stepBaseClass}>[ 품질 검사 중 ]</p>}
        {visibleStep >= 4 && (
          <p className={isDefect ? finalStepDefectClass : finalStepNormalClass}>
            {isDefect
              ? `[ ⚠ 최종 판정: 불량 (${percentage}%) ]`
              : `[ 최종 판정: 정상 ]`}
          </p>
        )}
      </div>
    </div>
  );
};

export default StreamingLogItem;
