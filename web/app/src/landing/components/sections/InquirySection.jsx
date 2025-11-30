import React from 'react';
import { motion } from 'framer-motion';

const InquirySection = () => {
  return (
    <section id="inquiry" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
        >
          <h2 className="text-3xl md:text-4xl font-semibold text-gray-800 mb-4">
            ZeroQ Factory 도입을 망설이고 계신가요?
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
            전문 컨설턴트가 기업의 환경에 최적화된 스마트 팩토리 솔루션을 제안해 드립니다.
          </p>
          <a
            href="#"
            className="bg-accent text-white font-medium py-3 px-8 rounded-lg text-lg hover:opacity-90 transition-opacity"
          >
            문의하기
          </a>
        </motion.div>
      </div>
    </section>
  );
};

export default InquirySection;
