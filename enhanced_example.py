"""
Enhanced Example: Demonstrating the Updated Google Maps Route Planner

This example shows the enhanced features including autocomplete address search
and individual address deletion capabilities.
"""

import os
from dotenv import load_dotenv
from route_planner import RouteOptimizer


def demonstrate_enhanced_features():
    """
    Demonstrate the enhanced route planning features
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("❌ Error: GOOGLE_MAPS_API_KEY not found in environment variables.")
        print("Please create a .env file with your Google Maps API key.")
        return
    
    # Create route optimizer instance
    optimizer = RouteOptimizer(api_key)
    
    print("=== Enhanced Route Planner Demo ===")
    print("This demo shows the enhanced features available in the web interface:")
    print()
    
    # Demonstrate programmatic address management
    sample_addresses = [
        "Times Square, New York, NY",
        "Central Park, New York, NY", 
        "Brooklyn Bridge, New York, NY",
        "Statue of Liberty, New York, NY",
        "Empire State Building, New York, NY",
        "9/11 Memorial, New York, NY"
    ]
    
    print("📍 Adding sample addresses...")
    for i, address in enumerate(sample_addresses):
        success = optimizer.add_address(address)
        if success:
            print(f"  ✅ {i+1}. {address}")
        else:
            print(f"  ❌ Failed to add: {address}")
    
    print(f"\n📊 Total addresses added: {len(optimizer.addresses)}")
    
    # Demonstrate address list display
    print("\n📋 Current address list:")
    for i, addr in enumerate(optimizer.addresses):
        print(f"  {i+1}. {addr['formatted']}")
    
    # Simulate removing an address (like the web interface would do)
    print("\n🗑️  Demonstrating address removal...")
    if len(optimizer.addresses) > 3:
        removed_address = optimizer.addresses.pop(2)  # Remove 3rd address
        print(f"  Removed: {removed_address['formatted']}")
        
        print("\n📋 Updated address list:")
        for i, addr in enumerate(optimizer.addresses):
            print(f"  {i+1}. {addr['formatted']}")
    
    # Calculate route with remaining addresses
    if len(optimizer.addresses) >= 2:
        print(f"\n🧮 Calculating optimal route for {len(optimizer.addresses)} locations...")
        
        try:
            # Calculate the optimal route
            route_data = optimizer.optimize_route(return_to_start=True)
            
            # Get and display route summary
            summary = optimizer.get_route_summary()
            
            print(f"\n=== Route Summary ===")
            print(f"📏 Total Distance: {summary['total_distance']['text']}")
            print(f"⏱️  Total Duration: {summary['total_duration']['text']}")
            print(f"🏁 Number of Stops: {summary['total_addresses']}")
            
            print(f"\n🗺️  Optimized Route Order:")
            for i, address in enumerate(summary['optimized_order']):
                print(f"  {i+1}. {address}")
            
            # Generate interactive map
            map_file = optimizer.generate_map("enhanced_demo_route.html")
            
            # Export route data
            data_file = optimizer.export_route_data("enhanced_demo_data.json")
            
            print(f"\n📁 Generated Files:")
            print(f"  🗺️  Interactive map: {map_file}")
            print(f"  📊 Route data: {data_file}")
            
            print(f"\n✅ Enhanced demo completed successfully!")
            
        except Exception as e:
            print(f"❌ Error calculating route: {str(e)}")


def demonstrate_autocomplete_simulation():
    """
    Simulate how the autocomplete feature would work programmatically
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("❌ Error: GOOGLE_MAPS_API_KEY not found in environment variables.")
        return
    
    # Create route optimizer instance
    optimizer = RouteOptimizer(api_key)
    
    print("\n=== Autocomplete Feature Simulation ===")
    print("Simulating how the address autocomplete works...")
    
    # Test search queries that would trigger autocomplete
    test_queries = [
        "Times Sq",
        "Central Park",
        "Brooklyn Br",
        "Empire State"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Search query: '{query}'")
        
        try:
            # Use Google Places API for autocomplete (same as web interface)
            autocomplete_result = optimizer.gmaps.places_autocomplete(
                input_text=query,
                types=['address'],
                language='en'
            )
            
            print(f"  📋 Found {len(autocomplete_result)} suggestions:")
            for i, prediction in enumerate(autocomplete_result[:3]):  # Show top 3
                structured = prediction.get('structured_formatting', {})
                main_text = structured.get('main_text', prediction['description'])
                secondary_text = structured.get('secondary_text', '')
                
                print(f"    {i+1}. {main_text}")
                if secondary_text:
                    print(f"       {secondary_text}")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")


def interactive_demo():
    """
    Interactive demo showing enhanced features
    """
    print("\n" + "="*60)
    print("🚀 ENHANCED GOOGLE MAPS ROUTE PLANNER DEMO")
    print("="*60)
    
    print("\n🎯 New Features Demonstrated:")
    print("  ✅ Autocomplete address suggestions as you type")
    print("  ✅ Individual address deletion with confirmation")
    print("  ✅ Enhanced user interface with better UX")
    print("  ✅ Keyboard navigation for autocomplete")
    print("  ✅ Real-time address validation")
    
    print("\n💻 Web Interface Features:")
    print("  • Type in the address field - suggestions appear after 3 characters")
    print("  • Use arrow keys to navigate suggestions")
    print("  • Press Enter to select a suggestion")
    print("  • Hover over addresses to see delete buttons")
    print("  • Click X button to delete individual addresses")
    print("  • Confirmation dialog prevents accidental deletions")
    
    print("\n🛠️  To use the enhanced web interface:")
    print("  1. python3 web_app.py")
    print("  2. Open http://localhost:5000")
    print("  3. Add your Google Maps API key to .env file")
    print("  4. Try typing addresses to see autocomplete in action!")
    
    # Run the demonstrations
    demonstrate_enhanced_features()
    demonstrate_autocomplete_simulation()
    
    print("\n🎉 Demo completed! Try the web interface for the full experience.")


if __name__ == "__main__":
    try:
        interactive_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("💡 Make sure your Google Maps API key is configured in the .env file.")