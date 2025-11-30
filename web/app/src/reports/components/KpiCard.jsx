import React from 'react';

const KpiCard = ({ title, value, unit, valueColor }) => (
  <div className="text-center">
    <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
    <dd className={`mt-1 text-3xl font-bold tracking-tight ${valueColor || 'text-gray-900'}`}>{value}{unit && <span className="ml-1 text-base font-medium">{unit}</span>}</dd>
  </div>
);

export default KpiCard;
