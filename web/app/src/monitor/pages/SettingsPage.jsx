import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import AdminInfoCard from '../components/AdminInfoCard';
import { API_BASE_URL } from '../../utils/config';

const SettingsPage = () => {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/settings/admins`);
      if (!response.ok) throw new Error('Failed to fetch settings');
      const data = await response.json();
      setSettings(data);
    } catch (error) {
      toast.error('설정 정보를 불러오는데 실패했습니다.');
      console.error(error);
      setSettings({
        monitor_admin: { name: "", department: "", phone: "", email: "", photo_url: null },
        quality_manager: { name: "", department: "", phone: "", email: "", photo_url: null }
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (role, dataToSave) => {
    if (!dataToSave.name || !dataToSave.department || !dataToSave.phone || !dataToSave.email) {
      toast.error('모든 필수 정보를 입력해주세요.');
      return Promise.reject(new Error('Validation failed'));
    }
    
    const currentSettings = { ...settings, [role]: dataToSave };

    const promise = fetch(`${API_BASE_URL}/api/settings/admins`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentSettings)
    });

    toast.promise(promise, {
      loading: '저장 중...',
      success: '성공적으로 저장되었습니다.',
      error: '저장에 실패했습니다.',
    });
    
    try {
        const response = await promise;
        if (!response.ok) throw new Error('Save failed');
        await fetchSettings(); // Refetch to ensure UI is in sync with DB
    } catch (error) {
        console.error(error);
        throw error; // Re-throw to be caught by AdminInfoCard if needed
    }
  };

  if (loading || !settings) {
    return (
      <div className="p-6">
        <div className="animate-pulse grid md:grid-cols-2 gap-6">
          <div className="bg-gray-200 rounded-xl h-96"></div>
          <div className="bg-gray-200 rounded-xl h-96"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="grid md:grid-cols-2 gap-6">
        <AdminInfoCard 
          title="모니터링 관리자" 
          data={settings.monitor_admin}
          onSave={(data) => handleSave('monitor_admin', data)}
          isInitiallyEditing={!settings.monitor_admin.name}
        />
        <AdminInfoCard 
          title="품질 책임자" 
          data={settings.quality_manager}
          onSave={(data) => handleSave('quality_manager', data)}
          isInitiallyEditing={!settings.quality_manager.name}
        />
      </div>
    </div>
  );
};

export default SettingsPage;
