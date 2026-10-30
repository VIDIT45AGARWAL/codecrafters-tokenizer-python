This is a starting point for Python solutions to the
["Build Your Own Tokenizer" Challenge](https://codecrafters.io/challenges/tokenizer).

In this challenge, you'll build a byte-pair encoding tokenizer that's capable of
training a vocabulary, encoding text, and decoding token IDs. Along the way
you'll learn about byte-level BPE, pretokenization, and GPT-2's encoding.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

# Passing the first stage

The entry point for your tokenizer is in `app/main.py`. Study and uncomment the
relevant code, and then run the command below to execute the tests on our
servers:

```sh
codecrafters submit
```

That's all!

# Stage 2 & beyond

Note: This section is for stages 2 and beyond.

1. Ensure you have `uv` installed locally
1. Run `./your_program.sh` to run your tokenizer, which is implemented in
   `app/main.py`.
1. Run `codecrafters submit` to submit your solution to CodeCrafters. Test
   output will be streamed to your terminal.

# Testing locally

The `your_program.sh` script reads the files you pass on the command line. For
example:

```sh
mkdir -p /tmp/testing && cd /tmp/testing
printf 'hi' > text.txt
/path/to/your/repo/your_program.sh bytes text.txt
```

To make this easier to type out, you could add a
[shell alias](https://shapeshed.com/unix-alias/):

```sh
alias mytokenizer=/path/to/your/repo/your_program.sh

mkdir -p /tmp/testing && cd /tmp/testing
printf 'hi' > text.txt
mytokenizer bytes text.txt
```
