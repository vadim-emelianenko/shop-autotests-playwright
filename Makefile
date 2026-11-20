IMAGE = shop-autotests
RUN = docker run --rm --user "$(shell id -u):$(shell id -g)" -e HOME=/tmp \
	-v "$(CURDIR)/allure-results:/tests/allure-results" \
	-v "$(CURDIR)/test-results:/tests/test-results" $(IMAGE)

# One command: build the image and run every test inside it.
test:
	mkdir -p allure-results test-results
	docker build -q -t $(IMAGE) .
	$(RUN) pytest

smoke:
	mkdir -p allure-results test-results
	docker build -q -t $(IMAGE) .
	$(RUN) pytest -m smoke

.PHONY: test smoke
