import CVUpload from '../components/CVUpload';

export default function Home() {
  return (
    <div className="py-10">
      <h1 className="text-3xl font-bold text-center mb-2">Bienvenue sur JobMatch</h1>
      <p className="text-center text-gray-600 mb-8">Déposez votre CV pour trouver les offres d'emploi qui vous correspondent.</p>
      <CVUpload />
    </div>
  );
}