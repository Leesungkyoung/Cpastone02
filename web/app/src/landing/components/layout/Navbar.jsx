import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import logo from '../../../assets/logo.png';

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <motion.nav
      className={`fixed top-0 left-0 right-0 z-50 transition-colors duration-300 ${
        scrolled ? 'bg-white shadow-md' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* 로고 + 텍스트 */}
          <div className="flex-shrink-0">
            <Link to="/" className="flex items-center gap-3">
              <img
                src={logo}
                alt="ZeroQ Factory Logo"
                className="h-10 w-10 rounded-full object-contain scale-125"
              />
              <span
                className={`font-bold text-2xl ${
                  scrolled ? 'text-primary' : 'text-white'
                }`}
              >
                ZeroQ Factory
              </span>
            </Link>
          </div>

          {/* 오른쪽 메뉴 + 버튼 그룹 */}
          <div className="hidden md:flex items-center space-x-8">
            {/* 메뉴 */}
            <div className="flex items-baseline space-x-6">
              <a
                href="/#intro"
                className={`font-medium ${
                  scrolled
                    ? 'text-gray-600 hover:text-primary'
                    : 'text-white hover:text-secondary'
                }`}
              >
                솔루션 소개
              </a>
              <a
                href="/#features"
                className={`font-medium ${
                  scrolled
                    ? 'text-gray-600 hover:text-primary'
                    : 'text-white hover:text-secondary'
                }`}
              >
                특징
              </a>
            </div>

            {/* 관제 열기 버튼 */}
            <Link
              to="/monitor"
              className="bg-primary text-white font-medium py-2 px-4 rounded-lg hover:bg-secondary transition-colors"
            >
              실시간 관제 열기
            </Link>
          </div>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;