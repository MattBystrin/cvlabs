#include <algorithm>
#include <array>
#include <cmath>
#include <ctime>
#include <iostream>
#include <numeric>
#include <optional>
#include <string>
#include <sys/times.h>
#include <vector>
#include "CImg/CImg.h"
#include "argparse.hpp"
#include <sys/time.h>

namespace cimg=cimg_library;

double disp(uint8_t k, std::array<double, 256> &hist)
{
	double P1 = 0;
	double m = 0;
	double m_g = 0;
	for (int i = 0; i < k; i++) {
		P1 += hist[i];
		m += hist[i] * i;
	}
	for (int i = 0; i < hist.size(); i++)
		m_g += hist[i] * i;	
	return (m_g * P1 - m) * (m_g * P1 - m) / (P1 * (1 - P1));
}

void binarize_image(cimg::CImg<uint8_t> &img)
{
	/* Calculate normalized histogramm */
	auto h = img.get_histogram(256);
	double dim = img.height() * img.width();
	std::array<double, 256> hist;
	for (int i = 0; i < 256; i++)
		hist[i] = (double)img(i,0) / dim;
	/* Fing dispersion maximum */
	std::vector<uint8_t> max_ks;
	double max_disp = 0;
	for (uint8_t k = 0; k < 255; k++) {
		double d = disp(k, hist);
		if (d > max_disp) {
			max_disp = d;
		}
		if (d == max_disp) {
			max_ks.push_back(k);
		}
	}

	uint8_t max_k = std::accumulate(max_ks.begin(), max_ks.end(), 0) / max_ks.size();
	
	cimg_forXY(img, x, y) {
		img(x,y) = img(x,y) > max_k ? 255 : 0;
	}
	return;
}

using mtx = std::vector<std::vector<int>>;
mtx m0 = {
	{0, 2},
	{3, 1}
};
mtx create_bayer_matrix(int dim)
{
	if (dim == 1)
		return m0;
	mtx m = create_bayer_matrix(dim - 1);	
	int size = std::pow(2, dim);
	mtx ret;
	ret.resize(size, std::vector<int>(size));
	for (int i = 0; i < ret.size(); i++) {
		for (int j = 0; j < ret.size(); j++) {
			ret[i][j] = m[i/2][j/2] + m[i%2][j%2]*4;
		}
	}
	return ret;
}
/* 
 * Dithering image using Bayer alogirithm 
 * Careful ! Nostalgia is a very strong feeling
 * Gaze a star if you start hearing a chiptune
 */
void dithering(cimg::CImg<uint8_t> &img, int dim)
{
	mtx b = create_bayer_matrix(dim);
	std::vector<std::vector<double>> bias;
	bias.resize(b.size(), std::vector<double>(b.size()));
	for (int i = 0; i < bias.size(); i++) 
		for (int j = 0; j < bias.size(); j++) 
			bias[i][j] = (double)b[i][j] / (b.size()*b.size());
	cimg_forXY(img, x, y) {
		img(x,y) = img(x,y) > bias[x % bias.size()][y % bias.size()] * 255 ? 255 : 0;
	}
	return;
}

int main(int argc, char *argv[])
{
	argparse::ArgumentParser parser("binary");
	parser.add_argument("image").help("Image to process");
	parser.add_argument("-g", "--gui")
		.default_value(false)
		.implicit_value(true)
		.help("Enable gui mode");
	parser.add_argument("-o", "--output").help("Path for saving processed image");
	parser.add_argument("-d", "--dithering")
		.scan<'i', int>()
		.help("Cool dithering mode");

	std::string path;
	try {
		parser.parse_args(argc, argv);
		path = parser.get("image");

	} catch (const std::runtime_error &ex) {
		std::cerr << ex.what() << std::endl;
		std::cerr << parser;
		std::exit(1);
	}
	clock_t elapsed;
	clock_t start;
	clock_t end;

	cimg::CImg<uint8_t> img(path.c_str());
	if (parser.present<int>("-d").has_value()) {
		start = clock();
		dithering(img, parser.get<int>("-d"));
		end = clock();
	} else {
		start = clock();
		binarize_image(img);
		end = clock();
	}

	elapsed = end - start;
	std::cout << (double)elapsed / (double)CLOCKS_PER_SEC << std::endl;
	
	auto o = parser.present("-o");
	if (o != std::nullopt)
		img.save(o.value().c_str());

	if (!parser.get<bool>("-g"))
		return 0;

	cimg::CImgDisplay disp;
	disp.display(img);
	while(!disp.is_closed()) {
		disp.wait();
		if (disp.is_key('n'))
			break;
	}

	return 0;
}
