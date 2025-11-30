import { useState, useEffect, useCallback } from 'react';
import ReportsFilterBar from '../components/ReportsFilterBar';
import MonthlyHistoryView from '../components/MonthlyHistoryView';
import MonthlyBreakdownView from '../components/MonthlyBreakdownView';
import ProductionOverviewCard from '../components/ProductionOverviewCard';
import AlertQualityCard from '../components/AlertQualityCard';
import useReportsStore from '../../store/reportsStore';
import reportsData, { getDailyDataForMonth } from '../data/reportsData';
import { API_BASE_URL } from '../../utils/config';

const ReportsPage = () => {
  const [processedData, setProcessedData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isMonthDropdownOpen, setMonthDropdownOpen] = useState(false);

  const { filters, setFilters } = useReportsStore();
  const { periodType, selectedMonth, sortOrder } = filters;

  const processData = useCallback((currentFilters) => {
    setLoading(true);
    setError(null);
    try {
      if (currentFilters.periodType === 'summary') {
        const months = Object.keys(reportsData);
        const monthlyBarChartData = months.map(month => {
            const summary = reportsData[month].summary;
            return {
                name: month,
                '정상 제품': summary.total_production - summary.total_defects,
                '불량 의심': summary.total_defects,
                '확정 불량': summary.confirmed_defects,
                '오경보': summary.false_alarms,
                '미조치': summary.unresolved || 0,
            };
        });

        const totalSummary = months.reduce((acc, month) => {
            const summary = reportsData[month].summary;
            acc.total_production += summary.total_production;
            acc.total_defects += summary.total_defects;
            acc.confirmed_defects += summary.confirmed_defects;
            acc.false_alarms += summary.false_alarms;
            return acc;
        }, { total_production: 0, total_defects: 0, confirmed_defects: 0, false_alarms: 0 });

        const totalResolved = totalSummary.confirmed_defects + totalSummary.false_alarms;
        const unresolved = totalSummary.total_defects - totalResolved;

        const dataForCards = {
            production_overview: {
                total_production: totalSummary.total_production,
                total_defects: totalSummary.total_defects,
                defect_rate: totalSummary.total_production > 0 ? (totalSummary.total_defects / totalSummary.total_production) * 100 : 0,
                chart_data: monthlyBarChartData,
            },
            alert_quality: {
                total_defects: totalSummary.total_defects,
                confirmed_defects: totalSummary.confirmed_defects,
                false_alarms: totalSummary.false_alarms,
                unresolved: unresolved,
                resolution_rate: totalSummary.total_defects > 0 ? (totalResolved / totalSummary.total_defects) * 100 : 0,
                false_alarm_rate: totalSummary.total_defects > 0 ? (totalSummary.false_alarms / totalSummary.total_defects) * 100 : 0,
                chart_data: monthlyBarChartData,
            },
        };
        setProcessedData({ type: 'summary', data: dataForCards });
      } else if (['weekly', 'daily'].includes(currentFilters.periodType)) {
        const monthsToProcess = ['2008-07', '2008-08', '2008-09', '2008-10'];
        const breakdownData = monthsToProcess.map(month => {
          const monthData = reportsData[month];
          const chartData = currentFilters.periodType === 'weekly'
            ? monthData.weekly
            : getDailyDataForMonth(month);
          return {
            month: month,
            data: {
              production_overview: { ...monthData.summary, chart_data: chartData },
              alert_quality: { ...monthData.summary, chart_data: chartData },
            }
          };
        });
        setProcessedData({ type: 'breakdown', data: breakdownData });
      } else { // 'monthly'
        const months = Object.keys(reportsData);
        const monthlyChartData = months.map(month => {
          const summary = reportsData[month].summary;
          return {
            name: month,
            '정상 제품': summary.total_production - summary.total_defects,
            '불량 의심': summary.total_defects,
            '확정 불량': summary.confirmed_defects,
            '오경보': summary.false_alarms,
            '미조치': summary.unresolved,
          };
        });
        setProcessedData({ type: 'history', data: monthlyChartData });
      }
    } catch (err) {
      setError('리포트 데이터를 구성하는 중 오류가 발생했습니다.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    processData(filters);
  }, [filters, processData]);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const renderContent = () => {
    if (loading) return <div>Loading...</div>;
    if (error) return <div className="text-red-500">{error}</div>;
    if (!processedData) return null;

    if (processedData.type === 'summary') {
      return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ProductionOverviewCard data={processedData.data} />
          <AlertQualityCard data={processedData.data} />
        </div>
      );
    }

    if (processedData.type === 'breakdown') {
      const filteredBreakdownData = 
        selectedMonth === 'all'
          ? processedData.data
          : processedData.data.filter(item => item.month === selectedMonth);
      return <MonthlyBreakdownView data={filteredBreakdownData} sortOrder={sortOrder} />;
    }

    if (processedData.type === 'history') {
      const filteredMonthlyData =
        selectedMonth !== 'all'
          ? processedData.data.filter((monthData) => monthData.name === selectedMonth)
          : processedData.data;
      return <MonthlyHistoryView data={filteredMonthlyData} sortOrder={sortOrder} />;
    }
    
    return null;
  };
  
  return (
    <div className="p-6 bg-gray-50 h-full flex flex-col">
       <ReportsFilterBar
        filters={filters}
        onChange={handleFilterChange}
        isMonthDropdownOpen={isMonthDropdownOpen}
        setMonthDropdownOpen={setMonthDropdownOpen}
      />
      <div className="mt-6 flex-1 min-h-0 overflow-y-auto max-h-[680px]">
        {renderContent()}
      </div>
    </div>
  );
};

export default ReportsPage;
