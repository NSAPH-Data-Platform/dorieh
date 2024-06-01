# Building Docker Image
                               
The included Docker file builds a multi-architecture docker image for Dorieh. It includes support for 
R functions and FST file format. If you do not need FST and R support, comment out 
the installation of R in the Dockerfile and remove `[FST]` from requirements.txt.

To build docker image in this directory, run the following command:

    DOCKER_BUILDKIT=1 BUILDKIT_PROGRESS=plain docker buildx build --platform linux/arm64,linux/amd64 --no-cache --tag dorieh:latest .

To enable multiarchitecture build you might need to run the following commands first:

    docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
    docker buildx rm builder
    docker buildx create --name builder --driver docker-container --use
    docker buildx inspect --bootstrap

