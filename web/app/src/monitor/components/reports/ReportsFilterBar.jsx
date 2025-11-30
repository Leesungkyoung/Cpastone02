import React, { useState, useRef, useEffect } from 'react';
import { ChevronDownIcon } from "@heroicons/react/24/outline";

const useOutsideAlerter = (ref, handler) => {
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        handler();
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [ref, handler]);
};

const ToggleButton = ({ label, value, activeValue, onClick }) => (
  <button
    type="button"
    onClick={() => onClick(value)}
    className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors border ${
      activeValue === value
        ? 'bg-indigo-600 text-white shadow-sm border-indigo-600'
        : 'bg-white text-gray-700 hover:bg-gray-50'
    }`}
  >
    {label}
  </button>
);

const ReportsFilterBar = ({ filters, setFilters }) => {
  const { viewMode, periodType, selectedMonth, sortOrder } = filters;
  const { setViewMode, setPeriodType, setSelectedMonth, setSortOrder } = setFilters;
  
  const [isMonthDropdownOpen, setMonthDropdownOpen] = useState(false);
  const monthDropdownRef = useRef(null);
  useOutsideAlerter(monthDropdownRef, () => setMonthDropdownOpen(false));

  const handleMonthSelect = (month) => {
    setSelectedMonth(month);
    setMonthDropdownOpen(false);
  };

  return (
    <div className="flex flex-wrap items-center justify-between gap-4 p-4 bg-gray-50 rounded-lg border">
      {/* Left Filters */}
      <div className="flex items-center gap-x-4">
        {/* Period Type Toggle */}
        <div className="flex items-center space-x-2">
          <ToggleButton label="월별" value="monthly" activeValue={periodType} onClick={setPeriodType} />
          <ToggleButton label="주별" value="weekly" activeValue={periodType} onClick={setPeriodType} />
          <ToggleButton label="일별" value="daily" activeValue={periodType} onClick={setPeriodType} />
          <ToggleButton label="전체" value="all" activeValue={periodType} onClick={setPeriodType} />
        </div>

        {/* Month Dropdown */}
        <div className="relative" ref={monthDropdownRef}>
          <button
            onClick={() => setMonthDropdownOpen(!isMonthDropdownOpen)}
            disabled={periodType === 'all'}
            className="flex items-center justify-between w-32 px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:bg-gray-100 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <span>{selectedMonth ? `${selectedMonth}월` : "월 선택"}</span>
            <ChevronDownIcon className="h-5 w-5 text-gray-400" />
          </button>
          {isMonthDropdownOpen && (
            <div className="absolute z-10 mt-1 w-32 bg-white shadow-lg rounded-md border max-h-60 overflow-auto">
              <ul className="py-1">
                {Array.from({ length: 12 }, (_, i) => (
                  <li key={i + 1} onClick={() => handleMonthSelect(i + 1)} className="px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer">
                    {i + 1}월
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
      
      {/* Right Filters */}
      <div className="flex items-center gap-x-4">
        {/* View Mode Toggle */}
        <div className="flex items-center p-1 bg-gray-200 rounded-lg">
          <ToggleButton label="요약 보기" value="summary" activeValue={viewMode} onClick={setViewMode} />
          <ToggleButton label="시간대별 분석" value="time" activeValue={viewMode} onClick={setViewMode} />
        </div>

        <select
          value={sortOrder}
          onChange={(e) => setSortOrder(e.target.value)}
          className="w-40 pl-3 pr-8 py-2 text-sm border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-md"
        >
          <option value="latest">최신순</option>
          <option value="oldest">오래된순</option>
        </select>
      </div>
    </div>
  );
};

export default ReportsFilterBar;
