FROM docker.io/ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_PRIORITY=high

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    wget \
    gnupg \
    ca-certificates \
    # UI Requirements
    xvfb \
    xdotool \
    scrot \
    sudo \
    x11vnc \
    autocutsel \
    # Input monitoring tools
    xinput \
    x11-utils \
    # DNS tools
    dnsutils \
    # Network tools
    net-tools \
    netcat-openbsd \
    iputils-ping \
    openvpn \
    proxychains \
    # Remote clients (tigervnc only - FreeRDP built from source below)
    tigervnc-viewer \
    # Smart card and security libraries
    libpcsclite1 \
    pcscd \
    # Kerberos support
    krb5-user \
    # Python
    python3 \
    python3-pip \
    python3-venv \
    tightvncserver \
    # Video recording
    ffmpeg \
    # Build dependencies for FreeRDP with ARM gateway support
    build-essential \
    cmake \
    ninja-build \
    git \
    libssl-dev \
    libx11-dev \
    libxext-dev \
    libxinerama-dev \
    libxcursor-dev \
    libxdamage-dev \
    libxv-dev \
    libxkbfile-dev \
    libxkbcommon-dev \
    libasound2-dev \
    libpulse-dev \
    libcups2-dev \
    libpcsclite-dev \
    libusb-1.0-0-dev \
    libudev-dev \
    libdbus-glib-1-dev \
    uuid-dev \
    libxml2-dev \
    libavutil-dev \
    libavcodec-dev \
    libswscale-dev \
    libswresample-dev \
    libcjson-dev \
    libsdl2-dev \
    libsdl2-ttf-dev \
    libfuse3-dev \
    libkrb5-dev \
    libpkcs11-helper1-dev \
    libwebkit2gtk-4.1-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/* /var/tmp/*

# Build FreeRDP from source with ARM gateway (Azure Virtual Desktop) support
RUN git clone --depth 1 --branch 3.10.3 https://github.com/FreeRDP/FreeRDP.git /tmp/FreeRDP && \
    cd /tmp/FreeRDP && \
    cmake -B build -G Ninja \
        -DCMAKE_BUILD_TYPE=Release \
        -DWITH_AAD=ON \
        -DWITH_CUPS=ON \
        -DWITH_PULSE=ON \
        -DWITH_CHANNELS=ON \
        -DWITH_CLIENT_CHANNELS=ON \
        -DWITH_SERVER_CHANNELS=OFF \
        -DWITH_PCSC=ON \
        -DWITH_FFMPEG=ON \
        -DWITH_SWSCALE=ON \
        -DWITH_DSP_FFMPEG=ON \
        -DWITH_JPEG=OFF \
        -DWITH_WEBVIEW=ON \
        -DWITH_CLIENT=ON \
        -DWITH_SERVER=OFF \
        -DCHANNEL_URBDRC=ON && \
    cmake --build build -j$(nproc) && \
    cmake --install build && \
    ldconfig && \
    rm -rf /tmp/FreeRDP

# Install noVNC (git is already installed from build dependencies)
RUN git clone --depth 1 --branch v1.5.0 https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone --depth 1 --branch v0.12.0 https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# Install Tailscale using official package repository
RUN curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/noble.noarmor.gpg | tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null && \
    curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/noble.tailscale-keyring.list | tee /etc/apt/sources.list.d/tailscale.list && \
    apt-get update && \
    apt-get install -y tailscale && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# setup user
ENV USERNAME=legacy-use
ENV HOME=/home/$USERNAME
RUN useradd -m -s /bin/bash -d $HOME $USERNAME && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    mkdir -p $HOME/.cache && \
    chown -R $USERNAME:$USERNAME $HOME/.cache
USER legacy-use
WORKDIR $HOME

# Detect architecture and download appropriate wireproxy binary
ARG TARGETARCH
ARG TARGETOS=linux
RUN case "$TARGETARCH" in \
        amd64) ARCH=amd64 ;; \
        arm64) ARCH=arm64 ;; \
        arm) ARCH=armv7 ;; \
        *) echo "Unsupported architecture: $TARGETARCH" && exit 1 ;; \
    esac && \
    curl -L -o /tmp/wireproxy.tar.gz "https://github.com/whyvl/wireproxy/releases/download/v1.0.9/wireproxy_${TARGETOS}_${ARCH}.tar.gz" && \
    tar -xzf /tmp/wireproxy.tar.gz -C /tmp && \
    sudo mv /tmp/wireproxy /usr/local/bin/wireproxy && \
    sudo chmod +x /usr/local/bin/wireproxy && \
    rm /tmp/wireproxy.tar.gz

# Copy SOCKS proxy server script
COPY infra/docker/legacy-use-target/image/socks_proxy.py /socks_proxy.py

# Copy requirements.txt and install dependencies
COPY --chown=$USERNAME:$USERNAME infra/docker/legacy-use-target/requirements.txt $HOME/
# Create virtual environment
RUN python3 -m venv .venv
RUN .venv/bin/pip3 install --no-cache-dir -r requirements.txt

# setup desktop env & app
COPY --chown=$USERNAME:$USERNAME infra/docker/legacy-use-target/image/proxychains.conf /etc/proxychains.conf
COPY --chown=$USERNAME:$USERNAME infra/docker/legacy-use-target/image/ $HOME

ARG HOST_IP=unknown
ARG HOST_PORT=unknown
ARG REMOTE_USERNAME=unknown
ARG REMOTE_PASSWORD=unknown
ARG REMOTE_CLIENT_TYPE=unknown
ARG REMOTE_VPN_TYPE=unknown
ARG VPN_CONFIG=unknown
ARG VPN_USERNAME=unknown
ARG VPN_PASSWORD=unknown
ARG DISPLAY_NUM=1
ARG HEIGHT=768
ARG WIDTH=1024

ENV DISPLAY_NUM=$DISPLAY_NUM
ENV HEIGHT=$HEIGHT
ENV WIDTH=$WIDTH
ENV VPN_CONFIG=$VPN_CONFIG
ENV VPN_USERNAME=$VPN_USERNAME
ENV VPN_PASSWORD=$VPN_PASSWORD
ENV REMOTE_PASSWORD=$REMOTE_PASSWORD
ENV REMOTE_USERNAME=$REMOTE_USERNAME
ENV REMOTE_CLIENT_TYPE=$REMOTE_CLIENT_TYPE
ENV REMOTE_VPN_TYPE=$REMOTE_VPN_TYPE
ENV HOST_PORT=$HOST_PORT
ENV HOST_IP=$HOST_IP

ENTRYPOINT [ "./entrypoint.sh" ]
