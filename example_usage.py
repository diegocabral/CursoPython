"""
Example usage of the Google Maps Route Planner System

This script demonstrates how to use the RouteOptimizer class programmatically
to calculate optimal routes between multiple addresses.
"""

import os
from dotenv import load_dotenv
from route_planner import RouteOptimizer


def demo_route_planning():
    """
    Demonstrate route planning with sample addresses
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
    
    # Sample addresses for demonstration
    sample_addresses = [
        "Times Square, New York, NY",
        "Central Park, New York, NY", 
        "Brooklyn Bridge, New York, NY",
        "Statue of Liberty, New York, NY",
        "Empire State Building, New York, NY"
    ]
    
    print("=== Route Planning Demo ===")
    print("Adding sample addresses...")
    
    # Add addresses to the route planner
    for address in sample_addresses:
        success = optimizer.add_address(address)
        if not success:
            print(f"Failed to add address: {address}")
    
    if len(optimizer.addresses) < 2:
        print("Not enough valid addresses to calculate route.")
        return
    
    print(f"\nCalculating optimal route for {len(optimizer.addresses)} locations...")
    
    try:
        # Calculate the optimal route
        route_data = optimizer.optimize_route(return_to_start=True)
        
        # Get and display route summary
        summary = optimizer.get_route_summary()
        
        print(f"\n=== Route Summary ===")
        print(f"Total Distance: {summary['total_distance']['text']}")
        print(f"Total Duration: {summary['total_duration']['text']}")
        print(f"Number of Stops: {summary['total_addresses']}")
        
        print(f"\n=== Optimized Route Order ===")
        for i, address in enumerate(summary['optimized_order']):
            print(f"{i+1}. {address}")
        
        # Generate interactive map
        map_file = optimizer.generate_map("demo_route_map.html")
        
        # Export route data
        data_file = optimizer.export_route_data("demo_route_data.json")
        
        print(f"\n=== Generated Files ===")
        print(f"📍 Interactive map: {map_file}")
        print(f"📊 Route data: {data_file}")
        
        print(f"\n✅ Route planning completed successfully!")
        print(f"🗺️  Open '{map_file}' in your web browser to view the interactive map.")
        
    except Exception as e:
        print(f"❌ Error calculating route: {str(e)}")


def custom_route_example():
    """
    Example of creating a custom route with user-defined addresses
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("Error: GOOGLE_MAPS_API_KEY not found in environment variables.")
        return
    
    # Create route optimizer instance
    optimizer = RouteOptimizer(api_key)
    
    # Custom addresses - modify these for your specific use case
    custom_addresses = [
        "Los Angeles, CA",
        "San Francisco, CA",
        "Las Vegas, NV",
        "Phoenix, AZ"
    ]
    
    print("=== Custom Route Example ===")
    print("Adding custom addresses...")
    
    # Add addresses
    for address in custom_addresses:
        optimizer.add_address(address)
    
    # Calculate route without returning to start
    print("\nCalculating route (not returning to start)...")
    route_data = optimizer.optimize_route(return_to_start=False)
    
    # Display results
    summary = optimizer.get_route_summary()
    print(f"\nRoute Summary:")
    print(f"Distance: {summary['total_distance']['text']}")
    print(f"Duration: {summary['total_duration']['text']}")
    
    # Generate files with custom names
    optimizer.generate_map("custom_route_map.html")
    optimizer.export_route_data("custom_route_data.json")
    
    print("Custom route planning completed!")


if __name__ == "__main__":
    print("Choose an example to run:")
    print("1. Demo route planning (New York City attractions)")
    print("2. Custom route example (West Coast cities)")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            demo_route_planning()
        elif choice == "2":
            custom_route_example()
        else:
            print("Invalid choice. Running demo by default...")
            demo_route_planning()
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")