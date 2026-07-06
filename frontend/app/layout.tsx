import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";

export const metadata: Metadata = {
  title: "JobMatch",
  description: "Plateforme de matching CV ↔ offres d'emploi",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body className="bg-gray-50 text-gray-900 min-h-screen flex flex-col">
        <header className="bg-white shadow-sm p-4">
          <div className="max-w-5xl mx-auto flex justify-between items-center">
            <Link href="/" className="text-xl font-bold text-blue-600">JobMatch</Link>
            <nav className="space-x-4">
              <Link href="/" className="hover:text-blue-600">Upload CV</Link>
              <Link href="/dashboard" className="hover:text-blue-600">Dashboard</Link>
              <Link href="/profile" className="hover:text-blue-600">Profil</Link>
            </nav>
          </div>
        </header>
        <main className="flex-grow max-w-5xl mx-auto w-full p-4">
          {children}
        </main>
      </body>
    </html>
  );
}