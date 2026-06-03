import httpx
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.app.vector_store import get_vector_store

# ==============================================================================
# COMPREHENSIVE SEED DATA — Full Bilaad Realty Portfolio (All 14 Properties)
# Verified from bilaadnigeria.com — June 2026
# This is the primary, high-fidelity knowledge base for the RAG engine.
# ==============================================================================
SEED_DATA = [

    # ── CORPORATE OVERVIEW ──────────────────────────────────────────────────
    Document(
        page_content="""Bilaad Realty is a leading Nigerian real estate development company headquartered 
in Abuja, with the mission of "Building Sustainable Cities." The company delivers premium residential 
estates that blend luxury living with eco-friendly infrastructure, smart home automation, and 
community-centric design. Bilaad Realty serves high-net-worth investors and homeowners across 
Abuja's most prestigious districts including Gwarinpa, Lifecamp, Jabi, Katampe, Mabushi, and Maitama.

All developments are themed after world-famous islands and destinations — The Maldives, The Bali Island, 
Langkawi Island, Seychelles, Capri Island, Zanzibar, Bimini Island, Barbados, Bobowasi Island, 
Fiji Island, Mauritius Island, The Amazon, The Bahamas, and more.

Bilaad Realty offers flexible payment plans, premium investment packages, and is recognized for 
sustainability, green architecture, and community living.
Contact: www.bilaadnigeria.com | @BilaadRealty (Facebook, X, Instagram, LinkedIn)""",
        metadata={"title": "About Bilaad Realty", "category": "Corporate Overview", "url": "https://www.bilaadnigeria.com/"}
    ),

    Document(
        page_content="""Bilaad Realty sustainability standards across all estates:
- Solar grid systems and solar-powered street lighting (up to 40% energy reduction)
- Smart home automation integrated into premium units
- Greywater recycling systems and smart waste management
- Energy-efficient building materials and local material procurement
- Extensive green canopy cover to combat urban heat island effects
- 24-hour CCTV surveillance and gated security across all communities
- High-speed fiber-optic internet access in select estates
- Swimming pools, gyms, children's play areas, and pedestrian-friendly walkways
Bilaad Realty's vision is to lead Nigeria's transition toward sustainable urban living.""",
        metadata={"title": "Bilaad Realty Sustainability & Amenities", "category": "Sustainability", "url": "https://www.bilaadnigeria.com/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 1: THE MALDIVES
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""The Maldives by Bilaad Realty is a 1.29-hectare estate located in the heart of 
Gwarinpa II, Abuja FCT. It is designed to cater to individuals with high taste and an appeal for 
comfort. This estate comprises 19 units of spacious stand-alone Onyx homes in a secure and serene 
environment, each designed to provide a premium lifestyle experience. The Maldives features smart 
home automation, dedicated solar grid systems for clean energy, and smart waste management. 
It is one of Bilaad Realty's flagship estates setting the benchmark for sustainable residential 
development in Abuja.""",
        metadata={"title": "The Maldives by Bilaad", "location": "Gwarinpa II, Abuja", "category": "Premium Eco-Villas", "total_units": "19", "size": "1.29 hectares", "unit_type": "Onyx homes (stand-alone)", "url": "https://www.bilaadnigeria.com/maldives-by-bilaad/"}
    ),
    Document(
        page_content="""Maldives by Bilaad — Property Specifications:
Location: Gwarinpa II, Abuja FCT, Nigeria
Land area: 1.29 hectares
Total units: 19 exclusive stand-alone homes
Unit name: The Onyx
Unit type: Spacious stand-alone villas
Features: Smart home automation, solar grid, secure gated community, serene environment
Developer: Bilaad Realty — Building Sustainable Cities
URL: https://www.bilaadnigeria.com/maldives-by-bilaad/""",
        metadata={"title": "The Maldives — Specifications", "location": "Gwarinpa II, Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/maldives-by-bilaad/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 2: THE BALI ISLAND
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""The Bali Island by Bilaad is an exclusive luxury residential development located 
in Life Camp, Abuja. Inspired by resort living, it integrates tropical architectural aesthetics with 
eco-friendly infrastructure including solar-powered street lighting, energy-efficient building materials, 
and greywater recycling systems. The community is geared towards peace, luxury, and ecological balance, 
offering residents a harmonious blend of nature and modern living in one of Abuja's most prestigious areas.""",
        metadata={"title": "The Bali Island by Bilaad", "location": "Life Camp, Abuja", "category": "Luxury Resort Residences", "url": "https://www.bilaadnigeria.com/bali-island-by-bilaad/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 3: LANGKAWI ISLAND
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""Langkawi Island by Bilaad (officially LANGWANKI ISLAND BY BILAAD) is a refined 
residential estate located in Katampe Layout, Abuja. Spanning 2.63 hectares, the estate offers 103 
thoughtfully crafted homes. The property features multiple unit types:
- 5-bedroom villas — elegant and spacious premium units
- 4-bedroom townhouses — spacious and family-ready
- 3-bedroom apartments — stylish and functional
- 2-bedroom apartments — compact modern starter homes
Each unit is designed with comfort, functionality, and sophistication in mind. With serene surroundings 
and secure living, Langkawi Island delivers a luxurious lifestyle in Katampe, one of Abuja's premium 
neighbourhoods. Ideal for families and investors seeking long-term value in a gated community.""",
        metadata={"title": "Langkawi Island by Bilaad", "location": "Katampe Layout, Abuja", "category": "Mixed Residential Estate", "total_units": "103", "size": "2.63 hectares", "url": "https://www.bilaadnigeria.com/langkawi-by-bilaad/"}
    ),
    Document(
        page_content="""Langkawi Island — Property Specifications:
Location: Katampe Layout, Abuja, Nigeria
Land area: 2.63 hectares
Total homes: 103 units
Unit types: 5-bedroom villas, 4-bedroom townhouses, 3-bedroom apartments, 2-bedroom apartments
Setting: Gated community, secure and serene, luxury finishes
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/langkawi-by-bilaad/""",
        metadata={"title": "Langkawi Island — Specifications", "location": "Katampe Layout, Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/langkawi-by-bilaad/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 4: SEYCHELLES
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""Seychelles by Bilaad is an exclusive luxury estate set on 4,692 sqm in the lush 
heart of Jabi District, Abuja. This serene enclave is where nature and luxury coexist. The development 
features 8 exclusive units of the exquisite 5-bedroom Amber homes, thoughtfully designed for spacious 
living. Surrounded by greenery and offering captivating views of the Jabi Lake, Seychelles invites 
residents to reconnect with nature while enjoying the finest in contemporary residential design. 
With only 8 homes, Seychelles is one of the most exclusive limited offerings in Bilaad Realty's portfolio.""",
        metadata={"title": "Seychelles by Bilaad", "location": "Jabi District, Abuja", "category": "Exclusive Lake-View Residences", "total_units": "8", "size": "4,692 sqm", "unit_type": "The Amber (5-bedroom)", "url": "https://www.bilaadnigeria.com/seychelles-progress/"}
    ),
    Document(
        page_content="""Seychelles — Property Specifications:
Location: Jabi District, Abuja, Nigeria (near Jabi Lake)
Land area: 4,692 square metres (sqm)
Total units: 8 exclusive homes (very limited)
Unit name: The Amber
Unit type: 5-bedroom luxury homes
Views: Jabi Lake and lush green surroundings
Character: Ultra-exclusive, nature-meets-luxury enclave
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/seychelles-progress/""",
        metadata={"title": "Seychelles — Specifications", "location": "Jabi District, Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/seychelles-progress/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 5: CAPRI ISLAND
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""Capri Island by Bilaad is a sophisticated residential estate set across a vast 
3.04-hectare estate in the sought-after Lifecamp neighbourhood of Abuja. With 87 exclusive homes, 
the estate features three distinct house types designed with luxury, comfort, and functionality:
- The Aquamarine — premium villa, top-tier unit
- The Citrine — mid-range luxury family home
- The Aventurine — elegant spacious residence
More than just a place to live, Capri Island is a lifestyle destination offering modern architecture, 
high-end finishes, and a secure community environment in one of Abuja's most desirable addresses.""",
        metadata={"title": "Capri Island by Bilaad", "location": "Lifecamp, Abuja", "category": "Luxury Estate", "total_units": "87", "size": "3.04 hectares", "url": "https://www.bilaadnigeria.com/capri-island/"}
    ),
    Document(
        page_content="""Capri Island — Property Specifications:
Location: Lifecamp, Abuja, Nigeria
Land area: 3.04 hectares
Total homes: 87 exclusive units
Unit types:
  - The Aquamarine (premium villa tier)
  - The Citrine (mid-range luxury)
  - The Aventurine (elegant family home)
Setting: Gated estate, modern architecture, high-end finishes
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/capri-island/""",
        metadata={"title": "Capri Island — Specifications", "location": "Lifecamp, Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/capri-island/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 6: ZANZIBAR
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""Zanzibar by Bilaad is a Premium Plus Property estate crafted for spacious, 
upscale living in Abuja. The estate features 27 limited-edition 5-bedroom residences known as 
The Emerald. Classified as Bilaad Realty's Premium Plus tier, Zanzibar sets a new benchmark in 
design and comfort. Every unit combines modern architecture with high-end finishes, offering a 
seamless blend of style and functionality. Designed for discerning homeowners who demand exclusivity, 
Zanzibar represents the pinnacle of Bilaad Realty's residential portfolio.""",
        metadata={"title": "Zanzibar by Bilaad", "location": "Abuja", "category": "Premium Plus Estate", "total_units": "27", "unit_type": "The Emerald (5-bedroom)", "url": "https://www.bilaadnigeria.com/zanzibar/"}
    ),
    Document(
        page_content="""Zanzibar — Property Specifications:
Location: Abuja, Nigeria
Classification: Premium Plus Property (Bilaad Realty's highest tier)
Total units: 27 limited-edition residences
Unit name: The Emerald
Unit type: 5-bedroom luxury homes
Design: Modern architecture, high-end finishes, seamless style and functionality
Target: Ultra-discerning homeowners seeking exclusivity
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/zanzibar/""",
        metadata={"title": "Zanzibar — Specifications", "location": "Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/zanzibar/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 7: BIMINI ISLAND
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""Bimini Island by Bilaad is an exclusive enclave offering quiet sophistication 
tucked within the prestigious Ministers' Quarters of Mabushi District, Abuja. This thoughtfully 
planned development comprises just 8 limited-edition townhouses known as The Pearl. Each unit is 
a statement of refined taste and contemporary living, with spacious interiors, elegant finishes, 
and a privileged address in Mabushi — one of Abuja's most distinguished neighbourhoods. 
At only 8 units, Bimini Island is among Bilaad Realty's most exclusive limited-edition offerings.""",
        metadata={"title": "Bimini Island by Bilaad", "location": "Mabushi (Ministers' Quarters), Abuja", "category": "Ultra-Exclusive Townhouses", "total_units": "8", "unit_type": "The Pearl (townhouses)", "url": "https://www.bilaadnigeria.com/bimini/"}
    ),
    Document(
        page_content="""Bimini Island — Property Specifications:
Location: Ministers' Quarters, Mabushi District, Abuja, Nigeria
Total units: 8 limited-edition townhouses (ultra-exclusive)
Unit name: The Pearl
Unit type: Luxury townhouses
Setting: Ministers' Quarters — one of Abuja's most prestigious and secure addresses
Design: Contemporary living, spacious interiors, elegant finishes
Target: Senior executives, diplomats, ministers, ultra-high-net-worth individuals
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/bimini/""",
        metadata={"title": "Bimini Island — Specifications", "location": "Mabushi District, Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/bimini/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 8: BARBADOS
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""Barbados Island by Bilaad is an exciting premium residential development where a 
breathtaking landscape meets architectural brilliance. Set in a stunning environment adorned with 
vibrant, colourful gardens that showcase tranquility and wonder, the estate contains 24 units of 
five-bedroom villas with employee quarters. The signature unit is called The Onyx — a beautifully 
designed villa that is a perfect blend of creativity and craftsmanship. Barbados Island delivers 
an exceptional lifestyle with lush garden surroundings, high-end finishes, and modern living standards.""",
        metadata={"title": "Barbados Island by Bilaad", "location": "Abuja", "category": "Premium Villas", "total_units": "24", "unit_type": "The Onyx (5-bedroom villas with staff quarters)", "url": "https://www.bilaadnigeria.com/barbados-by-bilaad/"}
    ),
    Document(
        page_content="""Barbados Island — Property Specifications:
Location: Abuja, Nigeria
Total units: 24 units
Unit name: The Onyx
Unit type: 5-bedroom villas with employee/staff quarters
Setting: Vibrant, colourful landscaped gardens, breathtaking landscape
Design: Architectural brilliance, creativity and craftsmanship, tranquil surroundings
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/barbados-by-bilaad/""",
        metadata={"title": "Barbados Island — Specifications", "location": "Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/barbados-by-bilaad/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 9: BOBOWASI ISLAND
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""Bobowasi Island by Bilaad is envisioned as a vibrant, sustainable community 
featuring 40 exclusive Garnet Homes. Designed with residents' comfort in mind, the estate boasts 
an impressive array of world-class amenities including:
- 24-hour CCTV surveillance for security and peace of mind
- Fully equipped gym and fitness centre
- Refreshing swimming pool
- Dedicated children's play area
- High-speed fiber-optic internet access
Bobowasi Island represents Bilaad Realty's commitment to creating fully serviced, community-focused 
residential developments where every lifestyle need is catered to.""",
        metadata={"title": "Bobowasi Island by Bilaad", "location": "Abuja", "category": "Sustainable Community Estate", "total_units": "40", "unit_type": "The Garnet Homes", "url": "https://www.bilaadnigeria.com/bobowasi-by-bilaad/"}
    ),
    Document(
        page_content="""Bobowasi Island — Property Specifications:
Location: Abuja, Nigeria
Total units: 40 exclusive homes
Unit name: The Garnet Homes
Amenities: 24-hour CCTV, gym, swimming pool, children's play area, high-speed fiber-optic internet
Community type: Vibrant, sustainable, fully serviced residential community
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/bobowasi-by-bilaad/""",
        metadata={"title": "Bobowasi Island — Specifications", "location": "Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/bobowasi-by-bilaad/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 10: FIJI ISLAND
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""Fiji Island by Bilaad Realty is a 1-hectare estate located in the desirable 
Jabi area of Abuja. It is tailored to suit individuals with a refined taste and a love for comfort. 
This exclusive community features 18 units of spacious stand-alone Sapphire homes, each thoughtfully 
designed to offer a secure and serene living experience. The Fiji Island combines exclusivity with 
accessibility in one of Abuja's most vibrant neighbourhoods, providing a lifestyle of comfort, 
privacy, and elegance for its residents.""",
        metadata={"title": "Fiji Island by Bilaad", "location": "Jabi, Abuja", "category": "Exclusive Standalone Villas", "total_units": "18", "size": "1 hectare", "unit_type": "The Sapphire (stand-alone homes)", "url": "https://www.bilaadnigeria.com/fiji-by-bilaad/"}
    ),
    Document(
        page_content="""Fiji Island — Property Specifications:
Location: Jabi, Abuja, Nigeria
Land area: 1 hectare
Total units: 18 exclusive stand-alone homes
Unit name: The Sapphire
Unit type: Spacious stand-alone villas
Setting: Secure, serene, gated community in Jabi — one of Abuja's most desirable areas
Target: Individuals with refined taste and love for comfort
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/fiji-by-bilaad/""",
        metadata={"title": "Fiji Island — Specifications", "location": "Jabi, Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/fiji-by-bilaad/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 11: MAURITIUS ISLAND
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""Mauritius Island by Bilaad is a distinguished golf estate located in the 
prestigious Ministers' Quarters of Mabushi District, Abuja. This exclusive community blends luxury 
living with recreational charm and features 30 meticulously crafted homes across two signature 
residence types:
- The Peridot — signature luxury residence
- The Platinum — premium prestige residence
Each home offers generous space, high-end finishes, and thoughtful design. More than just a 
residential development, Mauritius Island is a lifestyle destination that combines a golf estate 
ambience with the best in contemporary residential architecture.""",
        metadata={"title": "Mauritius Island by Bilaad", "location": "Mabushi (Ministers' Quarters), Abuja", "category": "Golf Estate & Luxury Homes", "total_units": "30", "unit_type": "The Peridot & The Platinum", "url": "https://www.bilaadnigeria.com/mauritius/"}
    ),
    Document(
        page_content="""Mauritius Island — Property Specifications:
Location: Ministers' Quarters, Mabushi District, Abuja, Nigeria
Total units: 30 homes
Unit types:
  - The Peridot (signature luxury residence)
  - The Platinum (premium prestige residence)
Character: Distinguished golf estate, luxury living with recreational charm
Setting: Prestigious Ministers' Quarters — prime Abuja address
Design: Generous space, high-end finishes, thoughtful contemporary architecture
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/mauritius/""",
        metadata={"title": "Mauritius Island — Specifications", "location": "Mabushi District, Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/mauritius/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 12: THE AMAZON
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""The Amazon by Bilaad is an exclusive enclave of just 20 impeccably designed 
homes, each offering a harmonious blend of spacious interiors and serene outdoor spaces. This unique 
development features beautifully landscaped recreational areas, pedestrian-friendly walkways, and 
cutting-edge amenities for modern living. Security and convenience are paramount with:
- Automated sprinkler system for landscaping
- Solar-powered street lights
- High-speed fiber-optic internet connectivity
The Amazon delivers a green, technologically advanced living experience for discerning homeowners 
who want the very best in both nature and technology.""",
        metadata={"title": "The Amazon by Bilaad", "location": "Abuja", "category": "Eco-Tech Residential Enclave", "total_units": "20", "url": "https://www.bilaadnigeria.com/the-amazon-by-bilaad/"}
    ),
    Document(
        page_content="""The Amazon — Property Specifications:
Location: Abuja, Nigeria
Total units: 20 exclusive homes
Design: Spacious interiors, serene outdoor spaces, landscaped recreational areas
Amenities: Automated sprinkler system, solar-powered street lights, high-speed fiber-optic internet
Setting: Pedestrian-friendly walkways, lush landscaping, security-focused community
Character: Eco-friendly, technologically advanced, nature-inspired living
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/the-amazon-by-bilaad/""",
        metadata={"title": "The Amazon — Specifications", "location": "Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/the-amazon-by-bilaad/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 13: THE BAHAMAS
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""The Bahamas by Bilaad Realty is situated in one of the most picturesque streets 
in the Federal Capital Territory of Nigeria. Spanning 11.37 hectares in the heart of Maitama II, 
this exceptional estate features 505 premium homes designed for modern living. With a secure and 
serene environment, The Bahamas provides residents with the ultimate in luxury, comfort, and 
community living. This is Bilaad Realty's largest estate by both land area and unit count, 
making it one of Abuja's most ambitious premium residential developments. The Bahamas boasts an 
enviable and prestigious location in Maitama II — one of Abuja's most exclusive and high-value zones.""",
        metadata={"title": "The Bahamas by Bilaad", "location": "Maitama II, Abuja", "category": "Large-Scale Premium Estate", "total_units": "505", "size": "11.37 hectares", "url": "https://www.bilaadnigeria.com/the-bahamas-by-bilaad/"}
    ),
    Document(
        page_content="""The Bahamas — Property Specifications:
Location: Maitama II, Abuja FCT, Nigeria (one of Abuja's most prestigious addresses)
Land area: 11.37 hectares (Bilaad Realty's largest estate by area)
Total homes: 505 premium homes (Bilaad Realty's largest estate by unit count)
Setting: Secure, serene, gated community in the heart of Maitama II
Design: Modern living, premium homes, luxury and comfort
Character: Prestigious, large-scale community development
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/the-bahamas-by-bilaad/""",
        metadata={"title": "The Bahamas — Specifications", "location": "Maitama II, Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/the-bahamas-by-bilaad/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY 14: BORA BORA ISLAND
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""Bora Bora Island by Bilaad is a premium sustainable residential estate located 
on Ameh Ebute Street in Wuye, Abuja FCT. Spanning a strategic area in Wuye, the estate features 
63 elegant homes designed with comfort and sustainability in mind. The estate combines smart-home 
automation with energy efficiency (such as double-glazed windows) and modern community amenities. 
Bora Bora Island is ideally situated within walking distance to Wuye Modern Market, minutes from 
Stone Parks and Gardens, and offers quick access to the Abuja City Centre and the Nnamdi Azikiwe 
International Airport, setting a new standard for serene, connected living in Abuja.""",
        metadata={"title": "Bora Bora Island by Bilaad", "location": "Wuye, Abuja", "category": "Premium Sustainable Estate", "total_units": "63", "url": "https://www.bilaadnigeria.com/7622-2/"}
    ),
    Document(
        page_content="""Bora Bora Island — Property Specifications:
Location: Ameh Ebute Street, Wuye, Abuja, Nigeria
Total homes: 63 units
Unit types & names:
  - The Sapphire: 5-bedroom villa with en-suite employee/maid's quarters, spread across two suspended floors. Ideal for mid-to-large-sized families, featuring smart home integration.
  - The Ruby: 4-bedroom townhouse with en-suite employee/maid's quarters, spanning two levels. Blend of style, functionality, smart home automation, and energy-efficient design.
  - The Topaz: 3-bedroom apartment with en-suite bathrooms and an en-suite employee/maid's quarters. Built for growing families with functional layouts and intelligent home systems.
Amenities: Fully equipped gym, adult and children's swimming pools, high-speed fiber-optic internet connectivity, alternative/backup power systems, automated landscaping, gated security, and green recreational spaces.
Developer: Bilaad Realty
URL: https://www.bilaadnigeria.com/7622-2/""",
        metadata={"title": "Bora Bora Island — Specifications", "location": "Wuye, Abuja", "category": "Property Specifications", "url": "https://www.bilaadnigeria.com/7622-2/"}
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # COMPLETE PORTFOLIO COMPARISON TABLE
    # ─────────────────────────────────────────────────────────────────────────
    Document(
        page_content="""Bilaad Realty complete property portfolio — all 14 known estates (as of June 2026):

 1. THE MALDIVES         | Gwarinpa II, Abuja        | 19 units  | The Onyx (stand-alone villas)       | 1.29 ha
 2. THE BALI ISLAND      | Life Camp, Abuja          | N/A        | Luxury resort residences            |
 3. LANGKAWI ISLAND      | Katampe Layout, Abuja     | 103 units  | 5-bed villas, 4-bed TH, 2/3-bed apts | 2.63 ha
 4. SEYCHELLES           | Jabi District, Abuja      | 8 units    | The Amber (5-bedroom, lake views)   | 4,692 sqm
 5. CAPRI ISLAND         | Lifecamp, Abuja           | 87 units   | Aquamarine, Citrine, Aventurine     | 3.04 ha
 6. ZANZIBAR             | Abuja                     | 27 units   | The Emerald (5-bed) — Premium Plus  |
 7. BIMINI ISLAND        | Mabushi (Min. Quarters)   | 8 units    | The Pearl (luxury townhouses)       |
 8. BARBADOS             | Abuja                     | 24 units   | The Onyx (5-bed + staff quarters)   |
 9. BOBOWASI ISLAND      | Abuja                     | 40 units   | The Garnet Homes (full amenities)   |
10. FIJI ISLAND          | Jabi, Abuja               | 18 units   | The Sapphire (stand-alone villas)   | 1 ha
11. MAURITIUS ISLAND     | Mabushi (Min. Quarters)   | 30 units   | The Peridot & The Platinum (golf)   |
12. THE AMAZON           | Abuja                     | 20 units   | Eco-tech enclave, solar + fiber     |
13. THE BAHAMAS          | Maitama II, Abuja         | 505 units  | Premium homes — largest estate      | 11.37 ha
14. BORA BORA ISLAND     | Wuye, Abuja               | 63 units   | Sapphire, Ruby, Topaz               |

Total properties: 14 estates | Developer: Bilaad Realty | Website: www.bilaadnigeria.com""",
        metadata={"title": "Bilaad Realty — Complete Portfolio Overview", "category": "Portfolio Summary", "url": "https://www.bilaadnigeria.com/"}
    ),
]

# All known Bilaad Realty property URLs to scrape live
PROPERTY_URLS = [
    "https://www.bilaadnigeria.com/",
    "https://www.bilaadnigeria.com/maldives-by-bilaad/",
    "https://www.bilaadnigeria.com/bali-island-by-bilaad/",
    "https://www.bilaadnigeria.com/langkawi-by-bilaad/",
    "https://www.bilaadnigeria.com/seychelles-progress/",
    "https://www.bilaadnigeria.com/capri-island/",
    "https://www.bilaadnigeria.com/zanzibar/",
    "https://www.bilaadnigeria.com/bimini/",
    "https://www.bilaadnigeria.com/barbados-by-bilaad/",
    "https://www.bilaadnigeria.com/bobowasi-by-bilaad/",
    "https://www.bilaadnigeria.com/fiji-by-bilaad/",
    "https://www.bilaadnigeria.com/mauritius/",
    "https://www.bilaadnigeria.com/the-amazon-by-bilaad/",
    "https://www.bilaadnigeria.com/the-bahamas-by-bilaad/",
    "https://www.bilaadnigeria.com/7622-2/",
    "https://www.bilaadnigeria.com/our-project/",
    "https://www.bilaadnigeria.com/about-us/",
]


def scrape_page(url: str) -> Document | None:
    """Scrape a single page and return a Document with its text content."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = httpx.get(url, headers=headers, timeout=15.0, follow_redirects=True)
        if response.status_code != 200:
            print(f"[SCRAPER] Status {response.status_code} for {url}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract meta description — always reliable on this WordPress site
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = meta_tag["content"].strip()

        # Extract page title
        title_tag = soup.find("title")
        page_title = title_tag.get_text(strip=True) if title_tag else url

        # Extract visible text from key semantic tags
        paragraphs = []
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
            text = tag.get_text(separator=" ", strip=True)
            if len(text) > 30:
                paragraphs.append(text)

        combined = f"Page: {page_title}\nDescription: {meta_desc}\n\n" + "\n\n".join(paragraphs[:80])

        if len(combined) > 200:
            print(f"[SCRAPER] Scraped {len(combined)} chars from {url}")
            return Document(
                page_content=combined,
                metadata={"source": url, "title": page_title}
            )
    except Exception as e:
        print(f"[SCRAPER] Error scraping {url}: {e}")
    return None


def scrape_bilaad_website() -> list[Document]:
    """Scrape all known Bilaad Realty property pages and return Document objects."""
    documents = []
    print(f"[SCRAPER] Starting live scrape of {len(PROPERTY_URLS)} pages...")
    for url in PROPERTY_URLS:
        doc = scrape_page(url)
        if doc:
            documents.append(doc)
    print(f"[SCRAPER] Live scrape complete — {len(documents)} pages captured.")
    return documents


def ingest_portfolio_data() -> dict:
    """
    Scrapes all Bilaad Realty property pages, merges with comprehensive curated
    seed data covering all 14 known estates, chunks, and uploads to the vector store.
    """
    v_store = get_vector_store()
    if not v_store:
        return {"status": "error", "message": "Vector store not initialized. Cannot ingest data."}

    # 1. Scrape live pages
    live_docs = scrape_bilaad_website()

    # 2. Merge with curated seed data (all 14 properties + corporate info)
    all_documents = live_docs + SEED_DATA
    print(f"[INGESTION] Total documents before chunking: {len(all_documents)} ({len(live_docs)} live + {len(SEED_DATA)} seed)")

    # 3. Chunk documents for precise RAG retrieval
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    split_docs = text_splitter.split_documents(all_documents)
    print(f"[INGESTION] Created {len(split_docs)} chunks for ingestion.")

    # 4. Upload to vector store
    try:
        # Clear existing records first to avoid duplication
        from supabase.client import create_client
        from backend.app.config import Config
        try:
            supabase_client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
            # Delete all documents with id not equal to 0
            supabase_client.table("documents").delete().neq("id", 0).execute()
            print("[INGESTION] Cleared existing documents in Supabase.")
        except Exception as e:
            print(f"[INGESTION] Warning clearing old documents: {e}")

        # Ingest in batches of 10 with 20-second pauses to respect Gemini free tier rate limits
        import time
        batch_size = 10
        for i in range(0, len(split_docs), batch_size):
            batch = split_docs[i:i+batch_size]
            batch_ids = [j + 1 for j in range(i, i+len(batch))]
            print(f"[INGESTION] Uploading batch {i//batch_size + 1} ({len(batch)} chunks) with custom IDs...")
            
            # Retry loop for resilience against network glitches / timeouts
            max_retries = 5
            for retry in range(max_retries):
                try:
                    v_store.add_documents(batch, ids=batch_ids)
                    break
                except Exception as e:
                    if retry == max_retries - 1:
                        raise e
                    wait_time = 30 * (retry + 1)
                    print(f"[INGESTION] Batch upload failed: {e}. Retrying in {wait_time}s ({retry + 1}/{max_retries})...")
                    time.sleep(wait_time)

            if i + batch_size < len(split_docs):
                print("[INGESTION] Sleeping 20 seconds to avoid API rate limit...")
                time.sleep(20)

        print("[INGESTION] Successfully uploaded all chunks to vector store.")
        return {
            "status": "success",
            "message": f"Successfully ingested {len(split_docs)} chunks covering 14 Bilaad Realty properties.",
            "chunk_count": len(split_docs),
            "properties_covered": [
                "1. The Maldives — 19 units, The Onyx (Gwarinpa II)",
                "2. The Bali Island (Life Camp)",
                "3. Langkawi Island — 103 units (Katampe)",
                "4. Seychelles — 8 units, The Amber (Jabi, lake views)",
                "5. Capri Island — 87 units, Aquamarine/Citrine/Aventurine (Lifecamp)",
                "6. Zanzibar — 27 units, The Emerald, Premium Plus",
                "7. Bimini Island — 8 units, The Pearl (Mabushi)",
                "8. Barbados — 24 units, The Onyx 5-bed + staff quarters",
                "9. Bobowasi Island — 40 units, The Garnet Homes",
                "10. Fiji Island — 18 units, The Sapphire (Jabi, 1 ha)",
                "11. Mauritius Island — 30 units, The Peridot & Platinum (Mabushi golf estate)",
                "12. The Amazon — 20 units, eco-tech enclave",
                "13. The Bahamas — 505 units, 11.37 ha (Maitama II)",
                "14. Bora Bora Island — 63 units, Sapphire/Ruby/Topaz (Wuye)",
            ]
        }
    except Exception as e:
        print(f"[INGESTION] Error uploading to vector store: {e}")
        return {"status": "error", "message": f"Failed to upload embeddings: {str(e)}"}

