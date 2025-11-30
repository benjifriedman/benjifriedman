import os
import random
from configparser import ConfigParser

import flickrapi


def _get_flickr_credentials():
    """Fetch the API credentials from config file in local project.
    Otherwise, grab from GitHub secrets.
    Be sure to add "secrets.ini" to your .gitignore file!

    Expects a configuration file named "secrets.ini" with structure:

        [flickr]
        api_key=<YOUR-FLICKR-API-KEY>
        api_secret=<YOUR-FLICKR-API-SECRET>
        user_id=<YOUR-FLICKR-USER-ID>
    """
    try:
        config = ConfigParser()
        config.read("secrets.ini")
        api_key = config["flickr"]["api_key"]
        api_secret = config["flickr"]["api_secret"]
        user_id = config["flickr"]["user_id"]
    except Exception:
        api_key = os.environ.get("flickr_api_key")
        api_secret = os.environ.get("flickr_api_secret")
        user_id = os.environ.get("flickr_user_id")
    return api_key, api_secret, user_id


def get_random_flickr_photo():
    """Retrieve a random photo from Flickr user's photostream"""
    api_key, api_secret, user_id = _get_flickr_credentials()
    
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    
    # Get public photos from user
    photos_response = flickr.people.getPublicPhotos(
        user_id=user_id,
        per_page=500,
        extras='description,date_taken,geo,tags,url_o,url_k,url_h,url_l'
    )
    
    photos = photos_response['photos']['photo']
    
    if not photos:
        return None
    
    # Try to pick a landscape photo (width > height)
    # We'll check orientation after picking and retry if needed
    max_attempts = 20
    random_photo = None
    
    for _ in range(max_attempts):
        candidate = random.choice(photos)
        try:
            # Get sizes to check orientation
            sizes_response = flickr.photos.getSizes(photo_id=candidate['id'])
            sizes = sizes_response['sizes']['size']
            # Get the largest size available
            largest = sizes[-1]
            width = int(largest['width'])
            height = int(largest['height'])
            if width > height:
                random_photo = candidate
                break
        except:
            continue
    
    # If we couldn't find a landscape photo after max attempts, use the last candidate
    if random_photo is None:
        random_photo = random.choice(photos)
    
    # Get detailed photo info
    photo_info = flickr.photos.getInfo(photo_id=random_photo['id'])
    photo_data = photo_info['photo']
    
    # Try to get EXIF data
    try:
        exif_response = flickr.photos.getExif(photo_id=random_photo['id'])
        exif_data = exif_response['photo']['exif']
    except:
        exif_data = []
    
    # Get the best available image URL
    url = (random_photo.get('url_o') or 
           random_photo.get('url_k') or 
           random_photo.get('url_h') or 
           random_photo.get('url_l') or
           f"https://live.staticflickr.com/{random_photo['server']}/{random_photo['id']}_{random_photo['secret']}_b.jpg")
    
    # Extract EXIF data
    def get_exif_value(label):
        for item in exif_data:
            if item.get('label') == label:
                return item.get('raw', {}).get('_content', '')
        return ''
    
    # Build photo info dictionary
    photo_dict = {
        'url': url,
        'page_url': photo_data['urls']['url'][0]['_content'],
        'title': photo_data['title']['_content'],
        'description': photo_data['description']['_content'],
        'owner_name': photo_data['owner'].get('realname') or photo_data['owner'].get('username', 'Unknown'),
        'owner_url': f"https://www.flickr.com/photos/{photo_data['owner']['nsid']}/",
        'tags': ', '.join([tag['raw'] for tag in photo_data['tags']['tag']]) if photo_data['tags']['tag'] else '',
        'date_taken': photo_data['dates']['taken'],
        'camera_model': get_exif_value('Model'),
        'exposure': get_exif_value('Exposure'),
        'aperture': get_exif_value('Aperture'),
        'focal_length': get_exif_value('Focal Length'),
        'iso': get_exif_value('ISO Speed'),
    }
    
    # Add location data if available
    if 'location' in photo_data:
        location = photo_data['location']
        photo_dict['latitude'] = location.get('latitude', '')
        photo_dict['longitude'] = location.get('longitude', '')
        photo_dict['location'] = (location.get('locality', {}).get('_content') or 
                                 location.get('county', {}).get('_content') or '')
        photo_dict['country'] = location.get('country', {}).get('_content', '')
        
        if photo_dict['latitude'] and photo_dict['longitude']:
            photo_dict['google_maps'] = f"https://www.google.com/maps/search/?api=1&query={photo_dict['latitude']},{photo_dict['longitude']}"
        else:
            photo_dict['google_maps'] = ''
    else:
        photo_dict['latitude'] = ''
        photo_dict['longitude'] = ''
        photo_dict['location'] = ''
        photo_dict['country'] = ''
        photo_dict['google_maps'] = ''
    
    return photo_dict
