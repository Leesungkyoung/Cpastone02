import React, { useState, useEffect } from 'react';

const ReportsPage = () => {
  const [viewMode, setViewMode] = useState('summary'); // 'summary' | 'time'
  const [periodType, setPeriodType] = useState('monthly'); // 'monthly' | 'weekly' | 'daily' | 'all'
  const [selectedMonth, setSelectedMonth] = useState(11); // Default to November
  const [sortOrder, setSortOrder] = useState('latest');

  // TODO: Fetch and process data based on filters
  // const [summaryData, setSummaryData] = useState(null);
  // const [hourlyData, setHourlyData] = useState(null);

  useEffect(() => {
    // This effect will re-run whenever filters change
    console.log('Filters changed:', { viewMode, periodType, selectedMonth, sortOrder });
    // Fetch mock data here in a later step
  }, [viewMode, periodType, selectedMonth, sortOrder]);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">분석 리포트</h2>
      
      {/* Filter Bar - To be created */}
      <div className="p-4 border rounded-lg bg-gray-50 text-sm text-gray-500">
        ReportsFilterBar Component will go here.
      </div>

      {/* Conditional content based on viewMode */}
      {viewMode === 'summary' ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Summary View: Left Card */}
          <div className="p-4 border rounded-lg bg-white shadow-sm">
            ProductionOverviewCard will go here.
          </div>
          {/* Summary View: Right Card */}
          <div className="p-4 border rounded-lg bg-white shadow-sm">
            AlertQualityCard will go here.
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Time-based View: Left Card */}
          <div className="p-4 border rounded-lg bg-white shadow-sm">
            HourlyPatternChart will go here.
          </div>
          {/* Time-based View: Right Card */}
          <div className="p-4 border rounded-lg bg-white shadow-sm">
            PatternSummaryCard will go here.
          </div>
        </div>
      )}
    </div>
  );
};

export default ReportsPage;
