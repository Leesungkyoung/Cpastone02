import React, { useEffect } from 'react';
import { createBrowserRouter, Outlet, RouterProvider, useLocation } from 'react-router-dom';
import { Toaster } from 'react-hot-toast'; // Import the Toaster component
import { useStreamingStore } from './store/streamingStore.jsx'; // Updated import path
import NavigationHandler from './monitor/layout/NavigationHandler.jsx'; // Import the handler
import LandingPage from './landing/pages/LandingPage.jsx';
import TopHeader from './monitor/layout/TopHeader.jsx';
import TabNavigation from './monitor/layout/TabNavigation.jsx';
import MonitorPage from './monitor/pages/MonitorPage.jsx';
import AlertsPage from './monitor/pages/AlertsPage.jsx';
import ReportsPage from './reports/pages/ReportsPage.jsx'; // Import the new page
import SettingsPage from './monitor/pages/SettingsPage.jsx';

const MonitorLayout = () => {
  const location = useLocation();
  // ✅ CORRECT PATTERN: Select each state/action individually to prevent infinite loops.
  const setCurrentPath = useStreamingStore((state) => state.setCurrentPath);
  const closePopup = useStreamingStore((state) => state.closePopup);
  const isPopupOpen = useStreamingStore((state) => state.isPopupOpen);

  useEffect(() => {
    setCurrentPath(location.pathname);

    // If navigating away from the monitor page while a popup is open, close it.
    if (location.pathname !== '/monitor' && isPopupOpen) {
      closePopup();
    }
  }, [location, setCurrentPath, closePopup, isPopupOpen]);

  return (
    // Revert to min-h-screen and remove flex properties that caused the layout break
    <div className="min-h-screen bg-gray-50">
      <NavigationHandler /> {/* Render the headless navigation handler */}
      {/* Toaster component for global notifications */}
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />
      <TopHeader />
      <TabNavigation />
      {/* 
        Re-introduce the padding-top to offset the fixed headers.
        - TopHeader is ~88px (py-4 = 16px*2 + line-height). Let's use h-22 from Tailwind (~88px).
        - TabNavigation is positioned 88px from the top and has a height of h-14 (56px).
        - Total height occupied = 88px (TopHeader) + 56px (TabNav) + extra space for visual separation.
        - The original `pt-[168px]` seems appropriate. 
        - 88px (Header) + 56px (Nav) = 144px. The extra 24px is the gap.
      */}
      <main className="pt-[168px]">
        <div className="mx-auto w-[95%] max-w-8xl">
            {/* The white background and shadow are now applied here again */}
            <div className="rounded-xl bg-white p-6 shadow">
              <Outlet />
            </div>
        </div>
      </main>
    </div>
  );
};

const router = createBrowserRouter([
  {
    path: '/',
    element: <LandingPage />,
  },
  {
    path: '/',
    element: <MonitorLayout />,
    children: [
      { path: 'monitor', element: <MonitorPage /> },
      { path: 'alerts', element: <AlertsPage /> },
      { path: 'reports', element: <ReportsPage /> }, // Re-add the new route
      { path: 'settings', element: <SettingsPage /> },
    ],
  },
]);

// This will be our new root component where we can safely initialize the app.
function App() {
  // CORRECT: Select the function reference, don't call it.
  const initializeAndStartStream = useStreamingStore(
    (state) => state.initializeAndStartStream
  );

  // CORRECT: Call the action inside a useEffect with an empty dependency array
  // to ensure it runs only once when the app mounts.
  useEffect(() => {
    initializeAndStartStream();
  }, [initializeAndStartStream]);

  // The router is now rendered by this component.
  return <RouterProvider router={router} />;
}

// We now export the App component instead of the router directly.
export default App;
