// WordPress API utility functions

const WP_API_URL = process.env.NEXT_PUBLIC_WORDPRESS_API_URL || 'https://demo.wp-api.org/wp-json/wp/v2';

/**
 * Fetch posts from WordPress
 * @param {Object} params - Query parameters
 * @returns {Promise<Array>} Array of posts
 */
export async function getPosts(params = {}) {
  const { page = 1, perPage = 9, categories = '', search = '' } = params;
  
  const queryParams = new URLSearchParams({
    page: page.toString(),
    per_page: perPage.toString(),
    _embed: 'true', // Include author and featured media
  });

  if (categories) {
    queryParams.append('categories', categories);
  }

  if (search) {
    queryParams.append('search', search);
  }

  try {
    const response = await fetch(`${WP_API_URL}/posts?${queryParams.toString()}`, {
      next: { revalidate: 60 }, // ISR: revalidate every 60 seconds
    });

    if (!response.ok) {
      throw new Error('Failed to fetch posts');
    }

    const totalPages = parseInt(response.headers.get('X-WP-TotalPages') || '1');
    const totalPosts = parseInt(response.headers.get('X-WP-Total') || '0');
    const posts = await response.json();

    return {
      posts,
      totalPages,
      totalPosts,
      currentPage: page,
    };
  } catch (error) {
    console.error('Error fetching posts:', error);
    return {
      posts: [],
      totalPages: 1,
      totalPosts: 0,
      currentPage: 1,
    };
  }
}

/**
 * Fetch a single post by slug
 * @param {string} slug - Post slug
 * @returns {Promise<Object|null>} Post object or null
 */
export async function getPostBySlug(slug) {
  try {
    const response = await fetch(
      `${WP_API_URL}/posts?slug=${slug}&_embed=true`,
      {
        next: { revalidate: 60 },
      }
    );

    if (!response.ok) {
      throw new Error('Failed to fetch post');
    }

    const posts = await response.json();
    return posts[0] || null;
  } catch (error) {
    console.error('Error fetching post:', error);
    return null;
  }
}

/**
 * Fetch all categories
 * @returns {Promise<Array>} Array of categories
 */
export async function getCategories() {
  try {
    const response = await fetch(`${WP_API_URL}/categories?per_page=100`, {
      next: { revalidate: 3600 }, // Cache for 1 hour
    });

    if (!response.ok) {
      throw new Error('Failed to fetch categories');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching categories:', error);
    return [];
  }
}

/**
 * Fetch a category by slug
 * @param {string} slug - Category slug
 * @returns {Promise<Object|null>} Category object or null
 */
export async function getCategoryBySlug(slug) {
  try {
    const response = await fetch(`${WP_API_URL}/categories?slug=${slug}`, {
      next: { revalidate: 3600 },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch category');
    }

    const categories = await response.json();
    return categories[0] || null;
  } catch (error) {
    console.error('Error fetching category:', error);
    return null;
  }
}

/**
 * Extract featured image URL from post
 * @param {Object} post - WordPress post object
 * @returns {string} Image URL or placeholder
 */
export function getFeaturedImage(post) {
  if (post._embedded?.['wp:featuredmedia']?.[0]?.source_url) {
    return post._embedded['wp:featuredmedia'][0].source_url;
  }
  return '/placeholder-news.jpg';
}

/**
 * Extract author name from post
 * @param {Object} post - WordPress post object
 * @returns {string} Author name
 */
export function getAuthorName(post) {
  return post._embedded?.author?.[0]?.name || 'Unknown Author';
}

/**
 * Calculate reading time
 * @param {string} content - HTML content
 * @returns {number} Reading time in minutes
 */
export function calculateReadingTime(content) {
  const text = content.replace(/<[^>]*>/g, '');
  const wordCount = text.split(/\s+/).length;
  const readingTime = Math.ceil(wordCount / 200); // Assuming 200 words per minute
  return readingTime;
}

/**
 * Strip HTML tags from content
 * @param {string} html - HTML string
 * @returns {string} Plain text
 */
export function stripHtml(html) {
  return html.replace(/<[^>]*>/g, '');
}

/**
 * Create excerpt from content
 * @param {string} content - Content string
 * @param {number} maxLength - Maximum length
 * @returns {string} Excerpt
 */
export function createExcerpt(content, maxLength = 150) {
  const text = stripHtml(content);
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength).trim() + '...';
}