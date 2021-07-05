fc_release_url="https://github.com/firecracker-microvm/firecracker/releases"
fc_version=v0.24.4
fc_dir=release-${fc_version}
arch=`uname -m`
kernel_url="https://s3.amazonaws.com/spec.ccfc.min/img/quickstart_guide/x86_64/kernels/vmlinux.bin"
rootfs_url="https://s3.amazonaws.com/spec.ccfc.min/img/hello/fsfiles/hello-rootfs.ext4"

binaries = firecracker jailer

firecracker-release:
ifeq (,$(wildcard ./release-${fc_version}))
	curl -L ${fc_release_url}/download/${fc_version}/firecracker-${fc_version}-${arch}.tgz \
	| tar -xz
endif

$(binaries): firecracker-release
	@cp -u release-${fc_version}/$@-${fc_version}-$(arch) $@

kernel:
ifeq (,$(wildcard ./vmlinux.bin))
	curl -o vmlinux.bin -L ${kernel_url}
endif

rootfs:
ifeq (,$(wildcard ./hello-rootfs.ext4))
	curl -o hello-rootfs.ext4 -L ${rootfs_url}
endif

dev: $(binaries) kernel rootfs

start: dev clean-socket
	./firecracker --api-sock /tmp/firecracker.socket

.PHONY: clean $(binaries)

clean:
	-rm -r ${fc_dir} ${binaries}

clean-socket:
	@rm -f /tmp/firecracker.socket