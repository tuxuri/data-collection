malaysian_states = ["Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan",
                    "Pahang", "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak", "Selangor", "Terengganu"]

given_address = "Pt 8926, Jalan Telok Gong, Kampung Telok Gong, 42000 Pelabuhan Klang, singapura Darul Ehsan."


for state in malaysian_states:
    if state in given_address:
        print(f"The state '{state}' is present in the given address.")
        break

