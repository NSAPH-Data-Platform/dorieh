# Building Docker Image

Provided are two Dockerfiles:

* For general purpose usage in a non-secure environment. Has been tested for Intel/AMD64 and ARM platform 
  used by AWS Graviton family of virtual machines and newer Macs: [Dockerfile](Dockerfile)
* For Amazon Linux (AMD64 only) intended for use in secure and regulated data environments. This is a stripped 
   container without any of the optional dependencies, optimized for addressing any potential CVEs: 
   [Dockerfile.amzn](Dockerfile.amzn)

To build a container for a specific platform (tested on ARM64 and AMD64) run the following commands in this 
($repositoryRoot/docker) directory:

```shell
export dorieh_version=$(grep -E "version *= *[\"']" ../setup.py | head -1 | sed -E "s/.*version *= *[\"']([^\"']+)[\"'].*/\1/")
export arch=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
DOCKER_BUILDKIT=1 BUILDKIT_PROGRESS=plain docker buildx build --platform linux/${arch} --no-cache --tag forome/dorieh:${arch}-${dorieh_version} --load -f Dockerfile . &&\
    docker push forome/dorieh:${arch}-${dorieh_version}
```

To create a multiarch container, run the following commands:

```shell
docker pull forome/dorieh:amd64-${dorieh_version}
docker pull forome/dorieh:arm64-${dorieh_version}

docker manifest create forome/dorieh:${dorieh_version} --amend forome/dorieh:amd64-${dorieh_version} --amend forome/dorieh:arm64-${dorieh_version}
docker manifest annotate forome/dorieh:${dorieh_version}  forome/dorieh:amd64-${dorieh_version} --arch amd64
docker manifest annotate forome/dorieh:${dorieh_version}  forome/dorieh:arm64-${dorieh_version} --arch arm64
docker manifest push forome/dorieh:${dorieh_version}

# Optionally
docker manifest create forome/dorieh:latest --amend forome/dorieh:amd64-${dorieh_version} --amend forome/dorieh:arm64-${dorieh_version}
docker manifest annotate forome/dorieh:latest  forome/dorieh:amd64-${dorieh_version} --arch amd64
docker manifest annotate forome/dorieh:latest  forome/dorieh:arm64-${dorieh_version} --arch arm64
docker manifest push forome/dorieh:latest
```



