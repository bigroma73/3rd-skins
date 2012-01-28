SUBDIRS = skins

metadir = $(datadir)/meta
meta_DATA = index-3rd-skins.xml
CLEANFILES = index-3rd-skins.xml

index-3rd-skins.xml: $(top_srcdir)/genmetaindex.py $(top_srcdir)/skins/*/meta/skin_*.xml
	$(AM_V_GEN)$(PYTHON) $^ > $@
