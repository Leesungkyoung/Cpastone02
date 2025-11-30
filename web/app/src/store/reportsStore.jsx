import { create } from 'zustand';

const useReportsStore = create((set) => ({
  filters: {
    periodType: 'monthly', // 'monthly', 'weekly', 'daily'
    selectedMonth: 'all', // 'all', '2008-07', ...
    sortOrder: 'latest', // 'latest', 'oldest'
  },
  setFilters: (newFilters) => set((state) => ({
    filters: { ...state.filters, ...newFilters }
  })),
}));

export default useReportsStore;
