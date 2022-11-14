# gpglabs-notebook

This directory contains the files to build a docker-container for use with the
rest of the gpglabs repository. It basically follows the
[jupyter/docker-stacks](https://github.com/jupyter/docker-stacks) format, but
uses a conda lockfile as described by Phil Austin, see e.g. [this
post](https://pythonspeed.com/articles/conda-dependency-management/).

## Rebuilding the lockfile

You'll need a conda environment with
[conda-lock](https://github.com/conda-incubator/conda-lock) and
[mamba](https://anaconda.org/conda-forge/mamba). An `environment-dev.yml` file
with these dependencies is included, you can create it with
```bash
$ conda env create -f environment-build.yml
$ conda activate e350-build
```

To build the lockfile, create your
[environment.yml](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
as normal, then run it through `conda-lock`, telling it which architecture you
want to build for
```bash
$ conda-lock --mamba -k explicit --file environment.yml -p linux-64
```

## Rebuilding the image

The rest of the build is handled by docker. You can either build it manually or
use the `Makefile` provided in the root of the repository. The makefile will tag
the images with your git commit hash ready for Dockerhub etc.
```bash
$ cd ..
$ make build-all
```

The build is _fairly_ reproducible, but there are a handful of packages which
aren't available in `conda` which will be installed via pip (and hence not
version locked).
