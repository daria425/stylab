### Social Style Scan

an AI-powered fashion trend intelligence tool designed to help stylists, designers, marketers, and creative professionals keep up with emerging aesthetics without spending every waking hour on Pinterest or TikTok.

It uses multimodal AI models and social media scraping to automatically identify, summarize, and visualize fashion trends through structured insights and generative imagery.

---

## ✨ Features ✨

- **Visual Trend Detection**

  - Scrapes Pinterest boards and TikTok hashtags to collect real-world fashion imagery.
  - Uses FashionCLIP and GPT-Vision to classify each image into categories like:
    - Garment types
    - Fabrics
    - Silhouettes
    - Aesthetics
    - Styling details
    - Color palettes
    - Accessories

- **Trend Summarization Engine**

  - Automatically clusters and summarizes multiple image analyses into cohesive trend reports using GPT-4.

- **Garment Generation**

  - Uses Stability AI models (2D + 3D) to generate new garment concepts based on each trend profile.

- **Trend Cards (Planned)**
  - Will include:
    - Trend name (e.g., "Sheer Tailored Streetwear")
    - Adoption score
    - Lifecycle stage (Emerging / Growing / Peaking / Saturating)
    - Visual + keyword summary

---

## 🛠 Tech Stack

- **Backend**: Python, FastAPI (planned), Playwright (Pinterest scrape), Apify (TikTok)
- **AI Models**:
  - `patrickjohncyh/fashion-clip` for image classification
  - OpenAI GPT-4 Vision for summarization
  - Stability AI for image/3D garment generation
- **Database**: MongoDB (planned)
- **Deployment**: Docker (planned)

## Roadmap

- [x] Scrape and classify Pinterest fashion imagery
- [x] Summarize trends using GPT
- [x] Generate images based on trend profiles
- [ ] TikTok hashtag integration (search volume + example videos)
- [ ] 3D Image generation
- [ ] Trend card dashboard UI (with lifecycle model)
- [ ] Dynamic trend card editing
- [ ] Export trends/data to Notion / Airtable / PDF
