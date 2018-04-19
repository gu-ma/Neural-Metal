// Web scraper extension for Chrome: 'Create new Sitemap' / 'import Sitemap'
// copy and paste the content below

{
  "_id": "midimelody_ru",
  "startUrl": "http://en.midimelody.ru/",
  "selectors": [
  {
    "id": "Alphabet",
    "type": "SelectorLink",
    "selector": "div.span-5.last a",
    "parentSelectors": ["_root"],
    "multiple": true,
    "delay": ""
  },
  {
    "id": "Artist",
    "type": "SelectorLink",
    "selector": "div.post:nth-of-type(n+2) a",
    "parentSelectors": ["Alphabet", "Pagination"],
    "multiple": true,
    "delay": ""
  },
  {
    "id": "Pagination",
    "type": "SelectorLink",
    "selector": "a.page-numbers",
    "parentSelectors": ["Alphabet", "Pagination"],
    "multiple": true,
    "delay": ""
  },
  {
    "id": "Midi_Files",
    "type": "SelectorLink",
    "selector": "span a",
    "parentSelectors": ["Artist"],
    "multiple": true,
    "delay": ""
  }]
}