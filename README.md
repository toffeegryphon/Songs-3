# Songs-3 (BE)
Find songs by artist name. Using Python/FastAPI

## Development
```
create venv and install from requirements.txt
uvicorn src.main:app --reload
```

## Rationale
I had this idea before I discovered Last.FM's get songs by artist feature (`existing`).
Compared to `existing`, benefits include:
- Single click search (like Google), and 
- A more readable format compared to `existing`'s desktop version (but probably not mobile version).  

However, the cons are many:
- No sorting (yet)
- No listening (unlikely to implement)

Basically, no bells and whistles. However, I am considering adding features like:
- User ratings
- If you like..., you will like...
- Hyperlink to audio

## Thoughts
This is the third iteration. In previous ones, I was too caught up with "speed"; 
I was trying to push features and make it ready as quickly as possible. 
This 'proof-of-concept' mentality made the code really dirty, and made it very hard to sustain interest. 
After my internship, I realised (as in, I drilled in this notion) that development is way more than coding. 
Ultimately, this is a practice in enforcing good TDD practices, good code structure and documentation, 
and a shift in mentality towards a 'product-development' one.

 Much thanks to [Adam's Markdown-Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
