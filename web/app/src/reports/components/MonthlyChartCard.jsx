import React from 'react';
import ProductionOverviewCard from './ProductionOverviewCard';
import AlertQualityCard from './AlertQualityCard';

const MonthlyChartCard = ({ monthData }) => {
  if (!monthData || !monthData.data) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6 border animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm p-6 border">
      <h3 className="text-lg font-bold text-gray-800 mb-4">{monthData.month}</h3>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ProductionOverviewCard data={monthData.data} />
        <AlertQualityCard data={monthData.data} />
      </div>
    </div>
  );
};

export default MonthlyChartCard;
