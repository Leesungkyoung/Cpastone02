const reportsData = {
  '2008-07': {
    summary: {
      total_production: 64000,
      total_defects: 4480,
      defect_rate: 7.0,
      confirmed_defects: 2912,
      false_alarms: 1568,
      resolution_rate: 100,
      unresolved: 0,
      false_alarm_rate: 35.0,
    },
    weekly: [
      { name: '1주차', '전체 생산': 12800, '정상 제품': 11920, '불량 의심': 880, '확정 불량': 560, '오경보': 320, '미조치': 0 },
      { name: '2주차', '전체 생산': 13200, '정상 제품': 12280, '불량 의심': 920, '확정 불량': 600, '오경보': 320, '미조치': 0 },
      { name: '3주차', '전체 생산': 13000, '정상 제품': 12060, '불량 의심': 940, '확정 불량': 620, '오경보': 320, '미조치': 0 },
      { name: '4주차', '전체 생산': 12600, '정상 제품': 11720, '불량 의심': 880, '확정 불량': 560, '오경보': 320, '미조치': 0 },
      { name: '5주차', '전체 생산': 12400, '정상 제품': 11540, '불량 의심': 860, '확정 불량': 572, '오경보': 288, '미조치': 0 },
    ],
  },
  '2008-08': {
    summary: {
      total_production: 68000,
      total_defects: 4760,
      defect_rate: 7.0,
      confirmed_defects: 3332,
      false_alarms: 1428,
      resolution_rate: 100,
      unresolved: 0,
      false_alarm_rate: 30.0,
    },
    weekly: [
      { name: '1주차', '전체 생산': 13600, '정상 제품': 12680, '불량 의심': 920, '확정 불량': 640, '오경보': 280, '미조치': 0 },
      { name: '2주차', '전체 생산': 14000, '정상 제품': 13000, '불량 의심': 1000, '확정 불량': 720, '오경보': 280, '미조치': 0 },
      { name: '3주차', '전체 생산': 13600, '정상 제품': 12620, '불량 의심': 980, '확정 불량': 700, '오경보': 280, '미조치': 0 },
      { name: '4주차', '전체 생산': 13600, '정상 제품': 12640, '불량 의심': 960, '확정 불량': 680, '오경보': 280, '미조치': 0 },
      { name: '5주차', '전체 생산': 13200, '정상 제품': 12300, '불량 의심': 900, '확정 불량': 592, '오경보': 308, '미조치': 0 },
    ],
  },
    '2008-09': {
    summary: {
      total_production: 60000,
      total_defects: 3600,
      defect_rate: 6.0,
      confirmed_defects: 2700,
      false_alarms: 900,
      resolution_rate: 100,
      unresolved: 0,
      false_alarm_rate: 25.0,
    },
    weekly: [
      { name: '1주차', '전체 생산': 12000, '정상 제품': 11300, '불량 의심': 700, '확정 불량': 525, '오경보': 175, '미조치': 0 },
      { name: '2주차', '전체 생산': 12000, '정상 제품': 11240, '불량 의심': 760, '확정 불량': 560, '오경보': 200, '미조치': 0 },
      { name: '3주차', '전체 생산': 12000, '정상 제품': 11280, '불량 의심': 720, '확정 불량': 540, '오경보': 180, '미조치': 0 },
      { name: '4주차', '전체 생산': 12000, '정상 제품': 11260, '불량 의심': 740, '확정 불량': 555, '오경보': 185, '미조치': 0 },
      { name: '5주차', '전체 생산': 12000, '정상 제품': 11320, '불량 의심': 680, '확정 불량': 520, '오경보': 160, '미조치': 0 },
    ],
  },
  '2008-10': {
    summary: {
      total_production: 66000,
      total_defects: 4620,
      defect_rate: 7.0,
      confirmed_defects: 3696,
      false_alarms: 924,
      resolution_rate: 100,
      unresolved: 0,
      false_alarm_rate: 20.0,
    },
    weekly: [
      { name: '1주차', '전체 생산': 13400, '정상 제품': 12480, '불량 의심': 920, '확정 불량': 740, '오경보': 180, '미조치': 0 },
      { name: '2주차', '전체 생산': 13200, '정상 제품': 12240, '불량 의심': 960, '확정 불량': 780, '오경보': 180, '미조치': 0 },
      { name: '3주차', '전체 생산': 13200, '정상 제품': 12260, '불량 의심': 940, '확정 불량': 760, '오경보': 180, '미조치': 0 },
      { name: '4주차', '전체 생산': 13000, '정상 제품': 12100, '불량 의심': 900, '확정 불량': 710, '오경보': 190, '미조치': 0 },
      { name: '5주차', '전체 생산': 13200, '정상 제품': 12300, '불량 의심': 900, '확정 불량': 706, '오경보': 194, '미조치': 0 },
    ],
  },
};

const distributeWeeklyToDaily = (weeklyValue) => {
  if (weeklyValue === 0) return Array(7).fill(0);
  const base = Math.floor(weeklyValue / 7);
  const remainder = weeklyValue % 7;
  const dailyValues = Array(7).fill(base);
  for (let i = 0; i < remainder; i++) {
    dailyValues[i] = base + 1;
  }
  for (let i = dailyValues.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [dailyValues[i], dailyValues[j]] = [dailyValues[j], dailyValues[i]];
  }
  return dailyValues;
};

export const getDailyDataForMonth = (month) => {
  const monthData = reportsData[month];
  if (!monthData) return [];

  const dailyBreakdown = [];
  monthData.weekly.forEach((week, weekIndex) => {
    const dailyValues = {};
    const keysToDistribute = ['전체 생산', '정상 제품', '불량 의심', '확정 불량', '오경보'];
    
    keysToDistribute.forEach(key => {
      dailyValues[key] = distributeWeeklyToDaily(week[key]);
    });

    for (let i = 0; i < 7; i++) {
      const day = weekIndex * 7 + i + 1;
      const dayData = { name: `${day}일`, '미조치': 0 };
      keysToDistribute.forEach(key => {
        dayData[key] = dailyValues[key][i];
      });
      dailyBreakdown.push(dayData);
    }
  });
  
  return dailyBreakdown.slice(0, 31);
};

export default reportsData;
