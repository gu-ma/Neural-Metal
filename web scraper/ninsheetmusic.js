// Web scraper extension for Chrome: 'Create new Sitemap' / 'import Sitemap'
// copy and paste the content below

{
  "_id": "ninsheet",
  "startUrl": "http://www.ninsheetmusic.org/browse/series",
  "selectors": [
  {
    "id": "series",
    "type": "SelectorLink",
    "selector": "td#sidebarleft a",
    "parentSelectors": ["_root"],
    "multiple": true,
    "delay": ""
  },
  {
    "id": "song",
    "type": "SelectorElement",
    "selector": "td.content tr:nth-of-type(n+2)",
    "parentSelectors": ["series"],
    "multiple": true,
    "delay": ""
  },
  {
    "id": "title",
    "type": "SelectorText",
    "selector": "td:nth-of-type(1)",
    "parentSelectors": ["song"],
    "multiple": false,
    "regex": "",
    "delay": ""
  },
  {
    "id": "mid",
    "type": "SelectorLink",
    "selector": "td:nth-of-type(6) a",
    "parentSelectors": ["song"],
    "multiple": false,
    "delay": ""
  }]
}