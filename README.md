# Words in Political Media

Amalgamation of data for knowing how many times Fox News (and of course everyone else 
i.e. news outlets and media) says "SLAMS" (and other aggressive words). The point is to
see if the words chosen affect the audience via view count and like:dislike ratio based
on the current subscriber count and average viewership.

---
### Usage

Uses Python 3.9. `pip install -r requirements.txt`. Run `python main.py`

---
### Contributing

To contribute, please take a look at CONTRIBUTING.md.

---
### FAQ

> Is the project complete?

No. I still need to actually download the JSON for these
channels and make visuals for them so people are interested.

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
