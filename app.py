import facerecognition
import motiondetect

def main():
  #define mode number by push button gpio pins or flags or something
  mode = 1

  if mode == 0:
    #run face-recognition
    facerecognition.main()
  elif mode == 1:
    #run motion-detect
    motiondetect.main()
  
if __name__ == '__main__':
  main()
