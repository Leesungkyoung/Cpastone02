import React from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../../assets/logo.png';

const TopHeader = () => {
  const navigate = useNavigate();

  return (
    <header className="bg-primary text-white shadow-md fixed top-0 left-0 right-0 z-20">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        {/* 로고 + 타이틀 영역 */}
        <div
          className="flex items-center gap-3 cursor-pointer"
          onClick={() => navigate("/")}
        >
          <img
          src={logo}
          alt="ZeroQ Factory Logo"
          className="h-9 w-9 rounded-full object-contain scale-150 "
          />
          <h1 className="text-xl font-semibold">
            ZeroQ Factory Monitor
          </h1>
        </div>

        {/* 우측 메뉴(필요하면 여기에 아이콘/버튼 추가) */}
        {/* <div>...</div> */}
      </div>
    </header>
  );
};

export default TopHeader;