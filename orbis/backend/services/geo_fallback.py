"""
Country-code → (lat, lon, name) lookup used when Claude is unavailable.
Covers the most common GDELT sourcecountry codes.
"""

COUNTRY_GEO: dict[str, tuple[float, float, str, str]] = {
    # code: (lat, lon, country_name, capital_city)
    "US": (38.9072, -77.0369, "United States", "Washington D.C."),
    "GB": (51.5074, -0.1278, "United Kingdom", "London"),
    "DE": (52.5200, 13.4050, "Germany", "Berlin"),
    "FR": (48.8566, 2.3522, "France", "Paris"),
    "CN": (39.9042, 116.4074, "China", "Beijing"),
    "RU": (55.7558, 37.6176, "Russia", "Moscow"),
    "IN": (28.6139, 77.2090, "India", "New Delhi"),
    "JP": (35.6762, 139.6503, "Japan", "Tokyo"),
    "AU": (-35.2809, 149.1300, "Australia", "Canberra"),
    "BR": (-15.7975, -47.8919, "Brazil", "Brasília"),
    "CA": (45.4215, -75.6972, "Canada", "Ottawa"),
    "ZA": (-25.7479, 28.2293, "South Africa", "Pretoria"),
    "NG": (9.0579, 7.4951, "Nigeria", "Abuja"),
    "EG": (30.0444, 31.2357, "Egypt", "Cairo"),
    "KE": (-1.2921, 36.8219, "Kenya", "Nairobi"),
    "PK": (33.6844, 73.0479, "Pakistan", "Islamabad"),
    "MX": (19.4326, -99.1332, "Mexico", "Mexico City"),
    "ID": (-6.2088, 106.8456, "Indonesia", "Jakarta"),
    "TR": (39.9334, 32.8597, "Turkey", "Ankara"),
    "SA": (24.7136, 46.6753, "Saudi Arabia", "Riyadh"),
    "AR": (-34.6037, -58.3816, "Argentina", "Buenos Aires"),
    "IL": (31.7683, 35.2137, "Israel", "Jerusalem"),
    "UA": (50.4501, 30.5234, "Ukraine", "Kyiv"),
    "PL": (52.2297, 21.0122, "Poland", "Warsaw"),
    "IR": (35.6892, 51.3890, "Iran", "Tehran"),
    "TH": (13.7563, 100.5018, "Thailand", "Bangkok"),
    "PH": (14.5995, 120.9842, "Philippines", "Manila"),
    "SE": (59.3293, 18.0686, "Sweden", "Stockholm"),
    "NL": (52.3676, 4.9041, "Netherlands", "Amsterdam"),
    "ES": (40.4168, -3.7038, "Spain", "Madrid"),
    "IT": (41.9028, 12.4964, "Italy", "Rome"),
    "GH": (5.6037, -0.1870, "Ghana", "Accra"),
    "ET": (9.0300, 38.7400, "Ethiopia", "Addis Ababa"),
    "SG": (1.3521, 103.8198, "Singapore", "Singapore"),
    "KR": (37.5665, 126.9780, "South Korea", "Seoul"),
    "CO": (4.7110, -74.0721, "Colombia", "Bogotá"),
    "VE": (10.4806, -66.9036, "Venezuela", "Caracas"),
    "NO": (59.9139, 10.7522, "Norway", "Oslo"),
    "CH": (46.9481, 7.4474, "Switzerland", "Bern"),
    "AT": (48.2082, 16.3738, "Austria", "Vienna"),
    "PT": (38.7223, -9.1393, "Portugal", "Lisbon"),
    "GR": (37.9838, 23.7275, "Greece", "Athens"),
    "BE": (50.8503, 4.3517, "Belgium", "Brussels"),
    "HU": (47.4979, 19.0402, "Hungary", "Budapest"),
    "RO": (44.4268, 26.1025, "Romania", "Bucharest"),
    "CZ": (50.0755, 14.4378, "Czech Republic", "Prague"),
    "AE": (24.4539, 54.3773, "UAE", "Abu Dhabi"),
    "QA": (25.2854, 51.5310, "Qatar", "Doha"),
    "NZ": (-36.8485, 174.7633, "New Zealand", "Auckland"),
    "MA": (34.0209, -6.8416, "Morocco", "Rabat"),
    "DZ": (36.7372, 3.0863, "Algeria", "Algiers"),
    "TZ": (-6.1722, 35.7395, "Tanzania", "Dodoma"),
    "UG": (0.3476, 32.5825, "Uganda", "Kampala"),
    "SN": (14.6928, -17.4467, "Senegal", "Dakar"),
    "CI": (5.3540, -4.0075, "Ivory Coast", "Abidjan"),
    "BD": (23.8103, 90.4125, "Bangladesh", "Dhaka"),
    "MM": (16.8661, 96.1951, "Myanmar", "Naypyidaw"),
    "VN": (21.0285, 105.8542, "Vietnam", "Hanoi"),
    "MY": (3.1390, 101.6869, "Malaysia", "Kuala Lumpur"),
    "IQ": (33.3152, 44.3661, "Iraq", "Baghdad"),
    "SY": (33.5138, 36.2765, "Syria", "Damascus"),
    "LB": (33.8938, 35.5018, "Lebanon", "Beirut"),
    "KZ": (51.1801, 71.4460, "Kazakhstan", "Astana"),
    "LY": (32.9022, 13.1800, "Libya", "Tripoli"),
    "SD": (15.5007, 32.5599, "Sudan", "Khartoum"),
    "SO": (2.0469, 45.3182, "Somalia", "Mogadishu"),
    "AF": (34.5253, 69.1783, "Afghanistan", "Kabul"),
    "CL": (-33.4489, -70.6693, "Chile", "Santiago"),
    "PE": (-12.0464, -77.0428, "Peru", "Lima"),
    "CU": (23.1136, -82.3666, "Cuba", "Havana"),
}

DEFAULT = (0.0, 0.0, "World", "Unknown")

# Also index by full country name for GDELT sourcecountry field
_NAME_MAP: dict[str, tuple[float, float, str, str]] = {
    v[2].lower(): v for v in COUNTRY_GEO.values()
}


def lookup(country_ref: str) -> tuple[float, float, str, str]:
    """Accept 2-letter ISO code or full country name (case-insensitive)."""
    if not country_ref:
        return DEFAULT
    # Try 2-letter code first
    by_code = COUNTRY_GEO.get(country_ref.upper())
    if by_code:
        return by_code
    # Try full name
    return _NAME_MAP.get(country_ref.strip().lower(), DEFAULT)
