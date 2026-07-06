"use client";

import { useState, useEffect } from 'react';
import { searchJobs, getSearchResults } from '../lib/api';

export default function JobDashboard() {
  const [offers, setOffers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const cvId = localStorage.getItem('cvId');
    if (!cvId) {
      setLoading(false);
      return;
    }

    const fetchJobs = async () => {
      try {
        const { search_id } = await searchJobs(cvId);
        // In a real app, we might poll here if search is async
        const results = await getSearchResults(search_id);
        setOffers(results);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, []);

  const filteredOffers = offers.filter(offer => 
    offer.title.toLowerCase().includes(filter.toLowerCase()) || 
    offer.company.toLowerCase().includes(filter.toLowerCase())
  );

  if (loading) return <p>Recherche des meilleures offres en cours...</p>;

  return (
    <div>
      <div className="mb-6 flex justify-between items-center">
        <h2 className="text-2xl font-bold">Offres d'emploi recommandées</h2>
        <input 
          type="text" 
          placeholder="Filtrer par titre ou entreprise..." 
          className="border border-gray-300 rounded p-2 w-64"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
      </div>

      {offers.length === 0 ? (
        <p className="text-gray-500">Aucune offre trouvée. Avez-vous uploadé votre CV ?</p>
      ) : (
        <div className="grid gap-4">
          {filteredOffers.map((offer, idx) => (
            <div key={idx} className="bg-white p-4 rounded-lg shadow border border-gray-100 flex justify-between items-start">
              <div>
                <h3 className="text-lg font-semibold text-blue-700">{offer.title}</h3>
                <p className="text-gray-600">{offer.company} - {offer.location}</p>
                <p className="text-sm text-gray-500 mt-2 line-clamp-2">{offer.description}</p>
              </div>
              <div className="text-right ml-4 shrink-0">
                <div className="inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full font-bold text-lg">
                  {offer.score}% Match
                </div>
                <a 
                  href={offer.url} 
                  target="_blank" 
                  rel="noreferrer"
                  className="block mt-3 text-sm text-blue-600 hover:underline"
                >
                  Voir l'offre
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}