import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const KpiCard = ({ title, value }) => (
  <div className="bg-gray-50 p-3 rounded-lg text-center border">
    <dt className="text-xs font-medium text-gray-500 truncate">{title}</dt>
    <dd className="mt-1 text-xl font-semibold text-gray-900">{value}</dd>
  </div>
);

const AlertQualityCard = ({ data }) => {
  if (!data || data.length === 0) {
    return <div>데이터가 없습니다.</div>;
  }

  // Calculate total KPIs
  const totalSuspected = data.reduce((acc, cur) => acc + (cur.total || 0), 0);
  const totalConfirmed = data.reduce((acc, cur) => acc + (cur['확정 불량'] || 0), 0);
  const totalFalseAlarm = data.reduce((acc, cur) => acc + (cur['오경보'] || 0), 0);
  
  const falseAlarmRate = totalSuspected > 0 ? ((totalFalseAlarm / totalSuspected) * 100).toFixed(1) + '%' : '0%';
  const resolvedCount = totalConfirmed + totalFalseAlarm;
  const resolutionRate = totalSuspected > 0 ? ((resolvedCount / totalSuspected) * 100).toFixed(1) + '%' : '0%';

  return (
    <div className="bg-white rounded-xl shadow-sm p-6 border h-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">조치 결과 기준 실제 불량 분석</h3>
      
      {/* KPIs */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <KpiCard title="불량 의심 건수" value={totalSuspected.toLocaleString()} />
        <KpiCard title="확정 불량 건수" value={totalConfirmed.toLocaleString()} />
        <KpiCard title="오경보 비율" value={falseAlarmRate} />
        <KpiCard title="조치 완료율" value={resolutionRate} />
      </div>

      {/* Chart */}
      <div style={{ height: '300px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
            <XAxis type="number" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis type="category" dataKey="name" fontSize={12} tickLine={false} axisLine={false} width={60} />
            <Tooltip
              contentStyle={{
                borderRadius: '0.5rem',
                boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
                border: '1px solid #e5e7eb'
              }}
            />
            <Legend wrapperStyle={{ fontSize: "14px" }} />
            <Bar dataKey="확정 불량" stackId="a" fill="#d32f2f" />
            <Bar dataKey="오경보" stackId="a" fill="#66bb6a" />
            <Bar dataKey="미조치" stackId="a" fill="#bdbdbd" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default AlertQualityCard;
