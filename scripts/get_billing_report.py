#!/usr/bin/env python3
import argparse
import datetime
import sys
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def get_date_range(month_opt):
    today = datetime.date.today()
    if month_opt == 'current':
        start = today.replace(day=1)
        # End date in Cost Explorer is exclusive, so use tomorrow or today + 1 day
        end = today + datetime.timedelta(days=1)
        # If it's the first day of the month, range might be empty or invalid for Cost Explorer.
        # So we adjust start to include previous month or just handle it.
        if start == today:
            end = today + datetime.timedelta(days=1)
        return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), "Current Month"
    elif month_opt == 'previous':
        # First day of current month
        first_current = today.replace(day=1)
        # Last day of previous month
        last_prev = first_current - datetime.timedelta(days=1)
        # First day of previous month
        start_prev = last_prev.replace(day=1)
        # End date is exclusive, so the start of current month is the end of the previous month
        return start_prev.strftime('%Y-%m-%d'), first_current.strftime('%Y-%m-%d'), "Previous Month"
    else:
        # Expecting YYYY-MM
        try:
            parts = month_opt.split('-')
            year = int(parts[0])
            month = int(parts[1])
            start = datetime.date(year, month, 1)
            # Find next month
            if month == 12:
                end = datetime.date(year + 1, 1, 1)
            else:
                end = datetime.date(year, month + 1, 1)
            return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), f"{year}-{month:02d}"
        except Exception:
            print(f"Error: Invalid month format '{month_opt}'. Use 'current', 'previous', or 'YYYY-MM'.", file=sys.stderr)
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Generate a markdown billing report from AWS Cost Explorer.")
    parser.add_argument("--profile", help="AWS CLI profile to use (e.g., rcsevsv)")
    parser.add_argument("--month", choices=["current", "previous"], default="current",
                        help="Retrieve data for the 'current' or 'previous' month. Or specify format 'YYYY-MM'.")
    args, unknown = parser.parse_known_args()
    
    # If the user passed something like a custom month string not in choices
    month_opt = args.month
    if len(unknown) > 0:
        # Check if the user tried to pass custom month string directly
        month_opt = unknown[0]

    start_date, end_date, label = get_date_range(month_opt)
    
    try:
        session = boto3.Session(profile_name=args.profile) if args.profile else boto3.Session()
        ce = session.client('ce')
        
        response = ce.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        
        results = response.get('ResultsByTime', [])
        if not results:
            print(f"No cost data found for period: {start_date} to {end_date}.")
            return
            
        print(f"### AWS Cost Report: {label} ({start_date} to {end_date})")
        print(f"**Profile used:** `{args.profile or 'default'}`\n")
        print("| AWS Service | Cost (USD) |")
        print("| :--- | :--- |")
        
        total_cost = 0.0
        currency = "USD"
        
        # Sort groups by cost descending
        groups = []
        for group in results[0].get('Groups', []):
            service_name = group['Keys'][0]
            amount = float(group['Metrics']['UnblendedCost']['Amount'])
            unit = group['Metrics']['UnblendedCost']['Unit']
            groups.append((service_name, amount, unit))
            
        groups.sort(key=lambda x: x[1], reverse=True)
        
        for service_name, amount, unit in groups:
            currency = unit
            if amount > 0.00001:
                print(f"| {service_name} | ${amount:,.4f} {unit} |")
                total_cost += amount
                
        print(f"| **Total** | **${total_cost:,.2f} {currency}** |")
        
    except (BotoCoreError, ClientError) as e:
        print(f"AWS API Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
