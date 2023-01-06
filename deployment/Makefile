current_dir := $(PWD)
botpackagedir := $(current_dir)/..


build-PTBFunction:
	echo $(current_dir)
	cp *.py $(ARTIFACTS_DIR)
	cp $(botpackagedir)/requirements.txt $(ARTIFACTS_DIR)
	python -m pip install -r $(botpackagedir)/requirements.txt -t $(ARTIFACTS_DIR)
	python -m pip install $(botpackagedir) -t $(ARTIFACTS_DIR)
	rm -rf $(ARTIFACTS_DIR)/bin