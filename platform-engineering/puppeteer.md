# Solution for Puppeteer Chromium-browser Issue

## Errors:
* /usr/bin/chromium-browser: 12: xdg-settings: not found
* [1468083:1468163:1121/044444.477966:ERROR:object_proxy.cc(577)] Failed to call method: org.freedesktop.DBus.ListActivatableNames: object_path= /org/freedesktop/DBus: org.freedesktop.DBus.Error.AccessDenied: An AppArmor policy prevents this sender from sending this message to this recipient; type="method_call", sender=":1.961" (uid=1000 pid=1468083 comm="/snap/chromium/2695/usr/lib/chromium-browser/chrom" label="snap.chromium.chromium (enforce)") interface="org.freedesktop.DBus" member="ListActivatableNames" error name="(unset)" requested_reply="0" destination="org.freedesktop.DBus" (bus)
* [1468083:1468083:1121/044444.714621:ERROR:policy_logger.cc(157)] :components/enterprise/browser/controller/chrome_browser_cloud_management_controller.cc(163) Cloud management controller initialization aborted as CBCM is not enabled.

## Solutions:
1. Check enough disk space is available at root folder i.e. at /
    ```
    $ df -h
    ```
2. If not check which files are too large and taking more space
    ```
    $ sudo du -h --max-depth=1 /
    ```
3. Then if large files and folders are not important, you may remove them manually.
4. Try cleaning up the package cache to remove downloaded package files. This can often free up a significant amount of space.
    ```
    $ sudo apt clean
    ```
5. Try cleaning packages that can no longer downloaded.
    ```
    $ sudo apt autoclean
    ```
6. Uninstall unnecessary packages
    ```
    $ sudo apt autoremove
    ```
7. Update your system.
    ```
    $ sudo apt update
    ```
8. Install chromium using snap
    ```
    $ sudo snap install chromium
    ```
9. If snap is not working fine, it may because of not enough space available, check snap status
    ```
    $ sudo systemctl status snapd
    ```
10. If it is having issue try to restart snapd. And then try installing chromium again as specified in step no. 8
    ```
    sudo systemctl restart snapd
    ```