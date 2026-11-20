IMAGE = shop-autotests

# One command: build the image and run every test inside it.
test:
	docker build -q -t $(IMAGE) .
	docker run --rm -v "$(CURDIR)/allure-results:/tests/allure-results" $(IMAGE) pytest

smoke:
	docker build -q -t $(IMAGE) .
	docker run --rm $(IMAGE) pytest -m smoke

report:
	allure serve allure-results

.PHONY: test smoke report
