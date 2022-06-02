# [Use containers to Build, Share and Run your applications](https://www.docker.com/resources/what-container)

## Package Software into Standardized Units for Development, Shipment and Deployment

A container is a standard unit of software that packages up code and all its dependencies. 

Docker creates simple tooling and a universal packaging approach that bundles up all application dependencies inside a container which is then run on Docker Engine. 

- code
- runtime
- System tools
- system libraries
- Settings

Container images become containers at runtime.

- cross-platform
- Isolated
- standard
- lightweight
- secure

## Comparing Containers and Virtual Machines

containers virtualize the **operating system instead of hardware**.

- portable
- efficient
- Lightweight

## Container Standards and Industry Leadership

the container image specification and runtime code now known as [**runc**](https://github.com/opencontainers/runc)

[**containerd**](https://containerd.io/) is an industry-standard container runtime that leverages runc and was created with an emphasis on simplicity, robustness and portability.

**Docker now use containerd as their contianer runtime.**