# oddly enought this Makefile prdouces silly results with make-3.81 so please only use >=make-3.82 on debian

runos:
	python run_redox_eq_os.py
rungim:
	python run_redox_eq_gim.py
run: rungim runos

visualize:
	python view_redox2.py

all: clean run visualize
clean:
	find 0.1/ -maxdepth 1 ! -iname '*.dat' -type f -delete;  \
	find 1.0/ -maxdepth 1 ! -iname '*.dat' -type f -delete;  \
	find 10/ -maxdepth 1 ! -iname '*.dat' -type f -delete;  

