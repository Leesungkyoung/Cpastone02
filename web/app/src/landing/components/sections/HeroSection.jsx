import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import logo from '../../../assets/logo.png';

const HeroSection = () => {
  return (
    <section id="hero" className="relative h-screen flex items-center justify-center text-white">
      {/* 배경 이미지 및 오버레이 */}
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: "url('/images/hero_bg.jpg')" }}
      >
        <div className="absolute inset-0 bg-primary opacity-70"></div>
      </div>

      {/* 배경 로고 (희미하게) */}
      <img
        src={logo}
        alt="background logo"
        className="absolute inset-0 w-full h-full object-contain p-30 opacity-5 z-0 translate-y-8" //여기가 크기 조절
      />

      <motion.div
        className="relative z-10 text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        {/* 1줄: 브랜드 이름 (가장 크게) */}
        <h1 className="text-4xl md:text-6xl font-semibold mb-2">
          ZeroQ Factory
        </h1>

        {/* 2줄: 솔루션 설명 (조금 더 작은 크기) */}
        <p className="text-2xl md:text-3xl font-semibold mb-4">
          AI 기반 제조 공정 실시간 관제 솔루션
        </p>

        {/* 3줄: 프로젝트 맞춤 설명 (더 작은 크기) */}
        <p className="text-base md:text-lg max-w-4xl mx-auto mb-8">
          센서 데이터를 기반으로 불량 의심 제품을 실시간으로 감지하고,
          빠른 수거·조치를 돕는 품질 모니터링 솔루션입니다.
        </p>
        
        <Link
          to="/monitor"
          className="bg-white text-primary font-medium py-3 px-8 rounded-lg text-lg hover:bg-secondary hover:text-white transition-colors"
        >
          실시간 관제 열기
        </Link>
      </motion.div>
    </section>
  );
};

export default HeroSection;
