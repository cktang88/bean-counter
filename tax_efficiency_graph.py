import matplotlib.pyplot as plt
import numpy as np

# Tax brackets (rate, min, max)
tax_brackets = [
    (0.10, 0, 11600),
    (0.12, 11601, 47150),
    (0.22, 47151, 100525),
    (0.24, 100526, 191950),
    (0.32, 191951, 243725),
    (0.35, 243726, 609350),
    (0.37, 609351, float('inf'))
]

standard_deduction = 14600

# Salaries to analyze
salaries = [100000, 150000, 200000, 250000, 300000]

def calculate_tax(gross_income):
    """Calculate federal tax based on progressive tax brackets"""
    taxable_income = max(0, gross_income - standard_deduction)
    tax = 0
    
    for rate, bracket_min, bracket_max in tax_brackets:
        if taxable_income <= bracket_min:
            break
        
        # Calculate the amount of income taxed at this rate
        if taxable_income >= bracket_max:
            # All of this bracket is taxable
            taxable_in_bracket = bracket_max - bracket_min
        else:
            # Only part of this bracket is taxable
            taxable_in_bracket = taxable_income - bracket_min
        
        tax += taxable_in_bracket * rate
    
    return tax

def get_work_days(calendar_days):
    """Calculate number of work days in a given number of calendar days"""
    # Assuming we start on a Monday (Jan 1)
    # 5 work days per 7 calendar days
    full_weeks = calendar_days // 7
    remaining_days = calendar_days % 7
    
    # Count work days in full weeks
    work_days = full_weeks * 5
    
    # Count work days in remaining partial week
    # If remaining days include weekend, cap at 5
    work_days += min(remaining_days, 5)
    
    return work_days

def calculate_efficiency(annual_salary, calendar_days):
    """Calculate post-tax hourly wage (efficiency) based on calendar days"""
    work_days = get_work_days(calendar_days)
    if work_days == 0:
        return 0
    
    hours_per_day = 8
    total_hours = work_days * hours_per_day
    
    # Standard work year: 260 work days
    work_days_per_year = 260
    
    # Daily rate based on work days only
    daily_rate = annual_salary / work_days_per_year
    
    # Calculate gross income for days worked
    gross_income = daily_rate * work_days
    
    # Calculate tax based on this partial year income (as if it's the annual income)
    tax = calculate_tax(gross_income)
    net_income = gross_income - tax
    
    hourly_wage = net_income / total_hours
    return hourly_wage

# Create the plot
plt.figure(figsize=(12, 8))

# Calendar days range (1 to 365)
days = np.linspace(1, 365, 100)

# Plot efficiency for each salary
for i, salary in enumerate(salaries):
    efficiencies = [calculate_efficiency(salary, d) for d in days]
    label = f"${salary:,}"
    plt.plot(days, efficiencies, label=label, linewidth=2)

plt.xlabel('Calendar Days per Year', fontsize=12)
plt.ylabel('Post-Tax Hourly Wage ($)', fontsize=12)
plt.title('Tax Efficiency: Post-Tax Hourly Wage vs Calendar Days\n(2024 Tax Brackets with $14,600 Standard Deduction)', fontsize=14)
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.xlim(0, 365)
plt.ylim(0, max([calculate_efficiency(salaries[-1], 1)]) * 1.1)

# Add annotations for key insights
plt.axvline(x=365, color='gray', linestyle='--', alpha=0.5)
plt.text(365, plt.ylim()[1] * 0.95, 'Full year\n(260 work days)', 
         ha='center', va='top', fontsize=10, color='gray')

plt.tight_layout()
plt.savefig('tax_efficiency_graph.png', dpi=150, bbox_inches='tight')
print("Graph saved as tax_efficiency_graph.png")

# Print some example calculations
print("Example calculations (calendar days → work days):")
print("-" * 80)
for cal_days in [7, 90, 365]:
    work_days = get_work_days(cal_days)
    print(f"\n{cal_days} calendar days = {work_days} work days:")
    for salary in salaries[:3]:  # Just show first 3 brackets for brevity
        daily_rate = salary / 260
        gross_for_days = daily_rate * work_days
        tax = calculate_tax(gross_for_days)
        net = gross_for_days - tax
        eff = calculate_efficiency(salary, cal_days)
        print(f"  Annual salary ${salary:,} → Daily rate ${daily_rate:.2f} → Gross ${gross_for_days:,.2f}")
        print(f"    Tax ${tax:,.2f} → Net ${net:,.2f} → Post-tax hourly: ${eff:.2f}")
    print()