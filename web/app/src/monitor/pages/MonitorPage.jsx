import React, { useEffect } from 'react';
import StreamingLogBox from '../components/StreamingLogBox';
import AlertPopup from '../components/AlertPopup';
import IntegratedKPIHeader from '../components/IntegratedKPIHeader';
import DefectHistoryPanel from '../components/DefectHistoryPanel';
import { useStreamingStore } from '../../store/streamingStore';

const MonitorPage = () => {
  // --- MODIFIED: Subscribe to all necessary states and actions from the store ---
  const productionCount = useStreamingStore((state) => state.productionCount);
  const defectCount = useStreamingStore((state) => state.defectCount);
  const popupData = useStreamingStore((state) => state.popupData);
  const isPopupOpen = useStreamingStore((state) => state.isPopupOpen);
  const closePopup = useStreamingStore((state) => state.closePopup);
  const confirmAlerts = useStreamingStore((state) => state.confirmAlerts);

  // The confirmation handler is now simpler.
  // The alert is already persisted when the defect is detected.
  const handleConfirmAlert = () => {
    confirmAlerts(); // Acknowledge the alert
    closePopup();    // Close the UI
  };

  return (
    <>
      {/* --- MODIFIED: Pass state down to the AlertPopup component --- */}
      <AlertPopup 
        isOpen={isPopupOpen}
        alertData={popupData}
        onConfirm={handleConfirmAlert} 
        onClose={closePopup}
      />
      <div className="flex flex-col space-y-6">
        <IntegratedKPIHeader productionCount={productionCount} defectCount={defectCount} />
        <div className="grid grid-cols-3 gap-6">
          <div className="col-span-2">
            <StreamingLogBox />
          </div>
          <div className="col-span-1">
            <DefectHistoryPanel />
          </div>
        </div>
      </div>
    </>
  );
};

export default MonitorPage;
