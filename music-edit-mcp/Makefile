.PHONY: setup licenses

setup:
	git config core.hooksPath .githooks

licenses:
	uv run pip-licenses \
	  --format=markdown \
	  --with-urls \
	  --with-authors \
	  --with-description \
	  --order=license \
	  | { printf '# Third-Party Notices\n\nThis project uses the following open-source software.\n\n'; cat; } \
	  > ../THIRD_PARTY_NOTICES.md
