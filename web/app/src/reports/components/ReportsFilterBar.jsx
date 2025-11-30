import React, { useEffect, useRef } from 'react';
import { ChevronDownIcon } from '@heroicons/react/24/outline';

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

const ReportsFilterBar = ({ filters, onChange, isMonthDropdownOpen, setMonthDropdownOpen }) => {
  const monthDropdownRef = useRef(null);
  useOutsideAlerter(monthDropdownRef, () => setMonthDropdownOpen(false));

  const handlePeriodChange = (type) => {
    // When changing period, if the new period is 'all', reset month selection
    const newMonth = type === 'all' ? 'all' : filters.selectedMonth;
    onChange({ ...filters, periodType: type, selectedMonth: newMonth });
  };

  const handleMonthSelect = (newMonth) => {
    onChange({ ...filters, selectedMonth: newMonth });
    setMonthDropdownOpen(false);
  };
  
  const handleSortChange = (e) => {
    onChange({ ...filters, sortOrder: e.target.value });
  };

  const handleViewModeChange = (mode) => {
    onChange({ ...filters, viewMode: mode });
  };

  const periodButtons = [
    { key: 'summary', label: '전체' },
    { key: 'monthly', label: '월별' },
    { key: 'weekly', label: '주별' },
    { key: 'daily', label: '일별' },
  ];
  
  const viewModeButtons = [
    { key: 'summary', label: '요약 보기' },
  ];

  return (
    <div className="p-4 bg-white border rounded-xl shadow-sm flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0">
      <div className="flex items-center space-x-4">
        <div className="isolate inline-flex rounded-md shadow-sm">
           {viewModeButtons.map((mode, idx) => (
            <button
              key={mode.key}
              onClick={() => handleViewModeChange(mode.key)}
              className={`relative inline-flex items-center px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300 focus:z-10 ${
                filters.viewMode === mode.key
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white text-gray-900 hover:bg-gray-50'
              } rounded-md`}
            >
              {mode.label}
            </button>
          ))}
        </div>
        <div className="isolate inline-flex rounded-md shadow-sm">
          {periodButtons.map((period, idx) => (
            <button
              key={period.key}
              onClick={() => handlePeriodChange(period.key)}
              className={`relative inline-flex items-center px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300 focus:z-10 ${
                filters.periodType === period.key
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white text-gray-900 hover:bg-gray-50'
              } ${idx === 0 ? 'rounded-l-md' : ''} ${idx === periodButtons.length - 1 ? 'rounded-r-md' : '-ml-px'}`}
            >
              {period.label}
            </button>
          ))}
        </div>
      </div>
      
      <div className="flex items-center space-x-2">
        <div className="relative" ref={monthDropdownRef}>
          <button
            onClick={() => setMonthDropdownOpen(!isMonthDropdownOpen)}
            disabled={filters.periodType === 'all'}
            className="flex items-center justify-between w-32 px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span>{filters.selectedMonth === 'all' ? '월 선택' : `${parseInt(filters.selectedMonth.split('-')[1], 10)}월`}</span>
            <ChevronDownIcon className="h-5 w-5 text-gray-400" />
          </button>
          {isMonthDropdownOpen && (
            <div className="absolute z-50 mt-1 w-32 bg-white shadow-lg rounded-md border max-h-60 overflow-auto">
              <ul className="py-1">
                <li
                  onClick={() => handleMonthSelect('all')}
                  className="px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                >
                  전체 월
                </li>
                {Array.from({ length: 12 }, (_, i) => {
                  const month = i + 1;
                  const monthValue = `2008-${String(month).padStart(2, '0')}`;
                  const monthLabel = `${month}월`;
                  return (
                    <li
                      key={monthValue}
                      onClick={() => handleMonthSelect(monthValue)}
                      className="px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                    >
                      {monthLabel}
                    </li>
                  );
                })}
              </ul>
            </div>
          )}
        </div>
        <select
          id="sort"
          name="sort"
          value={filters.sortOrder}
          onChange={handleSortChange}
          className="block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6"
        >
          <option value="latest">최신순</option>
          <option value="oldest">오래된순</option>
        </select>
      </div>
    </div>
  );
};

export default ReportsFilterBar;
