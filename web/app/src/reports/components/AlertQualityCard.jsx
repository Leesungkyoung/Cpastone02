import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import KpiCard from './KpiCard';

const AlertQualityCard = ({ data }) => {
  if (!data) return <div className="p-6 bg-white border rounded-xl shadow-sm animate-pulse h-full"></div>;
  
  const { chart_data, total_defects, confirmed_defects, resolution_rate, false_alarm_rate } = data.alert_quality;

  return (
    <div className="p-6 bg-white border rounded-xl shadow-sm flex flex-col h-full">
      <h3 className="text-lg font-semibold text-gray-900">조치 결과 기준 실제 불량 분석</h3>
      
      <div className="grid grid-cols-4 gap-4 my-6">
        <KpiCard title="기간 내 의심 건수" value={total_defects.toLocaleString()} unit="건" />
        <KpiCard title="확정 불량" value={confirmed_defects.toLocaleString()} unit="건" valueColor="text-red-500" />
        <KpiCard title="조치 완료율" value={`${resolution_rate.toFixed(1)}%`} valueColor="text-green-500" />
        <KpiCard title="오경보 비율" value={`${false_alarm_rate.toFixed(1)}%`} />
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
          <Bar dataKey="미조치" stackId="a" fill="#a0aec0" name="미조치" />
          <Bar dataKey="오경보" stackId="a" fill="#81C784" name="오경보" />
          <Bar dataKey="확정 불량" stackId="a" fill="#f87171" name="확정 불량" />
        </BarChart>
      </div>
    </div>
  );
};

export default AlertQualityCard;
