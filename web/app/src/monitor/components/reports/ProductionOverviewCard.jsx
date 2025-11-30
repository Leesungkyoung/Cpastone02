import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const KpiCard = ({ title, value }) => (
  <div className="bg-gray-50 p-4 rounded-lg text-center border">
    <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
    <dd className="mt-1 text-2xl font-semibold text-gray-900">{value}</dd>
  </div>
);

const ProductionOverviewCard = ({ data }) => {
  if (!data || data.length === 0) {
    return <div>데이터가 없습니다.</div>;
  }
  
  // Calculate total KPIs from the aggregated data
  const totalProduction = data.reduce((acc, cur) => acc + (cur.total || 0), 0);
  const totalSuspected = data.reduce((acc, cur) => acc + (cur.suspected || 0), 0);
  const defectRate = totalProduction > 0 ? ((totalSuspected / totalProduction) * 100).toFixed(1) + '%' : '0%';

  return (
    <div className="bg-white rounded-xl shadow-sm p-6 border h-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">생산량 & 의심 건수</h3>
      
      {/* KPIs */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <KpiCard title="전체 생산량" value={totalProduction.toLocaleString()} />
        <KpiCard title="불량 의심 총 건수" value={totalSuspected.toLocaleString()} />
        <KpiCard title="불량 의심률" value={defectRate} />
      </div>

      {/* Chart */}
      <div style={{ height: '300px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="name" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis fontSize={12} tickLine={false} axisLine={false} />
            <Tooltip
              contentStyle={{
                borderRadius: '0.5rem',
                boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
                border: '1px solid #e5e7eb'
              }}
            />
            <Legend wrapperStyle={{ fontSize: "14px" }} />
            <Bar dataKey="normal" name="정상" stackId="a" fill="#22c55e" radius={[4, 4, 0, 0]} />
            <Bar dataKey="suspected" name="불량 의심" stackId="a" fill="#ef4444" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ProductionOverviewCard;
