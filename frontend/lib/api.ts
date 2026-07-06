const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function uploadCV(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  
  const res = await fetch(`${API_BASE_URL}/cv/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}

export async function getCVStatus(id: string) {
  const res = await fetch(`${API_BASE_URL}/cv/${id}/status`);
  if (!res.ok) throw new Error('Failed to fetch status');
  return res.json();
}

export async function getCVProfile(id: string) {
  const res = await fetch(`${API_BASE_URL}/cv/${id}/profile`);
  if (!res.ok) throw new Error('Failed to fetch profile');
  return res.json();
}

export async function searchJobs(cvId: string) {
  const res = await fetch(`${API_BASE_URL}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ cv_id: cvId }),
  });
  if (!res.ok) throw new Error('Search failed');
  return res.json();
}

export async function getSearchResults(searchId: string) {
  const res = await fetch(`${API_BASE_URL}/search/${searchId}/results`);
  if (!res.ok) throw new Error('Failed to fetch results');
  return res.json();
}