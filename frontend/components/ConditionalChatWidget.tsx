'use client';

import { usePathname } from 'next/navigation';
import ChatWidget from './ChatWidget';

// Pages where ChatWidget should NOT appear
const EXCLUDED_PATHS = [
  '/landing',
  '/auth/signup',
  '/auth/signin',
];

export default function ConditionalChatWidget() {
  const pathname = usePathname();

  // Don't show ChatWidget on excluded paths
  if (EXCLUDED_PATHS.includes(pathname)) {
    return null;
  }

  return <ChatWidget />;
}
