import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#4F46E5', // indigo-600
        success: '#10B981', // green-500
        warning: '#F59E0B', // amber-500
        danger: '#EF4444', // red-500
        neutral: '#9CA3AF', // gray-400
        background: '#F8FAFC', // slate-50
      },
    },
  },
  plugins: [],
};

export default config;
