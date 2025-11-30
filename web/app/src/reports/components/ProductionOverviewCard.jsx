import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import KpiCard from './KpiCard';

const ProductionOverviewCard = ({ data }) => {
  if (!data) return <div className="p-6 bg-white border rounded-xl shadow-sm animate-pulse h-full"></div>;

  const { chart_data, total_production, total_defects, defect_rate } = data.production_overview;

  return (
    <div className="p-6 bg-white border rounded-xl shadow-sm flex flex-col h-full">
      <h3 className="text-lg font-semibold text-gray-900">생산량 & 의심 건수 현황</h3>
      
      <div className="grid grid-cols-3 gap-4 my-6">
        <KpiCard title="기간 내 전체 생산량" value={total_production.toLocaleString()} unit="ea" />
        <KpiCard title="기간 내 불량 의심" value={total_defects.toLocaleString()} unit="건" valueColor="text-red-500" />
        <KpiCard title="기간 내 불량 의심률" value={`${defect_rate.toFixed(2)}%`} valueColor="text-red-500" />
      </div>

      <div className="flex-1 w-full min-h-0 flex items-center justify-center">
        <BarChart 
          width={500} 
          height={260} 
          data={chart_data} 
          margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="name" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis fontSize={12} tickLine={false} axisLine={false} />
          <Tooltip
            contentStyle={{
              borderRadius: '0.5rem',
              borderColor: '#e5e7eb',
              fontSize: '0.875rem'
            }}
          />
          <Legend wrapperStyle={{ fontSize: '0.875rem' }} />
          <Bar dataKey="정상 제품" fill="#81C784" name="정상 제품" />
          <Bar dataKey="불량 의심" fill="#f87171" name="불량 의심" />
        </BarChart>
      </div>
    </div>
  );
};

export default ProductionOverviewCard;
