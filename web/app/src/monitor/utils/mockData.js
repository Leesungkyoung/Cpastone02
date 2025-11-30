// This utility generates plausible mock data for the reports page.

// Helper function to get the number of days in a given month (for a non-leap year)
const getDaysInMonth = (month) => {
  return new Date(2023, month, 0).getDate();
};

// --- Summary View Data Generators ---

/**
 * Generates data for the "Production & Suspected Defects" overview chart.
 * @param {string} periodType - 'monthly', 'weekly', 'daily', 'all'
 * @param {number} selectedMonth - 1-12
 * @returns {Array} Data formatted for Recharts BarChart
 */
export const generateProductionSummary = (periodType, selectedMonth) => {
  if (periodType === 'all') {
    const totalProduction = Math.floor(Math.random() * 5000) + 10000;
    const suspected = Math.floor(totalProduction * (Math.random() * 0.05 + 0.02));
    const normal = totalProduction - suspected;
    return [{ name: '전체 기간', normal, suspected, total: totalProduction }];
  }

  if (periodType === 'monthly') {
    return Array.from({ length: 12 }, (_, i) => {
      const totalProduction = Math.floor(Math.random() * 800) + 1000;
      const suspected = Math.floor(totalProduction * (Math.random() * 0.05 + 0.01));
      const normal = totalProduction - suspected;
      return { name: `${i + 1}월`, normal, suspected, total: totalProduction };
    });
  }

  if (periodType === 'weekly') {
    return Array.from({ length: 5 }, (_, i) => {
      const totalProduction = Math.floor(Math.random() * 200) + 250;
      const suspected = Math.floor(totalProduction * (Math.random() * 0.06 + 0.02));
      const normal = totalProduction - suspected;
      return { name: `${i + 1}주차`, normal, suspected, total: totalProduction };
    });
  }

  if (periodType === 'daily') {
    const days = getDaysInMonth(selectedMonth);
    return Array.from({ length: days }, (_, i) => {
      const totalProduction = Math.floor(Math.random() * 20) + 30;
      const suspected = Math.floor(totalProduction * (Math.random() * 0.08 + 0.02));
      const normal = totalProduction - suspected;
      return { name: `${i + 1}일`, normal, suspected, total: totalProduction };
    });
  }
  return [];
};

/**
 * Generates data for the "Alert Quality Analysis" chart.
 * @param {Array} productionSummaryData - The output from generateProductionSummary
 * @returns {Array} Data formatted for Recharts Stacked BarChart
 */
export const generateAlertQualitySummary = (productionSummaryData) => {
  return productionSummaryData.map(period => {
    const totalSuspected = period.suspected;
    const falseAlarm = Math.floor(totalSuspected * (Math.random() * 0.15 + 0.05)); // 5-20% false alarm rate
    const unresolved = Math.floor(totalSuspected * (Math.random() * 0.1 + 0.05)); // 5-15% unresolved rate
    const confirmedDefect = totalSuspected - falseAlarm - unresolved;
    
    return {
      name: period.name,
      '확정 불량': confirmedDefect,
      '오경보': falseAlarm,
      '미조치': unresolved,
      total: totalSuspected,
    };
  });
};


// --- Time-based View Data Generator ---

/**
 * Generates data for the "Hourly Defect Pattern" chart.
 * @returns {Array} Data formatted for Recharts AreaChart/BarChart
 */
export const generateHourlyPattern = () => {
  return Array.from({ length: 24 }, (_, i) => {
    // Simulate higher defect rates during night shifts
    const hour = i;
    let baseDefects = Math.random() * 5 + 2;
    if (hour >= 22 || hour <= 4) {
      baseDefects *= (Math.random() * 1.5 + 1.2); // 20-170% higher
    }
    return {
      name: `${hour.toString().padStart(2, '0')}:00`,
      '불량 의심 건수': Math.floor(baseDefects),
    };
  });
};
