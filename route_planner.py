"""
Google Maps Route Planner System

This system connects to the Google Maps API to plot optimal routes between multiple addresses.
It provides functionality to:
- Geocode addresses to coordinates
- Calculate the best route visiting all addresses
- Generate interactive maps with the route
- Export route information
"""

import googlemaps
import folium
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dotenv import load_dotenv
import json


class RouteOptimizer:
    """
    A class to optimize routes using Google Maps API
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the RouteOptimizer with Google Maps API key
        
        Args:
            api_key (str): Google Maps API key
        """
        self.gmaps = googlemaps.Client(key=api_key)
        self.addresses = []
        self.coordinates = []
        self.route_data = None
    
    def add_address(self, address: str) -> bool:
        """
        Add an address to the route planning list
        
        Args:
            address (str): Address to add
            
        Returns:
            bool: True if address was successfully geocoded and added, False otherwise
        """
        try:
            # Geocode the address
            geocode_result = self.gmaps.geocode(address)
            
            if not geocode_result:
                print(f"Could not geocode address: {address}")
                return False
            
            location = geocode_result[0]['geometry']['location']
            formatted_address = geocode_result[0]['formatted_address']
            
            self.addresses.append({
                'original': address,
                'formatted': formatted_address,
                'coordinates': (location['lat'], location['lng'])
            })
            
            print(f"Added: {formatted_address}")
            return True
            
        except Exception as e:
            print(f"Error adding address '{address}': {str(e)}")
            return False
    
    def clear_addresses(self):
        """Clear all addresses from the route planning list"""
        self.addresses = []
        self.route_data = None
        print("All addresses cleared.")
    
    def optimize_route(self, start_index: int = 0, return_to_start: bool = False) -> Dict:
        """
        Calculate the optimal route visiting all addresses
        
        Args:
            start_index (int): Index of the starting address (default: 0)
            return_to_start (bool): Whether to return to the starting point
            
        Returns:
            Dict: Route data including directions, distance, and duration
        """
        if len(self.addresses) < 2:
            raise ValueError("At least 2 addresses are required to calculate a route")
        
        if start_index >= len(self.addresses):
            raise ValueError("Start index is out of range")
        
        try:
            # Prepare waypoints (all addresses except start and end)
            start_location = self.addresses[start_index]['coordinates']
            waypoints = []
            
            for i, addr in enumerate(self.addresses):
                if i != start_index:
                    waypoints.append(addr['coordinates'])
            
            # Determine end location
            if return_to_start:
                end_location = start_location
            else:
                # Use the last waypoint as destination and remove it from waypoints
                end_location = waypoints.pop()
            
            # Calculate optimized route
            directions_result = self.gmaps.directions(
                origin=start_location,
                destination=end_location,
                waypoints=waypoints,
                optimize_waypoints=True,
                mode="driving",
                departure_time=datetime.now()
            )
            
            if not directions_result:
                raise Exception("No route found")
            
            # Extract route information
            route = directions_result[0]
            self.route_data = {
                'directions': directions_result,
                'total_distance': self._calculate_total_distance(route),
                'total_duration': self._calculate_total_duration(route),
                'waypoint_order': route.get('waypoint_order', []),
                'optimized_addresses': self._get_optimized_address_order(route, start_index, return_to_start)
            }
            
            return self.route_data
            
        except Exception as e:
            print(f"Error calculating route: {str(e)}")
            raise
    
    def _calculate_total_distance(self, route: Dict) -> Dict:
        """Calculate total distance of the route"""
        total_meters = 0
        for leg in route['legs']:
            total_meters += leg['distance']['value']
        
        return {
            'meters': total_meters,
            'kilometers': round(total_meters / 1000, 2),
            'text': f"{round(total_meters / 1000, 2)} km"
        }
    
    def _calculate_total_duration(self, route: Dict) -> Dict:
        """Calculate total duration of the route"""
        total_seconds = 0
        for leg in route['legs']:
            total_seconds += leg['duration']['value']
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        return {
            'seconds': total_seconds,
            'minutes': round(total_seconds / 60, 1),
            'hours': round(total_seconds / 3600, 2),
            'text': f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        }
    
    def _get_optimized_address_order(self, route: Dict, start_index: int, return_to_start: bool) -> List[Dict]:
        """Get the optimized order of addresses"""
        optimized_order = [self.addresses[start_index]]  # Start with the starting address
        
        # Add waypoints in optimized order
        waypoint_order = route.get('waypoint_order', [])
        other_addresses = [addr for i, addr in enumerate(self.addresses) if i != start_index]
        
        for waypoint_idx in waypoint_order:
            if waypoint_idx < len(other_addresses):
                optimized_order.append(other_addresses[waypoint_idx])
        
        # Add any remaining addresses not in waypoint_order
        if not return_to_start and len(other_addresses) > len(waypoint_order):
            optimized_order.append(other_addresses[-1])
        
        return optimized_order
    
    def generate_map(self, filename: str = "route_map.html") -> str:
        """
        Generate an interactive map with the calculated route
        
        Args:
            filename (str): Output filename for the map
            
        Returns:
            str: Path to the generated map file
        """
        if not self.route_data:
            raise ValueError("No route calculated. Call optimize_route() first.")
        
        # Get the route coordinates
        route = self.route_data['directions'][0]
        
        # Create a folium map centered on the first address
        center_lat = self.addresses[0]['coordinates'][0]
        center_lng = self.addresses[0]['coordinates'][1]
        
        m = folium.Map(
            location=[center_lat, center_lng],
            zoom_start=10,
            tiles='OpenStreetMap'
        )
        
        # Add markers for all addresses
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
                 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
        
        for i, addr in enumerate(self.route_data['optimized_addresses']):
            color = colors[i % len(colors)]
            icon_name = 'play' if i == 0 else ('stop' if i == len(self.route_data['optimized_addresses']) - 1 else 'info-sign')
            
            folium.Marker(
                location=addr['coordinates'],
                popup=folium.Popup(f"{i+1}. {addr['formatted']}", max_width=300),
                tooltip=f"Stop {i+1}",
                icon=folium.Icon(color=color, icon=icon_name)
            ).add_to(m)
        
        # Add the route line
        route_coordinates = []
        for leg in route['legs']:
            for step in leg['steps']:
                # Decode the polyline
                polyline_points = googlemaps.convert.decode_polyline(step['polyline']['points'])
                route_coordinates.extend([(point['lat'], point['lng']) for point in polyline_points])
        
        if route_coordinates:
            folium.PolyLine(
                locations=route_coordinates,
                weight=5,
                color='blue',
                opacity=0.7
            ).add_to(m)
        
        # Add route information to the map
        route_info = f"""
        <div style='font-family: Arial; font-size: 14px;'>
        <h4>Route Information</h4>
        <p><strong>Total Distance:</strong> {self.route_data['total_distance']['text']}</p>
        <p><strong>Total Duration:</strong> {self.route_data['total_duration']['text']}</p>
        <p><strong>Number of Stops:</strong> {len(self.addresses)}</p>
        </div>
        """
        
        folium.Marker(
            location=[center_lat - 0.1, center_lng],
            popup=folium.Popup(route_info, max_width=300),
            icon=folium.Icon(color='lightgray', icon='info-sign')
        ).add_to(m)
        
        # Save the map
        m.save(filename)
        print(f"Map saved as: {filename}")
        return filename
    
    def get_route_summary(self) -> Dict:
        """
        Get a summary of the calculated route
        
        Returns:
            Dict: Route summary information
        """
        if not self.route_data:
            return {"error": "No route calculated"}
        
        return {
            "total_addresses": len(self.addresses),
            "total_distance": self.route_data['total_distance'],
            "total_duration": self.route_data['total_duration'],
            "optimized_order": [addr['formatted'] for addr in self.route_data['optimized_addresses']],
            "route_calculated_at": datetime.now().isoformat()
        }
    
    def export_route_data(self, filename: str = "route_data.json") -> str:
        """
        Export route data to a JSON file
        
        Args:
            filename (str): Output filename
            
        Returns:
            str: Path to the exported file
        """
        if not self.route_data:
            raise ValueError("No route calculated. Call optimize_route() first.")
        
        export_data = {
            "addresses": self.addresses,
            "route_summary": self.get_route_summary(),
            "detailed_directions": self.route_data['directions']
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"Route data exported to: {filename}")
        return filename


def main():
    """
    Main function to demonstrate the route planning system
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("Error: GOOGLE_MAPS_API_KEY not found in environment variables.")
        print("Please create a .env file with your Google Maps API key.")
        return
    
    # Create route optimizer instance
    optimizer = RouteOptimizer(api_key)
    
    print("=== Google Maps Route Planner ===")
    print("Enter addresses to visit. Type 'done' when finished.")
    print("Type 'clear' to clear all addresses.")
    print("Type 'quit' to exit.\n")
    
    while True:
        command = input("Enter address (or command): ").strip()
        
        if command.lower() == 'quit':
            break
        elif command.lower() == 'done':
            if len(optimizer.addresses) < 2:
                print("Please add at least 2 addresses before calculating route.")
                continue
            break
        elif command.lower() == 'clear':
            optimizer.clear_addresses()
            continue
        elif command:
            optimizer.add_address(command)
    
    # If we have addresses, calculate the route
    if len(optimizer.addresses) >= 2:
        print(f"\nCalculating optimal route for {len(optimizer.addresses)} addresses...")
        
        try:
            # Ask user preferences
            return_to_start = input("Return to starting point? (y/n): ").lower().startswith('y')
            
            # Calculate route
            route_data = optimizer.optimize_route(return_to_start=return_to_start)
            
            # Display route summary
            summary = optimizer.get_route_summary()
            print(f"\n=== Route Summary ===")
            print(f"Total Distance: {summary['total_distance']['text']}")
            print(f"Total Duration: {summary['total_duration']['text']}")
            print(f"Number of Stops: {summary['total_addresses']}")
            
            print(f"\n=== Optimized Route Order ===")
            for i, address in enumerate(summary['optimized_order']):
                print(f"{i+1}. {address}")
            
            # Generate map
            map_file = optimizer.generate_map()
            
            # Export data
            data_file = optimizer.export_route_data()
            
            print(f"\nFiles generated:")
            print(f"- Interactive map: {map_file}")
            print(f"- Route data: {data_file}")
            
        except Exception as e:
            print(f"Error calculating route: {str(e)}")


if __name__ == "__main__":
    main()