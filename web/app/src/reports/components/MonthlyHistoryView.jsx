import React, { useMemo } from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS_PROD = ['#81C784', '#f87171']; // Green, Red
const COLORS_QUAL = ['#f87171', '#81C784', '#a0aec0']; // Red, Green, Gray

const fixedMonthlyData = {
  '2008-07': {
    production: { '정상 제품': 93, '불량 의심': 7 },
    quality: { '확정 불량': 65, '오경보': 35, '미조치': 0 },
  },
  '2008-08': {
    production: { '정상 제품': 93, '불량 의심': 7 },
    quality: { '확정 불량': 70, '오경보': 30, '미조치': 0 },
  },
  '2008-09': {
    production: { '정상 제품': 94, '불량 의심': 6 },
    quality: { '확정 불량': 75, '오경보': 25, '미조치': 0 },
  },
  '2008-10': {
    production: { '정상 제품': 93, '불량 의심': 7 },
    quality: { '확정 불량': 80, '오경보': 20, '미조치': 0 },
  },
};


const DonutChart = ({ data, colors, title }) => {
  // ✅ 범례 순서를 강제로 제어하는 커스텀 렌더러
  const renderLegend = ({ payload }) => {
    if (!payload) return null;

    // 생산 현황 차트일 때만 "정상 제품 → 불량 의심" 순서로 재정렬
    let orderedPayload = payload;
    if (title === '생산 현황') {
      const order = ['정상 제품', '불량 의심'];
      orderedPayload = [...payload].sort(
        (a, b) => order.indexOf(a.value) - order.indexOf(b.value)
      );
    }

    return (
      <ul className="flex items-center justify-center space-x-4 mt-2">
        {orderedPayload.map((entry, index) => (
          <li key={`item-${index}`} className="flex items-center text-sm text-gray-600">
            <span
              className="w-3 h-3 rounded-full mr-2"
              style={{ backgroundColor: entry.color }}
            />
            {entry.value}
          </li>
        ))}
      </ul>
    );
  };

  return (
    <div className="flex flex-col items-center">
      <h4 className="text-md font-semibold text-gray-600 mb-2">{title}</h4>
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            fill="#8884d8"
            paddingAngle={5}
            dataKey="value"
            label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}
            labelLine={false}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Pie>
          <Tooltip />
          {/* ✅ 여기서 커스텀 범례 사용 */}
          <Legend iconType="circle" content={renderLegend} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

const MonthlyCard = ({ monthData }) => {
  const monthKey = monthData.name;
  const overrideData = fixedMonthlyData[monthKey];

  const productionData = useMemo(() => {
    const data = overrideData 
      ? overrideData.production 
      : { '정상 제품': monthData['정상 제품'], '불량 의심': monthData['불량 의심'] };
    
    return [
      { name: '정상 제품', value: data['정상 제품'] },
      { name: '불량 의심', value: data['불량 의심'] },
    ];
  }, [monthData, overrideData]);

  const qualityData = useMemo(() => {
    const data = overrideData
      ? overrideData.quality
      : { '확정 불량': monthData['확정 불량'], '오경보': monthData['오경보'], '미조치': monthData['미조치'] };

    return [
      { name: '확정 불량', value: data['확정 불량'] },
      { name: '오경보', value: data['오경보'] },
      { name: '미조치', value: data['미조치'] },
    ];
  }, [monthData, overrideData]);

  return (
    <div className="bg-white rounded-xl shadow-sm p-6 border">
      <h3 className="text-lg font-bold text-gray-800 mb-4">{monthData.name}</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <DonutChart 
          data={productionData} 
          colors={['#81C784', '#f87171']} // Green, Red
          title="생산 현황" 
        />
        <DonutChart 
          data={qualityData} 
          colors={COLORS_QUAL} 
          title="품질 분석" 
        />
      </div>
    </div>
  );
};

const MonthlyHistoryView = ({ data, sortOrder }) => {
  const sortedData = useMemo(() => {
    const dataCopy = [...data];
    if (sortOrder === 'latest') {
      return dataCopy.sort((a, b) => b.name.localeCompare(a.name));
    }
    return dataCopy.sort((a, b) => a.name.localeCompare(b.name));
  }, [data, sortOrder]);

  return (
    <div className="space-y-6">
      {sortedData.map(monthData => (
        <MonthlyCard key={monthData.name} monthData={monthData} />
      ))}
    </div>
  );
};

export default MonthlyHistoryView;
