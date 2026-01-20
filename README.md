# NewsHub - Modern Headless WordPress News Website

A production-ready, SEO-optimized news website built with Next.js 14 (App Router), Tailwind CSS, and headless WordPress as CMS.

## 🚀 Features

### Core Features
- ✅ **Headless WordPress Integration** - Fetch content via WordPress REST API
- ✅ **Homepage** - Latest news in responsive grid layout with pagination
- ✅ **Dynamic Article Pages** - SEO-optimized individual article pages with featured images
- ✅ **Category Pages** - Browse news by categories (Politics, Tech, Business, Sports)
- ✅ **Pagination** - Navigate through multiple pages of articles
- ✅ **ISR (Incremental Static Regeneration)** - Fresh content every 60 seconds
- ✅ **Mobile-First Design** - Fully responsive across all devices
- ✅ **SEO Optimized** - Dynamic meta tags, Open Graph, Twitter Cards
- ✅ **Reading Time** - Auto-calculated reading time for each article
- ✅ **Clean UI** - Modern design with shadcn/ui components

### Technical Features
- Next.js 14 App Router with Server Components
- Tailwind CSS for styling with semantic design tokens
- WordPress REST API integration with _embed support
- ISR for optimal performance and fresh content
- TypeScript-ready structure
- Production-ready error handling

## 📁 Project Structure

```
/app
├── app/
│   ├── layout.js                 # Root layout with Header & Footer
│   ├── page.js                   # Homepage with latest articles
│   ├── article/[slug]/
│   │   ├── page.js              # Dynamic article page
│   │   └── not-found.js         # 404 for missing articles
│   ├── category/[slug]/
│   │   ├── page.js              # Dynamic category page
│   │   └── not-found.js         # 404 for missing categories
│   └── api/[[...path]]/
│       └── route.js             # API health check
├── components/
│   ├── Header.js                # Navigation header
│   ├── Footer.js                # Site footer
│   ├── ArticleCard.js           # Article preview card
│   ├── Pagination.js            # Pagination component
│   └── LoadingSpinner.js        # Loading state
├── lib/
│   └── wordpress.js             # WordPress API utilities
├── .env                         # Environment variables
└── README.md                    # This file
```

## 🛠 Setup & Installation

### 1. Configure WordPress API

Edit `.env` file:

```bash
# WordPress API Configuration
NEXT_PUBLIC_WORDPRESS_API_URL=https://your-wordpress-site.com/wp-json/wp/v2

# Or use the demo TechCrunch API (default)
NEXT_PUBLIC_WORDPRESS_API_URL=https://techcrunch.com/wp-json/wp/v2
```

### 2. Install Dependencies

```bash
yarn install
```

### 3. Run Development Server

```bash
yarn dev
```

The site will be available at `http://localhost:3000`

### 4. Build for Production

```bash
yarn build
yarn start
```

## 🔧 Configuration

### WordPress Setup

**Using Your Own WordPress Site:**

1. Ensure WordPress REST API is enabled (enabled by default)
2. Install WP plugins (optional but recommended):
   - Yoast SEO (for better meta descriptions)
   - Featured Images (should be enabled by default)
3. Update `.env` with your WordPress URL:
   ```
   NEXT_PUBLIC_WORDPRESS_API_URL=https://yourdomain.com/wp-json/wp/v2
   ```
4. Create categories: Politics, Tech, Business, Sports (or use your own)

### Customization

#### Change Number of Articles Per Page

Edit `lib/wordpress.js`:
```javascript
// Change default perPage value
const { page = 1, perPage = 9, ... } = params;  // Change 9 to your desired number
```

#### Customize Categories

Edit `components/Header.js` to add/remove categories:
```javascript
const categories = [
  { name: 'Politics', slug: 'politics' },
  { name: 'Tech', slug: 'tech' },
  // Add more categories...
];
```

#### ISR Revalidation Time

Change revalidation frequency in page files:
```javascript
export const revalidate = 60; // Change to desired seconds
```

## 🎨 Styling

This project uses:
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Beautiful, accessible component library
- **Semantic color tokens** - Consistent theming

To customize the theme, edit `tailwind.config.js` and `app/globals.css`.

## 📱 Pages & Routes

### Homepage
- Route: `/`
- Shows latest 9 articles with pagination
- SEO optimized with site-wide meta tags

### Article Page
- Route: `/article/[slug]`
- Dynamic route based on WordPress post slug
- Features: Featured image, author, date, reading time, full content
- SEO: Dynamic meta tags, Open Graph, Twitter Cards

### Category Page
- Route: `/category/[slug]`
- Filters articles by category
- Shows article count and pagination
- Categories: politics, tech, business, sports (or dynamic)

## 🚀 Deployment

### Deploy to Vercel (Recommended)

1. Push code to GitHub
2. Import project to Vercel
3. Add environment variable:
   ```
   NEXT_PUBLIC_WORDPRESS_API_URL=your_wordpress_url
   ```
4. Deploy!

Vercel automatically handles:
- ISR (Incremental Static Regeneration)
- Image optimization
- Edge caching
- Automatic HTTPS

### Deploy to Other Platforms

This is a standard Next.js app and can be deployed to:
- Netlify
- AWS Amplify
- DigitalOcean App Platform
- Railway
- Any Node.js hosting

## 🔍 SEO Features

- ✅ Dynamic meta titles and descriptions
- ✅ Open Graph tags for social sharing
- ✅ Twitter Card support
- ✅ Semantic HTML structure
- ✅ Mobile-friendly viewport
- ✅ Fast loading with ISR
- ✅ Image optimization with Next.js Image

## 📊 WordPress API Endpoints Used

- `GET /wp-json/wp/v2/posts` - Fetch posts
- `GET /wp-json/wp/v2/posts?slug={slug}` - Get single post
- `GET /wp-json/wp/v2/categories` - Fetch categories
- `GET /wp-json/wp/v2/categories?slug={slug}` - Get category

All requests use `_embed=true` to include author and featured media.

## 🛡 Error Handling

- Graceful fallbacks for missing data
- 404 pages for invalid articles/categories
- Loading states during data fetching
- API error handling with fallback responses

## 🎯 Performance

- **ISR**: Content revalidates every 60 seconds
- **Server Components**: Fast initial page load
- **Image Optimization**: Next.js automatic image optimization
- **Pagination**: Efficient data loading

## 📝 API Utility Functions

Available in `lib/wordpress.js`:

```javascript
// Fetch posts with pagination and filters
await getPosts({ page: 1, perPage: 9, categories: '123' })

// Get single post by slug
await getPostBySlug('my-article-slug')

// Fetch all categories
await getCategories()

// Get category by slug
await getCategoryBySlug('tech')

// Helper functions
getFeaturedImage(post)
getAuthorName(post)
calculateReadingTime(content)
stripHtml(html)
createExcerpt(content, maxLength)
```

## 🐛 Troubleshooting

### No Articles Showing

1. Check WordPress API URL in `.env`
2. Test API manually: `curl https://your-site.com/wp-json/wp/v2/posts`
3. Ensure WordPress REST API is enabled
4. Check CORS settings if using custom WordPress

### Images Not Loading

- WordPress featured images must be set
- Falls back to `/placeholder-news.jpg` if no featured image
- Next.js Image optimization requires proper image URLs

### Categories Not Working

- Ensure categories exist in WordPress with correct slugs
- Categories are case-sensitive in URLs
- Category slugs should match URL slugs

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

This is a template project. Feel free to customize for your needs!

## 📞 Support

For WordPress-specific issues, refer to [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/).

---

**Built with ❤️ using Next.js, Tailwind CSS, and WordPress**
