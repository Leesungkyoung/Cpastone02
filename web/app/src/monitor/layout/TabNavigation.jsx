import React from 'react';
import { NavLink } from 'react-router-dom';
import { useStreamingStore } from '../../store/streamingStore.jsx';

const navLinks = [
  { name: '실시간 관제', href: '/monitor' },
  { name: '불량 알림 이력', href: '/alerts' },
  { name: '분석 리포트', href: '/reports' },
  { name: '설정', href: '/settings' },
];

const TabNavigation = () => {
  const unconfirmedAlertsCount = useStreamingStore((state) => state.unconfirmedAlerts.length);

  return (
    <nav
      className="
        fixed
        top-[88px]      /* 🔥 탑헤더와 간격 더 넓힘 */
        left-0 right-0
        z-40
        flex
        justify-center
        pointer-events-none   /* 전체 박스 크기 유지용 */
      "
    >
      <div
        className="
          pointer-events-auto
          max-w-8xl
          w-[95%]              /* 🔥 양옆 여백 확보 */
          bg-primary           /* 🔥 탑헤더와 동일 색상 */
          rounded-md         /* 🔥 둥근 네비 박스 */
          shadow-md
          h-14
          flex items-center
          px-8                 /* 🔥 내용 좌우 여백 */
        "
      >
        <div className="flex items-center space-x-10">
          {navLinks.map((link) => (
            <NavLink
              key={link.name}
              to={link.href}
              className={({ isActive }) =>
                `
                py-2 px-1
                text-sm font-medium
                transition-colors
                relative /* For badge positioning */

                ${
                  isActive
                    ? 'text-white font-semibold border-b-2 border-white'
                    : 'text-[#CFE0FF] hover:text-white'
                }
              `
              }
            >
              {link.name}
              {/* Badge for "실시간 관제" tab */}
              {link.name === '실시간 관제' && unconfirmedAlertsCount > 0 && (
                <span className="absolute top-0 right-[-16px] flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-xs font-bold text-white">
                  {unconfirmedAlertsCount}
                </span>
              )}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default TabNavigation;