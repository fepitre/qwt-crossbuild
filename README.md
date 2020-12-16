# qwt-crossbuild (FOR TESTING/DEV. PURPOSES ONLY)
Qubes Windows Tools crossbuild environment based on mingw, wine and docker

In comparison with the original ITL's Qubes Tools qwt-crossbuild contains several in-progress improvements:

- [ ] source files signature verification (including winetricks tool and downloads)
- [x] rebuild QWT utils (mingw, x86, x86\_64)
- [x] include updated xen pv drivers (8.2.2)
- [x] avoid high cpu consumption (move qga CreateEvent outside an event processing loop)
- [x] fix dhcp dependencies (winhttproxy wants to stay alive)
- [x] hide command prompt windows during setup execution (WixQuiteExec)
- [x] sign and install drivers without prompt (libwdi-based pkihelper utility)
- [x] remove format dialog (diskpart instead of prepare-volume)
- [ ] troubleshoot bsod errors (0x101, 0xc5, 0x50)
- [x] prepare reproducible/deterministic build (binaries only)
- [x] support Qubes-r4.1 (qrexec v2 backward compatibility)

## Build QWT

```shell_session
$ git clone https://github.com/QubesOS/qubes-builder
$ cd qubes-builder
$ ln -s example-configs/qubes-os-master.conf builder.conf
$ make install-deps get-sources COMPONENTS='$(BUILDER_PLUGINS) qwt-crossbuild' GIT_URL_qwt_crossbuild=https://github.com/fepitre/qwt-crossbuild INSECURE_SKIP_CHECKING="qwt-crossbuild"
$ make qubes-dom0 COMPONENTS="qwt-crossbuild"
```

## QWT Runtime prerequisuites

1. Fully/partially updated Windows 7/10
1. Testsigning mode on
1. Backup

## Feature status
| Feature | Windows 7 x64 (en,ru)| Windows 10 x64 (en,ru) |
| --- | :---: | :---: |
| Qubes Video Driver | + | - |
| Qubes Network Setup | + | + |
| Private Volume Setup (move profiles)  | + | + |
| File sender/receiver | + | + |
| Clipboard Copy/Paste | + | + |
| Application shortcuts | + | + |
| Copy/Edit in Disposible VM | + | + |
| Block device | + | + |
| USB device | - | - |
| Audio | - | - |
