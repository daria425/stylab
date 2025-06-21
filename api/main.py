from app.services.fashion_classifier import FashionClassifier
from app.utils.logger import logger
import time
import json
dset=[
  {
    "title": "Sacai Spring 2025 Menswear Fashion Show | Vogue Street Casual, Summer 2025 Runway, Denim Street Style 2025, Denim Spring Summer 2025, Denim Spring 2025, Sacai Spring 2023 Ready To Wear, Sacai Runway, Jeans Trend, Trendy Fall Fashion",
    "url": "/pin/3729612256806176/",
    "img": "https://i.pinimg.com/236x/91/cd/df/91cddf7888d9151ddcbc0435da0de97e.jpg"
  },
  {
    "title": "Checkered Knit Cardigan, Copenhagen Fashion Week Street Style, Pattern Outfits, Pullovers Outfit, Fashion Trend Forecast, Black White Outfit, Casual Outfit Inspiration, Copenhagen Style, Copenhagen Fashion Week",
    "url": "/pin/97671885662642322/",
    "img": "https://i.pinimg.com/236x/72/c0/39/72c0390e61540f7a73b7414e75deb37d.jpg"
  },
  {
    "title": "East Coast Fashion, Copenhagen Fashion Week Street Style, Hot Summer Outfits, Loungewear Fashion, Street Style Edgy, Copenhagen Fashion Week, Copenhagen Style, Street Style Summer, Autumn Fashion Casual",
    "url": "/pin/46865652368407344/",
    "img": "https://i.pinimg.com/236x/e5/74/f4/e574f4c3088322e69dabc076da5b5f72.jpg"
  },
  {
    "title": "Milan Street Fashion, 2025 Street Fashion, Fashion Week 2025, Paris Fashion Week 2025 Street Style, Street Style 2025, Paris Fashion Week Street Style 2025, Paris Fashion Week Street Style, Stripe Outfits, Street Style Paris",
    "url": "/pin/25966135347770049/",
    "img": "https://i.pinimg.com/236x/b4/87/12/b48712f2093116c6ced2a0716a033b7e.jpg"
  },
  {
    "title": "Street Style 2025 Spring Summer Street Style 2025, Spring 2025 Street Style, Street Style 2025, Aladin Pants, Balloon Pants, Tokyo Fashion, Summer Pants, Fashion Sense, Pants Outfit",
    "url": "/pin/14636767535941231/",
    "img": "https://i.pinimg.com/236x/7b/85/64/7b8564db7f04b2478de2ae9bccb4a6d2.jpg"
  },
  {
    "title": "Spring Jacket Ideas 2025 Edgy Day Outfit, Modern Jeans Outfit, Tuesday Outfit Casual, Casual Mom Style Winter, Trend Style 2025 Spring, Winter Trends 2025 Women, Women\u2019s Style 2025, Chill Style Outfits, Women\u2019s Spring Style 2025",
    "url": "/pin/563018698416580/",
    "img": "https://i.pinimg.com/236x/51/6a/81/516a818a8aae59c29f8ee4203dbb1ffc.jpg"
  },
  {
    "title": "January 2025 Fashion, Trend Fashion 2025, Fashion 2025, Outfit Look, Looks Street Style, Mode Inspo, \uac00\uc744 \ud328\uc158, Mode Inspiration, Lookbook Outfits",
    "url": "/pin/12666442696773799/",
    "img": "https://i.pinimg.com/236x/f1/fa/7d/f1fa7d254bb9e1cca58a95f8a2b487a2.jpg"
  },
  {
    "title": "Discover the 15 hottest 2025 fashion trends that are stylish, wearable, and perfect for any wardrobe. Find out what\u2019s in for 2025 and how to rock these wearable, on-trend looks every day! These wearable trends have you covered for every season. Stay on trend with bold prints, timeless classics, and chic outfits perfect for spring, summer, fall, and winter. #2025FashionTrends #HotTrends #StyleInspo Whats In Style 2025, Women\u2019s 2025 Fashion, Fall 2026 Fashion Trends, 2025 Summer Trends Fashion, On Trend Outfits 2025, Current Fashion Trends 2025 Women, Women Fashion Trends 2025, Trending Looks, 2025 Outfit Ideas Women",
    "url": "/pin/14496030045418866/",
    "img": "https://i.pinimg.com/236x/7a/c8/3d/7ac83d4a6150c23c16d7aca31698ad62.jpg"
  },
  {
    "title": "Street Style 2025 Spring Euro Street Style, Spring 2025 Street Style, Best Casual Dresses, High Fashion Trends, Spring Fashion Chic, Fashion Week Outfit, Queen Outfit, Street Chic, Work Fashion",
    "url": "/pin/140806234062442/",
    "img": "https://i.pinimg.com/236x/21/ff/72/21ff724c43fc12b12aa3b066ea5c98db.jpg"
  },
  {
    "title": "Street Style 2025 Spring 2025 Street Style, Street Style 2025, Global Fashion, Fashion Inspo Outfits, Chic Style, Fashion Inspo, Street Style, Fashion Outfits, Clothes",
    "url": "/pin/3518505954666482/",
    "img": "https://i.pinimg.com/236x/ca/53/9a/ca539a3fd48a697819dddc3455ed8748.jpg"
  },
  {
    "title": "27 Spring Dressing Ideas for Women Over 50 - Stylish Outfits and Trends for 2025 Spring Style 2025, Dressing Over 50, Fashion Inspiration Board, Street Style Inspiration, T Shirt And Jeans, Nyc Fashion, Spring Dress, High Waisted Denim, Casual Chic",
    "url": "/pin/5136987070285588/",
    "img": "https://i.pinimg.com/236x/04/31/2d/04312da2529ccfabb9eb29fc4e7bc56c.jpg"
  },
  {
    "title": "Cargo Pant Outfit Winter, Copenhagen Clothing Style, Everyday Outfits Cold Weather, Cozy Sneaker Outfit, Dublin Style Winter, Copenhagen Chic, Networking Outfit Women Winter, Winter Copenhagen Outfits, Cold Weather Jeans Outfits",
    "url": "/pin/1618549864038432/",
    "img": "https://i.pinimg.com/236x/52/67/38/526738a3aa32d81a42ae6248d6e2e61d.jpg"
  },
  {
    "title": "Bella Hadid wearing shorts fashion trend 2023",
    "url": "/pin/211174978047829/",
    "img": "https://i.pinimg.com/236x/c6/99/e9/c699e9a103089c9b4fa7a53061be377d.jpg"
  },
  {
    "title": "Wonder what made 2025 Fashion Week so memorable? These 22 iconic street style outfits showcase the groundbreaking trends and unforgettable looks that defined this year's fashion scene. Gen Z Fashion Trends 2025, High Fashion Street Style 2025, 2025 Street Fashion, Fashion Week Street Style 2025, Nyc Street Style 2025, 2025 Street Style Trends, London Fashion Week Street Style 2025, 2025 Street Style, Street Style 2025",
    "url": "/pin/1005569423053832291/",
    "img": "https://i.pinimg.com/236x/eb/60/57/eb605736dbbaf9b89330ba8987e089ab.jpg"
  },
  {
    "title": "30 Spring Outfits Ideas for Women Over 40 \u2013 2025 Trends for Chic & Timeless Looks Looks Chic, \uac00\uc744 \ud328\uc158, Mode Inspiration, Office Fashion, Work Fashion, Outfits Casuales, Casual Chic, Winter Fashion, Fall Outfits",
    "url": "/pin/66920744457019214/",
    "img": "https://i.pinimg.com/236x/89/93/04/8993044f733805e192ae7404399af8c9.jpg"
  },
  {
    "title": "Adidas Street Style, Sport Casual Outfit, Sports Chic Outfit, Track Pants Outfit, Looks Adidas, Adidas Hose, Adidas Samba Outfit, Moda Denim, Outfit Jeans",
    "url": "/pin/40813940369123482/",
    "img": "https://i.pinimg.com/236x/8d/1d/eb/8d1deba71df261f7956b30de1258dbbe.jpg"
  },
  {
    "title": "Cute Spring Outfits: Trends and Ideas for 2025 Spring Trends Outfits, Cute Spring Outfits, Cute Spring, Casual Chic Outfit, New Fashion Trends, Winter Fashion Outfits, Comfy Outfits, Outfits For Teens, Dress To Impress",
    "url": "/pin/51158145761062798/",
    "img": "https://i.pinimg.com/236x/82/e8/52/82e8521dba0e3c1d9658c20946dc9d36.jpg"
  },
  {
    "title": "Spring 2024 Fashion Trends: Chic Outfits & Wardrobe Essentials Contemporary Luxe Style, Street Chic Outfits Summer, 2024 Spring Street Style, 2024 Fashion Week Street Style, Edgy Spring Outfits 2024, New York Spring Outfits 2024, Spring 2024 Street Style, Streetstyle Summer 2024, Street Style Spring 2024",
    "url": "/pin/3166662232602060/",
    "img": "https://i.pinimg.com/236x/9e/6d/47/9e6d4739f74bcf517a0efa29de166038.jpg"
  },
  {
    "title": "Spring Street Style 2024: A Canvas of Bold Trends and Classic Comfort Casual Sleek Outfit, Seville Street Style, Sassy Chic, Soft Dramatic Street Style, European Street Style 2024, Street Style 2024 Spring, 2024 Nyc Street Style, Nyc Street Style 2024, Smart Casual Aesthetic",
    "url": "/pin/85779567898113906/",
    "img": "https://i.pinimg.com/236x/72/5c/b6/725cb67f539e64f9f12a9bc84133a92b.jpg"
  }
]

classifier= FashionClassifier()
results = []
for i, d in enumerate(dset):
    image_url = d["img"]
    logger.info(f"Processing image {i+1}/{len(dset)}: {d['title']}")
    result = classifier.process_label_classification(image_url)
    results.append({
        "title": d["title"],
        "url": d["url"],
        "img": d["img"],
        "classification": result
    })
    time.sleep(1)  # Sleep to avoid rate limiting or overloading the API
for res in results:
    print(res)
with open("fashion_classification_results.json", "w") as f:
    json.dump(results, f, indent=2)