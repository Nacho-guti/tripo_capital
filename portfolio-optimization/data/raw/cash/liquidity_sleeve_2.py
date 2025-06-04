
def tranche_purchase(shortfall, coupon_rate, price_clean):
    """
    Calculate the face value, cost, and coupon income of a bond tranche purchase.
    
    Parameters:
    shortfall (float): Cash needed in that year.
    coupon_rate (float): Annual coupon rate of the bond.
    price_clean (float): Clean price of the bond as a fraction of face value.
    
    Returns:
    tuple: Face value, cost of the bond, and coupon income.
    """
    # Calculate the face value of the bond
    face_value = shortfall / (1 + coupon_rate)
    # Calculate the price of the bond
    price_bond = face_value * price_clean
    # Coupon Income
    coupon_income = face_value * coupon_rate
    # Calculate the face value of the bond
    face_value = shortfall / (1+ coupon_rate)
    # Calculate the price of the bond
    price_bond = face_value * price_clean
    # Coupon Income
    coupon_income = face_value * coupon_rate

    print(f"Face Value of the Bond: £{face_value:,.2f}") # Need to deliver this amount at maturity
    print(f"Cost of the Bond: £{price_bond:,.2f}") # Cost today to purchase the bond
    print(f"Coupon Income: £{coupon_income:,.2f}") # Coupon at maturity
    print(f"Gross proceeds at maturity: £{face_value* (1 + coupon_rate):,.2f}") # Gross proceeds at maturity
    return face_value, price_bond, coupon_income

# Year 2026 (Year 1)
print ("=" * 70)
print("Year 2026 (Year 1)")
print("=" * 70)
tranche_purchase(110_000, 0.015, 97.342 / 100)  # Shortfall, coupon rate, clean price
print("=" * 70)
# Year 2027 (Year 2)
print ("=" * 70)
print("Year 2027 (Year 2)")
print("=" * 70)
tranche_purchase(110_000, 3.75/100, 99.459 / 100)  # Shortfall, coupon rate, clean price
print("=" * 70)
# Year 2028 (Year 3)
print("Year 2027 (Year 3)")
print("=" * 70)
tranche_purchase(110_000, 4.5/100, 101.238 / 100)  # Shortfall, coupon rate, clean price
print("=" * 70)
# Year 2029 (Year 4)
print("Year 2028 (Year 4)")
print("=" * 70)
tranche_purchase(110_000, (4 + (1/8))/100, 99.971 / 100)  # Shortfall, coupon rate, clean price
print("=" * 70)
# Year 2030 (Year 5)
print("Year 2029 (Year 5)")
print("=" * 70)
tranche_purchase(110_000, (4 + (3/8))/100, 100.731 / 100)  # Shortfall, coupon rate, clean price
print("=" * 70)

