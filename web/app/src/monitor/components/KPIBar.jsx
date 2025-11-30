import React from 'react';
import { ShieldExclamationIcon, StopCircleIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';

const KPIBar = ({ productionCount, defectCount, onNavigateAlerts }) => {
  const dailyGoal = 554;
  const navigate = useNavigate();

  return (
    <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
      <div className="flex justify-between items-center">
        {/* KPIs */}
        <div className="flex items-center space-x-8">
          <div className="text-center">
            <p className="text-sm text-gray-500">월간 생산 목표</p>
            <p className="text-2xl font-bold text-gray-800">{dailyGoal.toLocaleString()}</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-500">오늘 생산 실적</p>
            <p className="text-2xl font-bold text-green-600">{productionCount.toLocaleString()}</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-500">오늘 품질 경보</p>
            <p className="text-2xl font-bold text-red-600">{defectCount.toLocaleString()}</p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center space-x-3">
          <button 
            onClick={() => navigate('/alerts')}
            className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-200 transition-colors"
          >
            <ShieldExclamationIcon className="w-5 h-5 mr-2" />
            불량 의심 이력 보기
          </button>
          <button className="flex items-center px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-md hover:bg-red-700 transition-colors">
            <StopCircleIcon className="w-5 h-5 mr-2" />
            긴급 중단
          </button>
        </div>
      </div>
    </div>
  );
};

export default KPIBar;
