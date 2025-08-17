import type { Metadata } from "next";
import { Poppins } from "next/font/google";
import "./globals.css";
import Navigation from '@/components/Navigation';
import Footer from '@/components/Footer';

const poppins = Poppins({
  subsets: ["latin"],
  weight: ['300', '400', '500', '600', '700', '800'],
  variable: '--font-poppins',
});

export const metadata: Metadata = {
  title: "Stat4Ballers - Statistiques Football des 5 Grands Championnats",
  description: "Analysez les performances des joueurs de Ligue 1, Premier League, Liga, Serie A et Bundesliga avec des statistiques détaillées et des graphiques radar.",
  keywords: "football, statistiques, Ligue 1, Premier League, Liga, Serie A, Bundesliga, stats joueurs, xG, xA",
  openGraph: {
    title: "Stat4Ballers - Stats Football Européen",
    description: "Toutes les statistiques des joueurs des 5 grands championnats européens",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body className={`${poppins.className} antialiased`}>
        <Navigation />
        <div className="pt-16">
          {children}
        </div>
        <Footer />
      </body>
    </html>
  );
}
