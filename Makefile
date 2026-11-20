IMAGE = shop-autotests
RUN = docker run --rm -v "$(CURDIR)/allure-results:/tests/allure-results" $(IMAGE)

# One command: build the image and run every test inside it.
test:
	docker build -q -t $(IMAGE) .
	$(RUN) pytest

smoke:
	docker build -q -t $(IMAGE) .
	$(RUN) pytest -m smoke

.PHONY: test smoke
