import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

class ExpenseTracker:
    def __init__(self):
        # Initialize an empty DataFrame with the correct columns
        self.expenses = pd.DataFrame(columns=['Amount', 'Category', 'Date'])
        self.load_expenses()
    
    def load_expenses(self):
        """Load expenses from CSV file if it exists"""
        if os.path.exists('expenses.csv'):
            try:
                self.expenses = pd.read_csv('expenses.csv')
                # Convert Date column to datetime format
                self.expenses['Date'] = pd.to_datetime(self.expenses['Date'])
                print("Expenses loaded successfully!")
            except Exception as e:
                print(f"Error loading expenses: {e}")
    
    def save_expenses(self):
        """Save expenses to CSV file"""
        try:
            self.expenses.to_csv('expenses.csv', index=False)
            print("Expenses saved successfully!")
        except Exception as e:
            print(f"Error saving expenses: {e}")
    
    def add_expense(self, amount, category, date):
        """Add a new expense to the tracker"""
        try:
            # Create a new DataFrame for the new expense
            new_expense = pd.DataFrame({
                'Amount': [amount],
                'Category': [category],
                'Date': [date]
            })
            
            # Convert Date to datetime
            new_expense['Date'] = pd.to_datetime(new_expense['Date'])
            
            # Add to existing expenses
            self.expenses = pd.concat([self.expenses, new_expense], ignore_index=True)
            self.save_expenses()
            print(f"Added expense: ${amount} for {category} on {date}")
        except Exception as e:
            print(f"Error adding expense: {e}")
    
    def view_all_expenses(self):
        """Display all expenses"""
        if self.expenses.empty:
            print("No expenses recorded yet.")
            return
        
        print("\n=== ALL EXPENSES ===")
        # Format date for better display
        display_df = self.expenses.copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
        print(display_df.to_string(index=False))
    
    def filter_by_category(self, category):
        """Show expenses for a specific category"""
        if self.expenses.empty:
            print("No expenses recorded yet.")
            return
        
        filtered = self.expenses[self.expenses['Category'].str.lower() == category.lower()]
        
        if filtered.empty:
            print(f"No expenses found for category: {category}")
        else:
            print(f"\n=== EXPENSES FOR {category.upper()} ===")
            display_df = filtered.copy()
            display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
            print(display_df.to_string(index=False))
    
    def monthly_summary(self):
        """Show monthly spending summary with a bar chart"""
        if self.expenses.empty:
            print("No expenses recorded yet.")
            return
        
        # Group by month and sum amounts
        monthly = self.expenses.copy()
        monthly['Month'] = monthly['Date'].dt.to_period('M')
        monthly_sum = monthly.groupby('Month')['Amount'].sum()
        
        print("\n=== MONTHLY SUMMARY ===")
        print(monthly_sum.to_string())
        
        # Create bar chart
        monthly_sum.plot(kind='bar', color='skyblue')
        plt.title('Monthly Expenses')
        plt.xlabel('Month')
        plt.ylabel('Amount ($)')
        plt.show()
    
    def category_analysis(self):
        """Show spending by category with a pie chart"""
        if self.expenses.empty:
            print("No expenses recorded yet.")
            return
        
        # Group by category and sum amounts
        category_sum = self.expenses.groupby('Category')['Amount'].sum()
        
        print("\n=== CATEGORY SUMMARY ===")
        print(category_sum.to_string())
        
        # Create pie chart
        category_sum.plot(kind='pie', autopct='%1.1f%%')
        plt.title('Spending by Category')
        plt.ylabel('')  # Remove the 'Amount' label
        plt.show()

def get_valid_amount():
    """Get a valid positive number for amount"""
    while True:
        try:
            amount = float(input("Enter amount spent: $"))
            if amount <= 0:
                print("Amount must be positive.")
            else:
                return amount
        except ValueError:
            print("Please enter a valid number.")

def get_valid_date():
    """Get a valid date in YYYY-MM-DD format"""
    while True:
        date = input("Enter date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def main():
    tracker = ExpenseTracker()
    
    while True:
        print("\n" + "="*50)
        print("DAILY EXPENSE TRACKER".center(50))
        print("="*50)
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Filter by Category")
        print("4. Monthly Summary")
        print("5. Category Analysis")
        print("6. Exit")
        
        try:
            choice = int(input("Enter your choice (1-6): "))
        except ValueError:
            print("Please enter a number between 1-6.")
            continue
        
        if choice == 1:
            print("\nADD NEW EXPENSE")
            amount = get_valid_amount()
            category = input("Enter category: ").strip().title()
            date = get_valid_date()
            tracker.add_expense(amount, category, date)
            
        elif choice == 2:
            tracker.view_all_expenses()
            
        elif choice == 3:
            category = input("Enter category to filter: ").strip().title()
            tracker.filter_by_category(category)
            
        elif choice == 4:
            tracker.monthly_summary()
            
        elif choice == 5:
            tracker.category_analysis()
            
        elif choice == 6:
            print("Goodbye! Your expenses have been saved.")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1-6.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()