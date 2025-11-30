import React, { useMemo } from 'react';
import MonthlyChartCard from './MonthlyChartCard';

const MonthlyBreakdownView = ({ data, sortOrder }) => {
  const sortedData = useMemo(() => {
    if (!data) return [];
    const dataCopy = [...data];
    if (sortOrder === 'latest') {
      return dataCopy.sort((a, b) => b.month.localeCompare(a.month));
    }
    return dataCopy.sort((a, b) => a.month.localeCompare(b.month));
  }, [data, sortOrder]);

  if (!data) {
    return (
      <div className="space-y-6">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl shadow-sm p-6 border animate-pulse h-96"></div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {sortedData.map(monthData => (
        <MonthlyChartCard key={monthData.month} monthData={monthData} />
      ))}
    </div>
  );
};

export default MonthlyBreakdownView;
