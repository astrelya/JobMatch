"use client";

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadCV, getCVStatus } from '../lib/api';
import { useRouter } from 'next/navigation';

export default function CVUpload() {
  const [status, setStatus] = useState<'idle' | 'uploading' | 'parsing' | 'done' | 'error'>('idle');
  const [errorMsg, setErrorMsg] = useState('');
  const router = useRouter();

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    const file = acceptedFiles[0];
    
    try {
      setStatus('uploading');
      const { id } = await uploadCV(file);
      
      setStatus('parsing');
      // Poll for status
      const interval = setInterval(async () => {
        try {
          const { status: parseStatus } = await getCVStatus(id);
          if (parseStatus === 'done') {
            clearInterval(interval);
            setStatus('done');
            localStorage.setItem('cvId', id);
            router.push('/profile');
          } else if (parseStatus === 'error') {
            clearInterval(interval);
            setStatus('error');
            setErrorMsg('Erreur lors de l\\'analyse du CV');
          }
        } catch (e) {
          clearInterval(interval);
          setStatus('error');
          setErrorMsg('Erreur de connexion');
        }
      }, 2000);
    } catch (e) {
      setStatus('error');
      setErrorMsg('Erreur lors de l\\'upload');
    }
  }, [router]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: { 'application/pdf': ['.pdf'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'] } });

  return (
    <div className="max-w-xl mx-auto mt-10">
      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed p-10 text-center rounded-lg cursor-pointer transition-colors ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'}`}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p className="text-blue-500">Déposez le CV ici...</p>
        ) : (
          <p className="text-gray-600">Glissez-déposez votre CV (PDF ou DOCX) ici, ou cliquez pour sélectionner</p>
        )}
      </div>
      
      {status !== 'idle' && (
        <div className="mt-6 p-4 rounded bg-white shadow">
          <p className="font-medium">Statut : 
            {status === 'uploading' && <span className="text-blue-500 ml-2">Upload en cours...</span>}
            {status === 'parsing' && <span className="text-yellow-500 ml-2">Analyse du CV en cours...</span>}
            {status === 'done' && <span className="text-green-500 ml-2">Terminé ! Redirection...</span>}
            {status === 'error' && <span className="text-red-500 ml-2">{errorMsg}</span>}
          </p>
        </div>
      )}
    </div>
  );
}