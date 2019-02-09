# Kindle-Highlights to PDF Synchronizer

This script aims at synchronizing highlights that you created for a **PDF** file on your Kindle Paperwhite (**7th generation** tested only!).

Other eBook formats than *PDF*, e.g. *EPUB*, are currently not supported!

## Requirements

You need to be in possession of the `My Clippings.txt` file, which is stored in the `Documents` directory of your eBook reader. This file contains text passages that you marked/highlighted on your reader.<br/>
The file will be parsed for blocks of the following format:

```txt
[BOOK TITLE (- AUTHORS)]
- [YOUR CLIPPING ON PAGE XXX-YYY] | [ADDED ON ...]

[HIGHTLIGHTED TEXT]
==========
```

In addition, you need a local copy of the PDF file that you highlighted on your reader.

Note that the language of the `- [YOUR CLIPPING ON PAGE XXX-YYY]` line does not matter. Also, only the `XXX` page number is parsed, as in my file the `XXX` and `YYY` never differed.

## Installation

This script used [PyMuPDF](https://github.com/rk700/PyMuPDF) which you have to install prior to executing the script.

## Usage

```bash
usage: kindle-pdf-highlighter.py [-h] --book BOOK --clippings CLIPPINGS
                                 --title TITLE [--outfile OUTFILE]

required arguments:
  --book "/path/to/book.pdf"                    Path to your PDF file
  --clippings "/path/to/MY Clippings.txt"       Path to your "My Clippings.txt" file
  --title "Example Booktitle - Famous Author"   Full book title line as found in the "My Clippings.txt"

optional arguments:
  -h, --help                                    show this help message and exit
  --outfile "/path/to/outfile.pdf"              (Optional) Path for the highlighted PDF file
```

As mentioned above, the script parses the file for blocks containing the book title.<br/>
Blocks for clippings from other ebooks are ignored.

**The provided paths must be absolute paths to the respective files. Paths stating with `~/`, `./` or `../` are currently not supported!**<br/>
Furthermore, the paths for `--book` and `--outfile` must differ.

### Example

You find the files used for this example in the `example` directory.

The `My Clippings.txt` contains the following blocks:

```text
Lorem Ipsum - manshanden
- Ihre Markierung auf Seite 1-1 | Hinzugefügt am Dienstag, 27. September 2016 02:49:21

sit amet consequat lorem
==========
```

For the example files, you may use the following command to execute the script:

```bash
./synchronizer.py \
    --book "/Users/rflume/Kindle-Highlights-to-PDF-Synchronizer/example/lorem-ipsum.pdf" \
    --clippings "/Users/rflume/Kindle-Highlights-to-PDF-Synchronizer/example/My Clippings.txt" \
    --title "Lorem Ipsum - manshanden" \
    --outfile "/Users/rflume/Kindle-Highlights-to-PDF-Synchronizer/example/lorem-ipsum-highlighted.pdf"
```

The output file will then be the *PDF* `example/lorem-ipsum-highlighted.pdf`.

## Contributions

Please feel free to optimize code, add functionality, supported ebook formats, etc.!
