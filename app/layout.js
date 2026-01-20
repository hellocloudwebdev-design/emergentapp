import './globals.css'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export const metadata = {
  title: 'Newspaper Now - Latest News & Updates',
  description: 'Stay informed with the latest news from around the world. Politics, Tech, Business, Sports, and more from Newspaper Now.',
  openGraph: {
    title: 'Newspaper Now - Latest News & Updates',
    description: 'Stay informed with the latest news from around the world.',
    type: 'website',
  },
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-background text-foreground antialiased">
        <Header />
        <main className="min-h-[calc(100vh-200px)]">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}