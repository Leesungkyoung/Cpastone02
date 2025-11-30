import { useState, useEffect, useMemo, useRef } from "react";
import { CheckCircleIcon, ChevronDownIcon } from "@heroicons/react/24/outline";
import AlertDetailModal from "../components/AlertDetailModal";
import { API_BASE_URL } from "../../utils/config";


// Custom Hook to detect click outside
const useOutsideAlerter = (ref, handler) => {
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        handler();
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref, handler]);
};


const AlertsPage = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // 필터 및 정렬 상태
  const [monthFilter, setMonthFilter] = useState("all"); // 'all', 1, 2, ...
  const [periodFilter, setPeriodFilter] = useState("all"); // 'all', 'today', '7d'
  const [weekFilter, setWeekFilter] = useState('all'); // 'all', 1, 2, 3, 4, 5
  const [statusFilter, setStatusFilter] = useState("all"); // 'all', 'unresolved', 'resolved'
  const [sortOption, setSortOption] = useState("latest"); // 'latest', 'oldest', 'highestProb', 'productIndex'
  
  const [isMonthDropdownOpen, setMonthDropdownOpen] = useState(false);
  const monthDropdownRef = useRef(null);
  useOutsideAlerter(monthDropdownRef, () => setMonthDropdownOpen(false));

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/alerts`);
      if (!response.ok) {
        throw new Error('데이터를 불러오는데 실패했습니다.');
      }
      const data = await response.json();
      setAlerts(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  const handleResolveClick = async (alertId) => {
    const originalAlerts = [...alerts];
    const updatedAlerts = alerts.map(a => 
      a.id === alertId ? { ...a, resolved: true, resolved_at: new Date().toISOString() } : a
    );
    setAlerts(updatedAlerts);

    try {
      const response = await fetch(`${API_BASE_URL}/api/alerts/${alertId}/resolve`, { method: 'PATCH' });
      if (!response.ok) {
        throw new Error('상태 업데이트 실패');
      }
      // Optimistic update was successful, no need to refetch
    } catch (error) {
      console.error("Failed to resolve alert:", error);
      setAlerts(originalAlerts); // Revert on failure
    }
  };

  const openModal = (alert) => {
    setSelectedAlert(alert);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedAlert(null);
  };
  
  const handleMonthSelect = (month) => {
    setMonthFilter(month);
    setPeriodFilter('all'); // 다른 필터 초기화
    setWeekFilter('all');   // 다른 필터 초기화
    setMonthDropdownOpen(false);
  };

  const filteredAndSortedAlerts = useMemo(() => {
    let processedAlerts = [...alerts];

    // 1. 월(Month) 필터
    if (monthFilter !== "all") {
      processedAlerts = processedAlerts.filter(alert => {
        const alertMonth = new Date(alert.timestamp).getMonth() + 1;
        return alertMonth === parseInt(monthFilter, 10);
      });
      
      // 1a. 주차(Week) 필터 - 월이 선택되었을 때만 동작
      if (weekFilter !== 'all') {
        const week = parseInt(weekFilter, 10);
        processedAlerts = processedAlerts.filter(alert => {
            const dayOfMonth = new Date(alert.timestamp).getDate();
            if (week === 1) return dayOfMonth >= 1 && dayOfMonth <= 7;
            if (week === 2) return dayOfMonth >= 8 && dayOfMonth <= 14;
            if (week === 3) return dayOfMonth >= 15 && dayOfMonth <= 21;
            if (week === 4) return dayOfMonth >= 22 && dayOfMonth <= 28;
            if (week === 5) return dayOfMonth >= 29;
            return true;
        });
      }
    } else {
      // 2. 기간(Period) 필터 - '전체 월'일 때만 동작
      if (periodFilter !== "all") {
        const demoDateStr = import.meta.env.VITE_DEMO_DATE;
        const todayDate = demoDateStr ? new Date(demoDateStr) : new Date();

        if (periodFilter === 'today') {
          // 데모 날짜(예: "2008-11-25")를 기준으로 필터링합니다.
          const year = todayDate.getFullYear();
          const month = String(todayDate.getMonth() + 1).padStart(2, '0');
          const day = String(todayDate.getDate()).padStart(2, '0');
          const todayStr = `${year}-${month}-${day}`;
          
          processedAlerts = processedAlerts.filter(alert => {
            return alert.timestamp.startsWith(todayStr);
          });
        }
        // '7d' 필터는 현재 요청사항이 아니므로 기존 로직을 유지합니다.
        else if (periodFilter === '7d') {
            const now = new Date();
            let startDate = new Date();
            startDate.setDate(now.getDate() - 7);
            startDate.setHours(0, 0, 0, 0);
            
            processedAlerts = processedAlerts.filter(alert => {
                const alertDate = new Date(alert.timestamp);
                return alertDate >= startDate;
            });
        }
      }
    }

    // 3. 상태(Status) 필터
    if (statusFilter !== "all") {
      processedAlerts = processedAlerts.filter(alert => {
        if (statusFilter === "resolved") return alert.resolved;
        if (statusFilter === "unresolved") return !alert.resolved;
        return true;
      });
    }

    // 4. 정렬(Sorting)
    processedAlerts.sort((a, b) => {
      switch (sortOption) {
        case "latest":
          return new Date(b.timestamp) - new Date(a.timestamp);
        case "oldest":
          return new Date(a.timestamp) - new Date(b.timestamp);
        case "highestProb":
          return (b.prob || 0) - (a.prob || 0);
        case "productIndex":
          return a.product_id - b.product_id;
        default:
          return 0;
      }
    });

    return processedAlerts;
  }, [alerts, monthFilter, periodFilter, weekFilter, statusFilter, sortOption]);


  const kpiData = useMemo(() => {
    // VITE_DEMO_DATE 환경 변수가 있으면 데모 날짜를, 없으면 실제 오늘 날짜를 사용합니다.
    const demoDate = import.meta.env.VITE_DEMO_DATE;
    const todayDate = demoDate ? new Date(demoDate) : new Date();

    // 로컬 시간대 기준으로 오늘의 YYYY-MM-DD 문자열 생성
    const year = todayDate.getFullYear();
    const month = String(todayDate.getMonth() + 1).padStart(2, '0');
    const day = String(todayDate.getDate()).padStart(2, '0');
    const today = `${year}-${month}-${day}`;

    const todayCount = alerts.filter(a => a.timestamp.slice(0, 10) === today).length;
    const todayResolved = alerts.filter(a => a.timestamp.slice(0, 10) === today && a.resolved).length;
    
    const totalCount = alerts.length;
    const totalResolved = alerts.filter(a => a.resolved).length;

    return { todayCount, todayResolved, totalCount, totalResolved };
  }, [alerts]);

  if (loading) return <div className="text-center py-10">로딩 중...</div>;
  if (error) return <div className="text-center py-10 text-red-500">데이터를 불러오는 중 오류가 발생했습니다: {error}</div>;

  return (
    <div className="p-6 bg-gray-50/50 flex flex-col h-full">
      {/* --- Top Fixed Area --- */}
      <div className="flex-shrink-0">
        {/* KPI Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <KpiCard title="오늘 의심 발생 건수" value={kpiData.todayCount} valueColor="text-[#E53935]" />
          <KpiCard title="오늘 조치 완료 건수" value={kpiData.todayResolved} valueColor="text-[#28A745]" />
          <KpiCard title="누적 의심 발생 건수" value={kpiData.totalCount} valueColor="text-[#E53935]" />
          <KpiCard title="누적 조치 완료 건수" value={kpiData.totalResolved} valueColor="text-[#28A745]" />
        </div>

        {/* Filters Section */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4 p-4 bg-white rounded-lg border shadow-sm">
          {/* Left Filters */}
          <div className="flex items-center gap-x-4">
            {/* Month Dropdown */}
            <div className="relative" ref={monthDropdownRef}>
              <button
                onClick={() => setMonthDropdownOpen(!isMonthDropdownOpen)}
                className="flex items-center justify-between w-32 px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <span>{monthFilter === "all" ? "월 선택" : `${monthFilter}월`}</span>
                <ChevronDownIcon className="h-5 w-5 text-gray-400" />
              </button>
              {isMonthDropdownOpen && (
                <div className="absolute z-50 mt-1 w-32 bg-white shadow-lg rounded-md border max-h-60 overflow-auto">
                  <ul className="py-1">
                    <li
                      onClick={() => handleMonthSelect("all")}
                      className="px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                    >
                      전체 월 
                    </li>
                    {Array.from({ length: 12 }, (_, i) => (
                      <li
                        key={i + 1}
                        onClick={() => handleMonthSelect(i + 1)}
                        className="px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                      >
                        {i + 1}월
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Period/Week Buttons */}
            <div className="isolate inline-flex rounded-md shadow-sm">
              {monthFilter === 'all' ? (
                <>
                  <button
                    onClick={() => setPeriodFilter('today')}
                    className={`relative inline-flex items-center rounded-l-md px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300 focus:z-10 ${
                      periodFilter === 'today'
                        ? 'bg-indigo-600 text-white'
                        : 'bg-white text-gray-900 hover:bg-gray-50'
                    }`}
                  >
                    오늘
                  </button>
                  <button
                    onClick={() => setPeriodFilter('all')}
                    className={`relative -ml-px inline-flex items-center rounded-r-md px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300 focus:z-10 ${
                      periodFilter === 'all'
                        ? 'bg-indigo-600 text-white'
                        : 'bg-white text-gray-900 hover:bg-gray-50'
                    }`}
                  >
                    전체
                  </button>
                </>
              ) : (
                <>
                  {[
                    { value: 1, label: '1주차' }, { value: 2, label: '2주차' },
                    { value: 3, label: '3주차' }, { value: 4, label: '4주차' },
                    { value: 5, label: '5주차+' }, { value: 'all', label: '전체 월' }
                  ].map((btn, idx, arr) => (
                    <button key={btn.value} onClick={() => setWeekFilter(btn.value)}
                      className={`relative inline-flex items-center px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300 focus:z-10 ${weekFilter === btn.value ? 'bg-indigo-600 text-white' : 'bg-white text-gray-900 hover:bg-gray-50'} ${idx === 0 ? 'rounded-l-md' : '-ml-px'} ${idx === arr.length - 1 ? 'rounded-r-md' : ''}`}>
                      {btn.label}
                    </button>
                  ))}
                </>
              )}
            </div>
          </div>
          
          {/* Right Filters */}
          <div className="flex items-center gap-x-4">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-36 pl-3 pr-8 py-2 text-sm border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-md"
            >
              <option value="all">전체 상태</option>
              <option value="unresolved">미조치</option>
              <option value="resolved">조치 완료</option>
            </select>
            <select
              value={sortOption}
              onChange={(e) => setSortOption(e.target.value)}
              className="w-48 pl-3 pr-8 py-2 text-sm border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-md"
            >
              <option value="latest">최신 발생순</option>
              <option value="oldest">오래된순</option>
              <option value="highestProb">불량 의심 확률 높은 순</option>
              <option value="productIndex">제품 번호 순</option>
            </select>
          </div>
        </div>
      </div>

      {/* --- Bottom Scrollable Table Area --- */}
      <div className="overflow-y-auto bg-white shadow-sm rounded-xl border h-[520px]">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50 sticky top-0 z-10">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">날짜</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">시간</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">제품 번호</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">의심 센서</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">불량 의심 확률</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">상태</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">조치</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredAndSortedAlerts.map((alert) => (
              <tr key={alert.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {new Date(alert.timestamp).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">
                  {alert.product_id}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  <div className="max-w-[200px] whitespace-normal">
                    {Array.isArray(alert.top_sensors) ? alert.top_sensors.join(', ') : ''}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {alert.prob ? `${(alert.prob * 100).toFixed(1)}%` : 'N/A'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <span 
                    onClick={() => openModal(alert)}
                    className={`px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full cursor-pointer ${
                    alert.resolved 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {alert.resolved ? '조치 완료' : '미조치'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <button
                    onClick={() => handleResolveClick(alert.id)}
                    disabled={alert.resolved}
                    className={`inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-full shadow-sm transition-colors ${
                      alert.resolved
                        ? "bg-[#E4F4EA] text-[#3F8D4E] cursor-not-allowed"
                        : "bg-[#FFE8D6] text-[#D96A2B] hover:brightness-95 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FFE8D6]"
                    }`}
                  >
                    {alert.resolved ? (
                      <>
                        <CheckCircleIcon className="h-4 w-4 mr-1" />
                        완료
                      </>
                    ) : (
                      "조치하기"
                    )}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {isModalOpen && (
        <AlertDetailModal 
          alert={selectedAlert} 
          onClose={closeModal} 
          onResolve={handleResolveClick} 
        />
      )}
    </div>
  );
};

const KpiCard = ({ title, value, valueColor }) => (
  <div className="bg-white p-6 rounded-xl shadow-sm border">
    <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
    <dd className={`mt-1 text-3xl font-semibold ${valueColor || 'text-gray-900'}`}>{value}</dd>
  </div>
);

export default AlertsPage;
