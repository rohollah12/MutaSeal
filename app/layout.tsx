import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'MutaSeal | Self-evolving GenLayer guard',
  description: 'A bounded self-evolving security contract powered by GenLayer consensus.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
