import cv2

nets = []
models = [
    'eccv16/la_muse.t7',
    'eccv16/starry_night.t7',
    'eccv16/the_wave.t7',
    'instance_norm/the_scream.t7',
    'instance_norm/mosaic.t7',
    'instance_norm/candy.t7',
    'instance_norm/feathers.t7',
]
for i in range(len(models)):
    net = cv2.dnn.readNetFromTorch('models/' + models[i])
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV);
    nets.append(net)

cap = cv2.VideoCapture(0)

cv2.namedWindow('Styled image', cv2.WINDOW_NORMAL)
while cv2.waitKey(1) < 0:
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv2.waitKey()
        break

    inWidth = 300
    inHeight = 200
    inp = cv2.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight),
                              (103.939, 116.779, 123.68), swapRB=False, crop=False)

    for i in range(len(nets)):
        net = nets[i]
        net.setInput(inp)
        out = net.forward()

        out = out.reshape(3, out.shape[2], out.shape[3])
        out[0] += 103.939
        out[1] += 116.779
        out[2] += 123.68
        out /= 255
        out = out.transpose(1, 2, 0)

        cv2.imshow('Styled image %d' % i, out)
