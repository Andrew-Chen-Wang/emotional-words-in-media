## Contributions to the Dataset

Hey! Thanks for taking a look at this repo. I'm always looking to improve this repo's 
code, visuals, and methodologies, so PRs are definitely welcome.

This repo is licensed under the Apache 2.0 license, and the dataset at Dolthub 
is licensed under CC0.

To maintain compatibility, please respect the interface when updating data in Dolthub 
using the src.extract class to do so.

### Setting up

1. `pip install -r requirements_dev.txt`
2. To run the tests, run `pytest ./tests`
3. Lint: `black main.py src/ tests/ && isort main.py src/ tests/ --lines-after-import 2 --profile black`
4. Happy hacking! Eh hem, the politically correct word: "developing."

### Grabbing the correct playlist

The correct playlist is a channel's "Uploads" playlist.

1. Go to your specified YouTube channel
2. Click "Videos"
3. Click "Play All"
4. A video should be playing now. Below the video, you should see the playlist. 
   Press the header saying "Uploads for CHANNEL X". You should be redirected to a 
   dedicated page that shows the videos in the playlist.
5. Grab the link of the playlist. The playlist link should have the format: 
   `https://www.youtube.com/playlist?list=UUij2pN-twyNdzdsx2MUJLYw`
