#!/usr/bin/env python3
"""
Backend Testing Script for NewsHub News Website
Tests WordPress API integration and health check endpoint
"""

import requests
import json
import time
from urllib.parse import urljoin

# Configuration
BASE_URL = "https://headless-herald.preview.emergentagent.com"
WORDPRESS_API_URL = "https://techcrunch.com/wp-json/wp/v2"

def test_health_check():
    """Test the API health check endpoint"""
    print("\n=== Testing API Health Check ===")
    
    try:
        url = urljoin(BASE_URL, "/api/")
        print(f"Testing: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Verify expected fields
            required_fields = ['message', 'status', 'timestamp']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"❌ Missing required fields: {missing_fields}")
                return False
            
            if data.get('status') == 'healthy':
                print("✅ Health check endpoint working correctly")
                return True
            else:
                print(f"❌ Unexpected status: {data.get('status')}")
                return False
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Health check test failed: {str(e)}")
        return False

def test_wordpress_get_posts():
    """Test WordPress getPosts functionality"""
    print("\n=== Testing WordPress getPosts ===")
    
    try:
        # Test basic posts fetch
        url = f"{WORDPRESS_API_URL}/posts"
        params = {
            'page': 1,
            'per_page': 9,
            '_embed': 'true'
        }
        
        print(f"Testing: {url}")
        response = requests.get(url, params=params, timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ Fetched {len(posts)} posts")
            
            # Check pagination headers
            total_pages = response.headers.get('X-WP-TotalPages')
            total_posts = response.headers.get('X-WP-Total')
            print(f"Total Pages: {total_pages}, Total Posts: {total_posts}")
            
            # Verify post structure
            if posts and len(posts) > 0:
                post = posts[0]
                required_fields = ['id', 'title', 'content', 'excerpt', 'date', 'slug']
                missing_fields = [field for field in required_fields if field not in post]
                
                if missing_fields:
                    print(f"❌ Missing required post fields: {missing_fields}")
                    return False
                
                # Check embedded data
                if '_embedded' in post:
                    print("✅ Embedded data present")
                else:
                    print("⚠️ No embedded data found")
                
                print("✅ Post structure is valid")
                return True
            else:
                print("❌ No posts returned")
                return False
        else:
            print(f"❌ Failed to fetch posts: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ WordPress getPosts test failed: {str(e)}")
        return False

def test_wordpress_pagination():
    """Test WordPress pagination"""
    print("\n=== Testing WordPress Pagination ===")
    
    try:
        # Test page 1
        url = f"{WORDPRESS_API_URL}/posts"
        params1 = {'page': 1, 'per_page': 5, '_embed': 'true'}
        
        response1 = requests.get(url, params=params1, timeout=15)
        print(f"Page 1 Status: {response1.status_code}")
        
        if response1.status_code != 200:
            print("❌ Page 1 fetch failed")
            return False
        
        posts1 = response1.json()
        
        # Test page 2
        params2 = {'page': 2, 'per_page': 5, '_embed': 'true'}
        response2 = requests.get(url, params=params2, timeout=15)
        print(f"Page 2 Status: {response2.status_code}")
        
        if response2.status_code != 200:
            print("❌ Page 2 fetch failed")
            return False
        
        posts2 = response2.json()
        
        # Verify different posts
        if len(posts1) > 0 and len(posts2) > 0:
            post1_ids = [post['id'] for post in posts1]
            post2_ids = [post['id'] for post in posts2]
            
            if set(post1_ids).intersection(set(post2_ids)):
                print("⚠️ Some posts appear on both pages (might be expected)")
            
            print(f"✅ Pagination working - Page 1: {len(posts1)} posts, Page 2: {len(posts2)} posts")
            return True
        else:
            print("❌ Insufficient posts for pagination test")
            return False
            
    except Exception as e:
        print(f"❌ WordPress pagination test failed: {str(e)}")
        return False

def test_wordpress_get_post_by_slug():
    """Test WordPress getPostBySlug functionality"""
    print("\n=== Testing WordPress getPostBySlug ===")
    
    try:
        # First get a post to get its slug
        url = f"{WORDPRESS_API_URL}/posts"
        params = {'page': 1, 'per_page': 1, '_embed': 'true'}
        
        response = requests.get(url, params=params, timeout=15)
        if response.status_code != 200:
            print("❌ Failed to fetch posts for slug test")
            return False
        
        posts = response.json()
        if not posts:
            print("❌ No posts available for slug test")
            return False
        
        test_slug = posts[0]['slug']
        print(f"Testing with slug: {test_slug}")
        
        # Now test fetching by slug
        slug_url = f"{WORDPRESS_API_URL}/posts"
        slug_params = {'slug': test_slug, '_embed': 'true'}
        
        slug_response = requests.get(slug_url, params=slug_params, timeout=15)
        print(f"Status Code: {slug_response.status_code}")
        
        if slug_response.status_code == 200:
            slug_posts = slug_response.json()
            if slug_posts and len(slug_posts) > 0:
                post = slug_posts[0]
                if post['slug'] == test_slug:
                    print("✅ getPostBySlug working correctly")
                    return True
                else:
                    print(f"❌ Slug mismatch: expected {test_slug}, got {post['slug']}")
                    return False
            else:
                print("❌ No post returned for slug")
                return False
        else:
            print(f"❌ Failed to fetch post by slug: {slug_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ WordPress getPostBySlug test failed: {str(e)}")
        return False

def test_wordpress_get_categories():
    """Test WordPress getCategories functionality"""
    print("\n=== Testing WordPress getCategories ===")
    
    try:
        url = f"{WORDPRESS_API_URL}/categories"
        params = {'per_page': 100}
        
        print(f"Testing: {url}")
        response = requests.get(url, params=params, timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Fetched {len(categories)} categories")
            
            if categories and len(categories) > 0:
                category = categories[0]
                required_fields = ['id', 'name', 'slug']
                missing_fields = [field for field in required_fields if field not in category]
                
                if missing_fields:
                    print(f"❌ Missing required category fields: {missing_fields}")
                    return False
                
                print("✅ Category structure is valid")
                return True
            else:
                print("❌ No categories returned")
                return False
        else:
            print(f"❌ Failed to fetch categories: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ WordPress getCategories test failed: {str(e)}")
        return False

def test_wordpress_get_category_by_slug():
    """Test WordPress getCategoryBySlug functionality"""
    print("\n=== Testing WordPress getCategoryBySlug ===")
    
    try:
        # First get categories to get a slug
        url = f"{WORDPRESS_API_URL}/categories"
        params = {'per_page': 10}
        
        response = requests.get(url, params=params, timeout=15)
        if response.status_code != 200:
            print("❌ Failed to fetch categories for slug test")
            return False
        
        categories = response.json()
        if not categories:
            print("❌ No categories available for slug test")
            return False
        
        test_slug = categories[0]['slug']
        print(f"Testing with category slug: {test_slug}")
        
        # Now test fetching by slug
        slug_url = f"{WORDPRESS_API_URL}/categories"
        slug_params = {'slug': test_slug}
        
        slug_response = requests.get(slug_url, params=slug_params, timeout=15)
        print(f"Status Code: {slug_response.status_code}")
        
        if slug_response.status_code == 200:
            slug_categories = slug_response.json()
            if slug_categories and len(slug_categories) > 0:
                category = slug_categories[0]
                if category['slug'] == test_slug:
                    print("✅ getCategoryBySlug working correctly")
                    return True
                else:
                    print(f"❌ Slug mismatch: expected {test_slug}, got {category['slug']}")
                    return False
            else:
                print("❌ No category returned for slug")
                return False
        else:
            print(f"❌ Failed to fetch category by slug: {slug_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ WordPress getCategoryBySlug test failed: {str(e)}")
        return False

def test_wordpress_category_filtering():
    """Test WordPress category filtering"""
    print("\n=== Testing WordPress Category Filtering ===")
    
    try:
        # First get a category ID
        categories_url = f"{WORDPRESS_API_URL}/categories"
        cat_response = requests.get(categories_url, params={'per_page': 10}, timeout=15)
        
        if cat_response.status_code != 200:
            print("❌ Failed to fetch categories for filtering test")
            return False
        
        categories = cat_response.json()
        if not categories:
            print("❌ No categories available for filtering test")
            return False
        
        test_category_id = categories[0]['id']
        test_category_name = categories[0]['name']
        print(f"Testing filtering with category: {test_category_name} (ID: {test_category_id})")
        
        # Test filtering posts by category
        posts_url = f"{WORDPRESS_API_URL}/posts"
        filter_params = {
            'categories': test_category_id,
            'per_page': 5,
            '_embed': 'true'
        }
        
        filter_response = requests.get(posts_url, params=filter_params, timeout=15)
        print(f"Status Code: {filter_response.status_code}")
        
        if filter_response.status_code == 200:
            filtered_posts = filter_response.json()
            print(f"✅ Category filtering working - Found {len(filtered_posts)} posts in category '{test_category_name}'")
            return True
        else:
            print(f"❌ Category filtering failed: {filter_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ WordPress category filtering test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all backend tests"""
    print("🚀 Starting NewsHub Backend Tests")
    print("=" * 50)
    
    test_results = {}
    
    # Test API Health Check (LOW PRIORITY)
    test_results['health_check'] = test_health_check()
    
    # Test WordPress API Integration (HIGH PRIORITY)
    test_results['wordpress_get_posts'] = test_wordpress_get_posts()
    test_results['wordpress_pagination'] = test_wordpress_pagination()
    test_results['wordpress_get_post_by_slug'] = test_wordpress_get_post_by_slug()
    test_results['wordpress_get_categories'] = test_wordpress_get_categories()
    test_results['wordpress_get_category_by_slug'] = test_wordpress_get_category_by_slug()
    test_results['wordpress_category_filtering'] = test_wordpress_category_filtering()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All backend tests passed!")
    else:
        print("⚠️ Some tests failed - check logs above")
    
    return test_results

if __name__ == "__main__":
    run_all_tests()