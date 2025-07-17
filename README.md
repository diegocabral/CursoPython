# Google Maps Route Planner System

A comprehensive Python system that connects to the Google Maps API to calculate optimal routes between multiple addresses. The system provides both command-line and web interfaces for easy route planning and visualization.

## 🚀 Features

- **Route Optimization**: Automatically calculates the most efficient route visiting all destinations
- **Interactive Maps**: Generates beautiful, interactive maps with detailed route visualization
- **Multiple Interfaces**: 
  - Command-line interface for direct interaction
  - Web application with modern UI
  - Programmatic API for integration
- **Export Functionality**: Export route data and maps for offline use or sharing
- **Address Geocoding**: Automatically converts addresses to coordinates
- **Flexible Options**: Choose whether to return to starting point or end at final destination

## 📋 Prerequisites

- Python 3.7 or higher
- Google Maps API key with the following APIs enabled:
  - Maps JavaScript API
  - Directions API
  - Geocoding API
  - Places API (optional)

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Google Maps API key:**
   - Copy `.env.example` to `.env`
   - Replace `your_google_maps_api_key_here` with your actual API key
   ```bash
   cp .env.example .env
   # Edit .env file with your API key
   ```

## 🔑 Getting a Google Maps API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the required APIs:
   - Maps JavaScript API
   - Directions API
   - Geocoding API
4. Create credentials (API key)
5. Restrict the API key for security (optional but recommended)

## 💻 Usage

### 1. Command Line Interface

Run the main interactive script:

```bash
python route_planner.py
```

Follow the prompts to:
- Add addresses one by one
- Choose whether to return to the starting point
- View the optimized route and generated files

### 2. Web Application

Start the Flask web server:

```bash
python web_app.py
```

Then open your browser and navigate to `http://localhost:5000`

The web interface provides:
- Easy address input with validation
- Interactive route visualization
- Real-time route calculation
- Export functionality
- Responsive design for mobile and desktop

### 3. Programmatic Usage

Use the `RouteOptimizer` class in your own code:

```python
from route_planner import RouteOptimizer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_MAPS_API_KEY')

# Create optimizer instance
optimizer = RouteOptimizer(api_key)

# Add addresses
addresses = [
    "Times Square, New York, NY",
    "Central Park, New York, NY",
    "Brooklyn Bridge, New York, NY"
]

for address in addresses:
    optimizer.add_address(address)

# Calculate optimal route
route_data = optimizer.optimize_route(return_to_start=True)

# Get summary
summary = optimizer.get_route_summary()
print(f"Total Distance: {summary['total_distance']['text']}")
print(f"Total Duration: {summary['total_duration']['text']}")

# Generate map and export data
optimizer.generate_map("my_route.html")
optimizer.export_route_data("my_route_data.json")
```

### 4. Example Scripts

Run the provided example scripts:

```bash
# Demo with NYC attractions
python example_usage.py

# Choose from available examples
```

## 📁 Project Structure

```
├── route_planner.py          # Main RouteOptimizer class and CLI
├── web_app.py               # Flask web application
├── example_usage.py         # Example scripts and demos
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .env                    # Your API configuration (create this)
├── templates/
│   └── index.html          # Web application template
├── static/
│   ├── maps/              # Generated map files
│   └── exports/           # Exported route data
└── README.md              # This file
```

## 🔧 API Reference

### RouteOptimizer Class

#### Methods

- `__init__(api_key: str)` - Initialize with Google Maps API key
- `add_address(address: str) -> bool` - Add an address to the route
- `clear_addresses()` - Clear all addresses
- `optimize_route(start_index: int = 0, return_to_start: bool = False) -> Dict` - Calculate optimal route
- `generate_map(filename: str = "route_map.html") -> str` - Generate interactive map
- `get_route_summary() -> Dict` - Get route summary information
- `export_route_data(filename: str = "route_data.json") -> str` - Export route data

#### Properties

- `addresses` - List of added addresses with coordinates
- `route_data` - Calculated route information

## 🌐 Web API Endpoints

- `GET /` - Main web interface
- `POST /api/add_address` - Add an address
- `POST /api/clear_addresses` - Clear all addresses
- `GET /api/get_addresses` - Get current addresses
- `POST /api/calculate_route` - Calculate optimal route
- `POST /api/export_data` - Export route data

## 📊 Output Files

The system generates several types of output:

1. **Interactive Maps** (`*.html`):
   - Folium-based interactive maps
   - Color-coded markers for each stop
   - Route polylines with detailed paths
   - Popup information for each location

2. **Route Data** (`*.json`):
   - Complete route information
   - Turn-by-turn directions
   - Distance and duration data
   - Optimized address order

## 🚨 Error Handling

The system handles various error conditions:

- Invalid or non-geocodable addresses
- API rate limits and quota exceeded
- Network connectivity issues
- Missing API key configuration
- Insufficient number of addresses

## 🔒 Security Considerations

- Store your API key in the `.env` file (never commit this to version control)
- Restrict your API key in the Google Cloud Console
- Consider implementing rate limiting for production use
- Validate all user inputs

## 🐛 Troubleshooting

### Common Issues

1. **"API not configured" error**:
   - Ensure your `.env` file exists and contains the correct API key
   - Verify the API key is valid and has the required APIs enabled

2. **"Could not geocode address" error**:
   - Check that the address is correctly formatted
   - Ensure the Geocoding API is enabled
   - Verify you haven't exceeded API quotas

3. **Map not displaying**:
   - Check that the Maps JavaScript API is enabled
   - Ensure there are no browser console errors
   - Verify the generated HTML file is accessible

4. **Web application not starting**:
   - Ensure Flask is installed (`pip install flask`)
   - Check that port 5000 is available
   - Verify all dependencies are installed

### Getting Help

- Check the Google Maps API documentation
- Verify your API key permissions and quotas
- Review the error messages for specific guidance

## 📈 Performance Notes

- The system uses Google's route optimization for the best results
- Processing time increases with the number of addresses
- API calls are rate-limited by Google's quotas
- Generated maps are optimized for fast loading

## 🤝 Contributing

Feel free to contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and practical use. Please ensure compliance with Google Maps API terms of service.

## 🙏 Acknowledgments

- Google Maps API for routing and geocoding services
- Folium library for interactive map generation
- Flask framework for the web interface
- Bootstrap for responsive UI components

---

**Note**: This system requires a valid Google Maps API key and active internet connection to function properly. API usage may incur charges based on Google's pricing structure.