BLENDER_USER_SCRIPTS=src/knife_maker

BLENDER_BACKGROUND_OPTS=--background

BLENDER_AUTOEXEC=--enable-autoexec

BLENDER_DEBUG_OPTS=--debug-all

all: knife_maker

knife_maker : $(BLENDER_USER_SCRIPTS)/knife_maker.py
	blender $(BLENDER_AUTOEXEC) --python $^

.PHONY: all
