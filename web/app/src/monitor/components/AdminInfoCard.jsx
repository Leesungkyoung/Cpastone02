import React, { useState, useRef, useEffect } from 'react';
import { UserCircleIcon, PhotoIcon, PhoneIcon, EnvelopeIcon, BuildingOffice2Icon, UserIcon } from '@heroicons/react/24/solid';

const AdminInfoCard = ({ title, data, onSave, isInitiallyEditing = false }) => {
  const [isEditing, setIsEditing] = useState(isInitiallyEditing);
  const [formData, setFormData] = useState(data);
  const [photoPreview, setPhotoPreview] = useState(data.photo_url || null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    setIsEditing(isInitiallyEditing);
  }, [isInitiallyEditing]);

  useEffect(() => {
    setFormData(data);
    setPhotoPreview(data.photo_url || null);
  }, [data]);


  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };
  
  const handlePhotoClick = () => fileInputRef.current.click();

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && (file.type === 'image/jpeg' || file.type === 'image/png')) {
      const previewUrl = URL.createObjectURL(file);
      setPhotoPreview(previewUrl);
      setFormData({ ...formData, photo_file: file, photo_url: previewUrl });
    } else {
      alert('이미지 파일(JPG, PNG)만 업로드 가능합니다.');
    }
  };

  const handleSaveClick = async () => {
    await onSave(formData);
    setIsEditing(false);
  };

  const handleCancelClick = () => {
    setFormData(data); 
    setPhotoPreview(data.photo_url || null);
    setIsEditing(false);
  };
  
  const renderViewMode = () => (
    <div className="flex flex-col items-center">
        <div className="w-40 h-40 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden border-2 border-white shadow-md mb-6">
            {data.photo_url ? (
            <img src={data.photo_url} alt="Profile" className="w-full h-full object-cover" />
            ) : (
            <UserCircleIcon className="h-full w-full text-gray-300" />
            )}
        </div>
        <h3 className="text-2xl font-semibold text-gray-900 mb-6 text-center">{title}</h3>
        <div className="w-full max-w-sm space-y-4">
            <InfoRow icon={<UserIcon className="h-5 w-5 text-gray-400"/>} label="이름" value={data.name} />
            <InfoRow icon={<BuildingOffice2Icon className="h-5 w-5 text-gray-400"/>} label="소속" value={data.department} />
            <InfoRow icon={<PhoneIcon className="h-5 w-5 text-gray-400"/>} label="전화번호" value={data.phone} />
            <InfoRow icon={<EnvelopeIcon className="h-5 w-5 text-gray-400"/>} label="E-mail" value={data.email} />
        </div>
        <div className="mt-8 flex justify-end w-full max-w-sm">
            <button onClick={() => setIsEditing(true)} className="px-4 py-2 bg-gray-200 text-gray-800 font-semibold rounded-md hover:bg-gray-300">수정</button>
        </div>
    </div>
  );

  const renderEditMode = () => (
    <div className="flex flex-col items-center">
        <div className="flex flex-col items-center space-y-4 mb-8">
            <div className="w-40 h-40 rounded-full bg-gray-100 flex items-center justify-center cursor-pointer overflow-hidden" onClick={handlePhotoClick}>
                <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" accept="image/png, image/jpeg" />
                {photoPreview ? <img src={photoPreview} alt="Profile preview" className="w-full h-full object-cover" /> : <PhotoIcon className="h-20 w-20 text-gray-300" />}
            </div>
            <div className='text-sm text-gray-500 text-center'>
                <p>클릭하여 이미지를 업로드하세요.</p>
                <p>(JPG, PNG / 5MB 이하)</p>
            </div>
        </div>
        <h3 className="text-2xl font-semibold text-gray-900 mb-6 text-center">{title}</h3>
        <div className="w-full max-w-sm space-y-4">
            <EditRow label="이름" name="name" value={formData.name} onChange={handleInputChange} />
            <EditRow label="소속 (부서/팀명)" name="department" value={formData.department} onChange={handleInputChange} />
            <EditRow label="전화번호" name="phone" value={formData.phone} onChange={handleInputChange} />
            <EditRow label="E-mail" name="email" value={formData.email} onChange={handleInputChange} />
        </div>
        <div className="mt-8 flex justify-end space-x-3 w-full max-w-sm">
            <button onClick={handleCancelClick} className="px-4 py-2 bg-gray-200 text-gray-800 font-semibold rounded-md hover:bg-gray-300">취소</button>
            <button onClick={handleSaveClick} className="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-md shadow-sm hover:bg-indigo-700">저장</button>
        </div>
    </div>
  );

  return (
    <div className="bg-white rounded-xl shadow-sm p-8">
      {isEditing ? renderEditMode() : renderViewMode()}
    </div>
  );
};

const InfoRow = ({ icon, label, value }) => (
  <div className="flex items-start">
    <div className="flex-shrink-0 w-8 pt-1">{icon}</div>
    <div>
      <p className="text-xs text-gray-500">{label}</p>
      <p className="font-medium text-gray-900">{value || '-'}</p>
    </div>
  </div>
);

const EditRow = ({ label, name, value, onChange }) => (
    <div>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700">{label}</label>
      <input
        type="text" name={name} id={name} value={value} onChange={onChange}
        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    </div>
);

export default AdminInfoCard;
