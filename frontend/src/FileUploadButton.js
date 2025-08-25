import React, { useState, useRef } from 'react';
import axios from 'axios';
import "./FileUploadButton.css"

const FileUploadButton = () => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('idle'); // 'idle', 'uploading', 'success', 'error'
  const fileInputRef = useRef(null);

  // 处理文件选择
  const handleFileSelect = () => {
    fileInputRef.current?.click();
  };

  // 处理文件上传
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // 重置状态
    setUploadProgress(0);
    setIsUploading(true);
    setUploadStatus('uploading');

    try {
      // 创建 FormData 对象
      const formData = new FormData();
      formData.append('file', file);

      // 发送文件到后端
      const response = await axios.post(`/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          // 计算上传进度百分比
          if (progressEvent.total) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(percentCompleted);
          }
        },
      });

      // 上传成功
      setUploadStatus('success');
      setIsUploading(false);

    } catch (error) {
      console.error('上传失败:', error);
      setUploadStatus('error');
      setIsUploading(false);
    }
  };

  // 根据上传状态渲染不同的 UI
  const renderButtonContent = () => {
    if (isUploading) {
      return (
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>上传中...</span>
          <div className="uploading">
            <div style={{
              width: `${uploadProgress}%`,
              height: '100%',
              backgroundColor: '#4caf50',
              transition: 'width 0.3s ease'
            }}></div>
          </div>
          <span>{uploadProgress}%</span>
        </div>
      );
    } else if (uploadStatus === 'success') {
      return '上传成功';
    } else if (uploadStatus === 'error') {
      return '上传失败';
    } else {
      return '上传文件';
    }
  };

  return (
    <div style={{ display: 'inline-block' }}>
      {/* 隐藏的文件输入元素 */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        style={{ display: 'none' }}
        disabled={isUploading}
      />

      {/* 上传按钮 */}
      <button
        onClick={handleFileSelect}
        disabled={isUploading}
        className="upload-button"
        style={{
          backgroundColor: uploadStatus === 'success' ? '#4caf50' :
                          uploadStatus === 'error' ? '#f44336' : '#3f51b5',
          cursor: isUploading ? 'wait' : 'pointer',
        }}
      >
        {renderButtonContent()}
      </button>
    </div>
  );
};

export default FileUploadButton;