# Building Docker Image
                               
The included Docker file builds a multi-architecture docker image for Dorieh. It includes support for 
R functions and FST file format. If you do not need FST and R support, comment out 
the installation of R in the Dockerfile and remove `[FST]` from requirements.txt.

To build docker images in this directory, run the following commands, replacing $(version) with the current version:

    DOCKER_BUILDKIT=1 BUILDKIT_PROGRESS=plain docker buildx build --platform linux/amd64 --no-cache --tag forome/dorieh:amd64 --load -f Dockerfile.amd64 . && docker push forome/dorieh:amd64
    DOCKER_BUILDKIT=1 BUILDKIT_PROGRESS=plain docker buildx build --platform linux/arm64 --no-cache --tag forome/dorieh:arm64 --load -f Dockerfile.arm64 . && docker push forome/dorieh:arm64
    docker manifest create forome/dorieh:latest --amend forome/dorieh:arm64 --amend forome/dorieh:amd64 && docker manifest push forome/dorieh:latest
    docker tag forome/dorieh:latest forome/dorieh:$(version)
    docker push forome/dorieh:$(version)

To enable multiarchitecture build you might need to run the following commands first:

    docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
    docker buildx rm builder
    docker buildx create --name builder --driver docker-container --use
    docker buildx inspect --bootstrap

