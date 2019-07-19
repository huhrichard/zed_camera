import cv2
import pyzed.sl as sl
import sys
from multiprocessing import Process
import time

res = sl.RESOLUTION.RESOLUTION_HD1080
fps = 15

def main():
    zed1 = sl.Camera()
    zed2 = sl.Camera()
    print("Running...")
    init_params = sl.InitParameters()
    init_params.camera_resolution = res
    init_params.camera_fps = fps

    init_params.camera_linux_id = 0
    if not zed1.is_opened():
	    print("Opening ZED Camera 1 ...")

    err = zed1.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
    init_params.camera_linux_id = 1 # Specify the camera index
    if not zed2.is_opened():
        print("Opening ZED Camera 2 ...")

    err = zed2.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))


    runtime = sl.RuntimeParameters()
    mat1 = sl.Mat()
    mat2 = sl.Mat()

    print_camera_information(zed1)
    print_camera_information(zed2)

    key = ''

    while key != 113:  # for 'q' key
        # print('reading')
        err = zed1.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            zed1.retrieve_image(mat1, sl.VIEW.VIEW_LEFT)
            cv2.imshow("ZED 1", mat1.get_data())

        err = zed2.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            zed2.retrieve_image(mat2, sl.VIEW.VIEW_LEFT)
            cv2.imshow("ZED 2", mat2.get_data())

        key = cv2.waitKey(5)
    cv2.destroyAllWindows()
    zed1.close()
    zed2.close()
    print("\nFINISH")

def main_single(cam_id):
    zed1 = sl.Camera()
    print("Running...")
    init_params = sl.InitParameters()
    init_params.camera_resolution = res
    init_params.camera_fps = fps

    init_params.camera_linux_id = cam_id
    if not zed1.is_opened():
	    print("Opening ZED Camera "+str(cam_id)+" ...")

    err = zed1.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        exit(1)


    runtime = sl.RuntimeParameters()
    mat1 = sl.Mat()
    # mat2 = sl.Mat()

    print_camera_information(zed1)
    # print_camera_information(zed2)
    winname = "ZED"+str(cam_id)
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(winname, 640, 360)

    key = ''
    start = time.time()
    minutes_gone = 0
    hours_gone = 0
    # counter = 100
    while key != 113:  # for 'q' key
        err = zed1.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            zed1.retrieve_image(mat1, sl.VIEW.VIEW_LEFT)
            cv2.imshow(winname, mat1.get_data())
        processed = time.time() - start
        current_ran_minute = (processed%3600)//(60)
        current_ran_hour = processed//3600
        # if (current_ran_minute-minutes_gone) >= 1:
        minutes_gone = current_ran_minute
        if zed1.get_camera_fps() == fps:
            print('Ran for ', processed//(3600),'hours ', (processed%3600)//(60), 'mins ', processed%60,'seconds')
            print("Camera FPS: {0}.".format(zed1.get_camera_fps()))
        if zed1.get_camera_fps() < fps:
            if (current_ran_hour - hours_gone) >= 1:
                print('FPS dropped')
                print('Ran for ', processed // (3600), 'hours ', (processed % 3600) // (60), 'mins ', processed % 60,
                      'seconds')
                print("Camera FPS: {0}.".format(zed1.get_camera_fps()))
                hours_gone = current_ran_hour

        # err = zed2.grab(runtime)
        # if err == sl.ERROR_CODE.SUCCESS:
        #     zed2.retrieve_image(mat2, sl.VIEW.VIEW_LEFT)
        #     cv2.imshow("ZED 2", mat2.get_data())

        key = cv2.waitKey(5)
    cv2.destroyAllWindows()
    zed1.close()
    # zed2.close()
    print("\nFINISH")

def print_camera_information(cam):
    print("Resolution: {0}, {1}.".format( round(cam.get_resolution().width, 2), cam.get_resolution().height))
    print("Camera FPS: {0}.".format(cam.get_camera_fps()))
    print("Firmware: {0}.".format( cam.get_camera_information().firmware_version))
    print("Serial number: {0}.\n".format( cam.get_camera_information().serial_number))

if __name__ == '__main__':

    # p1 = Process(target=main_single, args=(0,))
    # p2 = Process(target=main_single, args=(1,))
    #
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    # main()
    cam_id = int(sys.argv[-1])
    main_single(cam_id)