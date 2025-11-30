import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStreamingStore } from '../../store/streamingStore.jsx';

/**
 * A headless component that listens for navigation requests from the Zustand store
 * and performs programmatic navigation using React Router's useNavigate hook.
 */
const NavigationHandler = () => {
  const navigate = useNavigate();
  // ✅ CORRECT PATTERN: Select each state/action individually to prevent infinite loops.
  const navigationRequest = useStreamingStore((state) => state.navigationRequest);
  const clearNavigationRequest = useStreamingStore((state) => state.clearNavigationRequest);

  useEffect(() => {
    if (navigationRequest) {
      navigate(navigationRequest.path);
      clearNavigationRequest(); // Reset the request after navigation
    }
  }, [navigationRequest, navigate, clearNavigationRequest]);

  return null; // This component does not render anything
};

export default NavigationHandler;
