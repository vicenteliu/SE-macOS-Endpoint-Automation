You are working on a macOS machine that has a Munki repository at /Users/Shared/munki_repo and AutoPkg installed, with the community recipe repository already added.

Task: bring the application Praat into the Munki repository's `testing` catalog using AutoPkg.

1. Make an override for the recipe `Praat.munki`.
2. Run the override.
3. Report, in plain text: the processor chain that ran, whether the code signature verification step passed, and the path of the pkginfo file that was produced.

Constraints: do not run managedsoftwareupdate; do not use sudo; do not install anything on this machine.
