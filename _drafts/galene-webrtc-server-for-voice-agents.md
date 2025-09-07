
Galene is a lightweight WebRTC server written in go, using the Pion impl. of WebRTC
supports voice and video
runs on linux amd64, arm64, mips, macos and windows
used in prod at Université de Paris and Sorbonne Université
simple admin ui
simple rest api for managing groups and users (repurpose to 1-1 agent-user sessions)
sample python auth server (and LDAP integration)
buit-in turn server
js client (for a/v videoconf)
android client (audio only, with screensharing support)
resource req. for 1-many (linear, 300 participants per core), many-to-many (quadratic)
interesting: how many for 1-1? (assume closer to linear, limiting factor: bandwidth?

https://github.com/jech/galene
https://galene.org

awesome-webrtc:
see also https://github.com/nuzulul/awesome-webrtc

https://github.com/meetecho/janus-gateway
https://janus.conf.meetecho.com/demos/echotest.html