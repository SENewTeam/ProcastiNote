# Researcher's Hive

Researcher's Hive is a research tool designed to help PhD students and researchers manage and organize their research knowledge. It provides efficient search, storage, visualization, commenting, and recommendation features to enhance the research workflow.

## Features
- Efficient Paper Search Quickly find relevant research papers based on topics of interest.
- Organized Research Knowledge Profile page organizes papers and notes based on recent activity.
- Graphical Visualization Visualize connections between research papers through authors and citations.
- Enhanced Notes and Annotations Add images, tables, and text-based comments to your research notes.
- Research Discoveries Get real-time alerts for similar research papers.
- AI-Enhanced Commenting Use AI to enhance the quality of comments.

## Tech Stack
- UI Design Figma
- Frontend ReactJS
- Backend Django
- Database MongoDB (for storing research papers and notes)
- Third-Party Tools
  - Semantic Scholar for gaining paper information
  - GooglePalm for AI integration in the comment section

## Setup Instructions

### Frontend
1. Navigate to the frontend directory
    bash
    cd frontend
    
2. Install dependencies
    bash
    npm i --force
    
3. Run the development server
    bash
    npm run dev
    
4. Open [localhost5173](httplocalhost5173) in the browser.

### Backend
1. Navigate to the backend directory
    bash
    cd backend
    
2. Install required Python packages
    bash
    pip install -r requirements.txt
    
3. Setup the PaLM API key in .env as per the .env.example file.
4. Apply database migrations
    bash
    python3 manage.py migrate
    
5. Run the backend server
    bash
    python3 manage.py runserver
    