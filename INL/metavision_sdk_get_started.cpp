#include <c:\Program Files\Prophesee\include\metavision\sdk\driver>

// main loop
int main(int argc, char *argv[]) {
    Metavision::Camera cam; // create the camera

    if (argc >= 2) {
        // if we passed a file path, open it
        cam = Metavision::Camera::from_file(argv[1]);
    } else {
        // open the first available camera
        cam = Metavision::Camera::from_first_available();
    }

    // start the camera
    cam.start();

    // keep running while the camera is on or the recording is not finished
    while (cam.is_running()) {
        std::cout << "Camera is running!" << std::endl;
    }

    // the recording is finished, stop the camera.
    // Note: we will never get here with a live camera
    cam.stop();
}