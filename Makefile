DESTDIR =
PREFIX = /usr
EBOOKVIEWER_DIR = ${PREFIX}/share/easy-ebook-viewer
BINDIR = ${PREFIX}/bin
PYTHON = ${BINDIR}/python3
INSTALL_DIR = ${DESTDIR}${EBOOKVIEWER_DIR}

all: easy-ebook-viewer

easy-ebook-viewer:
	echo "#!/bin/sh" > easy-ebook-viewer
	echo "${PYTHON} ${EBOOKVIEWER_DIR}/main.py \"\$$@\"" >> easy-ebook-viewer
	chmod +x easy-ebook-viewer

install: install-bin install-desktop install-locale

install-bin: easy-ebook-viewer
	install -d ${DESTDIR}${BINDIR}
	install -d ${INSTALL_DIR}
	install -d ${INSTALL_DIR}/css
	install -d ${INSTALL_DIR}/workers
	install -d ${INSTALL_DIR}/components
	install -d ${INSTALL_DIR}/misc
	install -d ${INSTALL_DIR}/locale
	install easy-ebook-viewer ${DESTDIR}${BINDIR}
	install -m 644 css/night.css ${INSTALL_DIR}/css/night.css
	install -m 644 css/day.css ${INSTALL_DIR}/css/day.css
	install -m 644 src/main.py ${INSTALL_DIR}/main.py
	install -m 644 src/main_window.py ${INSTALL_DIR}/main_window.py
	install -m 644 src/components/__init__.py ${INSTALL_DIR}/components/__init__.py
	install -m 644 src/components/file_chooser.py ${INSTALL_DIR}/components/file_chooser.py
	install -m 644 src/components/header_bar.py ${INSTALL_DIR}/components/header_bar.py
	install -m 644 src/components/viewer.py ${INSTALL_DIR}/components/viewer.py
	install -m 644 src/components/about_dialog.py ${INSTALL_DIR}/components/about_dialog.py
	install -m 644 src/components/chapters_list.py ${INSTALL_DIR}/components/chapters_list.py
	install -m 644 src/components/preferences_dialog.py ${INSTALL_DIR}/components/preferences_dialog.py
	install -m 644 src/constants.py ${INSTALL_DIR}/constants.py
	install -m 644 src/workers/__init__.py ${INSTALL_DIR}/workers/__init__.py
	install -m 644 src/workers/config_provider.py ${INSTALL_DIR}/workers/config_provider.py
	install -m 644 src/workers/xml2obj.py ${INSTALL_DIR}/workers/xml2obj.py
	install -m 644 src/workers/content_provider.py ${INSTALL_DIR}/workers/content_provider.py
	install -m 644 misc/easy-ebook-viewer-scalable.svg ${INSTALL_DIR}/misc/easy-ebook-viewer-scalable.svg

install-locale:
	install -d ${INSTALL_DIR}/locale/pl
	install -d ${INSTALL_DIR}/locale/pl/LC_MESSAGES
	install -m 644 po/pl.mo ${INSTALL_DIR}/locale/pl/LC_MESSAGES/easy-ebook-viewer.mo
	install -d ${INSTALL_DIR}/locale/fr
	install -d ${INSTALL_DIR}/locale/fr/LC_MESSAGES
	install -m 644 po/fr.mo ${INSTALL_DIR}/locale/fr/LC_MESSAGES/easy-ebook-viewer.mo
	install -d ${INSTALL_DIR}/locale/es
	install -d ${INSTALL_DIR}/locale/es/LC_MESSAGES
	install -m 644 po/es.mo ${INSTALL_DIR}/locale/es/LC_MESSAGES/easy-ebook-viewer.mo

install-desktop:
	install -d ${DESTDIR}${PREFIX}/share/icons/hicolor/24x24/apps
	install -d ${DESTDIR}${PREFIX}/share/icons/hicolor/32x32/apps
	install -d ${DESTDIR}${PREFIX}/share/icons/hicolor/48x48/apps
	install -d ${DESTDIR}${PREFIX}/share/icons/hicolor/64x64/apps
	install -d ${DESTDIR}${PREFIX}/share/icons/hicolor/scalable/apps
	install -d ${DESTDIR}${PREFIX}/share/applications
	install -m 644 misc/easy-ebook-viewer-scalable.svg \
		${DESTDIR}${PREFIX}/share/icons/hicolor/scalable/apps/easy-ebook-viewer.svg
	install -m 644 misc/easy-ebook-viewer.desktop \
		${DESTDIR}${PREFIX}/share/applications/easy-ebook-viewer.desktop
	

clean:
	rm -f easy-ebook-viewer

uninstall: uninstall-bin uninstall-desktop

uninstall-bin:
	rm -rf ${EBOOKVIEWER_DIR}
	rm -rf ${BINDIR}/easy-ebook-viewer

uninstall-desktop:
	rm -f ${PREFIX}/share/applications/easy-ebook-viewer.desktop
	rm -f ${PREFIX}/share/icons/hicolor/*/apps/easy-ebook-viewer.png

.PHONY: all install install-bin install-desktop
