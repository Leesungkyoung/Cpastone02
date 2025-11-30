import { create } from "zustand";
import toast from 'react-hot-toast';
import React from 'react';
import DefectToast from '../monitor/components/DefectToast';
import { API_BASE_URL } from '../utils/config';

const DISPLAY_INTERVAL_MS = 2000; // Display a new card every 2 seconds

export const useStreamingStore = create((set, get) => ({
  logs: [],
  logQueue: [],
  productionCount: 0,
  defectCount: 0,
  isStreamFinished: false,
  isPopupOpen: false,
  popupData: null,
  intervalId: null,
  isInitialized: false,
  completedLogIds: new Set(),
  currentPath: '/',
  unconfirmedAlerts: [],
  navigationRequest: null,
  lastVisibleAt: null,
  defectHistory: [],

  setCurrentPath: (path) => set({ currentPath: path }),
  setLastVisibleAt: (timestamp) => set({ lastVisibleAt: timestamp }),

  handleNewDefect: (log) => {
    // This part remains unchanged: Add to history for the right-side panel
    set(state => ({
      defectHistory: [log, ...state.defectHistory]
    }));

    const currentPath = get().currentPath;
    if (currentPath === '/monitor') {
      // --- MODIFIED: Open the main popup if on the monitor page ---
      get().openPopup(log);
    } else {
      // This part remains unchanged: Show a toast if on other pages
      toast.custom((t) => (
        <DefectToast
          t={t}
          log={log}
          onClick={() => {
            get().requestNavigation('/monitor');

            // After requesting navigation, also set the log for the popup to open upon arrival.
            // This ensures clicking the toast leads directly to the popup.
            get().openPopup(log);

            toast.dismiss(t.id);
          }}
        />
      ));
    }
  },

  persistAndNotifyDefect: async (log) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/alerts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_id: log.product_id,
          timestamp: log.timestamp,
          prob: log.prob, // "prediction_score" -> "prob"
          top_sensors: log.top_sensors || [],
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to save alert to DB');
      }
      
      console.log("Simulated alert saved to DB successfully.");
    } catch (error) {
      console.error('Error persisting simulated alert:', error);
    } finally {
      // Whether successful or not, show the notification
      get().handleNewDefect(log);
    }
  },

  startDisplayLoop: () => {
    if (get().intervalId) {
      clearInterval(get().intervalId);
    }

    const displayInterval = setInterval(() => {
      const { logQueue } = get();
      if (logQueue.length === 0) {
        console.log('[Streaming Store] Finished displaying all logs.');
        clearInterval(displayInterval);
        set({ intervalId: null, isStreamFinished: true });
        return;
      }

      const nextLog = logQueue.shift();
      const processedLog = {
        ...nextLog,
        id: `${nextLog.product_id}-${new Date().getTime()}`,
        createdAt: Date.now(),
      };

      set(state => ({
        logs: [processedLog, ...state.logs],
        logQueue: state.logQueue,
      }));
    }, DISPLAY_INTERVAL_MS);

    set({ intervalId: displayInterval });
  },
  
  stopStreaming: () => {
    if (get().intervalId) {
      console.log('[Streaming Store] stopStreaming called');
      clearInterval(get().intervalId);
      set({ intervalId: null, isStreamFinished: true });
    }
  },

  addLog: (newLog) => set((state) => ({ logs: [newLog, ...state.logs] })),

  markLogAsCompleted: (logId) => {
    set((state) => ({
      completedLogIds: new Set(state.completedLogIds).add(logId),
    }));
  },

  incrementProductionCount: () => set((state) => ({ productionCount: state.productionCount + 1 })),
  incrementDefectCount: () => set((state) => ({ defectCount: state.defectCount + 1 })),

  // These actions for popup state are already well-defined and will be reused.
  openPopup: (data) => set({ isPopupOpen: true, popupData: data }),
  
  closePopup: () => {
    set({ isPopupOpen: false, popupData: null });
    // Also clear the unconfirmed alerts queue, as the popup is the confirmation mechanism.
    get().confirmAlerts();
  },

  initializeAndStartStream: async () => {
    if (get().isInitialized) return;

    set({
      logs: [],
      logQueue: [],
      isStreamFinished: false,
      isInitialized: true,
      productionCount: 0,
      defectCount: 0,
      completedLogIds: new Set(),
      unconfirmedAlerts: [],
      defectHistory: [],
      intervalId: null,
    });

    console.log("Initializing stream: clearing previous demo data...");

    try {
      // First, clear any alert data from the previous demo session
      await fetch(`${API_BASE_URL}/api/reset_demo`, { method: 'DELETE' });

      console.log("Fetching historical demo data for playback...");
      const res = await fetch(`${API_BASE_URL}/api/stream/all_rows`);
      if (!res.ok) {
        throw new Error(`API request failed with status ${res.status}`);
      }
      const allLogs = await res.json();
      
      // Simulate random defects on the frontend for demonstration
      const logsWithSimulatedDefects = allLogs.map(log => {
        // Roughly 15% chance of being a defect
        const isDefect = Math.random() < 0.15;
        if (isDefect) {
          return {
            ...log,
            pred: 1, // Mark as defective
            // Simulate a high score between 0.70 and 0.91
            prob: 0.7 + Math.random() * 0.21, 
            top_sensors: ['sensor_015', 'sensor_253', 'sensor_119', 'sensor_488', 'sensor_301'].sort(() => 0.5 - Math.random()).slice(0, 3),
          };
        } else {
          return {
            ...log,
            pred: 0, // Mark as normal
            prob: 0.1 + Math.random() * 0.2, // Simulate a low score
            top_sensors: [],
          };
        }
      });

      set({ logQueue: logsWithSimulatedDefects });
      
      get().startDisplayLoop();
    } catch (error) {
      console.error("Error initializing historical stream:", error);
      set({ isInitialized: false });
    }
  },

  requestNavigation: (path) => set({ navigationRequest: { path } }),
  clearNavigationRequest: () => set({ navigationRequest: null }),
  
  confirmAlerts: () => set({ unconfirmedAlerts: [] }),
}));
