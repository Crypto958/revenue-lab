"""Verified nationwide SEO cohort.

Source: owner-supplied urbanloop_verified_service_area_dataset.zip, verified
2026-10-04. Internal operator IDs and evidence are deliberately not imported
into page content. This first cohort contains 20 city pages and 30 route pages.
"""

CITY_COHORT = [
    ("Delhi", "delhi", "Delhi", ["Agra", "Haridwar", "Rishikesh"]),
    ("Mumbai", "mumbai", "Maharashtra", ["Lonavala", "Nashik", "Shirdi"]),
    ("Bengaluru", "bengaluru", "Karnataka", ["Mysuru", "Hassan", "Chitradurga"]),
    ("Hyderabad", "hyderabad", "Telangana", ["Warangal", "Nalgonda", "Bidar"]),
    ("Chennai", "chennai", "Tamil Nadu", ["Mahabalipuram", "Puducherry", "Tirupati"]),
    ("Kolkata", "kolkata", "West Bengal", ["Digha", "Durgapur", "Haldia"]),
    ("Pune", "pune", "Maharashtra", ["Mahabaleshwar", "Nashik", "Mumbai"]),
    ("Ahmedabad", "ahmedabad", "Gujarat", ["Gandhinagar", "Vadodara", "Rajkot"]),
    ("Surat", "surat", "Gujarat", ["Saputara", "Vadodara", "Bharuch"]),
    ("Jaipur", "jaipur", "Rajasthan", ["Ajmer", "Pushkar", "Agra"]),
    ("Lucknow", "lucknow", "Uttar Pradesh", ["Ayodhya", "Kanpur", "Prayagraj"]),
    ("Chandigarh", "chandigarh", "Chandigarh", ["Shimla", "Amritsar", "Rishikesh"]),
    ("Kochi", "kochi", "Kerala", ["Munnar", "Alappuzha", "Thekkady"]),
    ("Coimbatore", "coimbatore", "Tamil Nadu", ["Ooty", "Kochi", "Madurai"]),
    ("Indore", "indore", "Madhya Pradesh", ["Ujjain", "Omkareshwar", "Maheshwar"]),
    ("Bhopal", "bhopal", "Madhya Pradesh", ["Sanchi", "Ujjain", "Pachmarhi"]),
    ("Nagpur", "nagpur", "Maharashtra", ["Pench", "Amravati", "Chandrapur"]),
    ("Patna", "patna", "Bihar", ["Gaya", "Bodh Gaya", "Rajgir"]),
    ("Bhubaneswar", "bhubaneswar", "Odisha", ["Puri", "Konark", "Chilika"]),
    ("Guwahati", "guwahati", "Assam", ["Shillong", "Kaziranga", "Tezpur"]),
]

ROUTE_COHORT = [
    (city, slug, state, destination)
    for city, slug, state, destinations in CITY_COHORT[:10]
    for destination in destinations
]
