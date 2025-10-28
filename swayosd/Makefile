NAME := swayosd
GITNAME := SwayOSD
VERSION := 0.2.1

.PHONY: all vendor clean

all: vendor clean

vendor:
	# Download source if not present
	[ -f $(GITNAME)-$(VERSION).tar.gz ] || \
		curl -L -o $(GITNAME)-$(VERSION).tar.gz \
		https://github.com/ErikReider/SwayOSD/archive/v$(VERSION)/$(GITNAME)-$(VERSION).tar.gz

	# Extract, vendor dependencies, and create vendor tarball
	tar xf $(GITNAME)-$(VERSION).tar.gz && \
	pushd $(GITNAME)-$(VERSION) && \
	cargo vendor && \
	tar Jcvf ../$(NAME)-$(VERSION)-vendor.tar.xz vendor/ && \
	popd

clean:
	rm -rf $(GITNAME)-$(VERSION)
