"use client";

import { useState, useEffect } from 'react';
import { getCVProfile } from '../lib/api';
import { useRouter } from 'next/navigation';

export default function ProfileEditor() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const cvId = localStorage.getItem('cvId');
    if (!cvId) {
      setLoading(false);
      return;
    }
    
    getCVProfile(cvId)
      .then(data => {
        setProfile(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const handleSave = () => {
    // In a real app, we would send the updated profile to the backend
    alert('Profil sauvegardé !');
    router.push('/dashboard');
  };

  if (loading) return <p>Chargement du profil...</p>;
  if (!profile) return <p>Aucun CV trouvé. Veuillez uploader un CV d'abord.</p>;

  return (
    <div className="bg-white p-6 rounded-lg shadow max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Votre Profil (Extrait du CV)</h2>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Titres de poste</label>
          <input 
            type="text" 
            className="w-full border border-gray-300 rounded p-2" 
            value={profile.titles?.join(', ') || ''} 
            onChange={(e) => setProfile({...profile, titles: e.target.value.split(', ')})}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Compétences</label>
          <textarea 
            className="w-full border border-gray-300 rounded p-2" 
            rows={3}
            value={profile.skills?.join(', ') || ''} 
            onChange={(e) => setProfile({...profile, skills: e.target.value.split(', ')})}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Années d'expérience</label>
          <input 
            type="number" 
            className="w-full border border-gray-300 rounded p-2" 
            value={profile.years_experience || 0} 
            onChange={(e) => setProfile({...profile, years_experience: parseInt(e.target.value)})}
          />
        </div>
        
        <button 
          onClick={handleSave}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition-colors mt-4"
        >
          Valider et chercher des offres
        </button>
      </div>
    </div>
  );
}