```tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: 'Stat4Ballers - Statistiques Ligue 1',
  description: 'Toutes les stats des joueurs de Ligue 1 : données offensives, défensives et créatives pour chaque joueur.',
  keywords: ['Statistiques Ligue 1', 'Stats joueurs football', 'xG', 'xA', 'Data football'],
  openGraph: {
    title: 'Stat4Ballers - Stats Ligue 1',
    description: 'Visualisez toutes les stats des joueurs de Ligue 1 en un coup d\'œil.',
    url: 'https://stat4ballers.vercel.app',
    siteName: 'Stat4Ballers',
    type: 'website',
  },
  metadataBase: new URL('https://stat4ballers.vercel.app'),
  alternates: {
    canonical: '/',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```