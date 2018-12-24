#include <utility>
#include <fstream>
#include <iostream>
#include <vector>
#include <set>
#include <cmath>
#include <algorithm>
#include <limits>
#include <functional>

using Coord = std::pair<int, int>;
using Coords = std::vector<Coord>;
using Callback = std::function<int(int x, int y)>;

int manhattan_distance(const Coord &x, const Coord &y)
{
    return std::abs(x.first - y.first) + std::abs(x.second - y.second);
}

Coords load_coords_from_file(const std::string &filename)
{
    Coords coords;
    std::fstream file(filename);

    int x, y;
    char ch;
    while (file >> x >> ch >> y)
        coords.emplace_back(x, y);
    file.close();
    return coords;
}

// This is only fo optimisation purpose
void move_by(Coords &coords, const Coord &by)
{
    std::transform(coords.begin(), coords.end(), coords.begin(),
        [by](Coord &x) {
            return std::make_pair(x.first - by.first, x.second - by.second);
        });
}

void for_each_in_matrix(int **matrix, int max_i, int max_j, Callback cb)
{
    for (int i = 0; i < max_i; ++i) {
        for (int j = 0; j < max_j; ++j) {
            matrix[i][j] = cb(j, i);
        }
    }
}

int main()
{
    Coords coords = load_coords_from_file("data/6.txt");

    move_by(coords, *std::min_element(
        coords.cbegin(),
        coords.cend(),
        [](const Coord &x, const Coord &y) {
            return x.first + x.second < y.first + y.second;
        }));

    Coord idx = *std::max_element(
        coords.cbegin(),
        coords.cend(),
        [](const Coord &x, const Coord &y) {
            return x.first + x.second < y.first + y.second;
        }
    );

    idx.first = idx.first * 3;
    idx.second = idx.second * 3;

    // { Part 1 }
    Callback get_closest = [coords](int x, int y) {
        auto point = std::make_pair(x, y);
        int index;
        int closest = std::numeric_limits<int>::max();
        for (auto it = coords.cbegin(); it != coords.cend(); ++it) {
            int distance = manhattan_distance(point, *it);
            if (distance < closest) {
                closest = distance;
                index = std::distance(coords.cbegin(), it);
            }
            else if (distance == closest)
                index = -1;
        }
        return index;
    };

    int **matrix = new int *[idx.second + 1];
    for (int i = 0; i < idx.second + 1; ++i)
        matrix[i] = new int[idx.first + 1];

    for_each_in_matrix(matrix, idx.second + 1, idx.first + 1, get_closest);

    std::set<int> non_infinite;
    for (int i = 0; i < coords.size(); ++i)
        non_infinite.emplace(i);

    for (int i = 0; i < idx.second + 1; ++i)
        for (int j = 0; j < idx.first + 1; ++j)
            if (i == 0 || j == 0 || i == idx.second || j == idx.first)
                non_infinite.erase(matrix[i][j]);

    std::vector<int> areas(non_infinite.size());
    std::fill(areas.begin(), areas.end(), 0);
    for (int i = 0; i < idx.second + 1; ++i) {
        for (int j = 0; j < idx.first + 1; ++j) {
            auto it = non_infinite.find(matrix[i][j]);
            if (it != non_infinite.cend()) {
                int index = std::distance(non_infinite.cbegin(), it);
                areas[index] += 1;
            }
        }
    }

    std::cout << *std::max_element(areas.cbegin(), areas.cend()) << std::endl;

    // { Part 2 }
    move_by(coords, std::make_pair(-20, -20));

    Callback calc_sum_of_distances = [coords](int x, int y) {
        auto point = std::make_pair(x, y);
        int sum = 0;
        for (auto it = coords.cbegin(); it != coords.cend(); ++it)
            sum += manhattan_distance(point, *it);
        return sum;
    };
    for_each_in_matrix(matrix, idx.second + 1, idx.first + 1, calc_sum_of_distances);

    int area = 0;
    for (int i = 0; i < idx.second + 1; ++i)
        for (int j = 0; j < idx.first + 1; ++j)
            if (matrix[i][j] < 10000)
                area += 1;

    std::cout << area << std::endl;

    for (int i = 0; i < idx.first; ++i)
        delete[] matrix[i];
    delete[] matrix;
}
