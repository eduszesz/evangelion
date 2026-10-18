PREFIX ?= /app

install:
	install -d $(DESTDIR)$(PREFIX)/share/evangelion
	install -m 644 evangelion.py $(DESTDIR)$(PREFIX)/share/evangelion/
	install -m 644 tema_*.mp3 $(DESTDIR)$(PREFIX)/share/evangelion/
	install -m 644 icon-at.png $(DESTDIR)$(PREFIX)/share/evangelion/
	install -m 644 dejavu-sans-mono.bold.ttf $(DESTDIR)$(PREFIX)/share/evangelion/
	install -Dm 755 evangelion-run $(DESTDIR)$(PREFIX)/bin/evangelion-run
	install -Dm 644 io.github.eduszesz.Evangelion.desktop $(DESTDIR)$(PREFIX)/share/applications/io.github.eduszesz.Evangelion.desktop
	install -Dm 644 icon-at.png $(DESTDIR)$(PREFIX)/share/icons/hicolor/256x256/apps/io.github.eduszesz.Evangelion.png
	install -Dm 644 io.github.eduszesz.Evangelion.metainfo.xml $(DESTDIR)$(PREFIX)/share/metainfo/io.github.eduszesz.Evangelion.metainfo.xml
