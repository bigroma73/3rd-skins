SUBDIRS = skins

metadir = $(datadir)/meta
meta_DATA = index-domica-skins.xml
CLEANFILES = index-domica-skins.xml

index-domica-skins.xml: $(top_srcdir)/genmetaindex.py $(top_srcdir)/skins/*/meta/skin_*.xml
	$(AM_V_GEN)$(PYTHON) $^ > $@
