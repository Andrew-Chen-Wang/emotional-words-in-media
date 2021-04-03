# Words in Political Media

Amalgamation of data for knowing how many times Fox News (and of course everyone else 
i.e. news outlets and media) says "SLAMS" (and other aggressive words). The point is to
see if the words chosen affect the audience via view count and like:dislike ratio based
on view count and average viewership for that channel.

---
### Usage

Uses Python 3.9. `pip install -r requirements.txt`.
Run `python main.py --save-as-json`

If you'd like to integrate with Dolt instead, you need to set up
a dolt database which is possible with 
`dolt clone andrew-chen-wang/words-in-political-media`. You can also
simply create an empty dolt database by doing `dolt init`.

Finally, run `python main.py --save-in-dolt`. You can save it as JSON
at the same time with `python main.py --save-in-dolt --save-as-json`.

---
### Contributing

To contribute, please take a look at [CONTRIBUTING.md](https://github.com/Andrew-Chen-Wang/words-in-political-media/blob/main/CONTRIBUTING.md).

---
### FAQ

> Why only these channels?

There's more to come! But the main focus was mainstream media outlets.
Then we can get more like TheYoungTurks or Ben Shapiro show or Vox or Vice
or Buzzfeed News. Like there is plenty of competition in this field, and
those are just the ones I'm aware of. But the main point was to look at
the ones that have been around for decades.

I added The Hill, even though it is not as popular as the Initial (CNN,
ABC, NBC, Fox, MSNBC), as a balancing force in the 2D political balance
beam. Though as of 2 April 2021, I'm unsure if it'll be in the final
visuals/graphs. If anything, I'm only speaking of the database itself
and not the final outcome (for logging purposes).

There's also international ones like the BBC or CBC (I think) or Sky
News Australia which intriguingly talks a lot about America for being
Australian... anyways. Those can be included when I don't want to have
a VPN turned on and 13 GB of memory out of my 16 used up. Additionally,
I'll probably have space on my RPi 3 to download some more, so let
me know in the GitHub or Dolthub repositories and I'll download it!
Those currently aren't included simply because this project is American
focused. If I were to include international media, where standards and
even the cultures (e.g. the American v.s. British) are different, I feel
there would be too much bias in the final calculations.

> Why did you make this?

I've had this idea for a while, but I never got around to doing it. I created 
[Velnota](https://velnota.com/) to talk about stuff like average Joe's. But 2014-2021
has been pretty messy, and the news is no exception. The talk about fake news,
Fox having a monopoly stake in conservative media, etc. is something I found pretty
interesting.

So this project is just a bit of transparency on corporate media :)

> Why Dolt?

I thought it was an interesting product. Also, as I was creating
the models to store all the data on Dolthub, I realized I didn't
need a `last_updated` attribute for something like "Video.view_count"
which isn't constant and would be updated from time to time.

Ok but if I'm being honest, I just wanted a place to store my data.
Additionally, they didn't have JSON types yet for their database; otherwise,
I would've made some `extra` JSON type attribute for transferring sake.

> Why are some videos missing? Why not a perfectly 20,000 video set per channel?

Initially, all Uploads playlists have 20,000 ish-but-max videos. There are some
privatized videos too. Other times, my internet just dropped, and I honestly couldn't
bother trying to get the lost 20 videos.

> What did you learn from this?

I'm never using SQLAlchemy again. The downloading portion is just way too unstable
for me. Either I'm doing something wrong, because I keep getting an "ObjectDeletedError"
for a missing channel that's obviously not missing because it was just created and
saved... or uh I'm blaming Dolt or SQLAlchemy... Idek anymore.

The SQLAlchemy Python file (i.e. src/extract.py) might just be broken.
I would highly recommend saving as json (which will happen before saving
to Dolt) in addition to saving to Dolt because I have no idea when, where,
and why Dolt fails sometimes. The JSON files are about 4GB large for a channel
with ~20,000 videos. If Dolt does fail, then in src/extract.py, there's 
a helper method in `SaveItDolt` where you can save to Dolt via a JSON file
given a string path.

---
### License and Credit

[The code is on GitHub](https://github.com/Andrew-Chen-Wang/words-in-political-media),
and it's licensed under Apache 2.0 and can be found at the file `LICENSE`.
The database itself is hosted on
[Dolthub](https://www.dolthub.com/repositories/andrew-chen-wang/words-in-political-media)
which has the license CC0, which can be found at `LICENSE.md` and boilerplate:

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png)](http://creativecommons.org/publicdomain/zero/1.0/)   
To the extent possible under law, 
[Andrew Chen Wang](https://github.com/Andrew-Chen-Wang/words-in-political-media/) 
has waived all copyright and related or neighboring rights to Database of YouTube 
video titles by media/news outlets. This work is published from: United States.

By: Andrew Chen Wang

Date: March 4, 2021

I've had this idea for a while, but I never got around to doing it.
So here goes nothing...

Credit goes to ProtonVPN and the Proton Team. Without their
VPN, and no this isn't sponsored, I would totally get throttled by YouTube
and never be able to experience it again in the name of science.
(man I love such cliche quotes)... And without the YouTube-DL team, 
this project would not be possible. Thank you all and sponsor them please!
