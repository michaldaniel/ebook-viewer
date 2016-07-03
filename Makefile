PREFIX = /usr
EBOOKVIEWER_DIR = ${PREFIX}/share/ebook-viewer
BINDIR = ${PREFIX}/bin
PYTHON = ${BINDIR}/python3

all: ebook-viewer

ebook-viewer:

	echo "#!/bin/sh" > ebook-viewer
	echo "${PYTHON} ${EBOOKVIEWER_DIR}/main.py \"\$$@\"" >> ebook-viewer

install: install-bin install-desktop

install-bin: ebook-viewer
	install -d ${BINDIR}
	install -d ${EBOOKVIEWER_DIR}
	install -d ${EBOOKVIEWER_DIR}/css
	install -d ${EBOOKVIEWER_DIR}/workers
	install -d ${EBOOKVIEWER_DIR}/components
	install ebook-viewer ${BINDIR}
	install -m 644 css/night.css ${EBOOKVIEWER_DIR}/css/night.css
	install -m 644 css/day.css ${EBOOKVIEWER_DIR}/css/day.css
	install -m 644 src/main.py ${EBOOKVIEWER_DIR}/main.py
	install -m 644 src/main_window.py ${EBOOKVIEWER_DIR}/main_window.py
	install -m 644 src/components/__init__.py ${EBOOKVIEWER_DIR}/components/__init__.py
	install -m 644 src/components/file_chooser.py ${EBOOKVIEWER_DIR}/components/file_chooser.py
	install -m 644 src/components/header_bar.py ${EBOOKVIEWER_DIR}/components/header_bar.py
	install -m 644 src/components/viewer.py ${EBOOKVIEWER_DIR}/components/viewer.py
	install -m 644 src/workers/__init__.py ${EBOOKVIEWER_DIR}/workers/__init__.py
	install -m 644 src/workers/config_provider.py ${EBOOKVIEWER_DIR}/workers/config_provider.py
	install -m 644 src/workers/xml2obj.py ${EBOOKVIEWER_DIR}/workers/xml2obj.py
	install -m 644 src/workers/content_provider.py ${EBOOKVIEWER_DIR}/workers/content_provider.py


install-desktop:
	install -d ${PREFIX}/share/icons/hicolor/24x24/apps
	install -d ${PREFIX}/share/icons/hicolor/32x32/apps
	install -d ${PREFIX}/share/icons/hicolor/48x48/apps
	install -d ${PREFIX}/share/icons/hicolor/64x64/apps
	install -d ${PREFIX}/share/icons/hicolor/scalable/apps
	install -d ${PREFIX}/share/applications
	install -m 644 misc/ebook-viewer-24.png \
		${PREFIX}/share/icons/hicolor/24x24/apps/ebook-viewer.png
	install -m 644 misc/ebook-viewer-32.png \
		${PREFIX}/share/icons/hicolor/32x32/apps/ebook-viewer.png
	install -m 644 misc/ebook-viewer-48.png \
		${PREFIX}/share/icons/hicolor/48x48/apps/ebook-viewer.png
	install -m 644 misc/ebook-viewer-64.png \
		${PREFIX}/share/icons/hicolor/64x64/apps/ebook-viewer.png
	install -m 644 misc/ebook-viewer-scalable.svg \
		${PREFIX}/share/icons/hicolor/scalable/apps/ebook-viewer.svg
	install -m 644 misc/ebook-viewer.desktop \
		${PREFIX}/share/applications/ebook-viewer.desktop
	gtk-update-icon-cache -f ${PREFIX}/share/icons/hicolor/

clean:
	rm -f ebook-viewer

uninstall: uninstall-bin uninstall-desktop

uninstall-bin:
	rm -rf ${EBOOKVIEWER_DIR}
	rm -rf ${BINDIR}/ebook-viewer

uninstall-desktop:
	rm -f ${PREFIX}/share/applications/ebook-viewer.desktop
	rm -f ${PREFIX}/share/icons/hicolor/*/apps/ebook-viewer.png

.PHONY: all install install-bin install-desktop
