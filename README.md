# pinit

pinit is a project initializer.

## How to use it.

Well, how I'd use it is as follows:

```
git clone https://git.faulty.nl/faulty/pinit ~/.local/pinit
cd ~/.local/pinit
python tools/publish.py
export $PATH="$HOME/.local/pinit:$PATH"
```

It doesn't really matter where it's located as long as `./templates/` is located in the same directory as the executable.
