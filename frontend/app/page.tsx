import { redirect } from 'next/navigation';

export default function HomePage() {
  // Redirect to landing page for unauthenticated users
  redirect('/landing');
}
