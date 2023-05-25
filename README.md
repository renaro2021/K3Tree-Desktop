# K3Tree - Desktop

K3Tree stands for "K" pronounced as "Kei", "3" as "San" and "Tree" translated as "Ki" in Japanese. When you mixed that together you get "KeiSanKi" which is a Japanese word for Calculator ;) 

This was made for a High School Project regarding Cross-Platform Programs using Python.

Feel free to fork.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```
Then run main.py (Run it twice as if you succeed on setting the passcode at first, the program will quit itself)
```bash
python3 main.py 
#Python3.10.10 or under must be used. Kivy seeems to not support Python3.11 yet.

```
## Features
* Supported Image Format: .jpeg .png .gif

* Supported Video Format: .mp4 .mov .avi

* Supports Japanese Text for Displaying Filenames (Doesn't Support Japanese UI)


## Notes
### Support
About this program having any added features, that won't be promised and likely not possible.

Security Bugs will be prioritzed. Other Bugs aren't promised in terms of fixing speed.

It will likely continue to be updated so that it will run on modern devices.
### Recovery
The files you saved on the vault aren't encrypted. You can just run the sub.py directly and RESET to have a new code then
run main.py to access or view it again using the program.

But a faster way would be to just go into the "mainfolder" folder which is on the same directory as sub.py and main
py and then extract all files and recover them.

As the program doesn't have a Share or Export function and only has an Import function,
this very guide should be treated as a way to Share or Export the files in the vault instead.
## License

[MIT](https://choosealicense.com/licenses/mit/)
