.DEFAULT_GOAL: setup

setup:
	pip3 install -r requirements.txt
	chmod +x recover_playlist.py
	chmod +x ./misc/git-hooks/pre-commit
	ln -s -f `pwd`/misc/git-hooks/pre-commit ./.git/hooks/pre-commit