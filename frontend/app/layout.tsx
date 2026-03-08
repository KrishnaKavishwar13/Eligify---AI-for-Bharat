import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Providers from '@/components/Providers';
import NotificationBanner from '@/components/NotificationBanner';
import ConditionalChatWidget from '@/components/ConditionalChatWidget';
import '@/styles/globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Eligify - AI-Powered Employability Platform',
  description:
    'Build skills, unlock opportunities, and land your dream internship',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          {children}
          <NotificationBanner />
          <ConditionalChatWidget />
        </Providers>
      </body>
    </html>
  );
}
