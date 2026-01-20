import { getPosts, getCategoryBySlug } from '@/lib/wordpress';
import ArticleCard from '@/components/ArticleCard';
import Pagination from '@/components/Pagination';
import { Suspense } from 'react';
import LoadingSpinner from '@/components/LoadingSpinner';
import { notFound } from 'next/navigation';

export const revalidate = 60; // ISR: Revalidate every 60 seconds

export async function generateMetadata({ params }) {
  const category = await getCategoryBySlug(params.slug);
  
  if (!category) {
    return {
      title: 'Category Not Found',
    };
  }

  return {
    title: `${category.name} News - NewsHub`,
    description: category.description || `Latest ${category.name} news and updates`,
    openGraph: {
      title: `${category.name} News`,
      description: category.description || `Latest ${category.name} news and updates`,
      type: 'website',
    },
  };
}

async function CategoryPage({ params, searchParams }) {
  const category = await getCategoryBySlug(params.slug);
  
  if (!category) {
    notFound();
  }

  const page = parseInt(searchParams?.page || '1');
  const { posts, totalPages, totalPosts, currentPage } = await getPosts({ 
    page, 
    perPage: 9,
    categories: category.id 
  });

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Category Header */}
      <div className="mb-12">
        <h1 className="text-4xl md:text-5xl font-bold mb-4 capitalize">
          {category.name}
        </h1>
        {category.description && (
          <p className="text-xl text-muted-foreground">
            {category.description}
          </p>
        )}
        <p className="text-muted-foreground mt-2">
          {totalPosts} {totalPosts === 1 ? 'article' : 'articles'} found
        </p>
      </div>

      {/* Articles Grid */}
      {posts.length === 0 ? (
        <div className="text-center py-16">
          <h2 className="text-2xl font-bold mb-4">No Articles Found</h2>
          <p className="text-muted-foreground">
            There are no articles in this category yet. Check back later!
          </p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {posts.map((post) => (
              <ArticleCard key={post.id} post={post} />
            ))}
          </div>
          <Pagination currentPage={currentPage} totalPages={totalPages} />
        </>
      )}
    </div>
  );
}

export default function Page({ params, searchParams }) {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <CategoryPage params={params} searchParams={searchParams} />
    </Suspense>
  );
}