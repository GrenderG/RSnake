rsnake:
	make clean && mkdir build && cd build && cp ../rsnake.py . && mkdir etc && cp -R ../etc/fonts etc/ && cp ../etc/rsnake.retrofw.desktop . && cp ../etc/rsnake.sh . && cp ../etc/images/rsnake.png . && cd .. && mksquashfs build rsnake.opk

clean:
	rm -rf build