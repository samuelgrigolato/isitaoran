# Is it 'a' or 'an'?

Give me a word, and I'll tell you if it's a or an before it.

Usage:

```
$ ./aoran university
Hey, I need to download a copy of CMUdict (~3.5mb), can I? (Y/n)
Downloading...
Downloaded! Thanks for waiting.
a university
$ ./aoran UMBRELLA
an umbrella
$ ./aoran dfgertwesdf
Sorry, I couldn't find this word :(
```

## Wait, What?

English grammar has a special rule for when to use [a or an](https://www.grammar.com/a-an) before a word, based on the first sound of it. This may confuse people using English as a second language (like myself).

This tool uses [CMUdict](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) in order to solve this issue. Give it a word and it will lookup the first sound of it and tell you if it's a vowel sound or not.

## Ok, How Can I use This?

It's really easy. Just clone the repo and start calling it like the examples.

The auxiliary shell script assumes `python3` exists on your system. If not, you can call the python file directly, example:

```shell
$ python aoran.py table
a table
```
