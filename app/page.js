import { getPosts } from '@/lib/wordpress';
import ArticleCard from '@/components/ArticleCard';
import Pagination from '@/components/Pagination';
import { Suspense } from 'react';
import LoadingSpinner from '@/components/LoadingSpinner';

export const metadata = {
  title: 'Newspaper Now - Latest News & Updates',
  description: 'Stay informed with the latest news from around the world. Politics, Tech, Business, Sports, and more from Newspaper Now.',
};

export const revalidate = 60; // ISR: Revalidate every 60 seconds

async function HomePage({ searchParams }) {
  const page = parseInt(searchParams?.page || '1');
  const { posts, totalPages, totalPosts, currentPage } = await getPosts({ page, perPage: 9 });

  if (posts.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4">No Articles Found</h1>
          <p className="text-muted-foreground">
            We couldn't find any articles. Please check back later.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Hero Section */}
      <div className="mb-12">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Latest News & Updates
        </h1>
        <p className="text-xl text-muted-foreground">
          Stay informed with our comprehensive coverage of current events
        </p>
      </div>

      {/* Articles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {posts.map((post) => (
          <ArticleCard key={post.id} post={post} />
        ))}
      </div>

      {/* Pagination */}
      <Pagination currentPage={currentPage} totalPages={totalPages} />
    </div>
  );
}

export default function Page({ searchParams }) {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <HomePage searchParams={searchParams} />
    </Suspense>
  );
}