import React from 'react';
import { motion } from 'framer-motion';
import Tab0Img from '../../../assets/Tab0.png';
// 여기 이미지는 불량 팝업 뜨는거 넣으면 될 것같음 
const IntroSection = () => {
  return (
    <section id="intro" className="py-20 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid md:grid-cols-2 gap-16 items-center">
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-3xl md:text-4xl font-semibold text-gray-800 mb-4">
            스마트 제조 품질관리, 이제 자동화하세요
          </h2>
          <p className="text-gray-700 leading-relaxed">
            ZeroQ Factory는 공정 라인의 수백 개 센서 데이터를 실시간 분석하여
            불량 의심 제품을 빠르게 찾아내고, 조치가 필요한 지점을 바로 알려주는
            AI 기반 스마트 관제 시스템입니다.
            <br />
            라인에서 발생하는 미세한 이상 신호를 놓치지 않고 감지하여
            불량 제품을 신속히 수거하고, 2차 불량 확산을 최소화할 수 있습니다.
            <br />
            복잡한 센서 로그는 ZeroQ Factory가 대신 읽고,
            관리자는 “어떤 구간에서, 어떤 제품이, 왜 의심되는지”만 직관적으로 확인하면 됩니다.
          </p>
        </motion.div>
        <motion.div
          className="flex justify-center"
          initial={{ opacity: 0, x: 50 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <img
            src={Tab0Img}
            alt="Dashboard Main"
            className="rounded-xl shadow-lg w-full max-w-lg"
          />
        </motion.div>
      </div>
    </section>
  );
};

export default IntroSection;
