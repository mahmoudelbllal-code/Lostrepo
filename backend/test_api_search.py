import requests
import os

# Configuration
BASE_URL = 'http://localhost:5000/api/search'
TEST_IMAGE = 'test_search_image.jpg'

# Download a test image if not exists
if not os.path.exists(TEST_IMAGE):
    print("Downloading test image...")
    # Using a wallet image that should match the pink wallet in static DB
    img_url = 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=500'
    r = requests.get(img_url)
    with open(TEST_IMAGE, 'wb') as f:
        f.write(r.content)

def test_search():
    print(f"Testing search endpoint: {BASE_URL}")
    
    with open(TEST_IMAGE, 'rb') as f:
        files = {'image': f}
        try:
            response = requests.post(BASE_URL, files=files)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("Success!")
                results = data.get('results', [])
                print(f"Found {len(results)} results")
                
                if results:
                    first_match = results[0]
                    print(f"Top match: {first_match['post']['title']} ({first_match['similarity']:.2%})")
                else:
                    print("No matches found (but request succeeded)")
            else:
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed. Is the backend running?")

if __name__ == '__main__':
    test_search()
    # Cleanup
    if os.path.exists(TEST_IMAGE):
        os.remove(TEST_IMAGE)
