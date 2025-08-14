import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface FileUploadProps {
  file: File | null;
  onFileSelect: (file: File | null) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ file, onFileSelect }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false
  });

  return (
    <div className="file-upload">
      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
      >
        <input {...getInputProps()} />
        {file ? (
          <div className="file-info">
            <p>📄 {file.name}</p>
            <p className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            <button 
              type="button" 
              onClick={(e) => {
                e.stopPropagation();
                onFileSelect(null);
              }}
              className="remove-file"
            >
              ✕ Remover
            </button>
          </div>
        ) : (
          <div className="upload-prompt">
            <p>📁 Arraste o PDF do laudo aqui ou clique para selecionar</p>
            <p className="upload-hint">Apenas arquivos PDF são aceitos</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;