A basic scrapper to get all the projects that won a bounty with an organization and built at EthGlobal.

Currently it doesn't check for the projects that didn't win anything.

ethglobal website is a bit weird and there is no clear way to find who built on what.

so the basic idea is to look for an example project, company and the event. For this, i used LayerZero as an example.

from there, you inspect element on that project card and hover over LayerZero logo to find it's img src. The img src will contain this `/organizations/{identifier}/`. here the identifier is something like `dkzkp` for layerZero or `910t9` for Avail.

input this in user prompt along with city/name of the event and the scrapper should start looking at the website from page 1 to 100. you can customize this number too.

that's all.

To run:

start a python env: python3 -m venv {env name}

source venv/bin/activate

install necessary modules

run: python3 ethglobal-scrapper.py 
