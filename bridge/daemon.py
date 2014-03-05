import daemon

from bridge import main

with daemon.DaemonContext():
    main()
