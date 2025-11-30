import React from 'react';
import { motion } from 'framer-motion';
import Tab1Img from '../../../assets/Tab1.png';
import Tab2Img from '../../../assets/Tab2.png';   // 불량 알림 이력 탭 이미지
import Tab3Img from '../../../assets/Tab3.png';   // 분석 리포트 탭 이미지

const DashboardPreview = () => {
  return (
    <section id="features" className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        {/* 1. 실시간 관제 탭 설명 + 메인 프리뷰 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-3xl md:text-4xl font-semibold text-gray-800 mb-4">
            현장의 센서 데이터를 실시간으로 분석합니다.
          </h2>
          <p className="text-lg text-gray-600 max-w-4xl mx-auto mb-12">
            실시간 관제 탭은 공정 센서 데이터를 실시간 분석하여 불량 의심 제품을 바로 표시해 주는
            모니터링 화면입니다.<br />
            탐지된 제품은 알림 카드와 팝업으로 노출되어 빠른 수거·조치가 가능하고,
            모든 기록은 이력으로 남아 사후 분석에 활용됩니다.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <img
            src={Tab1Img}
            alt="실시간 관제 대시보드"
            className="rounded-xl shadow-lg w-full aspect-video object-cover"
          />
        </motion.div>

        {/* 2. 불량 알림 이력 섹션 */}
        <div className="mt-20 space-y-16">
          <motion.div
            className="flex flex-col md:flex-row items-center gap-10 text-left"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.1 }}
          >
            {/* 왼쪽 이미지 */}
            <div className="w-full md:w-1/2">
              <img
                src={Tab2Img}
                alt="불량 알림 이력 화면"
                className="rounded-xl shadow-lg w-full object-cover"
              />
            </div>

            {/* 오른쪽 텍스트 */}
            <div className="w-full md:w-1/2">
              <h3 className="text-2xl font-semibold text-gray-800 mb-4">
                불량 알림 이력
              </h3>
              <p className="text-lg text-gray-600 mb-3">
                불량 알림 이력 탭은 불량 의심 알림의 ‘로그 기록장’입니다.
              </p>
              <p className="text-lg text-gray-600">
                알림 발생부터 조치 완료까지의 과정을 시간순으로 추적하면서,
                누락된 제품이나 반복되는 알림 패턴을 빠르게 찾아낼 수 있습니다.
                과거 이력을 기반으로 모델 성능과 공정 운영 방식을 함께 되돌아볼 수 있습니다.
              </p>
            </div>
          </motion.div>

          {/* 3. 분석 리포트 섹션 */}
          <motion.div
            className="flex flex-col md:flex-row-reverse items-center gap-10 text-left"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            {/* 오른쪽 이미지 (flex-row-reverse로 인해 시각적으로 왼쪽) */}
            <div className="w-full md:w-1/2">
              <img
                src={Tab3Img}
                alt="분석 리포트 화면"
                className="rounded-xl shadow-lg w-full object-cover"
              />
            </div>

            {/* 왼쪽 텍스트 (flex-row-reverse로 인해 시각적으로 오른쪽) */}
            <div className="w-full md:w-1/2">
              <h3 className="text-2xl font-semibold text-gray-800 mb-4">
                분석 리포트
              </h3>
              <p className="text-lg text-gray-600 mb-3">
                분석 리포트 탭은 알림·생산 데이터를 모아서
                공정의 품질 트렌드를 한 눈에 보여주는 분석 화면입니다.
              </p>
              <p className="text-lg text-gray-600">
                기간별 불량률과 확정 불량·오경보 비율을 비교해
                모델 성능과 공정 품질을 함께 점검할 수 있습니다.
                시즌별·라인별 패턴을 파악해 향후 설비 튜닝이나
                운영 전략 수립에 활용할 수 있습니다.
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default DashboardPreview;