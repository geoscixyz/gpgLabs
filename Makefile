.PHONY: tests clean

# Use bash for inline if-statements in arch_patch target
SHELL:=bash
ARCH:=$(shell uname -m)
OWNER?=geoscixyz

# Get the current git commit hash
COMMIT := $$(git log -1 --pretty=%h)

# Need to list the images in build dependency order
# All of the images
ALL_IMAGES:= \
        gpglabs-notebook

# Enable BuildKit for Docker build
export DOCKER_BUILDKIT:=1

# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@echo "gpgscixyz/glgLabs-notebook"
	@echo "====================="
	@echo "Replace % with a stack directory name (e.g., make build/ggLabs-notebook)"
	@echo
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
build/%: DOCKER_BUILD_ARGS?=
build/%: ## build the latest image for a stack using the system's architecture
	@echo "::group::Build $(OWNER)/$(notdir $@) (system's architecture)"
	docker build $(DOCKER_BUILD_ARGS) --rm --force-rm -t $(OWNER)/$(notdir $@):latest ./$(notdir $@) --build-arg OWNER=$(OWNER)
	docker tag $(OWNER)/$(notdir $@):latest $(OWNER)/$(notdir $@):$(COMMIT)
	@echo -n "Built image size: "
	@docker images $(OWNER)/$(notdir $@):latest --format "{{.Size}}"
	@echo "::endgroup::"
build-all: $(foreach I, $(ALL_IMAGES), build/$(I)) ## build all stacks

cont-clean-all: cont-stop-all cont-rm-all ## clean all containers (stop + rm)
cont-stop-all: ## stop all containers
	@echo "Stopping all containers ..."
	-docker stop -t0 $(shell docker ps -a -q) 2> /dev/null
cont-rm-all: ## remove all containers
	@echo "Removing all containers ..."
	-docker rm --force $(shell docker ps -a -q) 2> /dev/null

hook/%: ## run post-build hooks for an image
	python3 -m tagging.tag_image --short-image-name "$(notdir $@)" --owner "$(OWNER)" && \
	python3 -m tagging.write_manifest --short-image-name "$(notdir $@)" --hist-line-dir /tmp/hist_lines/ --manifest-dir /tmp/manifests/ --owner "$(OWNER)"
hook-all: $(foreach I, $(ALL_IMAGES), hook/$(I)) ## run post-build hooks for all images

img-clean: img-rm-dang img-rm ## clean dangling and jupyter images
img-list: ## list jupyter images
	@echo "Listing $(OWNER) images ..."
	docker images "$(OWNER)/*"
img-rm: ## remove jupyter images
	@echo "Removing $(OWNER) images ..."
	-docker rmi --force $(shell docker images --quiet "$(OWNER)/*") 2> /dev/null
img-rm-dang: ## remove dangling images (tagged None)
	@echo "Removing dangling images ..."
	-docker rmi --force $(shell docker images -f "dangling=true" -q) 2> /dev/null



pre-commit-all: ## run pre-commit hook on all files
	@pre-commit run --all-files --hook-stage manual
pre-commit-install: ## set up the git hook scripts
	@pre-commit --version
	@pre-commit install



pull/%: ## pull a jupyter image
	docker pull $(OWNER)/$(notdir $@)
pull-all: $(foreach I, $(ALL_IMAGES), pull/$(I)) ## pull all images

push/%: ## push all tags for a jupyter image
	@echo "::group::Push $(OWNER)/$(notdir $@) (system's architecture)"
	docker push --all-tags $(OWNER)/$(notdir $@)
	@echo "::endgroup::"
push-all: $(foreach I, $(ALL_IMAGES), push/$(I)) ## push all tagged images



run-shell/%: ## run a bash in interactive mode in a stack
	docker run -it --rm $(OWNER)/$(notdir $@) $(SHELL)

run-sudo-shell/%: ## run a bash in interactive mode as root in a stack
	docker run -it --rm --user root $(OWNER)/$(notdir $@) $(SHELL)

tests:
	nosetests --logging-level=INFO

clean:
	find . -name "*.pyc" | xargs -I {} rm -v "{}"
	fine . -name "*.ipynb_checkpoints" | xargs -I {} rm -v "{}"
