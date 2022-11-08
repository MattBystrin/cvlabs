
bin: cpp/binary.cpp 
	g++ -o cpp/binary cpp/binary.cpp -g -O3 --std=c++17 $(shell pkg-config --libs x11) -lpthread
	g++ -o cpp/binary_noopt cpp/binary.cpp -g --std=c++17 $(shell pkg-config --libs x11) -lpthread
