FROM debian@sha256:a717a33469731894e77e912ea7d714e27c2dc38ee6554fd1a3102e92999cfc66
ENV DEBIAN_FRONTEND=noninteractive
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "--no-install-recommends", "openssl", "tpm2-openssl=1.3.0-1", "tpm2-tools=5.7-1", "tpm2-abrmd=3.0.0-1.2", "libtss2-tcti-tabrmd0=3.0.0-1.2", "dbus-daemon=1.16.2-2"]
RUN ["openssl", "version"]
RUN ["dpkg-query", "-W", "openssl", "tpm2-openssl", "tpm2-tools", "tpm2-abrmd", "libtss2-tcti-tabrmd0", "dbus-daemon"]
CMD ["tpm2_getcap", "-T", "device:/dev/tpmrm0", "properties-fixed"]
