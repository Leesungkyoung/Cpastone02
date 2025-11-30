import React from 'react';
import ReactDOM from 'react-dom/client';
// Import the App component, not the router
import App from './App'; 
import './styles/globals.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* Render the App component, which now contains the router provider */}
    <App />
  </React.StrictMode>
);
