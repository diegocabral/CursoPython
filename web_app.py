"""
Flask Web Application for Google Maps Route Planner

This web app provides a user-friendly interface for planning optimal routes
using the Google Maps API.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
from route_planner import RouteOptimizer
import json
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Global route optimizer instance
optimizer = None

def init_optimizer():
    """Initialize the RouteOptimizer with API key"""
    global optimizer
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if api_key:
        optimizer = RouteOptimizer(api_key)
        return True
    return False

@app.route('/')
def index():
    """Main page"""
    api_configured = init_optimizer()
    return render_template('index.html', api_configured=api_configured)

@app.route('/api/add_address', methods=['POST'])
def add_address():
    """Add an address to the route planning list"""
    global optimizer
    
    if not optimizer:
        return jsonify({'success': False, 'error': 'API not configured'})
    
    data = request.get_json()
    address = data.get('address', '').strip()
    
    if not address:
        return jsonify({'success': False, 'error': 'Address is required'})
    
    success = optimizer.add_address(address)
    
    if success:
        return jsonify({
            'success': True,
            'addresses': [addr['formatted'] for addr in optimizer.addresses],
            'count': len(optimizer.addresses)
        })
    else:
        return jsonify({'success': False, 'error': 'Could not geocode address'})

@app.route('/api/clear_addresses', methods=['POST'])
def clear_addresses():
    """Clear all addresses"""
    global optimizer
    
    if not optimizer:
        return jsonify({'success': False, 'error': 'API not configured'})
    
    optimizer.clear_addresses()
    return jsonify({'success': True, 'addresses': [], 'count': 0})

@app.route('/api/delete_address', methods=['POST'])
def delete_address():
    """Delete a specific address by index"""
    global optimizer
    
    if not optimizer:
        return jsonify({'success': False, 'error': 'API not configured'})
    
    data = request.get_json()
    index = data.get('index')
    
    if index is None or index < 0 or index >= len(optimizer.addresses):
        return jsonify({'success': False, 'error': 'Invalid address index'})
    
    # Remove the address at the specified index
    deleted_address = optimizer.addresses.pop(index)
    
    # Clear route data since addresses changed
    optimizer.route_data = None
    
    return jsonify({
        'success': True,
        'addresses': [addr['formatted'] for addr in optimizer.addresses],
        'count': len(optimizer.addresses),
        'deleted': deleted_address['formatted']
    })

@app.route('/api/search_addresses', methods=['POST'])
def search_addresses():
    """Search for address suggestions using Google Places API"""
    global optimizer
    
    if not optimizer:
        return jsonify({'success': False, 'error': 'API not configured'})
    
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if len(query) < 3:
        return jsonify({'success': False, 'error': 'Query too short'})
    
    try:
        # Use Google Places API for autocomplete
        autocomplete_result = optimizer.gmaps.places_autocomplete(
            input_text=query,
            types=['address'],  # Focus on addresses
            language='en'
        )
        
        suggestions = []
        for prediction in autocomplete_result[:5]:  # Limit to 5 suggestions
            # Extract main text and secondary text
            structured_formatting = prediction.get('structured_formatting', {})
            main_text = structured_formatting.get('main_text', prediction['description'])
            secondary_text = structured_formatting.get('secondary_text', '')
            
            suggestions.append({
                'place_id': prediction['place_id'],
                'description': prediction['description'],
                'main_text': main_text,
                'secondary_text': secondary_text
            })
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        print(f"Error in address search: {str(e)}")
        return jsonify({'success': False, 'error': 'Address search failed'})

@app.route('/api/get_addresses', methods=['GET'])
def get_addresses():
    """Get current list of addresses"""
    global optimizer
    
    if not optimizer:
        return jsonify({'success': False, 'error': 'API not configured'})
    
    return jsonify({
        'success': True,
        'addresses': [addr['formatted'] for addr in optimizer.addresses],
        'count': len(optimizer.addresses)
    })

@app.route('/api/calculate_route', methods=['POST'])
def calculate_route():
    """Calculate the optimal route"""
    global optimizer
    
    if not optimizer:
        return jsonify({'success': False, 'error': 'API not configured'})
    
    if len(optimizer.addresses) < 2:
        return jsonify({'success': False, 'error': 'At least 2 addresses are required'})
    
    data = request.get_json()
    return_to_start = data.get('return_to_start', False)
    
    try:
        route_data = optimizer.optimize_route(return_to_start=return_to_start)
        summary = optimizer.get_route_summary()
        
        # Generate map file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        map_filename = f"route_map_{timestamp}.html"
        map_path = optimizer.generate_map(f"static/maps/{map_filename}")
        
        return jsonify({
            'success': True,
            'summary': summary,
            'map_url': f'/static/maps/{map_filename}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/export_data', methods=['POST'])
def export_data():
    """Export route data to JSON"""
    global optimizer
    
    if not optimizer or not optimizer.route_data:
        return jsonify({'success': False, 'error': 'No route calculated'})
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"route_data_{timestamp}.json"
        filepath = f"static/exports/{filename}"
        
        # Ensure export directory exists
        os.makedirs('static/exports', exist_ok=True)
        
        optimizer.export_route_data(filepath)
        
        return jsonify({
            'success': True,
            'download_url': f'/static/exports/{filename}',
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/static/maps/<filename>')
def serve_map(filename):
    """Serve generated map files"""
    return send_from_directory('static/maps', filename)

@app.route('/static/exports/<filename>')
def serve_export(filename):
    """Serve exported data files"""
    return send_from_directory('static/exports', filename)

# Ensure required directories exist
os.makedirs('static/maps', exist_ok=True)
os.makedirs('static/exports', exist_ok=True)
os.makedirs('templates', exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)