# Ebook-Viewer
Modern GTK Python app to easily read ePub files

Ebook Viewer is currently in early stages of development. It's a re-write of old ebook reader called [pPub.](https://github.com/sakisds/pPub)

Planned for first public release:
- [x] ePub opening & display
- [x] Basic chapter navigation
- [x] Restoring of reading position
- [ ] Importing from other ebook file formats
- [ ] Chapter jumping
- [ ] Chapter index based navigation
- [ ] Per book bookmarks
- [ ] Switching between light and dark style
- [ ] Text size control

Future plans:
- [ ] eBook font picker
- [ ] Content searching
- [ ] Pernament highliting
- [ ] Book metadata display
- [ ] Ability to edit book metadata

## Installing

**Requires**: gir1.2-webkit-3.0, gir1.2-gtk-3.0, python3-gi (PyGObject for Python 3)

Download or clone this repository then run in project directory:

```sudo make install```

Note the lack of configure step so make sure you have all dependencies.

## Screenshots

![Dark theme](https://i.imgur.com/sQNZ3vi.png)


