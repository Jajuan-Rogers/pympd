#include <array>
#include <chrono>
#include <cmath>
#include <math.h>
#include <ncpp/NotCurses.hh>
#include <ncpp/Plane.hh>
#include <thread>

int main() {
  ncpp::NotCurses nc;
  ncpp::Plane *stdp = nc.get_stdplane();
  std::array<uint32_t, 5> Color{0x00FF00, 0x00CC00, 0x008200, 0x006800,
                                0x005300};
  ncinput ni;

  // We will use this to track which color we are on
  int color_index = 0;

  double degrees = 45.0;

  // 1. Convert degrees to radians
  // Formula: radians = degrees * (PI / 180)
  double pi = std::acos(-1.0); // A clever way to get a precise PI
  double radians = degrees * (pi / 180.0);
  double y = std::sin(radians);

  while (true) {
    // 1. Set the brush color
    stdp->erase();
    stdp->set_fg_rgb(Color[color_index]);

    // 2. Draw the text WITH the new brush color
    stdp->putstr(0, 0, "Press any key to exit...");
    stdp->putstr(y, radians, "WHOOOOOO !!");

    nc.render();
    color_index = (color_index + 1) % 5;
    y += pi/2;

    std::this_thread::sleep_for(std::chrono::milliseconds(100));

    struct timespec ts = {0, 0};
    uint32_t key = nc.get(&ts, &ni);

    if (key != (uint32_t)-1 && key != 0) {
      break;
    }
  }

  return 0;
}
