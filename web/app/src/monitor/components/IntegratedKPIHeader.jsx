import React from 'react';
import { useNavigate } from 'react-router-dom';

const KPI = ({ title, value, unit, colorClass = 'text-gray-900' }) => (
  <div className="relative">
    <dt>
      <p className="text-sm font-medium text-gray-500 truncate">{title}</p>
    </dt>
    <dd className="mt-1 flex items-baseline">
      <p className={`text-2xl font-semibold ${colorClass}`}>{value}</p>
      {unit && <p className="ml-2 text-sm font-medium text-gray-500">{unit}</p>}
    </dd>
  </div>
);

const IntegratedKPIHeader = ({ productionCount, defectCount }) => {
  const navigate = useNavigate();

  return (
    <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
      <div className="flex items-center">
        {/* Left Side: KPIs */}
        <div className="flex items-center space-x-8">
          <KPI title="월간 생산 목표" value="554" />
          <div className="border-l border-gray-200 h-10"></div>
          <KPI title="오늘 생산 실적" value={productionCount} colorClass="text-green-600" />
          <div className="border-l border-gray-200 h-10"></div>
          <KPI title="오늘 품질 경보" value={defectCount} colorClass="text-red-600" />
        </div>

        {/* Right Side: Buttons - pushed to the right with ml-auto */}
        <div className="flex items-center space-x-3 ml-auto">
          <button
            onClick={() => navigate('/alerts')}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            불량 의심 이력 보기
          </button>
          <button
            className="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            긴급 정지
          </button>
        </div>
      </div>
    </div>
  );
};

export default IntegratedKPIHeader;
