#!/usr/bin/env python3
"""
CLI script for logging productivity hours directly to Supabase.
Usage: python log_hours.py --hours 2 --category work --note "Deep work"
"""

import click
import os
from datetime import datetime, date
from dotenv import load_dotenv
from supabase import create_client, Client
import sys

# Load environment variables
load_dotenv()

def init_supabase():
    """Initialize Supabase client"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("Error: Please set SUPABASE_URL and SUPABASE_KEY environment variables")
        print("Create a .env file with your Supabase credentials")
        sys.exit(1)
    
    return create_client(url, key)

def get_categories(supabase: Client):
    """Get all available categories"""
    try:
        response = supabase.table("categories").select("*").order("name").execute()
        return {cat['name'].lower(): cat['id'] for cat in response.data}
    except Exception as e:
        print(f"Error fetching categories: {str(e)}")
        return {}

def authenticate_user(supabase: Client, email: str, password: str):
    """Authenticate user and return user ID"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response.user:
            return response.user.id
        else:
            print("Authentication failed")
            return None
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return None

def log_activity(supabase: Client, user_id: str, log_date: date, hours: float, category_id: int, note: str = ""):
    """Log activity to database"""
    try:
        # Get category rate to calculate value
        category_response = supabase.table("categories").select("rate").eq("id", category_id).execute()
        if not category_response.data:
            print("Category not found")
            return None
        
        rate = category_response.data[0]['rate']
        value = hours * rate
        
        response = supabase.table("logs").insert({
            "user_id": user_id,
            "date": log_date.isoformat(),
            "hours": hours,
            "category_id": category_id,
            "note": note,
            "value": value
        }).execute()
        
        if response.data:
            return response.data[0]
        else:
            print("Failed to log activity")
            return None
    except Exception as e:
        print(f"Error logging activity: {str(e)}")
        return None

@click.command()
@click.option('--hours', '-h', required=True, type=float, help='Number of hours worked')
@click.option('--category', '-c', required=True, help='Category name (work, personal, etc.)')
@click.option('--note', '-n', default='', help='Optional note about the activity')
@click.option('--date', '-d', default=None, help='Date (YYYY-MM-DD), defaults to today')
@click.option('--email', '-e', help='Your email for authentication')
@click.option('--password', '-p', help='Your password for authentication')
def log_hours(hours, category, note, date, email, password):
    """
    Log productivity hours to your tracker.
    
    Example:
    python log_hours.py --hours 2 --category work --note "Deep work"
    """
    
    # Initialize Supabase
    supabase = init_supabase()
    
    # Get categories
    categories = get_categories(supabase)
    if not categories:
        print("No categories found. Please check your database setup.")
        return
    
    # Validate category
    category_lower = category.lower()
    if category_lower not in categories:
        print(f"Invalid category: {category}")
        print(f"Available categories: {', '.join(categories.keys())}")
        return
    
    # Parse date
    if date:
        try:
            log_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD")
            return
    else:
        log_date = date.today()
    
    # Get authentication credentials
    if not email:
        email = click.prompt('Email')
    if not password:
        password = click.prompt('Password', hide_input=True)
    
    # Authenticate user
    user_id = authenticate_user(supabase, email, password)
    if not user_id:
        return
    
    # Log activity
    category_id = categories[category_lower]
    result = log_activity(supabase, user_id, log_date, hours, category_id, note)
    
    if result:
        # Get category rate for display
        try:
            cat_response = supabase.table("categories").select("rate").eq("id", category_id).execute()
            rate = cat_response.data[0]['rate'] if cat_response.data else 0
            value = hours * rate
            
            print(f"✅ Activity logged successfully!")
            print(f"   Date: {log_date}")
            print(f"   Hours: {hours}")
            print(f"   Category: {category}")
            print(f"   Value: ${value:.2f}")
            if note:
                print(f"   Note: {note}")
        except Exception as e:
            print(f"Activity logged, but couldn't fetch rate: {str(e)}")
    else:
        print("❌ Failed to log activity")

@click.command()
@click.option('--email', '-e', help='Your email for authentication')
@click.option('--password', '-p', help='Your password for authentication')
def list_categories(email, password):
    """List all available categories"""
    
    # Initialize Supabase
    supabase = init_supabase()
    
    # Get categories
    try:
        response = supabase.table("categories").select("*").order("name").execute()
        categories = response.data
        
        if not categories:
            print("No categories found.")
            return
        
        print("Available categories:")
        print("-" * 50)
        for cat in categories:
            print(f"{cat['name']:20} ${cat['rate']:>8.2f}/hour")
            if cat.get('description'):
                print(f"{'':20} {cat['description']}")
        
    except Exception as e:
        print(f"Error fetching categories: {str(e)}")

@click.group()
def cli():
    """Productivity Tracker CLI"""
    pass

cli.add_command(log_hours)
cli.add_command(list_categories)

if __name__ == '__main__':
    cli()
